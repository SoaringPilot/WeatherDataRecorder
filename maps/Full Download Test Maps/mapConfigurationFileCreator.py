########################################################################################################################
# Date: 05/18/2020
# File: mapConfigurationFileCreator.py
# Author: Tim Clark
# Description:
#   Dr Jack Soaring Forecast website produces maps with different colors denoting different soaring parameters.
#   I downloaded one of each type of map into a folder and opened each for analysis with this script.
#   Upon opening each map, typing 'f' will prompt the user for the average parameter value of the first color and then
#   the span of the values between the different colors. Information about each map is saved to "mapConfig.txt" in the
#   following form:
#           ==================================
#           Map Number: 0
#           Map Name: ./wfpm_woustar.curr.18z.png
#           Base URL: http://www.drjack.info/BLIP/NAM/SE/FCST/wfpm_woustar.curr.18z.png
#           BGR List: (255,70,0) (255,131,0) (255,200,0) (248,252,0) (182,232,2) (117,210,5)
#           Color Value List: 25.0, 75.0, 125.0, 175.0, 225.0, 275.0
#           ==================================
#
#   The resulting output file "mapConfig.txt" will be input to a different script which gets the most recent maps and
#   performs an analysis to determine if there is a good soaring day forecasted.
#
########################################################################################################################
import cv2

configFile = open("./mapConfig.txt", "w")
#./maps/2020-05-24/cape.18Z.2020-05-24_r4.png
# Input map filenames
filenames = ['./wfpm_woustar.curr.18z.png', './wfpm.curr.18z.png', './woustar.curr.18z.png',
             './hft.curr.18z.png',
             './hwcritft.curr.18z.png', './htift.curr.18z.png', './blwindkt_blwinddeg.curr.18z.png',
             './blwindkt.curr.18z.png',
             './blwinddeg.curr.18z.png', './blwindshearkt.curr.18z.png', './wblmaxkt.curr.18z.png',
             './zsfclclft_zsfclcldifft.curr.18z.png', './zblclft_zblcldifft.curr.18z.png',
             './zsfclcldifft.curr.18z.png',
             './zblcldifft.curr.18z.png', './zblclft.curr.18z.png', './maxblrh.curr.18z.png',
             './cape.curr.18z.png',
             './sfcdewptf.curr.18z.png', './totcloudpct.curr.18z.png', './sfcsunwm2.curr.18z.png',
             './dft.curr.18z.png',
             './qswm2.curr.18z.png', './sfctempf.curr.18z.png']

# Mouse position on click which gets color at that location. Writes BGR color to output file
def color_get(event, x, y, flags, param):
    global colorCounter
    if event == cv2.EVENT_LBUTTONDOWN:
        b, g, r = (image[y, x])
        print(b, g, r)
        configFile.write("(" + str(b) + "," + str(g) + "," + str(r) + ") ")
        colorCounter += 1


counter = 0

for filename in filenames:
    image = cv2.imread(filename)
    cv2.namedWindow(filename)
    cv2.setMouseCallback(filename, color_get)

    configFile.write("==================================\n")
    configFile.write("Map Number: " + str(counter) + "\n")
    configFile.write("Map Name: " + filename + "\n")
    configFile.write("Base URL: " + "http://www.drjack.info/BLIP/NAM/SE/FCST/" + filename.split("/")[1] + "\n")
    configFile.write("BGR List: ")

    counter += 1
    colorCounter = 0

    while True:
        key = cv2.waitKey(1) & 0xFF
        cv2.imshow(filename, image)

        if key == ord("q"):
            break
        if key == ord("f"):
            first = input("Enter Color 1st Value:")
            span = input("Enter span Value:")

    configFile.write("\n")

    # Generate list of parameter values based on the first parameter and the span
    configFile.write("Color Value List: ")
    for i in range(colorCounter):
        configFile.write(str(float(first) + i * float(span)))
        if i == (colorCounter - 1):
            configFile.write("\n")
        else:
            configFile.write(", ")

configFile.write("==================================\n")

configFile.close()
