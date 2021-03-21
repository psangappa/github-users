def test_get_users(test_client, users):
    response = test_client.get(f"/api/v1/users?usernames={users}")
    assert response.status_code == 200
    result = response.json()
    assert len(result["users"]) == len(users.split(","))


def test_users_invalid_input(test_client):
    response = test_client.get("/api/v1/users?usernam=1,2,3")
    assert response.status_code == 422
    result = response.json()

    assert "users" not in result
    assert result == {
        "detail": [
            {
                "loc": ["query", "usernames"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
