import re
import soundfile as sf
import os
import env

def saveSound(sound,name,sr, prefix):
    name = re.sub(r'[^\x00-\x7F]', '', name.rsplit('/', 1)[-1])
    path = str(prefix+"_"+name+'.wav')
    racine = env.racine
    sf.write(racine+"/generatedSounds/"+path, sound, sr)
    return path
    
def deleteSound(filename):
    racine = env.racine
    path = racine+'/generatedSounds/'+filename
    if os.path.exists(path):
        os.remove("generatedSounds/"+path)
        return True
    else:
        print("The file does not exist") 
    return False

def isPresent(filename):
    racine = env.racine
    path = racine+'/generatedSounds/'+filename
    print("pressseeent ===========")
    print(path)
    print(os.path.exists(path))
    return os.path.exists(path)

"""
Check if an argument is an URL
"""
def isUrl(arg):
    # Regular expression to match typical URL formats
    url_pattern = re.compile(r'^(?:http|ftp)s?://\S+$', re.IGNORECASE)

    # Check if the argument matches the URL pattern
    if re.match(url_pattern, arg):
        return True
    return False