import requests
import cv2
import numpy as np

session = requests.Session()
jar = requests.cookies.RequestsCookieJar()  # cookie jar is a list or dictionary of entries
jar.set('register', 'themileman88&glider&themileman88%40hotmail.com&Tim%20Clark&drjack')
session.cookies = jar

# r = requests.get('http://www.drjack.info/auth_default.css') #This did not have my username
r = session.get('http://www.drjack.info/auth_default.css')
print(r.text)

# r = requests.get('http://www.drjack.info/cgi-bin/FORECAST/auth_retrieve.pl') #This did not have my username
r = session.get('http://www.drjack.info/cgi-bin/FORECAST/auth_retrieve.pl')
print(r.text)

response = session.get("http://www.drjack.info/BLIP/NAM/SE/FCST/woustar.curr.18z.PNG")
# response = session.get("https://pyimagesearch.com/wp-content/uploads/2015/01/opencv_logo.png")
print(response.headers)
file = open("sample_image.png", "wb")
# file.write(r.content) #This isn't working
for chunk in response.iter_content(chunk_size=256):
    if chunk:
        file.write(chunk)
file.close()

# load the image
image = cv2.imread("./sample_image.png")

boundaries = [
    ([230, 120, 230], [255, 135, 255]),
    ([15, 0, 250], [40, 5, 255]),
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
# Get color at a location
b, g, r = (image[300, 300])

# if image type is b g r, then b g r value will be displayed.
# if image is gray then color intensity will be displayed.
print(b, g, r)

response = session.get('https://forecast.weather.gov/product.php?site=CRH&product=MIS&issuedby=GSO')

test = str(response.text)
# print(test)
start = test.find("SOARING FORECAST")
end = test.find("IT IS EMPHASIZED")
forecast = test[start:end]
fn = open("forecast.txt", "w")
fn.write(forecast)
fn.close()