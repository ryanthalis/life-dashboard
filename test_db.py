import unittest
import tempfile
import os
import db

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "test_database.db")
        self.original_path = db.FILE_PATH
        db.FILE_PATH = self.file_path
        db.init_db()

    def test_database_starts_empty(self):
        workouts = db.get_entries("workout")
        self.assertEqual(workouts, [])

    def test_add_and_get_entry(self):
        db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)
        row = db.get_entries("study")
        data = row[0]

        self.assertEqual(len(row), 1)
        self.assertEqual("2026-01-23", data["entry_date"])
        self.assertEqual("study", data["category"])
        self.assertEqual("Neuromechanical Matching", data["label"])
        self.assertEqual(35, data["quantity"])
        self.assertEqual("", data["notes"])

    def test_get_entries_filters_by_category(self):
        db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)
        db.add_entry("2026-01-23", "workout", "Unilateral recline curl with microloading", 2)

        row = db.get_entries("workout")
        data = row[0]
        self.assertEqual(len(row), 1)
        self.assertEqual("workout", data["category"])
        self.assertEqual("Unilateral recline curl with microloading", data["label"])

    def test_get_entries_orders_newest_first(self):
        db.add_entry("2026-01-15", "study", "Middle", 20)
        db.add_entry("2026-01-01", "study", "Oldest", 20)
        db.add_entry("2026-02-01", "study", "Newest", 20)

        rows = db.get_entries("study")
        actual_dates = [row["entry_date"] for row in rows]
        expected_dates = ["2026-02-01", "2026-01-15", "2026-01-01"]

        self.assertEqual(actual_dates, expected_dates)

    def test_get_entries_rejects_invalid_category(self):

        with self.assertRaises(ValueError):
            db.get_entries("minecraft")

    def test_update_entry_changes_existing_entry(self):
        db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)
        rows = db.get_entries("study")
        data = rows[0]
        original_id = data["id"]

        result = db.update_entry(
            original_id,
            "2026-02-01",
            "study",
            "Decrease in third spaces",
            5,
            "Updated notes",
        )

        data = db.get_entry(original_id)

        self.assertTrue(result)
        self.assertEqual(original_id, data["id"])
        self.assertEqual("2026-02-01", data["entry_date"])
        self.assertEqual("study", data["category"])
        self.assertEqual("Decrease in third spaces", data["label"])
        self.assertEqual(5, data["quantity"])
        self.assertEqual("Updated notes", data["notes"])

    def test_get_entry_returns_existing_entry(self):
        db.add_entry("2026-03-10", "workout", "Cable row", 4, "Test notes")
        entry_id = db.get_entries("workout")[0]["id"]

        row = db.get_entry(entry_id)

        self.assertIsNotNone(row)
        self.assertEqual(entry_id, row["id"])
        self.assertEqual("2026-03-10", row["entry_date"])
        self.assertEqual("workout", row["category"])
        self.assertEqual("Cable row", row["label"])
        self.assertEqual(4, row["quantity"])
        self.assertEqual("Test notes", row["notes"])

    def test_get_entry_returns_none_for_missing_id(self):
        row = db.get_entry(999)

        self.assertIsNone(row)

    def test_update_entry_returns_false_for_missing_id(self):
        result = db.update_entry(
            999,
            "2026-04-01",
            "workout",
            "Missing entry",
            1,
            "Should not be created",
        )
        rows = db.get_entries("workout")

        self.assertFalse(result)
        self.assertEqual(rows, [])

    def tearDown(self):
        db.FILE_PATH = self.original_path
        self.temp_dir.cleanup()
