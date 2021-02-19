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
import smtplib
import schedule
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from datetime import datetime
from datetime import timedelta
from datetime import date
from googletrans import Translator


translator = Translator(service_urls=['translate.googleapis.com'])

def get_contacts(filename):
    names = []
    emails = []
    latitud = []
    longitud = []
    lugar = []
    with open(filename, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
            latitud.append(a_contact.split()[2])
            longitud.append(a_contact.split()[3])
            lugar.append(a_contact.split()[4])
    return names, emails, latitud, longitud, lugar
def read_template(filename):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
names, emails, latitud, longitud, lugar = get_contacts('/home/pi/Weather/mycontacts.txt')  # read contacts
message_template = read_template('/home/pi/Weather/message.txt')
www_template = read_template('/home/pi/Weather/wwwaddress.txt')

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
    if isinstance(data, str):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    # if it's anything else, return it in its original form
    return data

# ============================================================================
# Constants
# ============================================================================
# Set to True to enable download of weather data to Weather Underground
WEATHER_DOWNLOAD = True
# some string constants
SINGLE_HASH = "#"
HASHES = "########################################"
SLASH_N = "\n"


def main():
    if WEATHER_DOWNLOAD:
       print("Downloading data from Weather Underground")
       today = date.today()
       for name, email, lati, longi, luga in zip(names, emails, latitud, longitud, lugar):
                www = www_template.substitute(latitud=lati.title(), longitud=longi.title())
                url = requests.get(www)
                json_data = json.loads(url.text)
                observe = format(json.dumps(json_data))
                y = json.loads(observe)
                j = y['dayOfWeek']
                k = y['daypart']
                weather = format(json.dumps(k))
                l = json.loads(weather)
                t = l[0]
                u = t['narrative']
                dia1a = translator.translate(j[0], dest = 'es')
                dia1 = dia1a.text
                dia2a = translator.translate(j[1], dest = 'es')
                dia2 = dia2a.text
                dia3a = translator.translate(j[2], dest = 'es')
                dia3 = dia3a.text
                dia4a = translator.translate(j[3], dest = 'es')
                dia4 = dia4a.text
                dia5a = translator.translate(j[4], dest = 'es')
                dia5 = dia5a.text
                dia6a = translator.translate(j[5], dest = 'es')
                dia6 = dia6a.text
                texto1ma = translator.translate(u[0], dest = 'es')
                texto1m = texto1ma.text
                texto1na = translator.translate(u[1], dest = 'es')
                texto1n = texto1na.text
                texto2ma = translator.translate(u[2], dest = 'es')
                texto2m = texto2ma.text
                texto2na = translator.translate(u[3], dest = 'es')
                texto2n = texto2na.text              
                texto3ma = translator.translate(u[4], dest = 'es')
                texto3m = texto3ma.text       
                texto3na = translator.translate(u[5], dest = 'es')
                texto3n = texto3na.text       
                texto4ma = translator.translate(u[6], dest = 'es')
                texto4m = texto4ma.text       
                texto4na = translator.translate(u[7], dest = 'es')
                texto4n = texto4na.text    
                texto5ma = translator.translate(u[8], dest = 'es')
                texto5m = texto5ma.text       
                texto5na = translator.translate(u[9], dest = 'es')
                texto5n = texto5na.text           
                texto6ma = translator.translate(u[10], dest = 'es')
                texto6m = texto6ma.text       
                texto6na = translator.translate(u[11], dest = 'es')
                texto6n = texto6na.text
                message = message_template.substitute(PERSON_NAME=name.title(), place=luga.title(), dia1=dia1, dia2=dia2, dia3=dia3, dia4=dia4, dia5=dia5, dia6=dia6, texto1m=texto1m, texto1n=texto1n, texto2m=texto2m, texto2n=texto2n, texto3m=texto3m, texto3n=texto3n, texto4m=texto4m, texto4n=texto4n, texto5m=texto5m, texto5n=texto5n, texto6m=texto6m, texto6n=texto6n)
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
       print(today.strftime("%d/%m/%Y"),'-> Mails Sent')

# ============================================================================
# here's where we start doing stuff
# ============================================================================
print(SLASH_N + HASHES)
print(SINGLE_HASH, "Forecast from WU         ", SINGLE_HASH)
print(SINGLE_HASH, "By Pablo Blanco-Gomez    ", SINGLE_HASH)
print(HASHES)

# Now see what we're supposed to do next
if __name__ == "__main__":
   schedule.every().day.at("08:00").do(main)
   while True:
       schedule.run_pending()
       time.sleep(1)

