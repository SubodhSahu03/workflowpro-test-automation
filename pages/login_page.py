class LoginPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("/login", wait_until="networkidle")

    def login(self, email, password):
        self.page.fill("#email", email)
        self.page.fill("#password", password)
        self.page.click("#login-btn")
