import json
import os.path
import time
from logging import info
from os.path import exists
from urllib.parse import urlencode

import requests as req

DEFAULT_CONFIG = {
    "schema": "https",
    "host": None,
    "token_path": None,
    "authorize_endpoint": None,
    "authorize_params": None,
    "authorize_headers": None,
    "token_endpoint": None,
    "token_params": None,
    "token_headers": None,
    "refresh_token_endpoint": None,
    "refresh_token_params": None,
    "refresh_token_headers": None
}


def read_config(config_path):
    with open(config_path, "r") as file:
        return json.loads(file.read())


class OAuth:

    def __init__(self, config: dict = None, config_path=None) -> None:
        self.token = None
        if config_path:
            self.config = {**DEFAULT_CONFIG, **read_config(config_path)}
        elif config:
            self.config = {**DEFAULT_CONFIG, **config}
        else:
            raise ValueError("config or config_path may not be None.")

    def base_url(self):
        return "{schema}://{host}".format(schema=self.config["schema"],
                                          host=self.config["host"])

    def authorize_url(self):
        params = urlencode(self.config["authorize_params"])
        return "{base_url}{endpoint}?{params}".format(base_url=self.base_url(),
                                                      endpoint=self.config["authorize_endpoint"],
                                                      params=params)

    def new_token(self, code):
        params = self.config["token_params"]
        params["code"] = code
        encoded_params = urlencode(params)
        url = "{base_url}{endpoint}?{params}".format(base_url=self.base_url(),
                                                     endpoint=self.config["token_endpoint"],
                                                     params=encoded_params)
        resp = req.post(url, headers=self.config["token_headers"])
        if resp.status_code == 200:
            token = resp.text
            self.token = json.loads(token)
            self.set_token_expires_at()
            self.write_token(json.dumps(self.token))
            info(f"[oauth client {self.config['name']}] token obtained successfully.")
            return self.token
        else:
            raise Exception("Status {} Error: {}".format(resp.status_code, resp.text))

    def refresh_token(self, refresh_token):
        params = self.config["refresh_token_params"]
        params["refresh_token"] = refresh_token
        encoded_params = urlencode(params)
        url = "{base_url}{endpoint}?{params}".format(base_url=self.base_url(),
                                                     endpoint=self.config["refresh_token_endpoint"],
                                                     params=encoded_params)
        resp = req.post(url, headers=self.config["refresh_token_headers"])
        if resp.status_code == 200:
            token = resp.text
            self.token = json.loads(token)
            self.set_token_expires_at()
            self.write_token(json.dumps(self.token))
            info(f"[oauth client {self.config['name']}] token refreshed successfully.")
            return self.token
        else:
            raise Exception("Status {} Error: {}".format(resp.status_code, resp.text))

    def set_token_expires_at(self):
        if "expires_at" not in self.token.keys():
            self.token["expires_at"] = round(time.time()) + self.token["expires_in"]

    def get_access_token(self):
        return self.get_token()["access_token"]

    def get_token(self):
        if not self.token or self.token_exists():
            self.token = json.loads(self.read_token())
        else:
            raise Exception("No token exists for configuration {}".format(self.config))

        if self.is_token_expired():
            self.token = self.refresh_token(self.token["refresh_token"])

        return self.token

    def is_token_expired(self):
        now = round(time.time())
        return now > self.token["expires_at"]

    def read_token(self):
        with open(self.token_filepath(), "r") as file:
            return file.read()

    def write_token(self, token):
        with open(self.token_filepath(), "w") as file:
            file.write(token)

    def token_filepath(self):
        path = "{token_path}/{name}.token.json".format(token_path=self.config["token_path"], name=self.config["name"])
        return os.path.abspath(path)

    def token_exists(self):
        return self.token or exists(self.token_filepath())
