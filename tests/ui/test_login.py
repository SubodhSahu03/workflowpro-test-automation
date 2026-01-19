def test_user_login(page):
    page.goto("/login", wait_until="networkidle")
    page.fill("#email", "admin@company1.com")
    page.fill("#password", "password123")
    page.click("#login-btn")

    page.wait_for_url("**/dashboard", timeout=15000)
    assert page.locator(".welcome-message").is_visible()
