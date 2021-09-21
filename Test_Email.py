import smtplib
import yaml


def load_yaml(filepath):
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


config = load_yaml("./config.yaml")

sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From:{sender}

This is a test e-mail message."""

try:
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(config['mailtrap_username'], config['mailtrap_password'])
        server.sendmail(sender, receiver, message)
except ConnectionRefusedError:
    print("Failed to connect to the server. Check your connection.")
except smtplib.SMTPServerDisconnected:
    print("Failed to connect to the server. Wrong user/password combination.")
except smtplib.SMTPException as e:
    print("SMTP error occurred: " + str(e) + """. Please contact customer
    support.""")
