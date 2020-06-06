# This will download the scraped images
# and will place them in suggestive folders

import os
import urllib.request
import os.path as path

class ImageDownloader:
    """ Downloads photos from URL and saves them in their specific folders """

    def __init__(self):
        self.root = path.abspath(path.join(__file__ ,"../../saved/"))

    def save(self, resource, location, counter):
        """ Creates required labeled folder and saves resource there with format <strainCOUNTER.jpg> """
        safeLocation = location.replace(" ", "_") # creating a safe filename (no spaces)
        path = os.path.join(self.root, safeLocation)
        os.makedirs(path, exist_ok = True)
        print(f"Saving to {safeLocation}")
        output = open(f"{self.root}/{safeLocation}/{safeLocation + str(counter)}.jpg", "wb")
        output.write(resource.read())
        output.close()

    def download(self, URL, savedTo, photoNum):
        """ Downloads image from URL """
        print(f"Downloading {savedTo + str(photoNum)}.jpg...", end = "\n" * 2)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
        page = urllib.request.Request(URL, headers=headers) 
        gotResource = urllib.request.urlopen(page) # holds the image data
        self.save(gotResource, savedTo, photoNum)

