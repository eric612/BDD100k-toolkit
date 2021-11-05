import argparse
from collections import OrderedDict
import json
import os
from pprint import pprint
import sys
import cv2
import numpy as np
#from split_lane_labels import parse_lane_label
sys.path.append(os.path.dirname(sys.path[0]))
CLASSES = (
           'person', 'rider', 'car', 'bus',
           'truck', 'bike', 'motor', 'traffic light', 'traffic sign',
           'train ')
color_array = [(0,0,255),(255,0,0)]
lane_Direction = ['parallel','vertical']      
Lane_Categories = ['crosswalk','double other','double white','double yellow','road curb','single other','single white','single yellow','background'] 

def parse_file_lists(set_names,filepath):

    my_dict = {"id":[],"image":[],"anno":[],"lane_label":[],"attr":[],"drivable_map":[],"lane_color":[]};
    for set in set_names:
        label_file = "{}/lane_{}.json".format(filepath,set)
        with open(label_file, 'r') as f:
            data=json.load(f)
        for index,label in enumerate(data):
            id, file_extension = os.path.splitext(label["name"])
            lane_label = "lane_labels/{}/{}.json".format(set,id)           
            image = "images/{}/{}.jpg".format(set,id)
            anno = "annotations/{}/{}.json".format(set,id)
            attr = "classfication/{}/{}.json".format(set,id)
            drivable_map = "drivable_maps/labels/{}/{}_drivable_id.png".format(set,id)
            lane_color = "bdd100k/labels/lane/colormaps/{}/{}.png".format(set,id)
            if os.path.exists(lane_label) and os.path.exists(image) and os.path.exists(anno):
                my_dict["id"].append(id)
                my_dict["image"].append(image)
                my_dict["anno"].append(anno)
                my_dict["lane_label"].append(lane_label)                
                if os.path.exists(attr) and os.path.exists(drivable_map) and os.path.exists(lane_color):
                    my_dict["attr"].append(attr)
                    my_dict["drivable_map"].append(drivable_map)
                    my_dict["lane_color"].append(lane_color)
    return my_dict
               
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
def parse_annotation(annotation_path):
    filename, file_extension = os.path.splitext(annotation_path)
    boxes = list()
    labels = list()       
    difficulties = list()   
    if file_extension == '.json':
        with open(annotation_path, 'r') as f:
            data=json.load(f)        
        width = int(data['image']['width'])-1
        height = int(data['image']['height'])-1
        object_number = len(data['annotation'])
        for j in range(object_number):
            class_id = int(data['annotation'][j]['category_id'])-1
            category_name = CLASSES[class_id]
            if category_name in CLASSES:
                new_class_id = CLASSES.index(category_name)
                xmin = int(float(data['annotation'][j]['bbox'][0])+0.5)            
                ymin = int(float(data['annotation'][j]['bbox'][1])+0.5)
                if xmin<0:
                    xmin = 0
                if ymin<0:
                    ymin = 0                    
                xmax = int(float(data['annotation'][j]['bbox'][0])+float(data['annotation'][j]['bbox'][2])+0.5)
                ymax = int(float(data['annotation'][j]['bbox'][1])+float(data['annotation'][j]['bbox'][3])+0.5)
                if xmax>width:
                    xmax = width
                if ymax>height:
                    ymax = height    
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(new_class_id)
                difficulties.append(0)
                #print(xmin,ymin,class_id)
        return boxes, labels, difficulties   
