#from flask import Flask
from twilio.rest import TwilioRestClient
import requests
import time, threading
import json
import datetime
import os

#app = Flask(__name__)

client = TwilioRestClient(os.environ['twilio_account'], os.environ['twilio_token'])

def periodic():
    print(time.ctime())
    
    #message = client.messages.create(to="+13476333706", from_="+12014925109", body="BODY")
    #payload = {'key1': 'value1', 'key2': 'value2'}
    payload = {'q' : 'New York City', 'mode' : 'json', 'appid' : os.environ['weather_appid']}
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=payload)
    data = json.loads(r.text)
    forecast = data['list']
    max = 0
    min = 100
    for entry in forecast:
        current_time = datetime.datetime.now().strftime('%d')
        forecast_time = datetime.datetime.fromtimestamp(int(entry['dt'])).strftime('%d')
        if current_time == forecast_time:
            temp_c = entry['main']['temp']-273
            if temp_c > max:
                max = temp_c
            if temp_c < min:
                min = temp_c
        #print entry['dt']
    min = min*1.8+32
    max = max*1.8+32
    message_text = "%s Weather" % data['city']['name']
    message_text += "\nLow: %f" % min
    message_text += "\nHigh: %f" % max

    message = client.messages.create(to="+13476333706", from_="+12014925109", body=message_text)
    threading.Timer(10, periodic).start()
periodic()






# @app.route("/")
# def hello():
#     r = requests.get('https://api.github.com/events')
#     return r.text

#if __name__ == "__main__":
#    app.run()