"""Run with python check_contracts.py; synthetic fixtures only."""

import unittest

from pydantic import ValidationError

from lesson_models import (
    BatchConfig, BatchReport, Prediction, average_score, process_records,
    select_predictions,
)


class ContractChecks(unittest.TestCase):
    def setUp(self):
        self.record = {"text": " Good ", "label": " POSITIVE ", "score": "0.9"}
        self.config = BatchConfig(batch_name="Checks", max_records=10)

    def test_normalization_and_source_preserved(self):
        prediction = Prediction.model_validate(self.record)
        self.assertEqual(prediction.text, "good")
        self.assertEqual(prediction.label, "positive")
        self.assertEqual(prediction.score, 0.9)
        self.assertEqual(self.record["text"], " Good ")
        self.assertIsNone(prediction.source)

    def test_score_boundaries_and_invalid_inputs(self):
        for score in (0.0, 1.0):
            self.assertEqual(Prediction.model_validate({**self.record, "score": score}).score, score)
        for value in (True, None, -0.1, 1.1, "nan", float("inf"), "unknown"):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                Prediction.model_validate({**self.record, "score": value})

    def test_required_fields_and_unknown_keys(self):
        for change in ({"text": "   "}, {"label": None}, {"label": "other"}, {"scroe": 0.5}):
            with self.subTest(change=change), self.assertRaises(ValidationError):
                Prediction.model_validate({**self.record, **change})
        for missing in ("text", "label", "score"):
            with self.assertRaises(ValidationError):
                Prediction.model_validate({k: v for k, v in self.record.items() if k != missing})
        self.assertIsNone(Prediction.model_validate({**self.record, "source": None}).source)

    def test_configuration(self):
        for change in ({"batch_name": " "}, {"threshold": True}, {"threshold": 2},
                       {"max_records": "3"}, {"max_records": 0}, {"max_records": True},
                       {"max_records": 1001}, {"unknown": 1}):
            with self.subTest(change=change), self.assertRaises(ValidationError):
                BatchConfig.model_validate({"batch_name": "Checks", **change})
        self.assertEqual(BatchConfig(batch_name=" Trim ").batch_name, "Trim")

    def test_assignment(self):
        prediction = Prediction.model_validate(self.record)
        with self.assertRaises(ValidationError):
            prediction.score = 2
        self.assertEqual(prediction.score, 0.9)

    def test_batch_and_multiple_issues(self):
        report = process_records([
            self.record, {**self.record, "score": 0.0},
            {**self.record, "label": "other", "score": 2}, None,
        ], self.config)
        self.assertEqual(len(report.accepted), 2)
        self.assertEqual(len(report.issues), 3)
        self.assertEqual({issue.position for issue in report.issues}, {2, 3})
        self.assertEqual(len(select_predictions(report)), 1)
        self.assertAlmostEqual(average_score(report.accepted), 0.45)
        self.assertEqual(BatchReport.model_validate_json(report.model_dump_json()), report)

    def test_empty_invalid_and_oversized(self):
        for records in ([], [None]):
            self.assertIsNone(average_score(process_records(records, self.config).accepted))
        with self.assertRaises(ValueError):
            process_records([self.record] * 11, self.config)

    def test_separate_lists_and_nested_errors(self):
        first = BatchReport(config=self.config)
        second = BatchReport(config=self.config)
        first.accepted.append(Prediction.model_validate(self.record))
        self.assertEqual(second.accepted, [])
        payload = first.model_dump()
        payload["accepted"][0]["score"] = 5
        with self.assertRaises(ValidationError) as caught:
            BatchReport.model_validate(payload)
        self.assertEqual(caught.exception.errors()[0]["loc"], ("accepted", 0, "score"))
        self.assertEqual(first.accepted[0].score, 0.9)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ContractChecks)
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("All contract checks passed")
