from server import db
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates


class Exercise(db.Model):
    __tablename__ = 'exercises'

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name='check_exercise_name'
        ),
        CheckConstraint(
            "length(trim(category)) > 0",
            name='check_exercise_category'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # An exercise can appear in many workout records
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    # An exercise can belong to many workouts
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True
    )

    @validates('name', 'category')
    def validate_text_fields(self, key, value):
        if not value or not value.strip():
            raise ValueError(f'{key} cannot be empty.')

        value = value.strip()

        if len(value) > 100:
            raise ValueError(f'{key} cannot exceed 100 characters.')

        return value

    def __repr__(self):
        return f'<Exercise {self.name}>'