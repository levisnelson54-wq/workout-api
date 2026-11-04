from marshmallow import Schema, fields, validate, validates, ValidationError
from server.schemas.exercise_schema import ExerciseSchema


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)

    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)

    reps = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Integer(
        required=True,
        validate=validate.Range(min=0)
    )

    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

    notes = fields.String(
        required=True,
        validate=validate.Length(max=1000)
    )

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )

    @validates('notes')
    def validate_notes(self, value):
        if not value.strip():
            raise ValidationError('Workout notes cannot be empty.')


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
