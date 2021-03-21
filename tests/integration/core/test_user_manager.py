def test_missing_users(test_client):
    missing_user = "someonemissing"
    response = test_client.get(f"/api/v1/users?usernames={missing_user}")
    assert response.status_code == 200
    result = response.json()
    assert result["missing"] == 1


def test_do_not_include_latest_commit(test_client, users):
    response = test_client.get(f"/api/v1/users?usernames={users}")
    assert response.status_code == 200
    result = response.json()
    assert all(
        [
            "latest_commit" not in repo
            for user in result["users"]
            for repo in user["public_repositories"]
        ]
    )


def test_include_latest_commit(test_client, users):
    response = test_client.get(f"/api/v1/users?usernames={users}&include=commit_latest")
    assert response.status_code == 200
    result = response.json()
    assert all(
        [
            "latest_commit" in repo
            for user in result["users"]
            for repo in user["public_repositories"]
        ]
    )


def test_repos_are_sorted_newest_to_oldest(test_client, users):
    response = test_client.get(f"/api/v1/users?usernames={users}")
    assert response.status_code == 200
    result = response.json()
    from datetime import datetime
    for user in result["users"]:
        updated_dates = [
            datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%S+00:00")
            for repo in user["public_repositories"]
        ]
        assert sorted(updated_dates, reverse=True) == updated_dates
