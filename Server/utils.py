import re
from urllib.parse import quote
import soundfile as sf
import os
import env


"""
Save a signal into an audio file in the sever
Parameters : sound = signal as numpy array
             name = filename
             sr = sample rate
             prefix = the mode of the signal
Return the location of the file
"""
def saveSound(sound,name,sr, prefix):
    path = str(prefix+"_"+name+'.wav')
    racine = env.racine
    sf.write(racine+"/generatedSounds/"+path, sound, sr)
    return path
    
"""
Delete an audio file in the sever
Parameters : filename
Return true if the file has been deleted
"""
def deleteSound(filename):
    racine = env.racine
    path = racine+'/generatedSounds/'+filename
    if os.path.exists(path):
        os.remove(path)
        return True
    else:
        print("The file does not exist") 
    return False

"""
Check if a file is present on the server
Parameters : filename
Return true if the file is present
"""
def isPresent(filename):
    racine = env.racine
    path = racine+'/generatedSounds/'+filename
    return os.path.exists(path)

"""
Check if an argument is an URL
"""
def isUrl(arg):
    if isinstance(arg, str) :
        # Regular expression to match typical URL formats
        url_pattern = re.compile(r'^(?:http|ftp)s?://\S+$', re.IGNORECASE)

        # Check if the argument matches the URL pattern
        if re.match(url_pattern, arg):
            return True
    return False

"""
Check if an argument is a path
"""
def isPath(arg):
     return isinstance(arg, str)
 
"""
Transform IRI (URL with not %-encoded character) to URL
Return the correct URL
"""
def iriToUrl(iri):
    if iri.find("%") != -1 :
        return iri
    return quote(iri, safe=':/')