import requests as req

from oauth import OAuth

from logging import debug


class RESTful:

    def __init__(self, host, oauth_client: OAuth = None, schema="https", headers=None, api_prefix=""):
        self.schema = schema
        self.host = host
        self.oauth_client = oauth_client
        if headers is None:
            headers = {}
        self.headers = headers
        self.api_prefix = api_prefix

    def to_url(self, endpoint: str) -> str:
        return f"{self.schema}://{self.host}{self.api_prefix}{endpoint}"

    def request(self, method: str, endpoint: str, params: dict = None, json: dict = None):
        debug(f"[{method}] [{self.host} {endpoint}]")
        url = self.to_url(endpoint)
        headers = self.headers
        if self.oauth_client and self.oauth_client.token_exists():
            headers["authorization"] = "Bearer {}".format(self.oauth_client.get_access_token())

        return req.request(method, url, params=params, json=json, headers=headers)

    def get(self, endpoint: str, params: dict = None):
        return self.request("GET", endpoint, params)

    def post(self, endpoint: str, params: dict = None, json: dict = None):
        return self.request("POST", endpoint, params, json)

    def put(self, endpoint: str, params: dict = None, json: dict = None):
        return self.request("PUT", endpoint, params, json)

    def delete(self, endpoint: str, params: dict = None, json: dict = None):
        return self.request("DELETE", endpoint, params, json)

    def upload(self, endpoint: str, file, params: dict = None):
        url = self.to_url(endpoint)
        headers = self.headers
        if self.oauth_client and self.oauth_client.token_exists():
            headers["authorization"] = f"Bearer {self.oauth_client.get_access_token()}"

        return req.post(url, params=params, files={"file": file}, headers=headers)

    def get_token(self):
        return self.oauth_client.get_token()
