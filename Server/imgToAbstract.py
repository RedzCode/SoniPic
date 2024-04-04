import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import urllib
from scipy.signal import lfilter
from utils import isUrl, isPath

"""
Transforms pixel value into an amplitude between [0,1]
Parameter : value = pixel value between [0,255]
Return : the normalized amplitude value
"""
def intensity_to_amplitude(value):
    return value / 255.0 

"""
Generate a signal from an image in grayscale
Parameter : gray_image = image in grayscale
Return : the generated sound as a numpy array
"""
def generate_sound(gray_image):
    
    height = gray_image.shape[0] #nb rows
    
    # Define the range of frequencies
    min_frequency = 70  # Minimum frequency in Hz
    max_frequency = 1200  # Maximum frequency in Hz
        
    #niquist :  sample_rate > 2 * maxFreq 
    # Sound parameters
    sample_rate = 22050 #norme
    timeByColumns = 0.025
    duration = int(gray_image.shape[1] * timeByColumns)     

    # Time array
    t = np.linspace(0, duration, duration * sample_rate)

    # init a sound with zero amplitude
    sound = 0 * np.sin(2 * np.pi * 0 * t)

    # Iterate over each pixel in the grayscale image
    row_index = 0
    for row in gray_image:

        # Init amplitude envelope of the signal
        amp_envelope = np.zeros(len(t)) 
        
        # Determine frequence of a row
        normalized_row_index = row_index / (height - 1)
        frequency = min_frequency + (max_frequency - min_frequency) * (1 - normalized_row_index)

        col_index = 0
        for pixel_value in row:

            amplitude = intensity_to_amplitude(pixel_value)

            # For each column associate (sample_rate*timeByColumns) points with the same amplitude
            # (sample_rate*timeByColumns) points =  0.025 secs
            born_inf = int(col_index * (sample_rate*timeByColumns))
            born_sup = int((sample_rate*timeByColumns) * (col_index+1))
            for j in range(born_inf, born_sup):
                if j < len(t):
                    amp_envelope[j] = amplitude
        
            col_index += 1
        
        # Generate signal of one row
        sinewave = amp_envelope * np.sin(2 * np.pi * frequency * t)
        #sinewave = modulator(sinewave, duration)
        row_index += 1
        # Addition signals
        sound += sinewave

    return sound/np.max(sound) * 0.95

"""
Decode an image into an abstract signal from left to right
Parameter : image_data = URL, file path or img data
Return : the signal numpy array
"""
def decodeAbstract(image_data) :
    
    if isUrl(image_data): 
         req = urllib.request.urlopen(image_data)
         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
         gray_image = cv.imdecode(arr, 0)
    elif isPath(image_data) :
         gray_image = cv.imread(image_data,0) # GrayScale
    else : 
        arr = np.asarray(bytearray(image_data), dtype=np.uint8)
        gray_image = cv.imdecode(arr,0)
    
    # resize image
    dim = (min(max(gray_image.shape[0], 40), 400), min(max(gray_image.shape[1],40), 400))
    resized_gray_image = cv.resize(gray_image, dim, interpolation = cv.INTER_AREA)

    #Display the image
    """cv.imshow("resized", resized_gray_image)
    cv.waitKey() """

    sound = generate_sound(resized_gray_image)

    #Plot signal
    """plt.plot(sound)
    plt.ylabel('Amplitude')
    plt.xlabel('Temps [sec]')
    plt.show()"""
    
    #Plot spectrogramme
    """fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Spectrogramme")
    ax.set_xlabel("Temps [sec]")
    ax.set_ylabel("Frequences [Hz]")
    pxx,  freq, t, cax = plt.specgram(sound, Fs=22050, mode="magnitude")
    #fig.colorbar(cax).set_label('Intensité [dB]')
    plt.ylim([50, 1200])
    plt.show()"""
    
    return sound, 22050    