def draw_image(cv_img,laneTypes=None,laneDirection=None,lane=None,boxes=None,labels=None,seg_id = False,attributes = False,lane_color_map = False): 
    #print(seg_id)
    #seg_id = (np.asarray(seg_id)!=0)*0.5

    #cv_img = cv_img*seg_id 
    cv_img[:,:,2] = (seg_id[:,:,2]==1)*127 + cv_img[:,:,2]*(seg_id[:,:,2]==0) + cv_img[:,:,2]*(seg_id[:,:,2]==1)*0.5
    #cv_img[:,:,1] = cv_img[:,:,1]*(seg_id[:,:,1]==0) + cv_img[:,:,1]*(seg_id[:,:,1]==1)*0.5
    #cv_img[:,:,0] = cv_img[:,:,0]*(seg_id[:,:,0]==0) + cv_img[:,:,0]*(seg_id[:,:,0]==1)*0.5
    cv_img[:,:,0] = (seg_id[:,:,0]==2)*127 + cv_img[:,:,0]*(seg_id[:,:,0]==0) + cv_img[:,:,0]*(seg_id[:,:,0]==2)*0.5
    #cv_img[:,:,1] = cv_img[:,:,1]*(seg_id[:,:,1]==0) + cv_img[:,:,1]*(seg_id[:,:,1]==2)*0.5
    #cv_img[:,:,2] = cv_img[:,:,2]*(seg_id[:,:,2]==0) + cv_img[:,:,2]*(seg_id[:,:,2]==2)*0.5
    mask = (lane_color_map!=0)
    cv_img[mask] = lane_color_map[mask]
    for idx,box in enumerate(boxes) : 
        cv2.rectangle(cv_img, (box[0],box[1]), (box[2],box[3]), (0,255,0), 2)
        text=CLASSES[int(labels[idx])].lower()
        cv2.putText(cv_img, text, (box[0],box[1]-5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 255), 1, cv2.LINE_AA)
    #print(attributes["weather"])
    '''
    for line,laneD in zip(lane,laneDirection): 
        #print(line)
        color = color_array[lane_Direction.index(laneD)]
        #cv2.polylines(cv_img, line, False, color, 2);      
        
        for idx,pt in enumerate(line):
            if idx==0:
                x1,y1 = line[0]
                continue            
            x2,y2 = line[idx]
            cv2.line(cv_img, (int(x1),int(y1)), (int(x2),int(y2)), color, 2)    
            x1 = x2
            y1 = y2
    '''    
        
    cv2.putText(cv_img, 'weather : '+str(attributes["weather"]), (10,680), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(cv_img, 'scene : '+str(attributes["scene"]), (350,680), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(cv_img, 'timeofday : '+str(attributes["timeofday"]), (700,680), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2, cv2.LINE_AA)
    return cv_img
    '''
    if laneTypes is not None:
        if 'road curb' in LaneCategories:
            color = color_array[0]
        else:
            color = color_array[1]
    else:
        color = color_array[0]
    '''
def parse_lane_label(lane_label_path):    
    filename, file_extension = os.path.splitext(lane_label_path)
    lane_label = list()
    if file_extension == '.json':
        with open(lane_label_path, 'r') as f:
            data=json.load(f)
            poly2d = list()
            laneTypes = list()
            laneDirection = list()
            if "labels" in data:
                labels = data["labels"]               
                for item in labels: 
                    
                    for coor in item['poly2d']:
                        #print(len(coor['vertices']))
                        poly2d.append(coor['vertices'])
                    laneDirection.append(item['attributes']['laneDirection'])
                    laneTypes.append(item['attributes']['laneTypes'])
            return (poly2d,laneTypes,laneDirection)

    else:
        return None,None    
def parse_attributes(attributes_path):
    with open(attributes_path, 'r') as f:
        data=json.load(f) 
    return data
def show_images(set_names,filepath):
    lists = parse_file_lists(set_names,filepath)
    
    #print(lists["id"][idx],lists["image"][idx],lists["anno"][idx],lists["lane_label"][idx])
    #original_image = Image.open(lists["image"][0], mode='r')
    #original_image = original_image.convert('RGB')
    #annotated_image_ = cv2.cvtColor(np.asarray(original_image), cv2.COLOR_RGB2BGR)
    for idx in range(len(lists["image"])):
        annotated_image = cv2.imread(lists["image"][idx])
        height,width = annotated_image.shape[0],annotated_image.shape[1]
        boxes, labels, difficulties = parse_annotation(lists["anno"][idx])
        lane,laneTypes,laneDirection = parse_lane_label(lists["lane_label"][idx])
        attr = parse_attributes(lists["attr"][idx])
        #print(lists["lane_color"][idx])
        d_map = cv2.imread(lists["drivable_map"][idx])
        lane_color_map = cv2.imread(lists["lane_color"][idx])
        annotated_image = draw_image(annotated_image,laneTypes,laneDirection,lane,boxes,labels,seg_id=d_map,attributes=attr,lane_color_map = lane_color_map)
        #print(boxes)
        cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', width, height)
        cv2.imshow('frame',annotated_image)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    return
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Split whole json lane labels to individual files.")
    parser.add_argument('-p', '--path', dest='path', default='bdd100k/labels/lane/polygons', type=str, metavar='PATH',help='path to label file')
    parser.add_argument('-s', '--sets', dest='sets', nargs='+', default=['train','val'], help='set names')
    #parser.add_argument('--action', default='split', const='split', nargs='?', choices=['split', 'show'])
    args = parser.parse_args()
    #if args.action == 'split':
    #    split_lane_labels(args.sets,args.path)
    #else:
    show_images(args.sets,args.path)
