from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from server import db
from server.models import Exercise
from server.schemas.exercise_schema import exercise_schema, exercises_schema


exercise_bp = Blueprint('exercises', __name__, url_prefix='/exercises')


@exercise_bp.route('', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@exercise_bp.route('/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


@exercise_bp.route('', methods=['POST'])
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    try:
        validated_data = exercise_schema.load(data)
        exercise = Exercise(**validated_data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({'errors': error.messages}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500


@exercise_bp.route('/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404

    try:
        db.session.delete(exercise)
        db.session.commit()
        return '', 204

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
