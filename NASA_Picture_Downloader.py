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


sender = "NASA <NASA@totallyNASA.com>"
receiver = "A Test User <to@example.com>"
endpoint = "https://api.nasa.gov/planetary/apod"

# load the configuration file contents
config = load_yaml("./config.yaml")
api_key = config["NASA_api_key"]

# define query parameters for the api call
query_params = {"api_key": api_key, "date": datetime.today().strftime("%Y-%m-%d")}

# make the api call
response = requests.get(endpoint, params=query_params)

# if the call is successful, the status code will be 200 and the code is going
# to run and write the email message
if response.status_code == 200:
    # extract the relevant information from the api call
    explanation = response.json()["explanation"]
    title = response.json()["title"]
    media_type = response.json()["media_type"]
    url = response.json()["url"]

    # according to the type of the media of the day, a message will be
    # scripted taking into account it being a video of the day or a picture
    # of the day
    if media_type == "image":
        message = f"""\
        Subject: Your Daily Astronomy Picture: {title}
        To: {receiver}
        From: {sender}

        Hello Fabrizio,

        This is the Astronomy Picture of the Day:

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
    print(message)
# If the call is unsuccessful, the program prints to console the error
else:
    print(f"{response.status_code}: {response.reason}")
