import logging
from logging import error

from oauth import OAuth
from rest import RESTful
from connector import Fitbit2Strava

logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(name)s] %(message)s [%(asctime)s]')
logging.addLevelName(level=logging.DEBUG, levelName="[DEBUG 🐜]")
logging.addLevelName(level=logging.INFO, levelName="[INFO ℹ]")
logging.addLevelName(level=logging.WARNING, levelName="[WARNING ⚠]")
logging.addLevelName(level=logging.ERROR, levelName="[ERROR 💣]")


def main():
    strava_oauth_client = OAuth(config_path="./config/strava-oauth.config.json")
    fitbit_oauth_client = OAuth(config_path="./config/fitbit-oauth.config.json")

    if not strava_oauth_client.token_exists() and not fitbit_oauth_client.token_exists():
        error("No token(s) found for Strava and Fitbit clients; Please run the setup.py script.")
        return

    strava_client = RESTful("www.strava.com", strava_oauth_client, api_prefix="/api/v3")
    fitbit_client = RESTful("api.fitbit.com", fitbit_oauth_client, api_prefix="/1")

    Fitbit2Strava(fitbit_client, strava_client).start()


if __name__ == "__main__":
    main()
