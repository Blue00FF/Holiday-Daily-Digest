import smtplib
import requests
import yaml
from datetime import datetime


# define a program that safely loads the data from the yaml configuration file
def load_yaml(filepath):
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


# load the configuration file contents
config = load_yaml("./config.yaml")

sender = "Calendarific <bot@calendarific.com>"
receiver = "A Test User <to@example.com>"

# define query parameters for the api call
api_key = config['calendarific_api_key']
query_params = {"api_key": api_key, "year": datetime.year,
                "month": datetime.month, "day": datetime.day, "country": "UK"}

# make the api call
response = requests.get("https://calendarific.com/api/v2/holidays", params=query_params)

# if the call is successful, the status code will be 200 and the code is going to
# run and send the email successfully
if response.status_code == 200:
    try:
        # extract the relevant information from the api call
        # in case the information is not there, i.e. there is no holiday on the
        # day, an IndexError will be raised and no message will be scripted nor
        # sent.
        name = response.json()["response"]["holidays"][0]["name"]
        description = response.json()["response"]["holidays"][0]["description"]

        # compose the message
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

        # send the message as email on the local host server
        with smtplib.SMTP("localhost", 1025) as server:
            server.sendmail(sender, receiver, message)
    except IndexError:
        # If the website does not provide any holidays corresponding to the day
        # no email will be sent to the user
        pass
# If the call is unsuccessful, the program prints to console the error
else:
    print(f"{response.status_code}: {response.reason}")
