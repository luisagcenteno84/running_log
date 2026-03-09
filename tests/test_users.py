def test_create_user_and_sign_in(client) -> None:
    create_response = client.post(
        '/api/v1/users',
        json={
            'name': 'Signed In Runner',
            'email': 'signin@example.com',
            'password': 'signin-pass-123',
        },
    )

    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user['email'] == 'signin@example.com'
    assert 'password' not in created_user

    sign_in_response = client.post(
        '/api/v1/users/sign-in',
        json={'email': 'signin@example.com', 'password': 'signin-pass-123'},
    )
    assert sign_in_response.status_code == 200
    assert sign_in_response.json()['id'] == created_user['id']


def test_sign_in_rejects_invalid_password(client) -> None:
    client.post(
        '/api/v1/users',
        json={
            'name': 'Wrong Password Runner',
            'email': 'wrongpass@example.com',
            'password': 'correct-pass-123',
        },
    )

    response = client.post(
        '/api/v1/users/sign-in',
        json={'email': 'wrongpass@example.com', 'password': 'bad-pass-123'},
    )
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid email or password'


def test_reset_password_allows_sign_in_with_new_password(client) -> None:
    client.post(
        '/api/v1/users',
        json={
            'name': 'Reset Runner',
            'email': 'reset@example.com',
            'password': 'old-pass-123',
        },
    )

    reset_response = client.post(
        '/api/v1/users/reset-password',
        json={'email': 'reset@example.com', 'new_password': 'new-pass-123'},
    )
    assert reset_response.status_code == 200

    old_sign_in = client.post(
        '/api/v1/users/sign-in',
        json={'email': 'reset@example.com', 'password': 'old-pass-123'},
    )
    assert old_sign_in.status_code == 401

    new_sign_in = client.post(
        '/api/v1/users/sign-in',
        json={'email': 'reset@example.com', 'password': 'new-pass-123'},
    )
    assert new_sign_in.status_code == 200
