# BDD100k toolkit

Convert bdd100k dataset to lmdb , for train [object detection + segmentation models](https://github.com/eric612/MobileNet-YOLO)

1. Download bdd100k dataset (images,json and driverable map) and save at $bdd100k , copy driverable maps and images into subfolder $bdd100k/train
2. Use this [repo](https://github.com/ucbdrive/bdd-data) to convert json to coco format
3. Use coco2voc.py to convert format to pascal voc and save at $bdd100k/train , or you can download my generated [xml file](https://drive.google.com/open?id=1hqLh24jZqk2Ih-PMccrldHxjzBLAQGjr) , the file tree will like below 

![alt](example.png)

4. cd folder [$bdd100k] 
```
Python create_list.py train train
```
