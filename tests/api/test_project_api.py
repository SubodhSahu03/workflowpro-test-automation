def test_create_project(api_client):
    payload = {
        "name": "API Project",
        "description": "Created via API"
    }

    response = api_client.create_project(payload)
    assert response.status_code == 201
