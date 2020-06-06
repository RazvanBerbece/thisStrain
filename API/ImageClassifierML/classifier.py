#!/usr/bin/env python3

# Import the necessary packages
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import SGD
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2
import os
from modelBuilder import VGGNet

# Data Key Info
data_dir = 'Data'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # API dir

# Will become numpy arrays
data = []
labels = []

# Grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images(os.path.join(ROOT_DIR, data_dir))))
print(imagePaths)
random.seed(420)
random.shuffle(imagePaths)

# Get all images data & all labels
for imagePath in imagePaths:
    print(f"Analyzing image at {imagePath}")
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (150, 150))
    data.append(image)

    label = imagePath.split(os.path.sep)[-2]
    label = label.replace("_", " ")
    labels.append(label)

# Casting to np array
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# Splitting data in train / test samples (80% train, 20% test)
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2, random_state=420)

# Convert the labels from integers to vectors 
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

# Construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# Initialize our VGG-like Convolutional Neural Network
model = VGGNet.build(width=150, height=150, depth=3,
	classes=len(lb.classes_))

# Initialize our initial learning rate, # of epochs to train for,
# and batch size
# INIT_LR = 0.1
EPOCHS = 50
BS = 32

# Initialize the model and optimizer 
model.compile(loss="categorical_crossentropy", optimizer="adam",
	metrics=["accuracy"])

# Train the network
history = model.fit(x=aug.flow(trainX, trainY, batch_size=BS),
	validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
	epochs=EPOCHS)

# Saves model & label binarizer to disk
model.save('strainClassifier', save_format="h5")
f = open('labelBinarizer', "wb")
f.write(pickle.dumps(lb))
f.close()
