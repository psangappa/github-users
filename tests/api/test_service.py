

def test_that_the_service_is_running(test_client):
    response = test_client.get("http://localhost:8000/redoc")
    assert response.status_code == 200
