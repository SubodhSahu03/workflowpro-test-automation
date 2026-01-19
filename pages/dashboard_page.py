class DashboardPage:
    def __init__(self, page):
        self.page = page

    def wait_for_load(self):
        self.page.wait_for_selector(".welcome-message", timeout=15000)

    def get_projects(self):
        return self.page.locator(".project-card")
