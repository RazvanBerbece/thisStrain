import base64
import numpy as np
import cv2
import io
from PIL import Image

class Decoder:
    """ Decodes a base64string to its Image Data """
    def __init__(self, base64string):
        self.imageData = base64string
    
    def decodeImage(self):
        """ Changes the imageData field to the decoded image data """
        self.imageData = base64.b64decode(self.imageData)

    def getImageData(self):
        """ Processes image and returns an np array containing the Image data """
        self.decodeImage()
        image = Image.open(io.BytesIO(self.imageData))
        image = cv2.cvtColor(np.array(image), cv2.IMREAD_ANYCOLOR)
        image = cv2.resize(image, (150, 150))
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        data = np.array(image, dtype='float') / 255.0
        return data