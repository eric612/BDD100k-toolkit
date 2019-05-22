# BDD100k toolkit

Convert bdd100k dataset to lmdb , for train [object detection + segmentation models](https://github.com/eric612/MobileNet-YOLO)

1. Download bdd100k dataset (images,json and driverable map) and save at $bdd100k
2. Use this [repo](https://github.com/ucbdrive/bdd-data) to convert json to coco format
3. Use coco2voc.py to convert format to pascal voc and save at $bdd100k/train
4. Python create_list.py [$bdd100k/train] train
