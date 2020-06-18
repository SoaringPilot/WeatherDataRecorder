# import the necessary packages
import argparse

import cv2
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image")
args = vars(ap.parse_args())
# load the image
image = cv2.imread(args["image"])

# define the colors associated with buoyancy shear factor
boundaries = [
    ([250, 120, 250], [255, 135, 255]),
    ([95, 0, 250], [105, 5, 255]),
    ([120, 150, 250], [130, 160, 255]),
    ([0, 210, 250], [5, 216, 255])
]

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    # show the images
    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)
