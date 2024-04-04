import re
from flask import Flask, Response, request, jsonify, send_file
from imgToAbstract import decodeAbstract
from imgToConcrete import decodeConcrete
from utils import saveSound, deleteSound, isPresent, iriToUrl
import pathlib
import env


from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

"""
Receive image URL or image date on the request body
Generate two audio files corresponding to abstract and concrete modes
Save the files and send back the paths of the files at the client
"""
@app.route("/post-sound/", methods=['POST'])
def post_sound():    
    dataToSend = ""
    
    if 'image' in request.files:
        # Extract the multipart/form-data Content-Type 
        image_data = (request.files.get('image')).read()
        
        filename = "img-website"
        
        # Abstract mode
        pathVisu = str("abs"+"_"+filename+'.wav')
        soundVisu,sr = decodeAbstract(image_data)
        saveSound(soundVisu, filename,sr, "abs")
            
        # Concrete mode
        pathListen = str("cr"+"_"+filename+'.wav')
        soundListen, sr = decodeConcrete(image_data)
        saveSound(soundListen,filename, sr, "cr" )
            
        dataToSend = {
            "pathVisu": str(pathVisu),
            "pathListen": str(pathListen)
        }
    elif request.json:
        # Extract the JSON data from the request body
        data = request.json
        if data.get('url') :
            url = data.get('url')
            url_encoded = iriToUrl(url)
            
            filename = re.sub(r'[^\x00-\x7F]', '', url.rsplit('/', 1)[-1])
            
            # Astract
            pathVisu = str("abs"+"_"+filename+'.wav')
            if not isPresent(pathVisu) : 
                soundVisu,sr = decodeAbstract(url_encoded)
                saveSound(soundVisu, filename,sr, "abs")
                
            # Concrete
            pathListen = str("cr"+"_"+filename+'.wav')
            if not isPresent(pathListen) :
                soundListen, sr = decodeConcrete(url_encoded)
                saveSound(soundListen,filename, sr, "cr" )
        
        # Return the files paths of the two generated audio files    
        dataToSend = {
            "pathAbstract": str(pathVisu),
            "pathConcrete": str(pathListen)
        }
                
    if dataToSend != "" :
        return jsonify(dataToSend)
    
    return Response("", status=404, mimetype='application/json')
 
 
"""
Receive the name of the file the client side want to retrieve
Return the audio file to the client
"""   
@app.route("/get-sound/<string:name>", methods=['GET'])
@cross_origin()
def get_sound(name):
    name_encoded = iriToUrl(name)
    racine = env.racine
    path = pathlib.PureWindowsPath(racine+"\\generatedSounds\\"+name_encoded)
    return send_file(path.as_posix())

"""
Delete an audio file 
"""   
@app.route("/delete-sound/<string:path>", methods=['DELETE'])
def delete_sound(name):
    return jsonify(deleteSound(name))

if __name__ == "__main__":
    app.run(debug=True)
