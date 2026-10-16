import unittest

from sqlalchemy import ForeignKeyConstraint, Identity, Numeric, UniqueConstraint

from server.models import (
    Base,
    Exercise,
    SessionExercise,
    User,
    WorkoutSession,
    WorkoutSet,
    WorkoutType,
)


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
            ["workout_type_id", "user_id", "name", "archived_at"],
        )
        self.assertTrue(WorkoutType.__table__.c.archived_at.type.timezone)
        self.assertTrue(WorkoutType.__table__.c.archived_at.nullable)

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
            ["exercise_id", "user_id", "name", "archived_at"],
        )
        self.assertTrue(Exercise.__table__.c.archived_at.type.timezone)
        self.assertTrue(Exercise.__table__.c.archived_at.nullable)

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


class WorkoutSessionModelTests(unittest.TestCase):
    def test_workout_session_table_is_registered_with_expected_columns(self):
        self.assertIs(
            Base.metadata.tables["workout_sessions"],
            WorkoutSession.__table__,
        )
        self.assertEqual(
            list(WorkoutSession.__table__.columns.keys()),
            ["workout_session_id", "user_id", "workout_type_id", "session_date"],
        )

    def test_workout_session_has_generated_identity_and_owner_cascade(self):
        identity = WorkoutSession.__table__.c.workout_session_id.identity
        foreign_keys = {
            constraint.name: constraint
            for constraint in WorkoutSession.__table__.constraints
            if isinstance(constraint, ForeignKeyConstraint)
        }

        self.assertIsInstance(identity, Identity)
        self.assertTrue(identity.always)
        self.assertEqual(
            foreign_keys["fk_workout_sessions_user_id_users"].ondelete,
            "CASCADE",
        )

    def test_workout_session_enforces_same_user_workout_type(self):
        constraint = next(
            constraint
            for constraint in WorkoutSession.__table__.constraints
            if constraint.name == "workout_sessions_workout_type_owner_fk"
        )

        self.assertEqual(
            tuple(element.parent.name for element in constraint.elements),
            ("workout_type_id", "user_id"),
        )
        self.assertEqual(
            tuple(element.target_fullname for element in constraint.elements),
            ("workout_types.workout_type_id", "workout_types.user_id"),
        )
        self.assertIsNone(constraint.ondelete)

    def test_workout_session_has_reference_key_and_history_index(self):
        unique_constraints = {
            constraint.name: tuple(column.name for column in constraint.columns)
            for constraint in WorkoutSession.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
        }
        indexes = {
            index.name: tuple(column.name for column in index.columns)
            for index in WorkoutSession.__table__.indexes
        }

        self.assertEqual(
            unique_constraints[
                "workout_sessions_workout_session_id_user_id_uq"
            ],
            ("workout_session_id", "user_id"),
        )
        self.assertEqual(
            indexes["workout_sessions_user_id_session_date_ix"],
            ("user_id", "session_date"),
        )


class SessionExerciseModelTests(unittest.TestCase):
    def test_session_exercise_table_is_registered_with_expected_columns(self):
        self.assertIs(
            Base.metadata.tables["session_exercises"],
            SessionExercise.__table__,
        )
        self.assertEqual(
            list(SessionExercise.__table__.columns.keys()),
            [
                "session_exercise_id",
                "workout_session_id",
                "exercise_id",
                "user_id",
                "exercise_order",
            ],
        )

    def test_session_exercise_enforces_same_user_parents(self):
        foreign_keys = {
            constraint.name: constraint
            for constraint in SessionExercise.__table__.constraints
            if isinstance(constraint, ForeignKeyConstraint)
        }

        self.assertEqual(
            tuple(
                element.target_fullname
                for element in foreign_keys[
                    "session_exercises_workout_session_owner_fk"
                ].elements
            ),
            (
                "workout_sessions.workout_session_id",
                "workout_sessions.user_id",
            ),
        )
        self.assertEqual(
            foreign_keys["session_exercises_workout_session_owner_fk"].ondelete,
            "CASCADE",
        )
        self.assertEqual(
            tuple(
                element.target_fullname
                for element in foreign_keys[
                    "session_exercises_exercise_owner_fk"
                ].elements
            ),
            ("exercises.exercise_id", "exercises.user_id"),
        )
        self.assertIsNone(
            foreign_keys["session_exercises_exercise_owner_fk"].ondelete
        )
        self.assertEqual(
            foreign_keys["fk_session_exercises_user_id_users"].ondelete,
            "CASCADE",
        )

    def test_session_exercise_order_is_positive_and_unique_per_session(self):
        check_names = {
            constraint.name
            for constraint in SessionExercise.__table__.constraints
            if constraint.__class__.__name__ == "CheckConstraint"
        }
        unique_constraints = {
            constraint.name: tuple(column.name for column in constraint.columns)
            for constraint in SessionExercise.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
        }

        self.assertEqual(
            check_names,
            {"ck_session_exercises_exercise_order_positive"},
        )
        self.assertEqual(
            unique_constraints[
                "session_exercises_workout_session_id_exercise_order_uq"
            ],
            ("workout_session_id", "exercise_order"),
        )


class WorkoutSetModelTests(unittest.TestCase):
    def test_set_table_is_registered_with_expected_columns(self):
        self.assertIs(Base.metadata.tables["sets"], WorkoutSet.__table__)
        self.assertEqual(
            list(WorkoutSet.__table__.columns.keys()),
            [
                "set_id",
                "session_exercise_id",
                "set_number",
                "repetitions",
                "rir",
                "load_lbs",
            ],
        )

    def test_set_has_generated_identity_and_parent_cascade(self):
        identity = WorkoutSet.__table__.c.set_id.identity
        foreign_key = next(
            iter(WorkoutSet.__table__.c.session_exercise_id.foreign_keys)
        )

        self.assertIsInstance(identity, Identity)
        self.assertTrue(identity.always)
        self.assertEqual(
            foreign_key.target_fullname,
            "session_exercises.session_exercise_id",
        )
        self.assertEqual(foreign_key.ondelete, "CASCADE")

    def test_set_performance_columns_have_expected_nullability_and_type(self):
        load_type = WorkoutSet.__table__.c.load_lbs.type

        self.assertFalse(WorkoutSet.__table__.c.repetitions.nullable)
        self.assertTrue(WorkoutSet.__table__.c.rir.nullable)
        self.assertTrue(WorkoutSet.__table__.c.load_lbs.nullable)
        self.assertIsInstance(load_type, Numeric)
        self.assertEqual((load_type.precision, load_type.scale), (8, 2))

    def test_set_value_rules_and_scoped_number_are_present(self):
        check_names = {
            constraint.name
            for constraint in WorkoutSet.__table__.constraints
            if constraint.__class__.__name__ == "CheckConstraint"
        }
        unique_constraints = {
            constraint.name: tuple(column.name for column in constraint.columns)
            for constraint in WorkoutSet.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
        }

        self.assertEqual(
            check_names,
            {
                "ck_sets_load_lbs_nonnegative",
                "ck_sets_repetitions_nonnegative",
                "ck_sets_rir_range",
                "ck_sets_set_number_positive",
            },
        )
        self.assertEqual(
            unique_constraints["sets_session_exercise_id_set_number_uq"],
            ("session_exercise_id", "set_number"),
        )


if __name__ == "__main__":
    unittest.main()
