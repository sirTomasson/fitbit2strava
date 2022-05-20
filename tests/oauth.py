import unittest
from fitbit2strava.oauth import OAuth


class TestOAuth(unittest.TestCase):

    def test_authorize_url(self):
        oauth_client = OAuth({
            "schema": "https",
            "host": "localhost",
            "authorize_endpoint": "/authorize",
            "authorize_params": {
                "redirect_uri": "https://localhost/callback",
                "client_id": 1,
                "client_secret": 2
            },
        })
        url = oauth_client.authorize_url()
        self.assertEqual(url,
                         "https://localhost/authorize?redirect_uri=https%3A%2F%2Flocalhost%2Fcallback&client_id=1&client_secret=2")

    def test_token(self):
        pass

    def test_refresh_token(self):
        pass


if __name__ == "__main__":
    unittest.main()
