import os
import subprocess
import sys
import zipfile
import shutil
import yaml
import json
from split_attributes import split_attributes
HOMEDIR = os.path.expanduser("/media/eric")
CURDIR = os.path.dirname(os.path.realpath(__file__))
python_cmd = "python3"
do_coco2voc = True
do_split_attributes = True
### Modify the address and parameters accordingly ###
# If true, redo the whole thing.
redo = True
# The root directory which stores the coco images, annotations, etc.
coco_data_dir = "{}/Data/bdd100k".format(HOMEDIR)
# The sets that we want to split. These can be downloaded at: http://mscoco.org
# Unzip all the files after download.
anno_sets = ["bdd100k_labels_images_det_coco_train", "bdd100k_labels_images_det_coco_val"]
# These are the sets that used in ION by Sean Bell and Ross Girshick.
# These can be downloaded at: https://github.com/rbgirshick/py-faster-rcnn/tree/master/data
# Unzip all the files after download. And move them to annotations/ directory.
# anno_sets = anno_sets + ["instances_minival2014", "instances_valminusminival2014"]
# The directory which contains the full annotation files for each set.
anno_dir = "{}/json".format(coco_data_dir)
# The root directory which stores the annotation for each image for each set.
out_anno_dir = "{}/annotations".format(coco_data_dir)
# The directory which stores the imageset information for each set.
imgset_dir = "{}/ImageSets".format(coco_data_dir)
bdd100k_drivable_map_file = '{}/bdd100k_drivable_maps.zip'.format(CURDIR)
bdd100k_images_file = '{}/bdd100k_images.zip'.format(CURDIR)
bdd100k_labels_release_file = '{}/bdd100k_labels_release.zip'.format(CURDIR)
zip_files = [bdd100k_drivable_map_file,bdd100k_images_file,bdd100k_labels_release_file]
bdd100k_label_filepath = '{}/bdd100k/labels/'.format(coco_data_dir)
labels_images = ['bdd100k_labels_images_train.json','bdd100k_labels_images_val.json']

def batch_split_annotation():
    
    
    if not os.path.exists('template.yaml'):
        print('not find template.yaml')
        return
    with open('template.yaml', 'r') as f:
        bdd100k_yaml = yaml.load(f, Loader=yaml.Loader)

        
        for file in zip_files:
            if os.path.isfile(file):
                print('unzip ... ' , file)
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(CURDIR)
            else:
              print('not find {}'.format(file))   
        
        if not os.path.isdir(anno_dir):
            os.mkdir(anno_dir)
        if do_split_attributes:
            split_attributes(labels_images,bdd100k_label_filepath)
        cmd = "{} {}/bdd2coco.py -l={} -s={}" \
                .format(python_cmd,CURDIR, bdd100k_label_filepath, anno_dir)
        print (cmd)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print (output)            
        
        ### Process each set ###
        for i in range(0, len(anno_sets)):
            anno_set = anno_sets[i]
            anno_file = "{}/{}.json".format(anno_dir, anno_set)

            if not os.path.exists(anno_file):
                print ("{} does not exist".format(anno_file))
                continue
            anno_name = anno_set.split("_")[-1]
            out_dir = "{}/{}".format(out_anno_dir, anno_name)
            imgset_file = "{}/{}.txt".format(imgset_dir, anno_name)
            if anno_name in "train":
                bdd100k_yaml["trainval_dataset_path"]["annos"].append(out_dir)
            if anno_name in ["test","val"]:
                bdd100k_yaml["test_dataset_path"]["annos"].append(out_dir)
            if redo or not os.path.exists(out_dir):
                cmd = "{} {}/split_annotation.py --out-dir={} --imgset-file={} {}" \
                        .format(python_cmd,CURDIR, out_dir, imgset_file, anno_file)
                print (cmd)
                process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
                output = process.communicate()[0]
                print (output)
                
        if do_coco2voc:
            for i in range(0, len(anno_sets)):
                anno_set = anno_sets[i]
                anno_name = anno_set.split("_")[-1]
                input_dir = "{}/{}".format(out_anno_dir, anno_name)
                save_dir = "{}/xml/{}".format(coco_data_dir, anno_name)
                #print(anno_name,out_dir)
                cmd = "{} {}/coco2voc.py --input_dir={} --save_path={}" \
                        .format(python_cmd,CURDIR,input_dir,save_dir)
                print (cmd)
                process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
                output = process.communicate()[0]
                print (output)

        

        
        original = '{}/bdd100k/drivable_maps'.format(CURDIR)
        target = '{}/drivable_maps'.format(CURDIR)
      
        shutil.move(original,target)
        target = '{}/drivable_maps/labels/train/'.format(CURDIR)
        bdd100k_yaml["trainval_dataset_path"]["segs"].append(target)
        target = '{}/drivable_maps/labels/val/'.format(CURDIR)
        bdd100k_yaml["test_dataset_path"]["segs"].append(target)
        
        original = '{}/bdd100k/images/100k/train'.format(CURDIR)
        target = '{}/images/train'.format(CURDIR)
        bdd100k_yaml["trainval_dataset_path"]["imgs"].append(target)
        shutil.move(original,target)

        original = '{}/bdd100k/images/100k/val'.format(CURDIR)
        target = '{}/images/val'.format(CURDIR)
        bdd100k_yaml["test_dataset_path"]["imgs"].append(target)
        shutil.move(original,target)
        
        target = '{}/ImageSets/train.txt'.format(CURDIR)
        bdd100k_yaml["trainval_dataset_path"]["lists"].append(target)
        
        target = '{}/ImageSets/val.txt'.format(CURDIR)
        bdd100k_yaml["test_dataset_path"]["lists"].append(target)
        
        rm_list = ['bdd100k','json']
        for l in rm_list:
            original = '{}/{}/'.format(CURDIR,l)
            shutil.rmtree(original)
        
        with open('bdd100k.yaml', 'w') as dest:
            yaml.dump(bdd100k_yaml,dest)    
    

if __name__ == '__main__':
    batch_split_annotation()