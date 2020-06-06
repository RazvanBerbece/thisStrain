#!/usr/bin/env python3

# Importing all necessary libraries 
from tensorflow.keras.models import load_model
import argparse
import pickle
import cv2
import matplotlib.pyplot as plt
import os, sys
import coremltools

model = load_model('strainClassifier')

def predictOnImage(filename):
    """ 
    Given a filename or a filepath of an image, loads and displays it together with
    a label, stating what strain can be analysed in the input
    """
    image = cv2.imread(filename, cv2.IMREAD_COLOR)

    if image is None:
        print("Empty image.")
    else:

        output = cv2.resize(image, (512, 512))

        image = cv2.resize(image, (150, 150))

        # scale the pixel values to [0, 1]
        image = image.astype("float") / 255.0

        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

        lb = pickle.loads(open("labelBinarizer", "rb").read())

        preds = model.predict(image)

        # find the class label index with the largest corresponding
        # probability   
        i = preds.argmax(axis=1)[0]
        labels = [lb.classes_[i]]

        # draw the class labels + probability on the output image
        text = "{}: {:.2f}%".format(labels[0], preds[0][i] * 100)
        cv2.putText(output, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the output image
        cv2.imshow("Image", output)
        cv2.waitKey(0)

def saveAsCoreML():
    """ Converts the Keras model to a CoreML model and saves it """
    print("Converting model...")
    coreml_model = coremltools.converters.keras.convert(model)
    coreml_model.author = 'Antonio Berbece'
    coreml_model.short_description = 'Trained model which has an Image input containing a cannabis nug, and outputs its strain.'
    coreml_model.input_description['image'] = 'A 150 x 150 pixel Image'
    coreml_model.output_description['output1'] = 'TODO'
    coreml_model.save('thisCoreStrain.mlmodel')
    print("Operation finished.")