import time
import json
import io
from datetime import datetime, timedelta

from logging import error, info

from rest import RESTful

OUTDOOR_WORKOUT = 1072


class Fitbit2Strava:

    def __init__(self, fitbit_client: RESTful, strava_client: RESTful):
        self.fitbit_client = fitbit_client
        self.strava_client = strava_client

    def start(self):
        while True:
            self.upload_activities()

            time.sleep(5 * 60)

    def upload_activities(self):
        strava_client = self.strava_client
        fitbit_client = self.fitbit_client

        after_date = datetime.today() - timedelta(days=7)
        after_date = after_date.strftime("%Y-%m-%d")

        user_id = fitbit_client.get_token()["user_id"]
        resp = fitbit_client.get(f"/user/{user_id}/activities/list.json", params={
            "afterDate": after_date,
            "sort": "asc",
            "limit": 10,
            "offset": 0
        })

        if resp.status_code != 200:
            error(f"Status: {resp.status_code}, Message: {resp.text}")
            return

        activities = json.loads(resp.text)["activities"]
        activities = filter(lambda x: x["activityTypeId"] == OUTDOOR_WORKOUT, activities)

        after_date = datetime.strptime(after_date, "%Y-%m-%d")
        after_date = round(after_date.timestamp())
        resp = strava_client.get("/athlete/activities", params={
            "after": after_date
        })

        if resp.status_code != 200:
            error(f"status:{resp.status_code}, message: {resp.text}")
            return

        strava_activities = json.loads(resp.text)
        external_ids = map(lambda x: x["external_id"], strava_activities)

        activities = filter(lambda x: f"fitbit_push_{x['logId']}" not in external_ids, activities)
        activities = list(activities)
        info(f"found {len(activities)} new Fitbit activities")

        for activity in activities:
            log_id = activity["logId"]

            resp = fitbit_client.get(f"/user/{user_id}/activities/{log_id}.tcx")
            if resp.status_code != 200:
                error(f"status:{resp.status_code}, message: {resp.text}")
                return

            with io.StringIO(resp.text) as activity_tcx:
                resp = strava_client.upload("/uploads", activity_tcx, params={
                    "name": "Outdoor Workout",
                    "data_type": "tcx",
                    "external_id": f"fitbit_push_{log_id}"
                })
                if resp.status_code != 201:
                    error(f"status:{resp.status_code}, message: {resp.text}")
                    return

                info("upload activity successful")
