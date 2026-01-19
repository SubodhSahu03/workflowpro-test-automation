import pytest
from playwright.sync_api import sync_playwright
from utils.api_client import APIClient

# ---------- Playwright Fixtures ----------

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def api_client():

    token = "dummy-test-token"
    tenant_id = "company1"

    return APIClient(token=token, tenant_id=tenant_id)
