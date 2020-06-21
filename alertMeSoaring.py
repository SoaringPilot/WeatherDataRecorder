# Phase one: Periodically analyze Dr Jack Maps, send email if conditions look good. Ability to log day
# Phase two: Add in wind data and general forecasting from NOAA
# Add graphical user interface

# Need to email myself after 6:30 download
# Daily trending


#   Silver distance parameters: wind,

#
# Class Ideas
#   (0) Soaring
#           List of soaring parameters (later wind, cloud cover, temp swing)
#           Location of PSS
#           Location of Asheboro
#
#   (1) Day of Soaring
#           Latest forecast 18Z
#           Latest forecast 21Z
#           Running average of forecast parameters
#           Highest parameter forecast
#           Longevity of the day 18Z-21Z
#           Forecast locational variability (10,30,60 miles out)
#
#   (2) Map Soaring Forecast
#           Maps of interest/future potential interest
#           Parameter colors/values relationship
#           Good, medium, bad soaring parameters values
#           Parameter units
#
import zulu as zulu
import os
import os.path
import cv2
import smtplib
import ssl
import schedule
import time

import numpy as np

CONFIG_FILE = "./mapConfig.txt"
NOM = 25  # Number of Maps in configuration file
PSS = [338, 165, "PSS"]  # Piedmont Soaring Society map pixel location
KHBI = [364, 181, "KHBI"]  # Asheboro Airport map pixel location
EMAIL_THRESH = -5
DEBUG = 0
DEBUG_R = 0


# Notes on map scale:
# 22.6 pixels per 42.3 miles
# 0.7066822927 pixels/miles
# 1.415063049 miles/pixel

# Class which holds properties for each map
class MapProperties:
    # Class variables lists which contain index numbers
    active_maps = []  # Active for forecast analysis
    inactive_maps = []  # Not setup for forecast analysis
    priority_maps = []  # Priority maps are downloaded regularly by "scraperDrJackMaps.py"
    insignificant_maps = []  # These maps are downloaded only once the day of for the 18Z
    # Other class variables
    px_mile = 0.707  # pixels per mile
    mile_px = 1.415  # miles per pixel

    def __init__(self, map_number):
        self.number = map_number
        self.name = None
        self.nickname = None
        self.base_url = None
        self.base_filename = None
        self.bgr_list = None
        self.color_list = None
        self.units = None
        self.rating_good = None
        self.rating_ok = None
        self.active = None
        self.priority = None
        self.init_map_variables()

    # Read information from mapConfig.txt file
    def init_map_variables(self):
        # Open mapConfig and look for map number
        file = open(CONFIG_FILE)
        self.bgr_list = []
        self.color_list = []
        while True:
            line = file.readline()
            if line == "":
                break
            # Search for specified map number in mapConfig.txt
            if line.split()[0] == "Map" and line.split()[1] == "Number:" and line.split()[2] == str(self.number):
                # Extract data from mapConfig.txt
                while True:
                    line = file.readline()
                    if line.find("=") == 0:
                        break
                    if line.find("Map Name:") == 0:
                        self.name = line.split("Name: ")[1].replace("\n", "")
                    elif line.find("Base URL:") == 0:
                        self.base_url = line.split("URL: ")[1].replace("\n", "")
                        self.base_filename = self.base_url.split("FCST/")[1].split(".")[0] + "."
                    elif line.find("BGR List:") == 0:
                        line = line.split("List:")[1]
                        line = line.replace("(", "")
                        line = line.replace(")", "")
                        length = line.count(" ")
                        for j in range(length):
                            b, g, r = line.split()[j].split(",")
                            self.bgr_list.append([int(b), int(g), int(r)])  # Generate color tuples
                    elif line.find("Color Value List:") == 0:
                        line = line.split("List:")[1]
                        length = line.count(" ")
                        for j in range(length):
                            self.color_list.append(float(line.split(",")[j]))
                    elif line.find("Units:") == 0:
                        self.units = line.split()[1]
                    elif line.find("Rating:") == 0:
                        line = line.split(": ")[1]
                        self.rating_good = float(line.split(",")[0])
                        self.rating_ok = float(line.split(",")[1])
                    elif line.find("Active:") == 0:
                        line = line.split()[1]
                        if line == "YES":
                            self.active = 1
                            if MapProperties.active_maps.count(self.number):
                                pass
                            else:
                                MapProperties.active_maps.append(self.number)
                        elif line == "NO":
                            self.active = 0
                            if MapProperties.inactive_maps.count(self.number):
                                pass
                            else:
                                MapProperties.inactive_maps.append(self.number)
                    elif line.find("Priority:") == 0:
                        line = line.split()[1]
                        if line == "YES":
                            self.priority = 1
                            if MapProperties.priority_maps.count(self.number):
                                pass
                            else:
                                MapProperties.priority_maps.append(self.number)
                        elif line == "NO":
                            self.priority = 0
                            if MapProperties.insignificant_maps.count(self.number):
                                pass
                            else:
                                MapProperties.insignificant_maps.append(self.number)
                    elif line.find("Nickname:") == 0:
                        self.nickname = line.split()[1]


