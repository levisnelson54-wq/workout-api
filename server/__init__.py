from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from server.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    # Apply test configuration before initializing the database
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register database models
    from server.models import Exercise, Workout, WorkoutExercise

    # Register API routes
    from server.routes import exercise_bp, workout_bp

    app.register_blueprint(exercise_bp)
    app.register_blueprint(workout_bp)

    return app