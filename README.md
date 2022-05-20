# Fitbit 2 Strava Activity Connector

## Docker build
```
$ docker build -t sirtomasson/fitbit2strava .
```

## Docker run
```
$ docker run -v ~/fitbit2strava/config:/fitbit2strava/config \
             -v ~/fitbit2strava/token:/fitbit2strava/token \
             sirtomasson/fitbit2strava
```

## Setup script
```
$ docker run -it -v ~/fitbit2strava/config:/fitbit2strava/config \
             -v ~/fitbit2strava/token:/fitbit2strava/token \
             sirtomasson/fitbit2strava python3 setup.py
```