# Class which holds prediction information for each map
class PredictionMap(MapProperties):

    def __init__(self, map_number, day, time_z):
        super().__init__(map_number)
        self.day = day
        self.time = time_z
        self.map_dir = "./maps/" + day + "/"
        self.filename = None
        self.f_ext = None
        self.last_rev = None
        self.init_filename()

    # Method to find all valid BLIPMAPS saved, save them as a list
    def init_filename(self):
        # Create test filename capturing .PNG or .png
        test_filename = self.map_dir + self.base_filename + self.time + "." + self.day + "_r0" + \
                        self.base_url.split("18z")[1]

        if os.path.isfile(test_filename):
            # Create empty list for all filename revisions and save first file
            self.filename = []
            self.filename.append(test_filename)
            self.f_ext = self.base_url.split("18z")[1]  # .PNG or .png
            self.last_rev = 0

            # Loop to save all valid filenames
            while True:
                # Check if next iteration of file name is valid and set new rev otherwise break
                test_filename = self.filename[self.last_rev].replace("_r" + str(self.last_rev),
                                                                     "_r" + str(self.last_rev + 1))
                if os.path.isfile(test_filename):
                    self.last_rev += 1
                    self.filename.append(test_filename)
                else:
                    break
        else:
            if DEBUG:
                # The non-priority maps at the 21z time will activate this statement
                print("Filename Not Found: " + self.day + self.time + test_filename)

    # Method to open specified map and get color at specified location
    def get_prediction(self, location, rev):
        stipple_flag = 0
        if str(self.last_rev) != "None" and self.active == 1:
            image = cv2.imread(self.filename[rev])
            color_result = image[location[1], location[0]]
            # Check for stipple color which is [0 0 0]
            if color_result[0] == 0 and color_result[1] == 0 and color_result[2] == 0:
                stipple_flag = 1

            # Any color artifacts in maps will cause the index to fail such as stipple or grey
            try:
                # If pixel location is stipple, then move one pixel down in y direction and get new result
                if stipple_flag:
                    color_result = image[location[1]+1, location[0]]

                value_result = self.color_list[self.bgr_list.index(color_result.tolist())]

                if DEBUG:
                    print(str(value_result) + "\t" + self.units + " " + self.name)
                return value_result
            except:
                print("ERROR: Failure Reading Scale for: " + self.name)
                print("\t" + self.filename[rev])
                print("Color Result: " + str(color_result))
                return None

    def get_last_prediction(self, location):
        return self.get_prediction(location, self.last_rev)


