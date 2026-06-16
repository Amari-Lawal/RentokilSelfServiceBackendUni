import os
from fastapi.testclient import TestClient
import requests

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
            # Live requests
            # Ensure the url starts with a single slash/is formatted correctly
            path = url
            if not path.startswith("/"):
                path = "/" + path
            full_url = self.base_url.rstrip("/") + path
            # Make the request to the live backend URL
            return getattr(requests, method)(full_url, **kwargs)

    def get(self, url, **kwargs):
        return self._request("get", url, **kwargs)

    def post(self, url, **kwargs):
        return self._request("post", url, **kwargs)

    def put(self, url, **kwargs):
        return self._request("put", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request("delete", url, **kwargs)
