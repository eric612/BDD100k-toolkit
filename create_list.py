import os 
from shutil import copyfile
import shutil
import cv2
import random
import voc_label
import xml.etree.ElementTree as ET
import openpyxl
import numpy
import sys
from openpyxl import Workbook


def collect_data(path,list_name) :

    im_names = list()
    if not os.path.exists('JPEGImages'):
        os.makedirs('JPEGImages')
    if not os.path.exists('Annotations'):
        os.makedirs('Annotations')
    if not os.path.exists('ImageSets//Main'):
        os.makedirs('ImageSets//Main')
    if not os.path.exists('data_statistics/'):
        os.makedirs('data_statistics/')
    count = 0
    cwd  = os.getcwd()
    path  = os.path.join(os.getcwd() , path)
    jpg_path  = "JPEGImages//"
    xml_path  = "Annotations//"
    png_path  = "Annotations//"
    ImageSets_path  = "ImageSets//Main//"
    xml_names = list()
    jpg_paths = list()
    xml_paths = list()
    png_paths = list()
    count = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(('.jpg')) :
                filepath = os.path.join(root,filename)
                copyfile(filepath,jpg_path+filename.replace(' ', ''))   
                filepath = jpg_path+filename.replace(' ', '')
                jpg_paths.append(os.path.join(cwd,filepath))
                #print(os.path.join(cwd,filepath))
                #print(filename[0:len(filename)-4])
                #if filename[0:len(filename)-4] in test_fixed :
                #    copyfile(filepath,jpg_path2+filename.replace(' ', ''))  
                #    print(filename[0:len(filename)-4])
            if filename.endswith(('.png')) :
                filepath = os.path.join(root,filename)
                copyfile(filepath,png_path+filename.replace('seg_', '').replace(' ', ''))   
                filepath = png_path+filename.replace('seg_', '').replace(' ', '')
                png_paths.append(os.path.join(cwd,filepath))
                #print(os.path.join(cwd,filepath))
                #print(filename[0:len(filename)-4])
                #if filename[0:len(filename)-4] in test_fixed :
                #    copyfile(filepath,jpg_path2+filename.replace(' ', ''))  
                #    print(filename[0:len(filename)-4])
            if filename.endswith(('.xml')) :
                filepath = os.path.join(root,filename)
                newFilename = filename.replace(' ', '')
                copyfile(filepath,xml_path+newFilename)
                #print(filename[0:len(filename)-4])
                #print("renaming " + xml_path+filename.replace(' ', ''))
                xml_names.append(os.path.splitext(filename.replace(' ', ''))[0])
                #print(filepath)
                filepath = xml_path+newFilename
                xml_paths.append(os.path.join(cwd,filepath))
                count = count + 1
    random.shuffle(xml_names)

    text_file1 = open("%s.txt"%list_name, "w")
    for xml_name in xml_names:
        text_file1.write("%s\n" % xml_name)
    text_file1.close()
    
    text_file1 = open("%s_jpg.txt"%list_name, "w")
    text_file2 = open("%s_xml.txt"%list_name, "w")
    for jpg_path in jpg_paths:
        text_file1.write("%s\n" % jpg_path)
    for xml_path in xml_paths:
        text_file2.write("%s\n" % xml_path)
    text_file1.close()
    text_file2.close()
    sets_names = list()
    sets_names.append(list_name)
    voc_label.generate_yolo_label(sets_names)
    shutil.move("%s.txt"%list_name,ImageSets_path+"%s.txt"%list_name)

if __name__ == '__main__':
    collect_data(sys.argv[1],sys.argv[2]) 