import unittest

from sqlalchemy import Identity

from server.models import Base, User


class UserModelTests(unittest.TestCase):
    def test_user_table_is_registered_with_expected_columns(self):
        self.assertIs(Base.metadata.tables["users"], User.__table__)
        self.assertEqual(
            list(User.__table__.columns.keys()),
            ["user_id", "username", "email"],
        )

    def test_user_id_is_an_always_generated_identity(self):
        identity = User.__table__.c.user_id.identity

        self.assertIsInstance(identity, Identity)
        self.assertTrue(identity.always)
        self.assertTrue(User.__table__.c.user_id.primary_key)

    def test_normalized_unique_indexes_are_present(self):
        indexes = {index.name: index for index in User.__table__.indexes}

        self.assertEqual(
            set(indexes),
            {"users_username_lower_uq", "users_email_lower_uq"},
        )
        self.assertTrue(all(index.unique for index in indexes.values()))

    def test_trimmed_nonblank_checks_are_present(self):
        check_names = {
            constraint.name
            for constraint in User.__table__.constraints
            if constraint.__class__.__name__ == "CheckConstraint"
        }

        self.assertEqual(
            check_names,
            {
                "ck_users_username_trimmed_nonblank",
                "ck_users_email_trimmed_nonblank",
            },
        )


if __name__ == "__main__":
    unittest.main()
