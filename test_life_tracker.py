import unittest
from unittest.mock import patch

import life_tracker


class SummaryTests(unittest.TestCase):

    def test_summary_with_workouts_and_studies(self):
        workouts = [
            {"quantity": 3},
            {"quantity": 4},
        ]
        studies = [
            {"quantity": 30, "label": "SQLite"},
            {"quantity": 45, "label": "Python"},
        ]
        expected = (2, 2, 7, 75, {"SQLite", "Python"})

        actual = life_tracker.get_summary(workouts, studies)

        self.assertEqual(actual, expected)

    def test_summary_with_empty_list(self):
        workouts = []
        studies = []

        expected = (0, 0, 0, 0, set())

        actual = life_tracker.get_summary(workouts, studies)

        self.assertEqual(actual, expected)


class InputValidationTests(unittest.TestCase):
    def test_get_nonempty_retries_and_strips_whitespace(self):
        inputs = ["", "   ", "  Bench press  "]

        with patch("builtins.input", side_effect=inputs) as mock_input:
            with patch("builtins.print"):
                actual = life_tracker.get_nonempty("Label: ")

        self.assertEqual(actual, "Bench press")
        self.assertEqual(mock_input.call_count, 3)

    def test_get_date_accepts_exact_iso_date(self):
        with patch("builtins.input", return_value="2026-09-04"):
            actual = life_tracker.get_date("Date: ")

        self.assertEqual(actual, "2026-09-04")

    def test_get_date_retries_invalid_formats(self):
        inputs = [
            "2026-02-30",
            "09/04/2026",
            "20260904",
            "",
            "2026-09-04",
        ]

        with patch("builtins.input", side_effect=inputs) as mock_input:
            with patch("builtins.print"):
                actual = life_tracker.get_date("Date: ")

        self.assertEqual(actual, "2026-09-04")
        self.assertEqual(mock_input.call_count, 5)

    def test_get_int_enforces_minimum_and_maximum(self):
        inputs = ["not a number", "0", "6", "3"]

        with patch("builtins.input", side_effect=inputs) as mock_input:
            with patch("builtins.print"):
                actual = life_tracker.get_int("Choice: ", 1, 5)

        self.assertEqual(actual, 3)
        self.assertEqual(mock_input.call_count, 4)

    def test_get_int_allows_no_maximum(self):
        inputs = ["0", "12"]

        with patch("builtins.input", side_effect=inputs) as mock_input:
            with patch("builtins.print"):
                actual = life_tracker.get_int("Quantity: ")

        self.assertEqual(actual, 12)
        self.assertEqual(mock_input.call_count, 2)


if __name__ == "__main__":
    unittest.main()