#   To Add:
#           Running average of forecast parameters
#           Highest parameter forecast
#           Forecast locational variability (10,30,60 miles out)
class SoaringDay:

    def __init__(self, date, location):
        self.date = date
        self.location = location
        self.daily_score = 0
        self.max_rev = None  # This will not be initialized if maps don't exist
        self.blipmaps18z = []
        self.blipmaps21z = []
        self.result18z = []  # Result of reading 18z forecast
        self.result21z = []  # Result of reading 21z forecast
        self.init_blipmaps()
        self.read_forecast()
        self.evaluate_forecast()

    # Create blipmap objects within a SoaringDay
    def init_blipmaps(self):
        for z in range(NOM):
            self.blipmaps18z.append(PredictionMap(z, self.date, "18z"))
            self.blipmaps21z.append(PredictionMap(z, self.date, "21z"))

            # Lookup the last rev, if it is None then the map does not exist
            if self.blipmaps18z[z].last_rev is not None:
                # If self.max_rev has not been initialized set it equal to first result
                if self.max_rev is None:
                    self.max_rev = self.blipmaps18z[z].last_rev
                elif self.blipmaps18z[z].last_rev > self.max_rev:
                    self.max_rev = self.blipmaps18z[z].last_rev

            if self.blipmaps21z[z].last_rev is not None:
                # If self.max_rev has not been initialized set it equal to first result
                if self.max_rev is None:
                    self.max_rev = self.blipmaps21z[z].last_rev
                elif self.blipmaps21z[z].last_rev > self.max_rev:
                    self.max_rev = self.blipmaps21z[z].last_rev

    # Read all map revisions and get predictions
    def read_forecast(self):
        # Populate 2D list with zeros, rows = map revision #, columns = active map forecast result, last col = score
        if self.max_rev is not None:
            self.result18z = [[0] * (len(MapProperties.active_maps) + 1) for i in range(self.max_rev + 1)]
            self.result21z = [[0] * (len(MapProperties.active_maps) + 1) for i in range(self.max_rev + 1)]

            # Loop through all active maps, i = map revision number, j = map type
            for i in range(self.max_rev + 1):
                for j in range(len(MapProperties.active_maps)):
                    # Sometimes certain files have higher revisions
                    if DEBUG or DEBUG_R:
                        print(self.max_rev, self.blipmaps18z[MapProperties.active_maps[j]].last_rev, i, j,
                              MapProperties.active_maps[j], self.blipmaps18z[MapProperties.active_maps[j]].name)
                    if self.blipmaps18z[MapProperties.active_maps[j]].last_rev is not None and self.blipmaps18z[
                        MapProperties.active_maps[j]].last_rev >= i:
                        self.result18z[i][j] = self.blipmaps18z[MapProperties.active_maps[j]].get_prediction(
                            self.location, i)
                    if self.blipmaps21z[MapProperties.active_maps[j]].last_rev is not None and self.blipmaps21z[
                        MapProperties.active_maps[j]].last_rev >= i:
                        self.result21z[i][j] = self.blipmaps21z[MapProperties.active_maps[j]].get_prediction(
                            self.location, i)

    # Determine if most recent forecast is good, ok, bad for all active maps
    def evaluate_forecast(self):
        if self.max_rev is not None:
            # Cycle through all revisions
            for i in range(self.max_rev + 1):
                self.daily_score = 0
                # Cycle through all active maps
                for j in range(len(MapProperties.active_maps)):
                    # Check if the last rev of the active map is valid, if not skip over evaluation
                    if self.blipmaps18z[MapProperties.active_maps[j]].last_rev >= i:
                        criteria_first = self.blipmaps18z[MapProperties.active_maps[j]].rating_good
                        criteria_second = self.blipmaps18z[MapProperties.active_maps[j]].rating_ok

                        if criteria_first > criteria_second:
                            # Calculate the index
                            best = len(self.blipmaps18z[MapProperties.active_maps[j]].color_list) - 1
                            good = self.blipmaps18z[MapProperties.active_maps[j]].color_list.index(criteria_first)
                            average = self.blipmaps18z[MapProperties.active_maps[j]].color_list.index(criteria_second)
                            # Calculate the values using the index
                            val_best = self.blipmaps18z[MapProperties.active_maps[j]].color_list[best]
                            val_good = self.blipmaps18z[MapProperties.active_maps[j]].color_list[good]
                            val_average = self.blipmaps18z[MapProperties.active_maps[j]].color_list[average]

                            # Evaluate the primary forecast at 18Z
                            if val_good <= self.result18z[i][j] <= val_best:
                                self.daily_score += 0.75
                            elif val_average <= self.result18z[i][j] < val_good:
                                self.daily_score += 0.5
                            elif self.result18z[i][j] < val_average:
                                # Don't subtract points if wind direction is not westerly
                                if self.blipmaps18z[MapProperties.active_maps[j]].number != 8:
                                    self.daily_score -= 0.75

                            # Evaluate the secondary forecast at 21Z
                            if val_good <= self.result21z[i][j] <= val_best:
                                self.daily_score += 0.25
                            elif val_average <= self.result21z[i][j] < val_good:
                                self.daily_score += 0.1
                            elif self.result21z[i][j] < val_average:
                                # Don't subtract points if wind direction is not westerly
                                if self.blipmaps18z[MapProperties.active_maps[j]].number != 8:
                                    self.daily_score -= 0.25

                        if criteria_first < criteria_second:
                            # Calculate the index
                            best = 0
                            good = self.blipmaps18z[MapProperties.active_maps[j]].color_list.index(criteria_first)
                            average = self.blipmaps18z[MapProperties.active_maps[j]].color_list.index(criteria_second)
                            # Calculate the values using the index
                            val_best = self.blipmaps18z[MapProperties.active_maps[j]].color_list[best]
                            val_good = self.blipmaps18z[MapProperties.active_maps[j]].color_list[good]
                            val_average = self.blipmaps18z[MapProperties.active_maps[j]].color_list[average]

                            # Evaluate the primary forecast at 18Z
                            if val_best <= self.result18z[i][j] <= val_good:
                                self.daily_score += 0.75
                            elif val_good < self.result18z[i][j] <= val_average:
                                self.daily_score += 0.5
                            elif self.result18z[i][j] > val_average:
                                # Don't subtract points if wind direction is not westerly
                                if self.blipmaps18z[MapProperties.active_maps[j]].number != 8:
                                    self.daily_score -= 0.75

                            # Evaluate the secondary forecast at 21Z
                            if val_best <= self.result21z[i][j] <= val_good:
                                self.daily_score += 0.25
                            elif val_good < self.result21z[i][j] <= val_average:
                                self.daily_score += 0.1
                            elif self.result21z[i][j] > val_average:
                                # Don't subtract points if wind direction is not westerly
                                if self.blipmaps18z[MapProperties.active_maps[j]].number != 8:
                                    self.daily_score -= 0.25
                self.result18z[i][-1] = round(self.daily_score, 2)
                self.result21z[i][-1] = round(self.daily_score, 2)

    # Print most recent forecast
    def print_forecast(self):
        if self.max_rev is not None:
            for x in range(len(MapProperties.active_maps)):
                value_18z = self.blipmaps18z[MapProperties.active_maps[x]].get_last_prediction(self.location)
                value_21z = self.blipmaps21z[MapProperties.active_maps[x]].get_last_prediction(self.location)
                print(self.blipmaps21z[MapProperties.active_maps[x]].name + ": " + str(value_18z) + "/" + str(
                    value_21z))

    # Print a table depicting all forecasts with oldest forecast first on the list
    def print_forecast_trend(self):
        if self.max_rev is not None:
            print("\n" + (" " + self.location[-1] + " Trending Forecast: " + self.date + " at 18z ").center(97, '#'))
            for i in MapProperties.active_maps:
                print("{:>8s}".format(self.blipmaps18z[i].nickname), end=" ")
            print("{:>8s}".format("Score"))
            for i in range(self.max_rev + 1):
                for j in range(len(MapProperties.active_maps)):
                    print("{:>8s}".format(str(self.result18z[i][j])), end=" ")
                print("{:>8s}".format(str("{:.2f}".format(self.result18z[i][-1]))))

            print("\n" + (" " + self.location[-1] + " Trending Forecast: " + self.date + " at 21z ").center(97, '#'))
            for i in MapProperties.active_maps:
                print("{:>8s}".format(self.blipmaps21z[i].nickname), end=" ")
            print("{:>8s}".format("Score"))
            for i in range(self.max_rev + 1):
                for j in range(len(MapProperties.active_maps)):
                    print("{:>8s}".format(str(self.result21z[i][j])), end=" ")
                print("{:>8s}".format(str("{:.2f}".format(self.result21z[i][-1]))))

    def send_email_alert(self, message):

        # self.send_email_alert("Subject: " + self.date + "\n\nBest Conditions for " + self.blipmaps18z[
        # MapProperties.active_maps[i]].name)

        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = "timothy.clark.dev@gmail.com"
        receiver_email = "timothy.clark.ee@gmail.com"
        password = "dev_python_88"

        # Create a secure SSL context
        context = ssl.create_default_context()

        message = "Subject: Soaring Forecast Alert\n\n" + message

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)  # Secure the connection
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()


