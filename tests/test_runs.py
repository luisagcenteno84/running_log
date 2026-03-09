def test_create_run_computes_pace_and_speed(client) -> None:
    user = client.post(
        '/api/v1/users',
        json={
            'name': 'Test Runner',
            'email': 'runner@example.com',
            'password': 'runner-pass-123',
        },
    )
    assert user.status_code == 201
    user_id = user.json()['id']

    payload = {
        'user_id': user_id,
        'date': '2026-01-10',
        'distance_km': 5.2,
        'duration_seconds': 1500,
        'avg_heart_rate': 152,
        'notes': 'Steady evening run',
    }
    response = client.post('/api/v1/runs', json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body['user_id'] == user_id
    assert body['avg_pace'] == '4:48/km'
    assert body['avg_speed_kmh'] == 12.48


def test_list_runs_with_filters(client) -> None:
    user = client.post(
        '/api/v1/users',
        json={
            'name': 'Filter Runner',
            'email': 'filter@example.com',
            'password': 'filter-pass-123',
        },
    )
    user_id = user.json()['id']

    client.post('/api/v1/runs', json={'user_id': user_id, 'date': '2026-01-10', 'distance_km': 3.0, 'duration_seconds': 1100})
    client.post('/api/v1/runs', json={'user_id': user_id, 'date': '2026-01-15', 'distance_km': 10.0, 'duration_seconds': 3200})

    response = client.get('/api/v1/runs', params={'user_id': user_id, 'min_distance_km': 5})
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 1
    assert rows[0]['distance_km'] == 10.0
