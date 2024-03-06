from pathlib import Path
import re
from detectron2.utils.logger import setup_logger
# Import some common libraries
import numpy as np
import cv2 as cv
import random
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.data import MetadataCatalog
import urllib
from pydub import AudioSegment

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
            if segment["isthing"] == True and segment["score"] > 0.8 :
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
    
    """cv.imshow("result", out.get_image()[:, :, ::-1])
    cv.waitKey(0)"""
    
    return segment_id_to_label
    
def labelsToSound(labels): 
    
    labels = list(dict.fromkeys(labels))
    
    output = AudioSegment.empty
    # Loop over all the labels
    for label in labels : 
        sound = AudioSegment.empty
        if label == "person":
            file_path = Path("sounds/person.mp3")
            absolute_path = file_path.absolute()
            print(absolute_path)
            sound = AudioSegment.from_file(absolute_path, format="mp3")
            print("add person")
        elif label == "car":
            file_path = Path("sounds/car.mp3")
            absolute_path = file_path.absolute()
            print(absolute_path)
            sound = AudioSegment.from_file(absolute_path, format="mp3")
            print("add car")
        elif label == "bicycle":
            print("bicy")
        elif label == "sea":
            print("sea")
        # mix sounds with sound1, starting at 5000ms into sound1)
        output = sound.overlay(output)
        
    # save
    output.export("mixed_sounds.mp3", format="mp3")

    

def decodeRegion(path_image):

    labels = segmentationDetection(path_image)
    sound = labelsToSound(labels)

decodeRegion("images/Street.jpg")
