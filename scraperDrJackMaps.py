########################################################################################################################
# Date: 05/22/2020
# File: scraperDrJackMaps.py
# Author: Tim Clark
# Description:
#   Dr Jack Soaring Forecast website produces maps with different colors denoting different soaring parameters.
#   This script downloads the maps, using cookies, and stores them in folders based on forecasting date. The maps
#   are downloaded on a regular basis four times a day. The first file is saved as r0 and subsequent revisions are
#   saved and do not overwrite over old forecasting data. Download times were chosen based on the information found
#   here: http://www.drjack.info/cgi-bin/forecast_availability.cgi?SE
#   These times allow all maps 18Z, 21Z, current, current +1 and current +2 maps would be ready.
#       Important time changes:
#           2Z      changes to next day
#           5Z      first time slot to get all forecasts    01:00 EST
#           12Z     second time slot to get all forecasts   08:00 EST
#           17:30   third time slot to get all forecast     13:30 EST
#           22:30   fourth time slot to get some forecasts  18:30 EST
#
#   Note: Maximum number of maps is 144 files, 94 files when only downloading active maps
#   Note: More than 300 requested map downloads a day is excess: http://www.drjack.info/INFO/registration.html
#   Note: Soaring parameters explained: http://www.drjack.info/BLIP/NAM/INFO/parameters.html
#   Note: At 8PM, zulu time changes to the next day. Dr. Jack doesn't change until 10PM, i.e. don't force download
#
########################################################################################################################

import time
import requests
import zulu as zulu
import os.path
from os import path
import schedule

CONFIG_FILE = "mapConfig.txt"


def create_urls(text_input):
    output_url = dict() #TODO: get rid of dictionary
    url = text_input.split()[2]
    output_url[0] = url
    output_url[1] = output_url[0].split("curr")[0] + "curr+1" + output_url[0].split("curr")[1]
    output_url[2] = output_url[0].split("curr")[0] + "curr+2" + output_url[0].split("curr")[1]
    output_url[3] = url.split("18")[0] + "21" + url.split("18")[1]
    output_url[4] = output_url[3].split("curr")[0] + "curr+1" + output_url[3].split("curr")[1]
    output_url[5] = output_url[3].split("curr")[0] + "curr+2" + output_url[3].split("curr")[1]
    return output_url


def create_filenames(input):
    filenames = dict()

    # Calculate forecast day in zulu
    day0 = str(zulu.parse(zulu.now())).split("T")[0]
    day1 = str(zulu.parse(zulu.now()).shift(hours=+24)).split("T")[0]
    day2 = str(zulu.parse(zulu.now()).shift(hours=+48)).split("T")[0]

    # Input Example = Base URL: http://www.drjack.info/BLIP/NAM/SE/FCST/wfpm.curr.18z.PNG
    url = input.split()[2]  # http://www.drjack.info/BLIP/NAM/SE/FCST/wfpm.curr.18z.PNG
    file = url.split('/')[7]  # wfpm.curr.18z.PNG
    parsed_18z = file.replace(".curr", "")  # wfpm.18z.PNG
    parsed_21z = parsed_18z.replace("18z", "21z")  # wfpm.21z.PNG

    # Make directory for soaring day if it doesn't exist
    if not os.path.isdir("./maps/" + day0):
        os.mkdir("./maps/" + day0)
    if not os.path.isdir("./maps/" + day1):
        os.mkdir("./maps/" + day1)
    if not os.path.isdir("./maps/" + day2):
        os.mkdir("./maps/" + day2)
    if parsed_18z.split(".")[2] == "png":
        cc = "cc_"
    elif parsed_18z.split(".")[2] == "PNG":
        cc = ""

    # Create filename example: wfpm.18z.2020-05-21_r0
    filenames[0] = "./maps/" + day0 + "/" + cc + parsed_18z.split(parsed_18z.split(".")[2])[0] + day0 + "_r0." + \
                   parsed_18z.split(".")[2]
    filenames[1] = "./maps/" + day1 + "/" + cc + parsed_18z.split(parsed_18z.split(".")[2])[0] + day1 + "_r0." + \
                   parsed_18z.split(".")[2]
    filenames[2] = "./maps/" + day2 + "/" + cc + parsed_18z.split(parsed_18z.split(".")[2])[0] + day2 + "_r0." + \
                   parsed_18z.split(".")[2]
    filenames[3] = "./maps/" + day0 + "/" + cc + parsed_21z.split(parsed_21z.split(".")[2])[0] + day0 + "_r0." + \
                   parsed_21z.split(".")[2]
    filenames[4] = "./maps/" + day1 + "/" + cc + parsed_21z.split(parsed_21z.split(".")[2])[0] + day1 + "_r0." + \
                   parsed_21z.split(".")[2]
    filenames[5] = "./maps/" + day2 + "/" + cc + parsed_21z.split(parsed_21z.split(".")[2])[0] + day2 + "_r0." + \
                   parsed_21z.split(".")[2]

    # Loop to check for latest revision
    for t in range(6):
        rev = 0
        while path.isfile(filenames[t]):
            rev += 1
            if rev <= 10:
                filenames[t] = filenames[t][:-5] + str(rev) + "." + filenames[t].split(".")[4]
            elif rev > 10:
                filenames[t] = filenames[t][:-6] + str(rev) + "." + filenames[t].split(".")[4]

    return filenames


