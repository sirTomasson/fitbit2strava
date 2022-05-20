FROM python:3.9

WORKDIR ./fitbit2strava

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY /fitbit2strava .

RUN mkdir /fitbit2strava/config && mkdir /fitbit2strava/token

CMD [ "python3", "main.py"]

