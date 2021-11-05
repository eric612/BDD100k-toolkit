# BDD100k toolkit

Convert bdd100k annotation to Coco or VOC format , also support driverable area 

## Usage
1. Download bdd100k dataset and save at $bdd100k/
``` 
'bdd100k_drivable_maps.zip'
'bdd100k_images.zip'
'bdd100k_labels_release.zip' 
'bdd100k_lane_labels_trainval.zip'
```
2. Do batch_split_annotation 
```
python batch_split_annotation.py
```
3. The output yaml file will save at $bdd100k/bdd100k.yaml , which can be used in my project [Mobilenet-YOLO-Pytorch](https://github.com/eric612/Mobilenet-YOLO-Pytorch) 


## Show labels

```
show_images.sh
```