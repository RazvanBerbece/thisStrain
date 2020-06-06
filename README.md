# thisStrain
Python-side, creates a ML model which identifies cannabis strains using a dataset of images scraped from the internet. The model takes as input an Image with (supposedly) a cannabis leaf and outputs its strain. Client-side (Swift), analyses the input image and outputs the strain label in a nicely-finished UI.

# Status
- [x] API
- [x] iOS Client
- [x] Model Prototype
- [x] Crawler
- [ ] Further training of ML model with more data
- [ ] Further UI/UX imporvements for the iOS Client

# API - Python
The API works by running it locally in a virtualenv and allowing Flask to host the network on the network in order for the iOS Client to work.

## The API uses data from :
- the **Web Crawler** (found in **API/Crawler**)
- Scrapes https://potguide.com/ for images and labels of cannabis strains and saves them in a folder with the label as name
- the **Image Classifier** (found in **API/ImageClassifierML**)
    - Machine Learning Model which uses a CNN trained on the pictures gathered by the Crawler above. The input is comprised of an image (which is resized to 150 x 150 px) and the output is the strain of the cannabis depicted in the picture and the accuracy of the classification.
The Server related methodology can be found in **API/Server** and an example of a Python Client can be found in **API/ClientExample**

Data images are passed to the API by encoding them in a *base64string*. The result is a **JSON** structure which holds a dictionary of type { "*Output*" : ["<*label*>", "<*accuracy*>"]

### API Calls :
> http://FLASK_HOST_ADDRESS:PORT/ (GET, checks API availability)

> http://FLASK_HOST_ADDRESS:PORT/predictOnImage (**POST**, **form-data** with format : **"data" : base64string**, sends base64 encoded image to Server and get the output of the ML model)

# Client - Swift (UIKit)
The Client is built in Swift and uses an AR Session View for easy image classification at the press of a button.

### Pods :
- Alamofire
- SwiftyJSON
