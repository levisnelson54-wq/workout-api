from datetime import date

from server import create_app, db
from server.models import Exercise, Workout, WorkoutExercise


app = create_app()

with app.app_context():
    db.create_all()

    if Exercise.query.first() is None:
        pushups = Exercise(
            name='Push-ups',
            category='Strength',
            equipment_needed=False
        )

        squats = Exercise(
            name='Squats',
            category='Strength',
            equipment_needed=False
        )

        running = Exercise(
            name='Running',
            category='Cardio',
            equipment_needed=False
        )

        db.session.add_all([pushups, squats, running])
        db.session.flush()

        workout = Workout(
            date=date.today(),
            duration_minutes=45,
            notes='Full body workout'
        )

        db.session.add(workout)
        db.session.flush()

        db.session.add_all([
            WorkoutExercise(
                workout_id=workout.id,
                exercise_id=pushups.id,
                reps=12,
                sets=3,
                duration_seconds=0
            ),
            WorkoutExercise(
                workout_id=workout.id,
                exercise_id=squats.id,
                reps=15,
                sets=3,
                duration_seconds=0
            )
        ])

        db.session.commit()

        print('Database seeded successfully!')

    else:
        print('Database already contains exercises. Skipping seed.')