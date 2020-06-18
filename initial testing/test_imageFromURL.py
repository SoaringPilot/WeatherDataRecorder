from urllib.request import urlopen
import cv2
import numpy as np

def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, readFlag)

    # return the image
    return img

image = url_to_image("https://pyimagesearch.com/wp-content/uploads/2015/01/opencv_logo.png")

cv2.imshow("Image", image)
cv2.waitKey(0)