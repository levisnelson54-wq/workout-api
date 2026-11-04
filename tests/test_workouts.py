def create_workout(client):
    return client.post('/workouts', json={
        'date': '2026-10-30',
        'duration_minutes': 45,
        'notes': 'Upper body training'
    })


def create_exercise(client):
    return client.post('/exercises', json={
        'name': 'Push-ups',
        'category': 'Strength',
        'equipment_needed': False
    })


def test_get_workouts_returns_empty_list(client):
    response = client.get('/workouts')

    assert response.status_code == 200
    assert response.json == []


def test_create_workout(client):
    response = create_workout(client)

    assert response.status_code == 201
    assert response.json['duration_minutes'] == 45
    assert response.json['notes'] == 'Upper body training'
    assert 'id' in response.json


def test_get_workout(client):
    created = create_workout(client)
    workout_id = created.json['id']

    response = client.get(f'/workouts/{workout_id}')

    assert response.status_code == 200
    assert response.json['duration_minutes'] == 45


def test_get_nonexistent_workout(client):
    response = client.get('/workouts/999')

    assert response.status_code == 404


def test_create_workout_with_missing_fields(client):
    response = client.post('/workouts', json={
        'notes': 'Training session'
    })

    assert response.status_code == 400


def test_create_workout_with_invalid_duration(client):
    response = client.post('/workouts', json={
        'date': '2026-10-30',
        'duration_minutes': 0,
        'notes': 'Training session'
    })

    assert response.status_code == 400


def test_create_workout_without_json(client):
    response = client.post('/workouts')

    assert response.status_code == 400


def test_delete_workout(client):
    created = create_workout(client)
    workout_id = created.json['id']

    response = client.delete(f'/workouts/{workout_id}')

    assert response.status_code == 204

    deleted = client.get(f'/workouts/{workout_id}')
    assert deleted.status_code == 404


def test_delete_nonexistent_workout(client):
    response = client.delete('/workouts/999')

    assert response.status_code == 404


def test_add_exercise_to_workout(client):
    workout = create_workout(client)
    exercise = create_exercise(client)

    response = client.post(
        f"/workouts/{workout.json['id']}/exercises/{exercise.json['id']}/workout_exercises",
        json={
            'reps': 12,
            'sets': 3,
            'duration_seconds': 0
        }
    )

    assert response.status_code == 201
    assert response.json['reps'] == 12
    assert response.json['sets'] == 3
    assert response.json['duration_seconds'] == 0


def test_add_duplicate_exercise_to_workout(client):
    workout = create_workout(client)
    exercise = create_exercise(client)

    url = (
        f"/workouts/{workout.json['id']}/exercises/"
        f"{exercise.json['id']}/workout_exercises"
    )

    data = {
        'reps': 12,
        'sets': 3,
        'duration_seconds': 0
    }

    first_response = client.post(url, json=data)
    second_response = client.post(url, json=data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_add_exercise_with_invalid_reps(client):
    workout = create_workout(client)
    exercise = create_exercise(client)

    response = client.post(
        f"/workouts/{workout.json['id']}/exercises/{exercise.json['id']}/workout_exercises",
        json={
            'reps': 0,
            'sets': 3,
            'duration_seconds': 0
        }
    )

    assert response.status_code == 400


def test_add_exercise_with_invalid_sets(client):
    workout = create_workout(client)
    exercise = create_exercise(client)

    response = client.post(
        f"/workouts/{workout.json['id']}/exercises/{exercise.json['id']}/workout_exercises",
        json={
            'reps': 12,
            'sets': 0,
            'duration_seconds': 0
        }
    )

    assert response.status_code == 400


def test_add_exercise_to_nonexistent_workout(client):
    exercise = create_exercise(client)

    response = client.post(
        f"/workouts/999/exercises/{exercise.json['id']}/workout_exercises",
        json={
            'reps': 12,
            'sets': 3,
            'duration_seconds': 0
        }
    )

    assert response.status_code == 404


def test_add_nonexistent_exercise_to_workout(client):
    workout = create_workout(client)

    response = client.post(
        f"/workouts/{workout.json['id']}/exercises/999/workout_exercises",
        json={
            'reps': 12,
            'sets': 3,
            'duration_seconds': 0
        }
    )

    assert response.status_code == 404
