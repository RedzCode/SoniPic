import os
import re
from flask import Flask, Response, request, jsonify, send_file
from imgToSound import decodeVisualisation
from imgToSegmentation import decodeRegion
from utils import saveSound, deleteSound, isPresent
import pathlib

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/post-sound/", methods=['POST'])
def post_sound():
   
    # Extract the JSON data from the request body
    data = request.json
        
    if data:
        url = data.get('url')
        print("urlllll =========== " +url)
        
        url_modified = re.sub(r'[^\x00-\x7F]', '', url.rsplit('/', 1)[-1])
        
        # Visualisation
        pathVisu = str("visu"+"_"+url_modified+'.wav')
        if not isPresent(pathVisu) :
            # Visualisation   
            soundVisu,sr = decodeVisualisation(url)
            saveSound(soundVisu, url,sr, "visu")
            
        # Listen
        pathListen = str("ln"+"_"+url_modified+'.wav')
        if not isPresent(pathListen) :
            soundListen, sr = decodeRegion(url)
            saveSound(soundListen,url, sr, "ln" )
                
        data = {
            "pathVisu": str(pathVisu),
            "pathListen": str(pathListen)
        }
    
        return jsonify(data)
    
    return Response("", status=404, mimetype='application/json')
    
@app.route("/get-sound/<string:name>", methods=['GET'])
@cross_origin()
def get_sound(name):
    name = re.sub(r'[^\x00-\x7F]', '', name)
    racine = os.path.abspath(os.getcwd())
    path = pathlib.PureWindowsPath(racine+"\\generatedSounds\\"+name)
    return send_file(path.as_posix())

@app.route("/delete-sound/<string:path>", methods=['DELETE'])
def delete_sound(name):
    return jsonify(deleteSound(name))

if __name__ == "__main__":
    app.run(debug=True)
