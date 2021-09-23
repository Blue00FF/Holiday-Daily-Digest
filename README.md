# Holiday-Daily-Digest
The aim of this project is to create a program that uses a Calendarific API to get information about holidays that are celebrated on the day within the UK and then 
send an email to the user with the holiday name and description. 

To showcase it I am inputing the first of January as it is a guaranteed holiday. The program then can be set to check for new holidays each day and only send emails 
to the user if there is indeed an holiday on the day. 

In order to show how the program functions without me or you having to insert credentials and actual sender/receiver addresses, I have used a local host server.
To set up the server, you can check the Real Python guide (https://realpython.com/python-send-email/#option-2-setting-up-a-local-smtp-server) or, if you trust me, 
you can just copy and paste to your command line the following instruction: 

FOR WINDOWS AND MACOS: python -m smtpd -c DebuggingServer -n localhost:1025
FOR LINUX: sudo python -m smtpd -c DebuggingServer -n localhost:1025

To use the program, you must register for a free account on Calendarific to get an API key.  (https://calendarific.com/signup)

I have also included a program that sends you NASA's picture/video of the day, which to be used requires to register on NASA's website for an API key as well. 
(https://api.nasa.gov/)

You must then insert your keys in the config.yaml file as specified inside it to run my program.  
