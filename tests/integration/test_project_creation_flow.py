def test_project_creation_flow(api_client, page):
    response = api_client.create_project({
        "name": "Integration Project",
        "description": "API + UI validation"
    })

    assert response.status_code == 201

    page.goto("/dashboard", wait_until="networkidle")
    assert page.locator("text=Integration Project").is_visible()

    page.set_viewport_size({"width": 375, "height": 812})
    assert page.locator("text=Integration Project").is_visible()
