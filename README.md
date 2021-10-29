# BDD100k toolkit

Convert bdd100k annotation to Coco or VOC format , also support driverable area 

1. Download bdd100k dataset (necessary file: 'bdd100k_drivable_maps.zip','bdd100k_images.zip','bdd100k_labels_release.zip') and save at $bdd100k/
2.  
    ```
    python batch_split_annotation.py
    ```
    The generated train and val list will save at $bdd100k/ImageSets
