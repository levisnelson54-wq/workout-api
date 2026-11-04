def test_get_exercises_returns_empty_list(client):
    response = client.get('/exercises')

    assert response.status_code == 200
    assert response.json == []


def test_create_exercise(client):
    response = client.post('/exercises', json={
        'name': 'Push-ups',
        'category': 'Strength',
        'equipment_needed': False
    })

    assert response.status_code == 201
    assert response.json['name'] == 'Push-ups'
    assert response.json['category'] == 'Strength'
    assert response.json['equipment_needed'] is False
    assert 'id' in response.json


def test_get_exercise(client):
    created = client.post('/exercises', json={
        'name': 'Squats',
        'category': 'Strength',
        'equipment_needed': False
    })

    exercise_id = created.json['id']

    response = client.get(f'/exercises/{exercise_id}')

    assert response.status_code == 200
    assert response.json['name'] == 'Squats'


def test_get_nonexistent_exercise(client):
    response = client.get('/exercises/999')

    assert response.status_code == 404
    assert response.json['error'] == 'Exercise not found'


def test_create_exercise_with_missing_fields(client):
    response = client.post('/exercises', json={
        'name': 'Push-ups'
    })

    assert response.status_code == 400


def test_create_exercise_with_empty_name(client):
    response = client.post('/exercises', json={
        'name': '',
        'category': 'Strength',
        'equipment_needed': False
    })

    assert response.status_code == 400


def test_create_exercise_without_json(client):
    response = client.post('/exercises')

    assert response.status_code == 400


def test_delete_exercise(client):
    created = client.post('/exercises', json={
        'name': 'Lunges',
        'category': 'Strength',
        'equipment_needed': False
    })

    exercise_id = created.json['id']

    response = client.delete(f'/exercises/{exercise_id}')

    assert response.status_code == 204

    deleted = client.get(f'/exercises/{exercise_id}')
    assert deleted.status_code == 404


def test_delete_nonexistent_exercise(client):
    response = client.delete('/exercises/999')

    assert response.status_code == 404
