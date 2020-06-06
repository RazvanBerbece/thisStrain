from tensorflow.keras.models import load_model
import argparse
import pickle
import cv2
import matplotlib.pyplot as plt
import os, sys

class Classifier:
    """ Initialised with a photo, has method which can be used to classifiy the image """

    def __init__(self, image):
        """ Initializes the model, the labeler and the image """
        self.image = image
        self.model = load_model('strainClassifier')
        self.lb = pickle.loads(open('labelBinarizer', 'rb').read())
    
    def getOutput(self):
        """ Outputs the strain found in the photo """
        preds = self.model.predict(self.image)
        i = preds.argmax(axis=1)[0]
        labels = [self.lb.classes_[i]]
        result = (labels[0], preds[0][i] * 100)
        return result