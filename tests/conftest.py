import os
import pytest
from fastapi.testclient import TestClient
import requests
from main import app

class FlexibleClient:
    def __init__(self, app, base_url=None):
        self.app = app
        self.base_url = base_url or os.getenv("BACKEND_TEST_BASE_URL")
        if not self.base_url:
            self.local_client = TestClient(app)
        else:
            self.local_client = None

    def _request(self, method, url, **kwargs):
        if self.local_client:
            return getattr(self.local_client, method)(url, **kwargs)
        else:
            path = url
            if not path.startswith("/"):
                path = "/" + path
            full_url = self.base_url.rstrip("/") + path
            return getattr(requests, method)(full_url, **kwargs)

    def get(self, url, **kwargs):
        return self._request("get", url, **kwargs)

    def post(self, url, **kwargs):
        return self._request("post", url, **kwargs)

    def put(self, url, **kwargs):
        return self._request("put", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request("delete", url, **kwargs)

@pytest.fixture(scope="session")
def client():
    return FlexibleClient(app)
