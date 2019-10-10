import os
import sys
import itertools
import math
import logging
import json
import re
import random
from collections import OrderedDict
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from matplotlib.patches import Polygon

from skimage import color, measure
from shapely.geometry import shape, Point, Polygon, LineString
import shapely
import statistics
import scipy
import pandas as pd

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

##get_rings
#get masks and extract plygons in some reasonable way
def mask_to_polygon(mask):# Takes one mask and turns it in polygone
    intmask = mask.astype(int)
    contours = measure.find_contours(intmask, level=0.9)
    poly = Polygon(contours[0])
    return(poly)# Returns shapely polygon and coordinates can be extracted by x,y = poly.exterior.xy

##take angle of particular ring and return angle
#positive value means its tilted counterclockwise
def ring_angle(mask):
    poly = mask_to_polygon(mask)
    recx, recy = poly.minimum_rotated_rectangle.exterior.xy
    pt1_x = recx[0] 
    pt1_y = recy[0]
    pt2_x = recx[1]
    pt2_y = recy[1]
    deltaY = pt2_y - pt1_y
    deltaX = pt2_x - pt1_x
    angle = math.atan2(deltaY, deltaX)
    angleInDegrees = math.degrees(angle)
    return(angleInDegrees)
    
#take plygon and adjust it by the angle
def align_polygon(mask):
    poly = mask_to_polygon(mask)
    angleInDegrees = ring_angle(mask)
    alignedPoly = shapely.affinity.rotate(poly, -angleInDegrees )
    return(alignedPoly)
    
#measure polygon width
def ring_width(mask, central_perc = 0.5):
    part_to_remove = 0.5 - (central_perc/2)
    
    alignedPoly = align_polygon(mask)
    ## 1) Get part of the polygon corresponding to the central part of the ring 
    x,y = alignedPoly.exterior.xy
    x = np.asarray(x)
    y = np.asarray(y)
    x_min = np.ndarray.min(x)
    x_max = np.ndarray.max(x)
    x_range = x_max - x_min
    x_minB = x_min + (x_range * part_to_remove) # change percent excluded on the ends
    x_maxB = x_max - (x_range * part_to_remove) # change percent excluded on the ends
    y_centre = y[(x > x_minB) & (x < x_maxB)]
    x_centre = x[(x > x_minB) & (x < x_maxB)]
    
    x_int = x.astype(int)
    x_int_centre = x_centre.astype(int)
    x_unique = np.unique(x_int_centre)

    x_value = list()
    ring_widths = list()

    for i in x_unique:
        yboth = y[x_int == i]
        yup = yboth[yboth > statistics.mean(yboth)]
        ydown = yboth[yboth < statistics.mean(yboth)]
        y_dist = statistics.mean(yup) - statistics.mean(ydown)
        ring_widths.append(y_dist)
        x_value.append(i)

    #print(ring_widths)

    ring_wid = np.mean(ring_widths)
    width_sem = scipy.stats.sem(ring_widths)
    return(ring_wid, width_sem)

## Measure for all rings on the picture, may be i should transformit to take a picture as an input?
def measure_all_rings(masks):
    ring_widths_all = list()
    width_sem_all = list()
    ring_angle_all = list()
    
    for i in range(masks.shape[2]):
        w,sem = ring_width(masks[:,:,i])
        angle = ring_angle(masks[:,:,i])
        ring_widths_all.append(w)
        width_sem_all.append(sem)
        ring_angle_all.append(angle)
    
    return(ring_widths_all, width_sem_all, ring_angle_all)
        
    