# Jobs:
#   create new day and delete old day objects at 2:30 am
#   evaluate all soaring days once a day, email if conditions good
#   interact with user: requested data

def alert():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day0 = str(zulu.parse(zulu.now()).shift(hours=+0)).split("T")[0]
    day1 = str(zulu.parse(zulu.now()).shift(hours=+24)).split("T")[0]
    day2 = str(zulu.parse(zulu.now()).shift(hours=+48)).split("T")[0]

    curr = SoaringDay(day0, PSS)
    curr_p1 = SoaringDay(day1, PSS)
    curr_p2 = SoaringDay(day2, PSS)

    if curr.daily_score > EMAIL_THRESH:
        curr.print_forecast_trend()
        curr.send_email_alert(
            days[zulu.parse(zulu.now()).weekday()] + " daily score is " + str(round(curr.daily_score, 2)))
    if curr_p1.daily_score > EMAIL_THRESH:
        curr_p1.print_forecast_trend()
        curr_p1.send_email_alert(days[zulu.parse(zulu.now()).shift(hours=+24).weekday()] + " daily score is " + str(
            round(curr_p1.daily_score, 2)))
    if curr_p2.daily_score > EMAIL_THRESH:
        curr_p2.print_forecast_trend()
        curr_p2.send_email_alert(days[zulu.parse(zulu.now()).shift(hours=+48).weekday()] + " daily score is " + str(
            round(curr_p2.daily_score, 2)))


#
# schedule.every().day.at("18:45").do(alert)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

today = SoaringDay("2020-06-11", PSS)
today.print_forecast_trend()
