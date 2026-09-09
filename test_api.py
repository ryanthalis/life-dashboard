from fastapi.testclient import TestClient
import unittest
import api
import tempfile
import os
import db

client = TestClient(api.app)

class FastApiTests(unittest.TestCase):

    def setUp(self):
            self.temp_dir = tempfile.TemporaryDirectory()
            self.file_path = os.path.join(self.temp_dir.name, "test_database.db")
            self.original_path = db.FILE_PATH
            db.FILE_PATH = self.file_path
            db.init_db()

    def test_post(self):

        payload = {"entry_date": "2026-06-05", "category": "study", "label": "Biarticulate Muscles", "quantity": 5, "notes": "Longhead of triceps,"
        "Rectus Femoris"}

        response = client.post("/entries", json=payload)

        self.assertEqual(response.status_code, 201 )

        response = response.json()

        self.assertIsNotNone(response["id"])

    def test_post_with_zero_quantity_input(self):
        payload = {"entry_date": "2026-06-05", "category": "study", "label": "Biarticulate Muscles", "quantity": 0, "notes": "Longhead of triceps,"
        "Rectus Femoris"}
        
        response = client.post("/entries", json=payload)
        self.assertEqual(response.status_code, 422 )

    def test_root(self):

        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Life Dashboard API")

    def test_get_entry(self):

        entry_id = db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)

        response = client.get(f"/entries/{entry_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], entry_id)

    def test_get_missing_entry(self):

        response = client.get("/entries/999")

        self.assertEqual(response.status_code, 404)

    def test_get_entries(self):

        db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)
        db.add_entry("2026-01-24", "workout", "Cable Row", 3)

        response = client.get("/entries")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_entries_filters_by_category(self):

        db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)
        db.add_entry("2026-01-24", "workout", "Cable Row", 3)

        response = client.get("/entries?category=study")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["category"], "study")

    def test_get_entries_rejects_invalid_category(self):

        response = client.get("/entries?category=sleep")

        self.assertEqual(response.status_code, 422)

    def test_patch(self):

        entry_id = db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)

        payload = {"quantity": 200}

        response = client.patch(f"/entries/{entry_id}", json=payload)

        self.assertEqual(response.status_code, 200)

        entry = db.get_entry(entry_id)
        self.assertEqual(entry["quantity"], 200)
        self.assertEqual(entry["label"], "Neuromechanical Matching")

    def test_patch_missing_entry(self):

        response = client.patch("/entries/999", json={"quantity": 200})

        self.assertEqual(response.status_code, 404)

    def test_patch_rejects_zero_quantity(self):

        entry_id = db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)

        response = client.patch(f"/entries/{entry_id}", json={"quantity": 0})

        self.assertEqual(response.status_code, 422)

    def test_delete_entry(self):

        entry_id = db.add_entry("2026-01-23", "study", "Neuromechanical Matching", 35)

        response = client.delete(f"/entries/{entry_id}")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(db.get_entry(entry_id))

    def test_delete_missing_entry(self):

        response = client.delete("/entries/999")

        self.assertEqual(response.status_code, 404)
        


    def tearDown(self):
        db.FILE_PATH = self.original_path
        self.temp_dir.cleanup()

