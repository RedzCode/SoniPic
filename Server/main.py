import base64
import json
from flask import Flask, request, jsonify
import cv2 as cv
from imgToSound import decode


app = Flask(__name__)

@app.route("/post-sound/", methods=['POST'])
def post_sound():
   
    # Extract the JSON data from the request body
    data = request.json
        
    if data:
        url = data.get('url')
           
    encodedSound = decode(url)
    
    data = {
        "encodedSound": str(encodedSound)
    }
    
    return jsonify(data)
    
    #return jsonify(encodedSound)


if __name__ == "__main__":
    app.run(debug=True)