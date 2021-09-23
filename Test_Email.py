import smtplib

sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

message = f"""\
Subject: Hi
To: {receiver}
From:{sender}

This is a test e-mail message."""

with smtplib.SMTP("localhost", 1025) as server:
    server.sendmail(sender, receiver, message)
