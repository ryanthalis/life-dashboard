import unittest

from sqlalchemy import Identity, UniqueConstraint

from server.models import Base, Exercise, User, WorkoutType


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


class WorkoutTypeModelTests(unittest.TestCase):
    def test_workout_type_table_is_registered_with_expected_columns(self):
        self.assertIs(Base.metadata.tables["workout_types"], WorkoutType.__table__)
        self.assertEqual(
            list(WorkoutType.__table__.columns.keys()),
            ["workout_type_id", "user_id", "name"],
        )

    def test_workout_type_has_generated_identity_and_cascading_owner(self):
        identity = WorkoutType.__table__.c.workout_type_id.identity
        user_foreign_key = next(iter(WorkoutType.__table__.c.user_id.foreign_keys))

        self.assertIsInstance(identity, Identity)
        self.assertTrue(identity.always)
        self.assertEqual(user_foreign_key.target_fullname, "users.user_id")
        self.assertEqual(user_foreign_key.ondelete, "CASCADE")

    def test_workout_type_has_same_user_reference_key(self):
        unique_constraints = {
            constraint.name: tuple(column.name for column in constraint.columns)
            for constraint in WorkoutType.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
        }

        self.assertEqual(
            unique_constraints["workout_types_workout_type_id_user_id_uq"],
            ("workout_type_id", "user_id"),
        )

    def test_workout_type_name_rules_are_present(self):
        indexes = {index.name: index for index in WorkoutType.__table__.indexes}
        check_names = {
            constraint.name
            for constraint in WorkoutType.__table__.constraints
            if constraint.__class__.__name__ == "CheckConstraint"
        }

        self.assertEqual(set(indexes), {"workout_types_user_id_name_lower_uq"})
        self.assertTrue(indexes["workout_types_user_id_name_lower_uq"].unique)
        self.assertEqual(
            check_names,
            {"ck_workout_types_name_trimmed_nonblank"},
        )


class ExerciseModelTests(unittest.TestCase):
    def test_exercise_table_is_registered_with_expected_columns(self):
        self.assertIs(Base.metadata.tables["exercises"], Exercise.__table__)
        self.assertEqual(
            list(Exercise.__table__.columns.keys()),
            ["exercise_id", "user_id", "name"],
        )

    def test_exercise_has_generated_identity_and_cascading_owner(self):
        identity = Exercise.__table__.c.exercise_id.identity
        user_foreign_key = next(iter(Exercise.__table__.c.user_id.foreign_keys))

        self.assertIsInstance(identity, Identity)
        self.assertTrue(identity.always)
        self.assertEqual(user_foreign_key.target_fullname, "users.user_id")
        self.assertEqual(user_foreign_key.ondelete, "CASCADE")

    def test_exercise_has_same_user_reference_key(self):
        unique_constraints = {
            constraint.name: tuple(column.name for column in constraint.columns)
            for constraint in Exercise.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
        }

        self.assertEqual(
            unique_constraints["exercises_exercise_id_user_id_uq"],
            ("exercise_id", "user_id"),
        )

    def test_exercise_name_rules_are_present(self):
        indexes = {index.name: index for index in Exercise.__table__.indexes}
        check_names = {
            constraint.name
            for constraint in Exercise.__table__.constraints
            if constraint.__class__.__name__ == "CheckConstraint"
        }

        self.assertEqual(set(indexes), {"exercises_user_id_name_lower_uq"})
        self.assertTrue(indexes["exercises_user_id_name_lower_uq"].unique)
        self.assertEqual(
            check_names,
            {"ck_exercises_name_trimmed_nonblank"},
        )


if __name__ == "__main__":
    unittest.main()
