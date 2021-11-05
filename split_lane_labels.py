import argparse
from collections import OrderedDict
import json
import os
from pprint import pprint
import sys
import cv2
import numpy as np
sys.path.append(os.path.dirname(sys.path[0]))
               
def split_lane_labels(set_names,filepath):
    for set in set_names:
        label_file = "{}/lane_{}.json".format(filepath,set)
        with open(label_file, 'r') as f:
            data=json.load(f)
        path = "lane_labels/{}/".format(set)
        if not os.path.isdir(path):
            os.makedirs(path)
        for index,label in enumerate(data):
            id, file_extension = os.path.splitext(label["name"])
            filename = "lane_labels/{}/{}.json".format(set,id)
            #print(filename)
            with open(filename, 'w') as f:
                json.dump(label,f, indent=4)
  
     
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Split whole json lane labels to individual files.")
    parser.add_argument('-p', '--path', dest='path', default='bdd100k/labels/lane/polygons', type=str, metavar='PATH',help='path to label file')
    parser.add_argument('-s', '--sets', dest='sets', nargs='+', default=['train','val'], help='set names')
    #parser.add_argument('--action', default='split', const='split', nargs='?', choices=['split', 'show'])
    args = parser.parse_args()
    split_lane_labels(args.sets,args.path)

