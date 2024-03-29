import re
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import urllib
from scipy.signal import lfilter
from utils import isUrl

"""
Transforms pixel value into an amplitude between [0,1]
"""
def intensity_to_amplitude(value):
    return value / 255.0 

def modulator(modulator, duration):
    
    # Parameters
    fs = 22050
    f_carrier = 635  # Carrier frequency in Hz (A4 note)

    # Time array
    t = np.arange(0, duration, 1/fs)

    # Carrier and Modulator signals
    carrier = np.sin(2 * np.pi * f_carrier * t)  # Carrier signal

    # Amplitude Modulated signal
    am_signal = carrier * modulator
    
    # Plotting
    plt.figure(figsize=(10, 8))

    # Carrier Signal
    plt.subplot(3, 1, 1)
    plt.plot(t, carrier)
    plt.title('Carrier Signal')

    # Modulator Signal
    plt.subplot(3, 1, 2)
    plt.plot(t, modulator)
    plt.title('Modulator Signal')
    
    # AM Signal
    plt.subplot(3, 1, 3)
    plt.plot(t, am_signal)
    plt.title('AM Signal')

    plt.tight_layout()
    plt.show()

    # Saving the AM signal as a WAV file
    am_signal_normalized = np.int16((am_signal / am_signal.max()) * 32767)  # Normalize the signal
    
    return am_signal_normalized

"""
Generate a signal from an image in grayscale
"""
def generate_sound(gray_image):
    
    print("(width, height) image = ",gray_image.shape)
    width = gray_image.shape[1] #nb columns
    height = gray_image.shape[0] #nb rows
    
    # Define the range of frequencies
    min_frequency = 70  # Minimum frequency in Hz #500 #100
    max_frequency = 1200  # Maximum frequency in Hz #1200 #1000
    
    #niquist :  sample_rate > 2 * maxFreq 
    # Sound parameters
    sample_rate = 22050 # norme echantillonage
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

    # Return the sum of signals
    # sound = sound[sound != 0]
    #n = 12  # the larger n is, the smoother curve will be
    #b = [1.0 / n] * n
    #a = 1
    #sound = lfilter(b, a, sound)
    return sound/np.max(sound) * 0.95

"""
Decode an image into a sound from left to right
Parameter : path_image = URL or file path
Return : the signal array
"""
def decodeVisualisation(path_image) :
    
    print("==================================")
    print(path_image)
    
    if isUrl(path_image): 
         req = urllib.request.urlopen(path_image)
         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
         gray_image = cv.imdecode(arr, 0)
    else : 
        gray_image = cv.imread(path_image,0) # GrayScale
        
    print("Gray image dim = ", gray_image.shape)
    
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


"""url = "images/line.png"
sound = decodeVisualisation(url)
path = saveSound(sound, url)
#deleteSound(path)"""
