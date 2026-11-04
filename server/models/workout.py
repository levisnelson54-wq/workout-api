from server import db
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates


class Workout(db.Model):
    __tablename__ = 'workouts'

    __table_args__ = (
        CheckConstraint(
            'duration_minutes > 0',
            name='check_workout_duration'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=False)

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError('Workout duration must be greater than zero.')
        return value

    @validates('notes')
    def validate_notes(self, key, value):
        if not value or not value.strip():
            raise ValueError('Workout notes cannot be empty.')
        return value.strip()

    def __repr__(self):
        return f'<Workout {self.id}>'
