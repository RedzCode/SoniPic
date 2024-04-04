import librosa
from detectron2.utils.logger import setup_logger
import numpy as np
import cv2 as cv
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import urllib
import librosa
from utils import isUrl, isPath
import env
import random
from collections import Counter
from math import *

"""
 Use MS COCO to apply the image segmentation on the image
 and returns the predicted labels
 Parameter : image
 Return : List of labels
"""
def segmentationDetection(image): 

    setup_logger()

    # Create configurations
    cfg = get_cfg()
    cfg.MODEL.DEVICE = env.device
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
    
    # Get class names of the two classes
    thing_classes = metadata.thing_classes
    stuff_classes = metadata.stuff_classes

    segment_id_to_label = []

    # get thing classes
    for segment in segmentInfo:
        if segment["category_id"] >= 0:
            # select labels with prediction > 0.9
            if segment["isthing"] == True and segment["score"] > 0.9 :
                segment_id_to_label.append(thing_classes[segment["category_id"]])

    # get stuff classes
    for segment in segmentInfo:
        if segment["category_id"] >= 0:
            if segment["isthing"] == False :
                segment_id_to_label.append(stuff_classes[segment["category_id"]])
    
    # Show image and labels
    """cv.imshow("result", out.get_image()[:, :, ::-1])
    cv.waitKey(0)"""
    
    return segment_id_to_label
    
"""
Generate a sound depending on the labels in input
Parameter : labels = list of predicted labels
Return : a signal as a numpy array
"""
def labelsToSound(labels): 

    uniqueLabels = list(dict.fromkeys(labels))
    dictLabels = processLabels(labels)
    
    size = 220000
    sound = np.zeros(size,)
    sr = 0
    
    racine = env.racine

    # Loop over all the labels
    for label in uniqueLabels : 
        occurrences = dictLabels[label]
        
        if label == "person":
            pas1, sr = librosa.load(racine+'/sounds/pas1.mp3')
            pas2, sr = librosa.load(racine+'/sounds/pas2.mp3')
            max = 1
            if occurrences >= 3 :
                 discus, sr = librosa.load(racine+'/sounds/foules.mp3')
                 max = 2
            for i in range(occurrences):
                rd = random.randint(0, max)
                if rd == 0:
                    sound += handleMix(pas1, size)
                elif rd == 1:
                    sound += handleMix(pas2, size)
                elif rd == 2: 
                    sound += handleMix(discus, size)
        elif label == "car":
            nb = labels.count(label)
            if nb > 10:
                car, sr = librosa.load(racine+'/sounds/periph.mp3')
                sound += handleMix(car, size)
            else :
                car, sr = librosa.load(racine+'/sounds/car.mp3')
                for i in range(occurrences):
                    sound += handleMix(car, size)
        elif label == "bicycle":
            bicy, sr = librosa.load(racine+'/sounds/velo.mp3')
            for i in range(occurrences):
                sound += handleMix(bicy, size)
        elif label == "tree" or label == "bird":
            forest, sr = librosa.load(racine+'/sounds/forest.mp3')
            sound += handleMix(forest, size)
        elif label == "sea":
            sea, sr = librosa.load(racine+'/sounds/sea.mp3')
            sound += handleMix(sea, size)
        elif label == "horse":
            horse, sr = librosa.load(racine+'/sounds/cheval.mp3')
            for i in range(occurrences):
                sound += handleMix(horse, size)
           
    if not np.any(sound) :
        sound, sr = librosa.load(racine+'/sounds/no_instances.mp3')
    
    return sound, sr

"""
Apply a limit of occurrences of a label, apply proportion to all the labels
Parameter : labels = list of labels
Return : a dictionnary of labels with their proportioned occurrences
"""
def processLabels(labels):
    dictLabels = Counter(labels)
    limit = 4
    maxOccurences = dictLabels['person']
    if maxOccurences >  limit : 
        maxLabel = list(dictLabels.keys())[0]
        for label, value in dictLabels.items():
            if label == maxLabel:
                dictLabels[label] = limit 
            elif value > limit:
                dictLabels[label] = ceil(limit * limit / maxOccurences)
            else : 
                dictLabels[label] = ceil(value * limit / maxOccurences)
    
    return dictLabels  
    
"""
Select randomly n seconds of the audio file
Parameter : file = audio file
            size = duration of the final audio
Return : a sub sound as a numpy array
"""
def handleMix(file, size):
    start = random.randint(0, len(file)-(size+1))
    subSound = file[start:start+size]
    
    return subSound


"""
Decode an image into a concrete sound representing the image
Parameter : image_data = URL, file path or img data
Return : the signal as numpy array
"""
def decodeConcrete(image_data):

    if isUrl(image_data): 
         req = urllib.request.urlopen(image_data)
         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
         image = cv.imdecode(arr, 1)
    elif isPath(image_data) :
        image = cv.imread(image_data)
    else : 
        arr = np.asarray(bytearray(image_data), dtype=np.uint8)
        image = cv.imdecode(arr,1)

    labels = segmentationDetection(image)
    sound,sr = labelsToSound(labels)
    
    return sound, sr
    

"""sound, sr = decodeRegion("../Data/images/amsterdam.jpg")
saveSound(sound, "test.mp3",sr, "ln")"""
