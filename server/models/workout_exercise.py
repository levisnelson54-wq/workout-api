from server import db
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    __table_args__ = (
        CheckConstraint('reps > 0', name='check_reps_positive'),
        CheckConstraint('sets > 0', name='check_sets_positive'),
        CheckConstraint(
            'duration_seconds >= 0',
            name='check_exercise_duration'
        ),
        UniqueConstraint(
            'workout_id',
            'exercise_id',
            name='unique_workout_exercise'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey('workouts.id'),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey('exercises.id'),
        nullable=False
    )

    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)

    workout = db.relationship(
        'Workout',
        back_populates='workout_exercises'
    )

    exercise = db.relationship(
        'Exercise',
        back_populates='workout_exercises'
    )

    @validates('reps', 'sets')
    def validate_positive_values(self, key, value):
        if value is None or value <= 0:
            raise ValueError(f'{key} must be greater than zero.')
        return value

    @validates('duration_seconds')
    def validate_duration(self, key, value):
        if value is None or value < 0:
            raise ValueError('Duration cannot be negative.')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}>'
