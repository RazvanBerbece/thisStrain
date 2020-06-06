# Example of client on Python side using the local served where the model is hosted through flask

import requests
import base64
import json

url = "http://127.0.0.1:5000/predictOnImage"

def main():
    with open('TestPhotos/testpic.jpg', 'rb') as picture:
        encoded_string = base64.b64encode(picture.read())
        response = requests.post(url, data={'data': encoded_string})
        response_dict = json.loads(response.text)
        print(response_dict['output']) # rd[0] or rd[1] to access fields with label and probability

if __name__ == "__main__":
    main()