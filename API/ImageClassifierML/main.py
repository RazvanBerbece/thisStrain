#!/usr/bin/env python3

from api import predictOnImage, saveAsCoreML

def main():

    # testing one of the sample pictures
    predictOnImage('TestPhotos/testpic.jpg')
    saveAsCoreML()

if __name__ == "__main__":
    main()