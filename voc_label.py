import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import numpy 
from openpyxl import Workbook
#sets=['trainval', 'test' , 'test_time_Day']
import xlsx_graph
classes = ["person", "rider", "car", "bus", "truck", "bike", "motor", "traffic light", "traffic sign", "train"]
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation( image_id,cls_array=classes):
    in_file = open('Annotations/%s.xml'%(image_id))
    #print('../xml/%s.xml'%(image_id))
    out_file = open('labels/%s.txt'%(image_id), 'w')
    #print('labels/%s.txt'%(image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    #cls_num = numpy.zeros(len(classes))
    #cls_num = [0,0,0,0,0,0,0,0]
    cls_num = list()
    for cls in cls_array:
        cls_num.append(0)
    #cls_num = zeros(cls_array.size())
    bbox=list()
    class_id=list()
    #print(cls_array)
    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in cls_array :
            #print(cls)
            continue
        #if int(difficult) == 1:      
        #    continue

        cls_id = cls_array.index(cls)
        #print(cls_id)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        cls_num[cls_id] = cls_num[cls_id]+1;

    return cls_num,bbox


def generate_yolo_label(sets):
    wd = getcwd()
    
    if not os.path.exists('labels/'):
        os.makedirs('labels/')
    if not os.path.exists('yolo/'):
        os.makedirs('yolo/')
    temp = open('bdd100k.names','r').readlines()
    cls_array = list()
    for l in temp :
        #print(l.strip('\n\r')) 
        cls_array.append(l.strip('\n\r'))
    for image_set in sets:
        #ws2['F5'] = 3.14
        print('\n%s dataset\n'%(image_set))
        image_ids = open('%s.txt'%(image_set)).read().strip().split()
        list_file = open('yolo/fisheye_%s.txt'%(image_set), 'w')
        #coor_file = open('yolo/coor_%s.csv'%(image_set), 'w')
        #cls_num_sum = numpy.zeros(len(classes))
        #cls_num_sum = [0,0,0,0,0,0,0,0]
        cls_num_sum = list()
        for cls in cls_array:
            cls_num_sum.append(0)
        x_y_sum = [0,0]
        count = 0
        for image_id in image_ids:
            filepath = os.path.join(wd,'JPEGImages/%s.jpg\n'%(image_id))
            list_file.write(filepath)
            #print('../jpg/%s.jpg\n'%(image_id))
            cls_num,bbox = convert_annotation(image_id,cls_array)
            for idx in range(0,len(cls_array)) :
                cls_num_sum[idx] = cls_num_sum[idx] + cls_num[idx]  
            
            #for n in range(0,len(bbox)):
            #    x_y_sum[0] += bbox[n][0]
            #    x_y_sum[1] += bbox[n][1]
            #    coor_file.write(str(bbox[n])[1:-1]+'\n')
            #    count = count + 1
        #x_y_sum[0] = x_y_sum[0]/count
        #x_y_sum[1] = x_y_sum[1]/count
        #print(x_y_sum)
        #print(cls_num)
        list_file.close()
        #coor_file.close()
        #print(cls_num_sum)
        sum = numpy.sum(cls_num_sum)
        #print(sum)
        print("\n")
        for idx in range(0,len(cls_array)) :
            cls_num_sum[idx] = cls_num_sum[idx]
            #ws1.cell(row=idx+1, column=1).value = cls_num_sum[idx]
            #ws2['A0'] = cls_num_sum[idx]
            print(cls_array[idx] + " : " + str(cls_num_sum[idx])+"\n")
        #xlsx_graph.draw_class_graph('data_statistics/%s'%image_set,cls_num_sum)
        