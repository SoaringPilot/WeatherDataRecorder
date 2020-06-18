# METHOD #2: scikit-image
import cv2
from skimage import io
# loop over the image URLs
urls2 = [
	"http://www.drjack.info/BLIP/NAM/SE/FCST/woustar.curr.18z.png?id=themileman88@hotmail.com&pw=glider",
	"http://www.drjack.info/BLIP/NAM/SE/FCST/woustar.curr+1.18z.png?id=themileman88@hotmail.com&pw=glider",
	"http://www.drjack.info/BLIP/NAM/SE/FCST/woustar.curr+2.18z.png?id=themileman88@hotmail.com&pw=glider",
]

urls = [
	"https://pyimagesearch.com/wp-content/uploads/2015/01/opencv_logo.png",
	"https://pyimagesearch.com/wp-content/uploads/2014/12/adrian_face_detection_sidebar.png",
]
for url in urls:
	# download the image using scikit-image
	image = io.imread(url)
	#cv2.imshow("Incorrect", image)
	cv2.imshow("Correct", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
	cv2.waitKey(0)