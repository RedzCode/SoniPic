import base64
from flask import Flask, request, jsonify
import cv2 as cv
import os
import urllib.request 
# for data transformation
import numpy as np
# for visualizing the data
import matplotlib.pyplot as plt
# for opening the media file
from scipy.io.wavfile import write
from scipy import signal

app = Flask(__name__)

@app.route("/get-sound/<image_url>")
def get_sound(image_url):
    #url = image_url.replace(".SN.", "/")
    """ url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Driebergen_Boom_Inhuldiging_Koning_Willem-Alexander.jpg/800px-Driebergen_Boom_Inhuldiging_Koning_Willem-Alexander.jpg"
    urllib.request.urlretrieve(url, "Server/tree.jpg") 
   """
    # Opening the image and displaying it (to confirm its presence) 
    """ img = Image.open(r"tree.jpg") 
    img.show()
    
    print("-------------------")
    print(os.path.isfile("tree.jpg")) """
    
    # audio parameters
    fs = 32000;                         # sampling frequency
    frame_duration = 0.064;             # frame duration in seconds
    M = int(frame_duration * fs);            # window size
    overlap = 0.875;                    # overlap between adjacent frames
    H = (1 - overlap) * M;              # hop size

    # image parameters
    height = int(M/2 + 1);                   # image height
    print(height)
    edge_detection = True;              # use edge detection?
    scaling_factor = 10;                # adjust loudness of output
    

    img = cv.imread("tree.jpg",0)
    
    dft = cv.dft(np.float32(img),flags = cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
    print(magnitude_spectrum)
    dim = (img.shape[1], height)
    
    # resize image
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)

    cv.imshow("resized", img)
    cv.waitKey() #Affiche l'image
    print("pixel value 0 0")
    print(img[0, 0])

    print("pixel value 20 40")
    print(img[20, 40])

    print(resized.shape)
    print(resized.shape[0])
    print(resized.shape[1])

    # edge detection
    if edge_detection :
        print("edge")
        
    x = 0
    y = 0
    greyLevel = resized[x,y]
    a = 1
    b = 0
    intensite = a * greyLevel + b

    # audio synthesis
    nframes = resized.shape[1];  # number of frames in STFT
    leny = int(M + (nframes - 1) * H);   # length of reconstructed signal
    print("leny shape = ", leny)
    y = np.zeros((leny, 1)) # initialise reconstructed signal      
    #hamming(M, 'periodic');     
    w = signal.windows.hamming(int(M), sym=False)     # window false car periodic
    X = np.zeros((M, nframes))        # initialise STFT
    offy = M/2;             # initialise offset in y


    for i in range(0, nframes):
        #samples = offy - M/2 + 1 : offy + M/2; 
        bornSup = int(offy + M/2)  
        bornInf = int(offy - M/2)    
        #nbSamples = bornSup - bornInf + 1    
        samples = np.arange(bornInf, bornSup) # samples of y to be reconstructed
        phase = 2 * np.pi * (np.random.rand(int(M/2 + 1), 1) - 0.5);  # randomize phase
        phase = np.squeeze(np.asarray(phase))
        
        #X(1 : M/2 + 1, i) = img_double(:, i) .* exp(1j * phase);  
        img_array = np.array(resized)
        X[0 : int(M/2 + 1), i] = np.multiply(img_array[:,i], np.exp(1j * phase))  # apply randomized phase
        
        X[int(M/2 + 2) : M, i] = np.conj(np.flipud(X[2 : int(M/2), i]));     # remaining values of FFT
        yfw = np.multiply(np.fft.ifft(X[:, i]), w);        # inverse FFT
        yfw = np.transpose(np.asmatrix(yfw))
        """  print("yfw shape = ", yfw.shape)
        print("y(samples) shape = ",y[samples].shape)
        print("y shape = ", y.shape) """

        y[samples] = y[samples] + yfw;                            # overlap add
        offy = offy + H;                                          # offset for next iteration of loop
    y = np.real(y)
    

    write('noise.wav', len(y), y)
    encoded=base64.b64encode(open("noise.wav", "rb").read())
    
    print("y")
    print(y)
    print(y.shape)
    # Serialization+
    """ numpyData = {"array": y}
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
    print("Printing JSON serialized NumPy array")
    print(encodedNumpyData)
     """
    return encoded


if __name__ == "__main__":
    app.run(debug=True)