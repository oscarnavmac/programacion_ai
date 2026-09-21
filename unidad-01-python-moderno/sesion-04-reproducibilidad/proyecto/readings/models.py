from pydantic import BaseModel, ConfigDict, Field


class Reading(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    station: str = Field(min_length=1)
    temperature: float = Field(allow_inf_nan=False)


class Report(BaseModel):
    count: int
    rejected: int
    average_temperature: float
