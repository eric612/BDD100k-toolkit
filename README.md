# BDD100k toolkit

Convert bdd100k annotation to Coco or VOC format , also support driverable area 

1. Download bdd100k dataset and save at $bdd100k/
``` 
'bdd100k_drivable_maps.zip'
'bdd100k_images.zip'
'bdd100k_labels_release.zip' 
```
2. Do batch_split_annotation 
```
python batch_split_annotation.py
```
3. The generated train and val list will save at $bdd100k/ImageSets
