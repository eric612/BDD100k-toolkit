# BDD100k toolkit

1. Download bdd100k dataset (images,json and driverable map) and save at $bdd100k
2. Use this [repo](https://github.com/ucbdrive/bdd-data) to convert json to coco format
3. Use coco2voc.py to convert format to pascal voc format and save at $bdd100k
4. Python create_list.py [$bdd100k] train