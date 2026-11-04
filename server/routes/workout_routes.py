from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from server import db
from server.models import Workout, Exercise, WorkoutExercise
from server.schemas.workout_schema import (
    workout_schema,
    workouts_schema,
    workout_exercise_schema
)


workout_bp = Blueprint('workouts', __name__, url_prefix='/workouts')


@workout_bp.route('', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@workout_bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404

    return jsonify(workout_schema.dump(workout)), 200


@workout_bp.route('', methods=['POST'])
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    try:
        validated_data = workout_schema.load(data)
        workout = Workout(**validated_data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({'errors': error.messages}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500


@workout_bp.route('/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404

    try:
        db.session.delete(workout)
        db.session.commit()
        return '', 204

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500


@workout_bp.route(
    '/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST']
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404

    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    try:
        validated_data = workout_exercise_schema.load(data)

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **validated_data
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({'errors': error.messages}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'error': 'This exercise is already in the workout.'
        }), 409

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
