import io
import re
from flask import Flask, Response, request, jsonify, send_file
from imgToSound import decodeVisualisation
from imgToSegmentation import decodeRegion
from utils import saveSound, deleteSound, isPresent, iriToUrl
import pathlib
import env
import base64
from PIL import Image
import cv2 as cv
import numpy as np



from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/post-sound/", methods=['POST'])
def post_sound():

    # Extract the JSON data from the request body
    
    dataToSend = ""
    
    if 'image' in request.files:
        image_data = (request.files.get('image')).read()
        
        filename = "img-website"
        
        # Visualisation
        pathVisu = str("visu"+"_"+filename+'.wav')
        soundVisu,sr = decodeVisualisation(image_data)
        saveSound(soundVisu, filename,sr, "visu")
            
        # Listen
        pathListen = str("ln"+"_"+filename+'.wav')
        soundListen, sr = decodeRegion(image_data)
        saveSound(soundListen,filename, sr, "ln" )
            
        dataToSend = {
            "pathVisu": str(pathVisu),
            "pathListen": str(pathListen)
        }
    elif request.json:
        data = request.json
        print(data)
        print(data.get('url'))
        if data.get('url') :
            url = data.get('url')
            print("urlllll =========== " +url)
            url_encoded = iriToUrl(url)
            print("url_encoded =========== " +url_encoded)
            
            filename = re.sub(r'[^\x00-\x7F]', '', url.rsplit('/', 1)[-1])
            
            # Visualisation
            pathVisu = str("visu"+"_"+filename+'.wav')
            if not isPresent(pathVisu) :
                # Visualisation   
                soundVisu,sr = decodeVisualisation(url_encoded)
                saveSound(soundVisu, filename,sr, "visu")
                
            # Listen
            pathListen = str("ln"+"_"+filename+'.wav')
            if not isPresent(pathListen) :
                soundListen, sr = decodeRegion(url_encoded)
                saveSound(soundListen,filename, sr, "ln" )
            
        dataToSend = {
            "pathVisu": str(pathVisu),
            "pathListen": str(pathListen)
        }
                
    if dataToSend != "" :
        return jsonify(dataToSend)
    
    return Response("", status=404, mimetype='application/json')
    
@app.route("/get-sound/<string:name>", methods=['GET'])
@cross_origin()
def get_sound(name):
    racine = env.racine
    path = pathlib.PureWindowsPath(racine+"\\generatedSounds\\"+name)
    return send_file(path.as_posix())

@app.route("/delete-sound/<string:path>", methods=['DELETE'])
def delete_sound(name):
    return jsonify(deleteSound(name))

if __name__ == "__main__":
    app.run(debug=True)
