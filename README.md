# Workout Application Backend API

## Project Description

The Workout Application Backend API is a Flask-based REST API designed to help personal trainers manage workouts and exercises.

The application allows trainers to create, retrieve, and delete exercises and workouts. It also allows exercises to be added to workouts with details such as repetitions, sets, and duration.

## Technologies Used

- Python 3.8
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite
- Pytest

## Project Structure

```text
workout-api/
├── migrations/
├── server/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── app.py
│   ├── config.py
│   └── __init__.py
├── tests/
├── seed.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Installation Instructions

### 1. Clone the repository

```bash
git clone git@github.com:levisnelson54-wq/workout-api.git
cd workout-api
```

### 2. Install dependencies

```bash
pipenv install
```

### 3. Activate the virtual environment

```bash
pipenv shell
```

### 4. Apply database migrations

```bash
flask --app server.app db upgrade
```

### 5. Seed the database

```bash
python seed.py
```

The seed file creates sample exercises, a workout, and workout-exercise records.

## Running the Application

Start the Flask development server:

```bash
flask --app server.app run
```

The application runs at:

`http://127.0.0.1:5000`

## API Endpoints

All endpoints return JSON responses unless otherwise specified.

### Exercise Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<exercise_id>` | Retrieve one exercise |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise |

#### Create Exercise

POST `/exercises`

Example request:

```json
{
  "name": "Push-ups",
  "category": "Strength",
  "equipment_needed": false
}
```

### Workout Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<workout_id>` | Retrieve one workout |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<workout_id>` | Delete a workout |

#### Create Workout

POST `/workouts`

Example request:

```json
{
  "date": "2026-11-06",
  "duration_minutes": 45,
  "notes": "Full body workout"
}
```

### Workout Exercise Endpoint

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

#### Add Exercise to Workout

POST `/workouts/1/exercises/1/workout_exercises`

Example request:

```json
{
  "reps": 12,
  "sets": 3,
  "duration_seconds": 60
}
```

## Validation and Error Handling

The application uses Marshmallow schemas and SQLAlchemy model validations to ensure data integrity.

It also implements database constraints to prevent invalid records.

Common HTTP status codes include:

- `200`: Successful request.
- `201`: Resource successfully created.
- `204`: Resource successfully deleted.
- `400`: Invalid request or validation error.
- `404`: Resource not found.
- `409`: Duplicate exercise added to a workout.
- `500`: Database error.

## Running Tests

Run the test suite using:

```bash
pipenv run pytest -v
```

The tests cover exercise operations, workout operations, validation, error handling, and workout-exercise relationships.

## Database Migrations

To apply existing migrations:

```bash
flask --app server.app db upgrade
```

To check the current migration version:

```bash
flask --app server.app db current
```

## Author

Levis Nelson

GitHub: https://github.com/levisnelson54-wq
