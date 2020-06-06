# This will crawl the potguide website and get all strain images,
# saving them in the saved folder

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from .downloader import ImageDownloader
import split_folders
import os
import os.path as path

class Crawler:
    """ Holds all methodology related to the crawler """

    def __init__(self):
        self.BASE_URL = "https://potguide.com"
        self.Downloader = ImageDownloader()

    def testConnection(self):
        """ Tests the result of the request to BASE_URL """
        page = requests.get(self.BASE_URL)
        print(page.content)

    def profileRequest(self, profileURL):
        """ This will be called on every strain profile and will crawl the photos """
        finalURL = self.BASE_URL + profileURL

        # Making Chrome run in the background so the UI doesn't get overflowed by Chrome tabs
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        
        # Installing chromedriver via webdriver-manager
        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        browser.get(finalURL)

        photoContainer = [] # this will hold all image links gathered from the strain page
        photoContainer = browser.find_elements_by_tag_name("img")

        toBeDownloaded = [] # holds relevant links for given strain URL, will be returned

        # By checking the list of links, the first 3 are non-related to the strain
        # the rest until the link changes are strain photos
        index = 0 
        for container in photoContainer:
            if index < 3:
                index += 1
                continue
            else:
                index += 1
                possiblePhotoLink = container.get_attribute("src")
                
                # Through observation, I have realised that all the relevant pic URLS 
                # contain base https://images.potguide.com/strains/
                if possiblePhotoLink and "https://images.potguide.com/strains/" in possiblePhotoLink:
                    toBeDownloaded.append(possiblePhotoLink)
                else:
                    continue


        browser.close()

        return toBeDownloaded

    def requestOnPage(self, page):

        print(f"On page {page}")

        if page == 25:
            return
        else:
            """ Requests URL on given page (possibility for recursion) """
            newRequestURL = self.BASE_URL + "/strain-profiles" + f"/?page={page}"
            newRequestResult = requests.get(newRequestURL)
            gotContent = newRequestResult.content

            soup = BeautifulSoup(gotContent, "html.parser")

            # Get all strain profile containers
            strainProfiles = soup.find_all("div", itemprop="itemListElement")
       
            # Iterating through profiles and crawling for name and photos
            for profile in strainProfiles:

                strainNameContainer = profile.find("h2", class_="strain-profile-name")
                strainNameSpan = strainNameContainer.find("span")

                strainName = strainNameSpan.text # holds the name of the strain

                # Make request on strain specific page and get photos from there
                strainURLContainer = profile.find("a", href=True)
                photoURLS = self.profileRequest(strainURLContainer["href"]) # list which holds all links

                index = 0
                for URL in photoURLS:
                    self.Downloader.download(URL, strainName, index)
                    print(f"On page {page}")
                    index += 1
            
            # Recursive calls until scraper reached page 24
            self.requestOnPage(page + 1)
    
    def organiseFiles(self):
        """ Organises the resulted folder into Training / Test Sets (0.8 / 0.1 / 0.1) """
        root = path.abspath(path.join(__file__ ,"../../saved/"))
        output = path.abspath(path.join(__file__ ,"../../output/"))
        split_folders.ratio(root, output = output, seed = 1337, ratio = (.8, .1, .1))

            