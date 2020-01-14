from datetime import datetime, timedelta
import requests
import json
import portolan

#Retrieve weather data from Dark Sky
latitude = "37.825522"
longitude = "-122.448270"
darkSkyKey = "" #Dark Sky API key, get with free account at https://darksky.net/
exclude = "minutely, hourly, daily, alerts, flags" #exclude unused data in response
units = "si"

URL_GET = "https://api.darksky.net/forecast/" + darkSkyKey + '/' + latitude + ',' + longitude
PARAMS_GET = {'exclude': exclude, 'units': units}

r = requests.get(url = URL_GET, params = PARAMS_GET)

data_get = r.json()

currently = data_get['currently']

unixTime = currently['time']
pacificTime = datetime.utcfromtimestamp(unixTime) + timedelta(hours = data_get['offset']) #adjust time using timezone offset from response

windSpeed = "{0:.1f}".format(currently['windSpeed'] * (900 / 463)) #convert m/s to knots
windGust = "{0:.1f}".format(currently['windGust'] * (900 / 463)) #convert m/s to knots
windDir = currently['windBearing']
windDirText = portolan.abbr(windDir).replace('b', 'x') #convert direction in degrees to point on compass, change formatting to use 'x' for by

#Send weather data to Geckoboard
URL_POST = "https://push.geckoboard.com/v1/send/"
geckoboardAccessKey = ""

#WidgetKeys
windSpeedKey = "770088-3684b8e0-17f5-0138-34bb-0ab5f1a7c0d5"
windGustKey = "770088-34490930-17f6-0138-a576-0aacb346e6e1"
windDirKey = "770088-1488cde0-17f4-0138-a575-0aacb346e6e1"
timeKey = "770088-6db27270-1864-0138-8b16-025a7fb2af0f"

#create requests
data_windSpeed = json.dumps(
            {
              "api_key": geckoboardAccessKey,
              "data": {
                    "item": windSpeed,
                            "min": {
                                "value": 0
                            },
                            "max": {
                                "value": 50
                            }
                    }
            })

data_windGust = json.dumps(
            {
              "api_key": geckoboardAccessKey,
              "data": {
                    "item": windGust,
                            "min": {
                                "value": 0
                            },
                            "max": {
                                "value": 50
                            }
                    }
            })

data_windDir = json.dumps(
            {
              "api_key": geckoboardAccessKey,
              "data": {
                    "item": [
                        {
                          "text": "<p><span style=\"font-size:100px;\">" + windDirText +
                          "<br>" + str(windDir) + "&deg</span><p>"
                        }
                      ]
                    }
            })

data_time = json.dumps(
            {
              "api_key": geckoboardAccessKey,
              "data": {
                    "item": [
                        {
                          "text": "<span style=\"font-size:36px;\">Last Updated: " + str(pacificTime) + "</span>"
                        }
                      ]
                    }
            })

#send requests
r = requests.post(url = URL_POST + windSpeedKey, data = data_windSpeed)
print("Wind Speed", windSpeed, r.text)
r = requests.post(url = URL_POST + windGustKey, data = data_windGust)
print("Wind Gusts", windGust, r.text)
r = requests.post(url = URL_POST + windDirKey, data = data_windDir)
print("Wind Dir", windDirText, windDir, r.text)
r = requests.post(url = URL_POST + timeKey, data = data_time)
print("Time", pacificTime, r.text)
