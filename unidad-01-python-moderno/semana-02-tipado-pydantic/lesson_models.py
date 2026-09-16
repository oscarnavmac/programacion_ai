"""Typed contracts for synthetic prediction records; no model is trained here."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

Label = Literal["positive", "neutral", "negative"]
Score = Annotated[float, Field(ge=0, le=1, allow_inf_nan=False)]


class Prediction(BaseModel):
    """Normalize text fields and validate one incoming prediction."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    text: str = Field(min_length=1)
    label: Label
    score: Score
    source: str | None = None

    @field_validator("text", "label", "source", mode="before")
    @classmethod
    def normalize_strings(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("score", mode="before")
    @classmethod
    def reject_boolean_score(cls, value: object) -> object:
        if isinstance(value, bool):
            raise ValueError("A boolean is not a score")
        return value


class BatchConfig(BaseModel):
    """Application settings supplied explicitly, without secrets or services."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    batch_name: str = Field(min_length=1)
    threshold: Score = 0.9
    max_records: int = Field(default=100, ge=1, le=1000, strict=True)

    @field_validator("batch_name")
    @classmethod
    def require_nonblank_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Batch name must not be blank")
        return value

    @field_validator("threshold", mode="before")
    @classmethod
    def reject_boolean_threshold(cls, value: object) -> object:
        if isinstance(value, bool):
            raise ValueError("A boolean is not a threshold")
        return value


class ValidationIssue(BaseModel):
    position: int
    field: str
    message: str
    error_type: str


class BatchReport(BaseModel):
    config: BatchConfig
    accepted: list[Prediction] = Field(default_factory=list)
    issues: list[ValidationIssue] = Field(default_factory=list)


def average_score(predictions: list[Prediction]) -> float | None:
    if not predictions:
        return None
    return sum(prediction.score for prediction in predictions) / len(predictions)


def process_records(records: list[object], config: BatchConfig) -> BatchReport:
    """Reject an oversized batch; preserve all validation issues for each row."""
    if len(records) > config.max_records:
        raise ValueError("Batch exceeds max_records")

    report = BatchReport(config=config)
    for position, record in enumerate(records):
        try:
            prediction = Prediction.model_validate(record)
        except ValidationError as error:
            for detail in error.errors():
                report.issues.append(
                    ValidationIssue(
                        position=position,
                        field=".".join(str(part) for part in detail["loc"]) or "<record>",
                        message=detail["msg"],
                        error_type=detail["type"],
                    )
                )
        else:
            report.accepted.append(prediction)
    return report


def select_predictions(report: BatchReport) -> list[Prediction]:
    """Select by confidence; this is not an accuracy measurement."""
    return [
        prediction
        for prediction in report.accepted
        if prediction.score >= report.config.threshold
    ]
