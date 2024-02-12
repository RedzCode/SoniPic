import cv2 as cv
# for data transformation
import numpy as np
# for visualizing the data
import matplotlib.pyplot as plt
# for saving the media file
from scipy.io.wavfile import write

"""
Transforms pixel value into an amplitude between [0,1]
"""
def intensity_to_amplitude(value):
    # TODO : intensité non linéaire pour s'adapter à l'oreille humaine
    return np.exp(0.02218*value - 5.6559) 
    #return value / 255.0 

"""
Generate a signal from an image in grayscale
"""
def generate_sound(gray_image):
    
    print("(width, height) image = ",gray_image.shape)
    width = gray_image.shape[1] #nb columns
    height = gray_image.shape[0] #nb rows
    
    # Define the range of frequencies
    min_frequency = 500  # Minimum frequency in Hz
    max_frequency = 1200  # Maximum frequency in Hz
    
    #niquist :  sample_rate > 2 * maxFreq 
    # Sound parameters
    sample_rate = 2100
    timeByColumns = 2
    duration = gray_image.shape[1] * timeByColumns # 2 sec by columns    

    # Time array
    t = np.linspace(0, duration, duration * sample_rate)

    # init a sound with zero amplitude
    # TODO : find a way to init properly ?
    sound = 0 * np.sin(2 * np.pi * 0 * t)

    # Iterate over each pixel in the grayscale image
    row_index = 0
    for row in gray_image:

        # Init amplitude envelope of the signal
        amp_envelope = np.zeros(len(t)) 
        
        # Determine frequence of a row
        normalized_row_index = row_index / (height - 1)
        frequency = min_frequency + (max_frequency - min_frequency) * normalized_row_index

        col_index = 0
        for pixel_value in row:

            amplitude = intensity_to_amplitude(pixel_value)

            # For each column associate 2000 points with the same amplitude
            # 2000 points =  2 secs
            born_inf = col_index * (sample_rate*timeByColumns)
            born_sup = (sample_rate*timeByColumns) * (col_index+1)
            for j in range(born_inf, born_sup):
                amp_envelope[j] = amplitude
        
            col_index += 1
        
        # Generate signal of one row
        sinewave = amp_envelope * np.sin(2 * np.pi * frequency * t)
        row_index += 1
        # Addition signals
        sound += sinewave

    # Return the sum of signals
    return sound

"""
Decode an image into a sound from left to right

Return : the signal array
"""
#"Server/line.png"
def decode(path_image) :
    
    """ check if image present
    print(os.path.isfile("tree.jpg")) """
    
    gray_image = cv.imread(path_image,0) # GrayScale
    print("Gray image dim = ", gray_image.shape)
    
    # resize image
    dim = (min(gray_image.shape[0], 400), min(gray_image.shape[1], 400))
    resized_gray_image = cv.resize(gray_image, dim, interpolation = cv.INTER_AREA)
    
    # TODO : Edge detection

    #Affiche l'image
    #cv.imshow("resized", resized_gray_image)
    #cv.waitKey() 

    sounds = generate_sound(resized_gray_image)
    

    plt.plot(sounds)
    plt.show()

    write('lineUp_10k.wav', 10000, sounds)
    write('lineUp_50k.wav', 50000, sounds)
    write('lineUp_100k.wav', 100000, sounds)
    write('lineUp_1000k.wav', 1000000, sounds)


decode("images/line.png")
