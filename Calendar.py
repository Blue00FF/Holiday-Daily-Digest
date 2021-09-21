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

session = requests.Session()
session_token = config['calendarific_api_key']
my_headers = {'Authorization': f'Bearer {session_token}'}
session.headers.update(my_headers)
response = session.get("https://calendarific.com/api/v2")

if response.status_code == 200:
    message = f"""\
    Subject: Your Daily Calendarific Summary
    To: {receiver}
    From:{sender}

    Hello user,

    This is your daily update from Calendarific on today's holidays from all over
    the world.

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

elif response.status_code == 301:
    print("""The server is redirecting you to a different endpoint. This can
    happen when a company switches domain names, or an endpoint name is
    changed.""")
elif response.status_code == 400:
    print("""The server thinks you made a bad request. This can happen when you
    don’t send along the right data, among other things.""")
elif response.status_code == 401:
    print("""The server thinks you’re not authenticated. Many APIs require
    login credentials, so this happens when you don’t send the right
    credentials to access an API.""")
elif response.status_code == 403:
    print("""The resource you’re trying to access is forbidden: you don’t have
    the right permissions to see it.""")
elif response.status_code == 404:
    print("The resource you tried to access wasn’t found on the server.")
elif response.status_code == 503:
    print("The server is not ready to handle the request.")
