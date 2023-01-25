import cv2
import numpy as np


cap = cv2.VideoCapture(0)

class Removebg():
    def __init__(self,upper_bond,lower_bond):
        self.upper_bond = upper_bond
        self.lower_bond = lower_bond
        self.image = None
        self.bg_image = cv2.imread("flag.png")

    def remove(self):
        img1 = self.image
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        img2 = self.bg_image
        img2 = cv2.resize(img2,(self.image.shape[1],self.image.shape[0]))
        mask = cv2.inRange(hsv, np.array(self.lower_bond), np.array(self.upper_bond))
        # Invert the mask
        mask = cv2.bitwise_not(mask)
        # Use the mask to create a masked version of image 2
        res = cv2.bitwise_and(img2, img2, mask=mask)
        # Use the mask to create a masked version of image 1
        img1 = cv2.bitwise_and(img1, img1, mask=cv2.bitwise_not(mask))
        # Combine the two images
        result = cv2.addWeighted(img1, 1, res, 1, 0)

        return result


rb = Removebg(upper_bond=[180,255,255],lower_bond=[0,27,0])

while True:
    _,frame = cap.read()
    rb.image = cv2.flip(frame,1)
    result = rb.remove()

    cv2.imshow('result', result)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()