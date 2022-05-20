from oauth import OAuth


def main():
    strava_oauth_client = OAuth(config_path="./config/strava-oauth.config.json")
    if not strava_oauth_client.token_exists():
        url = strava_oauth_client.authorize_url()
        print("Link your Strava account here: {} \n".format(url))
        code = input("Please enter your one-time code:\n")
        strava_oauth_client.new_token(code)

    fitbit_oauth_client = OAuth(config_path="./config/fitbit-oauth.config.json")
    if not fitbit_oauth_client.token_exists():
        url = fitbit_oauth_client.authorize_url()
        print("Link your Fitbit account: {} \n".format(url))
        code = input("Please enter your one-time code:\n")
        fitbit_oauth_client.new_token(code)


if __name__ == "__main__":
    main()
