import requests
import cv2
import numpy as np
import zulu as zulu

session = requests.Session()

# r = requests.get('http://www.drjack.info/auth_default.css') #This did not have my username
response = session.get('https://forecast.weather.gov/product.php?site=CRH&product=MIS&issuedby=GSO')

test = str(response.text)
start = test.find("SOARING FORECAST")
end = test.find("IT IS EMPHASIZED")
forecast = test[start:end]
print(forecast.find("12Z "))
date = forecast[112:120]
print(forecast[120:112])
day0 = str(zulu.parse(zulu.now()).format('%m/%d/%y'))

print("TIMC " +str(zulu.parse(zulu.now()).weekday()))

if day0 == date:
    print("match")
    print(day0 + " " + date)
else:
    print("No Match " + day0 +" "  + date)
# f_path = "../maps/" + day0 + "/"
# fn = open(f_path + "NOAA_Soaring_Forecast.txt", "w")
#
# fn.write(forecast)
# fn.close()
