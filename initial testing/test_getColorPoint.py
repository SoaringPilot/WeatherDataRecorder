import cv2


def color_get(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        result = (image[y, x])
        print(x, y, result)


image = cv2.imread("../maps/2020-05-24/cape.18Z.2020-05-24_r4.png")
cv2.namedWindow("image")
cv2.setMouseCallback("image", color_get)

while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
cv2.waitKey(0)
