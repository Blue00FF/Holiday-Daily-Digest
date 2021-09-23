from datetime import datetime
import smtplib
import requests
import yaml


# define a program that safely loads the data from the yaml configuration file
def load_yaml(filepath):
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


sender = "NASA <from@example.com>"
receiver = "A Test User <to@example.com>"
endpoint = "https://api.nasa.gov/planetary/apod"

# load the configuration file contents
config = load_yaml("./config.yaml")

# define query parameters for the api call
api_key = config["NASA_api_key"]
query_params = {"api_key": api_key, "date": datetime.today().strftime("%Y-%m-%d")}

# make the api call
response = requests.get(endpoint, params=query_params)

# if the call is successful, the status code will be 200 and the code is going
# to run and send the email successfully
if response.status_code == 200:
    # extract the information from the api call
    explanation = response.json()["explanation"]
    title = response.json()["title"]
    media_type = response.json()["media_type"]
    url = response.json()["url"]

    # the program checks whether the media of the day is an image or a video and
    # adjusts the message accordingly
    if media_type == "image":
        message = f"""\
        Subject: Your Daily Astronomy Picture: {title}
        To: {receiver}
        From: {sender}

        Hello Fabrizio,

        This is today's Astronomy Picture of the Day:

        {explanation}

        {url}
        """
    else:
        message = f"""\
        Subject: Your Daily Astronomy Video: {title}
        To: {receiver}
        From: {sender}

        Hello Fabrizio,

        This is the Astronomy Video of the Day:

        {explanation}

        {url}
        """
    # Since the email will potentially contain ascii incompatible characters
    # that would conflict with the send mail script, I get rid of them
    message = message.encode("ascii", "ignore").decode("ascii")

    # Send the email using the local host server
    with smtplib.SMTP("localhost", 1025) as server:
        server.sendmail(sender, receiver, message)

# If the call is unsuccessful, the program prints to console the error
else:
    print(f"{response.status_code}: {response.reason}")
