import librosa
from scipy.io.wavfile import write
from pathlib import Path
import re
from detectron2.utils.logger import setup_logger
# Import some common libraries
import numpy as np
import cv2 as cv
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import urllib
import librosa
from scipy.io.wavfile import write


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

def segmentationDetection(path_image): 
        
    if isUrl(path_image): 
         req = urllib.request.urlopen(path_image)
         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
         image = cv.imdecode(arr)
    else : 
        image = cv.imread(path_image)

    setup_logger()

    # Create config
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")
    predictor = DefaultPredictor(cfg)

    # Perform inference
    predictions, segmentInfo = predictor(image)["panoptic_seg"]
    

    # Visualize predictions
    metadata= MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
    viz = Visualizer(image[:,:,::-1 ], metadata=metadata)
    
    out = viz.draw_panoptic_seg_predictions(predictions.to("cpu"),segmentInfo)
    
    # Get class names (labels)
    thing_classes = metadata.thing_classes
    stuff_classes = metadata.stuff_classes

    segment_id_to_label = []

    # get thing classes
    for segment in segmentInfo:
        if segment["category_id"] >= 0:
            if segment["isthing"] == True and segment["score"] > 0.9 :
                segment_id_to_label.append(thing_classes[segment["category_id"]])

    # get stuff classes
    for segment in segmentInfo:
        if segment["category_id"] >= 0:
            if segment["isthing"] == False :
                segment_id_to_label.append(stuff_classes[segment["category_id"]])

    # Print segment IDs and corresponding 
    print(segmentInfo)
    for i in range(len(segment_id_to_label)):
          print(f"Label: {segment_id_to_label[i]}")
    
    cv.imshow("result", out.get_image()[:, :, ::-1])
    cv.waitKey(0)
    
    return segment_id_to_label
    
def labelsToSound(labels): 
    
    labels = list(dict.fromkeys(labels))
    
    size = 220000
    sound = np.zeros(size,)

    # Loop over all the labels
    for label in labels : 
        if label == "person":
            person, sr = librosa.load('sounds/person_10sec.mp3')
            person = person[0:size]
            sound += person
            print("add person")
        elif label == "car":
            car, sr = librosa.load('sounds/car_10sec.mp3')
            car = car[0:size]
            sound += car
            print("add car")
        elif label == "bicycle":
            print("bicy")
        elif label == "sea":
            print("sea")
        elif label == "tree":
            print("tree")
        elif label == "sea":
            print("sea")
        elif label == "horse":
            print("horse")
        
    # save
    write("generatedSounds/mix.wav", sr, sound)

def decodeRegion(path_image):

    labels = segmentationDetection(path_image)
    sound = labelsToSound(labels)

decodeRegion("images/street.jpg")

"""

    #ipd.Audio(data=car, rate = sr)

    print(car.shape)
    print(person.shape)

    size = min(car.shape, person.shape)[0]

    car = car[0:size]
    person = person[0:size]

    print(car.shape)
    print(person.shape)


    mix = car + person
"""