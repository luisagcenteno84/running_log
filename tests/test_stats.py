from datetime import date


def test_stats_summary_from_api(client) -> None:
    user = client.post(
        '/api/v1/users',
        json={
            'name': 'Stats Runner',
            'email': 'stats@example.com',
            'password': 'stats-pass-123',
        },
    )
    user_id = user.json()['id']

    client.post('/api/v1/runs', json={'user_id': user_id, 'date': str(date.today()), 'distance_km': 5.0, 'duration_seconds': 1400})
    client.post('/api/v1/runs', json={'user_id': user_id, 'date': str(date.today()), 'distance_km': 12.0, 'duration_seconds': 4200})

    response = client.get('/api/v1/stats', params={'user_id': user_id})
    assert response.status_code == 200

    body = response.json()
    assert body['total_distance_km'] == 17.0
    assert body['longest_run_id'] is not None
    assert body['fastest_run_id'] is not None
    assert body['training_frequency'] == 2
