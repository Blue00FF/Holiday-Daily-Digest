import smtplib
import requests
import yaml


def load_yaml(filepath):
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


config = load_yaml("./config.yaml")

sender = "Calendarific <bot@calendarific.com>"
receiver = "A Test User <to@example.com>"

api_key = config['calendarific_api_key']
query_params = {"api_key": api_key, "year": 2021, "month": 1, "day": 1, "country": "UK"}
response = requests.get("https://calendarific.com/api/v2/holidays", params=query_params)
name = response.json()["response"]["holidays"][0]["name"]
description = response.json()["response"]["holidays"][0]["description"]

if response.status_code == 200:
    message = f"""\
    Subject: Your Calendarific Notification
    To: {receiver}
    From:{sender}

    Hello user,

    This is you notification from Calendarific.

    Today is an holiday in your country!

    {name} :

    {description}
    """

    with smtplib.SMTP("localhost", 1025) as server:
        server.sendmail(sender, receiver, message)

else:
    print(f"{response.status_code}: {response.reason}")
