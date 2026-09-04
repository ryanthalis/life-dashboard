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


class ConfirmationTests(unittest.TestCase):
    def test_get_confirmation_accepts_yes(self):
        for user_input in ("y", " YES "):
            with self.subTest(user_input=user_input):
                with patch("builtins.input", return_value=user_input):
                    self.assertTrue(life_tracker.get_confirmation("Confirm: "))

    def test_get_confirmation_accepts_no(self):
        for user_input in ("n", " NO "):
            with self.subTest(user_input=user_input):
                with patch("builtins.input", return_value=user_input):
                    self.assertFalse(life_tracker.get_confirmation("Confirm: "))

    def test_get_confirmation_retries_invalid_input(self):
        inputs = ["maybe", "yes"]

        with patch("builtins.input", side_effect=inputs) as mock_input:
            with patch("builtins.print"):
                result = life_tracker.get_confirmation("Confirm: ")

        self.assertTrue(result)
        self.assertEqual(mock_input.call_count, 2)


class DeleteWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.row = {
            "id": 42,
            "entry_date": "2026-09-04",
            "category": "study",
            "label": "SQLite",
            "quantity": 30,
            "notes": "Test entry",
        }

    def test_confirmed_delete_calls_database(self):
        inputs = ["6", "42", "yes", "7"]

        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print") as mock_print:
                with patch.object(life_tracker.db, "init_db"):
                    with patch.object(life_tracker.db, "get_entry", return_value=self.row):
                        with patch.object(
                            life_tracker.db, "delete_entry", return_value=True
                        ) as mock_delete:
                            life_tracker.main()

        mock_delete.assert_called_once_with(42)
        mock_print.assert_any_call("Entry deleted")

    def test_cancelled_delete_does_not_call_database(self):
        inputs = ["6", "42", "no", "7"]

        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print") as mock_print:
                with patch.object(life_tracker.db, "init_db"):
                    with patch.object(life_tracker.db, "get_entry", return_value=self.row):
                        with patch.object(life_tracker.db, "delete_entry") as mock_delete:
                            life_tracker.main()

        mock_delete.assert_not_called()
        mock_print.assert_any_call("Deletion cancelled")

    def test_missing_id_does_not_call_delete(self):
        inputs = ["6", "999", "7"]

        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print") as mock_print:
                with patch.object(life_tracker.db, "init_db"):
                    with patch.object(life_tracker.db, "get_entry", return_value=None):
                        with patch.object(life_tracker.db, "delete_entry") as mock_delete:
                            life_tracker.main()

        mock_delete.assert_not_called()
        mock_print.assert_any_call("Entry not found")


if __name__ == "__main__":
    unittest.main()