def get_maps():
    # Connect to Dr. Jack Website
    # Create session to download Dr. Jack maps with cookies
    session = requests.Session()
    jar = requests.cookies.RequestsCookieJar()  # cookie jar is a list or dictionary of entries
    jar.set('register', 'themileman88&glider&themileman88%40hotmail.com&Tim%20Clark&drjack')
    session.cookies = jar

    f_mapConfig = open(CONFIG_FILE)  # Map configuration file with URL's and other information
    maps_urls = []
    fn = []

    while True:
        line = f_mapConfig.readline()
        if line == "":
            print("\nEnd of " + CONFIG_FILE + " File\n")
            break
        # Example Line: Base URL: http://www.drjack.info/BLIP/NAM/SE/FCST/wfpm.curr.18z.PNG
        if line.split()[0] == "Base":
            maps_urls = create_urls(line)
            fn = create_filenames(line)

            # Check for priority map file
            temp = f_mapConfig.readline()
            while temp.split()[0] != "Priority:":
                temp = f_mapConfig.readline()
            # Check if active map, if not only download if the day of
            if temp.split()[1] == "YES":
                range_val = 6  # Download all days and times
            elif temp.split()[1] == "NO":
                range_val = 1  # Download only 18z the day of
            else:
                range_val = 0
                print("ERROR: Problem reading map analysis")

            for i in range(range_val):
                # time.sleep(0.5)
                print("Getting Map: " + maps_urls[i])
                tempMap = session.get(maps_urls[i])
                tempMapFile = open(fn[i], "wb")

                for chunk in tempMap.iter_content(chunk_size=256):
                    if chunk:
                        tempMapFile.write(chunk)
                tempMapFile.close()
    f_mapConfig.close()


def get_noaa_forecast():
    session = requests.Session()
    response = session.get('https://forecast.weather.gov/product.php?site=CRH&product=MIS&issuedby=GSO')

    temp = str(response.text)
    # print(test)
    start = temp.find("SOARING FORECAST")
    end = temp.find("IT IS EMPHASIZED")
    forecast = temp[start:end]
    date = forecast[112:120]
    day0 = str(zulu.parse(zulu.now()).format('%m/%d/%y'))
    f_path = str(zulu.parse(zulu.now())).split("T")[0]
    f_path = "./maps/" + f_path + "/"
    if date == day0:
        fn = open(f_path + "NOAA_Soaring_Forecast.txt", "w")
        fn.write(forecast)
        fn.close()

schedule.every().day.at("01:00").do(get_maps)
schedule.every().day.at("08:00").do(get_maps)
schedule.every().day.at("13:30").do(get_maps)
schedule.every().day.at("18:30").do(get_maps)

schedule.every().day.at("13:45").do(get_noaa_forecast)
# TODO: add user interaction for requested data pull from command window
#   example: get just a certain map number

while True:
    schedule.run_pending()
    time.sleep(1)