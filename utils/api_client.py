import requests

class APIClient:
    def __init__(self, token, tenant_id):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": tenant_id
        }

    def create_project(self, payload):
        return requests.post(
            "https://app.workflowpro.com/api/v1/projects",
            headers=self.headers,
            json=payload
        )
