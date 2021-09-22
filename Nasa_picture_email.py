from datetime import datetime
import smtplib
import requests
import yaml


def load_yaml(filepath):
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


sender = "NASA <NASA@totallyNASA.com>"
receiver = "A Test User <to@example.com>"

endpoint = "https://api.nasa.gov/planetary/apod"
config = load_yaml("./config.yaml")
api_key = config["NASA_api_key"]
query_params = {"api_key": api_key, "date": datetime.today().strftime("%Y-%m-%d")}
response = requests.get(endpoint, params=query_params)
if response.status_code == 200:
    explanation = response.json()["explanation"]
    title = response.json()["title"]
    media_type = response.json()["media_type"]
    url = response.json()["url"]
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
    try:
        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login(config['mailtrap_username'], config['mailtrap_password'])
            server.sendmail(sender, receiver, message)
    except ConnectionRefusedError:
        print("Failed to connect to the server. Check your connection.")
    except smtplib.SMTPServerDisconnected:
        print("""Failed to connect to the server. Wrong user/password
        combination.""")
    except smtplib.SMTPException as e:
        print("SMTP error occurred: " + str(e) + """. Please contact customer
        support.""")
else:
    print(f"{response.status_code}: {response.reason}")
