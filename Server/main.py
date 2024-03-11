import base64
import json
import os
from flask import Flask, request, jsonify, send_file
import cv2 as cv
from imgToSound import decodeVisualisation, saveSound, deleteSound


app = Flask(__name__)

@app.route("/post-sound/", methods=['POST'])
def post_sound():
   
    # Extract the JSON data from the request body
    data = request.json
        
    if data:
        url = data.get('url')
           
    sound = decodeVisualisation(url)
    path = saveSound(sound, url)
    #deleteSound(path)
    
    data = {
        "path": str(path)
    }
    
    return jsonify(data)
    
    """data = {
        "encodedSound": str(encodedSound)
    }
    
    return jsonify(data)"""
    
    #return jsonify(encodedSound)
    
    
@app.route("/websitesSounds/<string:name>", methods=['GET'])
def get_sound(name):
    racine = os.path.abspath(os.getcwd())
    return send_file(racine+"/websitesSounds/"+name,as_attachment=True)

@app.route("/websitesSounds/<string:path>", methods=['DELETE'])
def delete_sound(path):
    racine = os.path.abspath(os.getcwd())
    #TODO : HANDLE error SEND HTTP 200 ou ...
    return jsonify(deleteSound(racine+'/websitesSounds/'+path))
    


if __name__ == "__main__":
    app.run(debug=True)