from flask import Flask, request
import json
import base64
from Classes import Decoder as dcd64
from Classes import Classifier as clsf
import matplotlib.pyplot as plt
import matplotlib

app = Flask(__name__)

matplotlib.use('agg')

@app.route('/', methods=['GET'])
def testConnection():
    """ Tests if the API is up and running """
    return json.dumps({'message': 'API working.'})

@app.route('/predictOnImage', methods=['POST'])
def predictOnImage():
    """ 
    Receives a base64string through a POST request and processes the data 
    returning a JSON pair with the label and the probability
    """
    responseDict = dict()
    gotData = request.form.to_dict()
    decoder = dcd64.Decoder(gotData['data'])
    classifier = clsf.Classifier(decoder.getImageData())
    responseDict['output'] = classifier.getOutput()
    return json.dumps(responseDict)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)