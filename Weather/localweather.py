#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function

import datetime
import os
import sys
import time
import requests
import json
import ast
import commands
import smtplib
import goslate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from datetime import datetime
from datetime import timedelta
import threading

gs=goslate.Goslate()

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails
def read_template(filename):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
names, emails = get_contacts('mycontacts.txt')  # read contacts
message_template = read_template('message.txt')

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

print( "Connecting to mysql database")

# ============================================================================
# Constants
# ============================================================================
# specifies how often to measure values from the Sense HAT (in minutes)
MEASUREMENT_INTERVAL = 5  # minutes
# Set to False when testing the code and/or hardware
# Set to True to enable download of weather data to Weather Underground
WEATHER_DOWNLOAD = True
# some string constants
SINGLE_HASH = "#"
HASHES = "########################################"
SLASH_N = "\n"


def main():
    now = datetime.now()
    run_at = now + timedelta(hours=1)
    delay = (run_at - now).total_seconds()
    if WEATHER_DOWNLOAD:
       print("Downloading data from Weather Underground")
       url = requests.get('https://api.weather.com/v3/wx/forecast/daily/5day?geocode=39.74,-0.56&format=json&units=m&language=sp-SPAIN&apiKey=')
       json_data = json.loads(url.text)
       observe = format(json.dumps(json_data))
       y = json_loads_byteified(observe)
       j = y['dayOfWeek']
       k = y['daypart']
       weather = format(json.dumps(k))
       l = json_loads_byteified(weather)
       t = l[0]
       u = t['narrative']
       dia1 = j[0]
       dia2 = j[1]
       dia3 = j[2]
       dia4 = j[3]
       dia5 = j[4]
       dia6 = j[5]
       texto1m = u[0]
       texto1n = u[1]
       texto2m = u[2]
       texto2n = u[3]
       texto3m = u[4]
       texto3n = u[5]
       texto4m = u[6]
       texto4n = u[7]
       texto5m = u[8]
       texto5n = u[9]
       texto6m = u[10]
       texto6n = u[11]
       for name, email in zip(names, emails):
           message = message_template.substitute(PERSON_NAME=name.title(), dia1=dia1, dia2=dia2, dia3=dia3, dia4=dia4, dia5=dia5, dia6=dia6, texto1m=texto1m, texto1n=texto1n, texto2m=texto2m, texto2n=texto2n, texto3m=texto3m, texto3n=texto3n, texto4m=texto4m, texto4n=texto4n, texto5m=texto5m, texto5n=texto5n, texto6m=texto6m, texto6n=texto6n)
           #print(message)
           #The mail addresses and password
           sender_address = '@hotmail.com'
           sender_pass = ''
           receiver_address = email
           #Setup the MIME
           msg = MIMEMultipart()
           msg['From'] = sender_address
           msg['To'] = receiver_address
           msg['Subject'] = 'Predicción meteorológica WU'   #The subject line
           #The body and the attachments for the mail
           msg.attach(MIMEText(message, 'plain'))
           #Create SMTP session for sending the mail
           session = smtplib.SMTP('smtp.live.com', 587) #use gmail with port
           session.starttls() #enable security
           session.login(sender_address, sender_pass) #login with mail_id and password
           text = msg.as_string()
           session.sendmail(sender_address, receiver_address, text)
           session.quit()
           print('Mail Sent')
    # You can always increase the sleep value below to check less often
    time.sleep(delay)  # this should never happen since the above is an infinite loop
print("Leaving main()")


# ============================================================================
# here's where we start doing stuff
# ============================================================================
print(SLASH_N + HASHES)
print(SINGLE_HASH, "Forecast from WU         ", SINGLE_HASH)
print(SINGLE_HASH, "By Pablo Blanco-Gomez    ", SINGLE_HASH)
print(HASHES)

# make sure we don't have a MEASUREMENT_INTERVAL > 60
if (MEASUREMENT_INTERVAL is None) or (MEASUREMENT_INTERVAL > 60):
    print("The application's 'MEASUREMENT_INTERVAL' cannot be empty or greater than 60")
    sys.exit(1)

# Now see what we're supposed to do next
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
       print("\nExiting application\n")
       sys.exit(0)
