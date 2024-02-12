import base64
from flask import Flask, request, jsonify
import cv2 as cv
import os
import urllib.request 
from imgToSound import decode


app = Flask(__name__)

@app.route("/get-sound/<image_url>")
def get_sound(image_url):
    #url = image_url.replace(".SN.", "/")
    # TODO : get image from body and not url
    """ url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Driebergen_Boom_Inhuldiging_Koning_Willem-Alexander.jpg/800px-Driebergen_Boom_Inhuldiging_Koning_Willem-Alexander.jpg"
    urllib.request.urlretrieve(url, "Server/tree.jpg") 
   """
   
    decode("images/line.png")
    
    return jsonify("test") #jsonify(str(encoded))


if __name__ == "__main__":
    app.run(debug=True)