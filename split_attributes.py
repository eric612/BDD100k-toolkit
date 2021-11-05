from collections import OrderedDict
import json
import os

def split_attributes(labels_images,bdd100k_label_filepath):
    for name in labels_images:
        filepath = os.path.join(bdd100k_label_filepath,name)
        anno_name = name.split("_")[-1]
        anno_name,_ = os.path.splitext(anno_name)
        path = "classfication/{}/".format(anno_name)
        if not os.path.isdir(path):
            os.makedirs(path)        
        with open(filepath) as f:
            labels = json.load(f)
            for label in labels:            
                id, file_extension = os.path.splitext(label["name"])            
                #print(anno_name)            
                filename = "classfication/{}/{}.json".format(anno_name,id)
                with open(filename, 'w') as f:
                    json.dump(label["attributes"],f, indent=4)
            #print(labels[0]["name"],labels[0]["attributes"])