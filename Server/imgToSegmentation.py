import librosa
import re
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
from utils import isUrl
import env
import random
from utils import saveSound, deleteSound, isPresent

def segmentationDetection(path_image): 
        
    if isUrl(path_image): 
         req = urllib.request.urlopen(path_image)
         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
         image = cv.imdecode(arr, 1)
    else : 
        image = cv.imread(path_image)

    setup_logger()

    # Create config
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
    
    # Show image and labels
    """cv.imshow("result", out.get_image()[:, :, ::-1])
    cv.waitKey(0)"""
    
    return segment_id_to_label
    
def labelsToSound(labels): 
    
    uniqueLabels = list(dict.fromkeys(labels))
    
    size = 220000
    sound = np.zeros(size,)
    sr = 0
    
    racine = env.racine

    # Loop over all the labels
    for label in uniqueLabels : 
        nb = labels.count(label)
        percent = int((nb * 6) / len(labels)) 
        
        if label == "person":
            pas1, sr = librosa.load(racine+'/sounds/pas1.mp3')
            pas2, sr = librosa.load(racine+'/sounds/pas2.mp3')
            max = 1
            if nb >= 3 :
                 discus, sr = librosa.load(racine+'/sounds/foules.mp3')
                 max = 2
            for i in range(percent):
                rd = random.randint(0, max)
                if rd == 0:
                    print("add pas")
                    sound += handleMix(pas1, size)
                elif rd == 1:
                    print("add pas")
                    sound += handleMix(pas2, size)
                elif rd == 2: 
                    print("add blabla")
                    sound += handleMix(discus, size)
                    
        elif label == "car":
            car, sr = librosa.load(racine+'/sounds/car.mp3')
            for i in range(percent):
                sound += handleMix(car, size)
        elif label == "bicycle":
            bicy, sr = librosa.load(racine+'/sounds/velo.mp3')
            sound += handleMix(bicy, size)
        elif label == "tree":
            forest, sr = librosa.load(racine+'/sounds/forest.mp3')
            sound += handleMix(forest, size)
        elif label == "sea":
            sea, sr = librosa.load(racine+'/sounds/sea.mp3')
            sound += handleMix(sea, size)
        elif label == "horse":
            horse, sr = librosa.load(racine+'/sounds/cheval.mp3')
            sound += handleMix(horse, size)
           
    if not np.any(sound) :
        sound, sr = librosa.load(racine+'/sounds/no_instances.mp3')
    
    return sound, sr

def handleMix(file, size):
    start = random.randint(0, len(file)-(size+1))
    subSound = file[start:start+size]
    
    return subSound


def decodeRegion(path_image):

    labels = segmentationDetection(path_image)
    sound,sr = labelsToSound(labels)
    
    return sound, sr
    

"""sound, sr = decodeRegion("images/beachHorse.jpg")
saveSound(sound, "test.mp3",sr, "ln")"""
