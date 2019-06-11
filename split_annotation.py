import argparse
from collections import OrderedDict
import json
import os
from pprint import pprint
import sys
sys.path.append(os.path.dirname(sys.path[0]))

from pycocotools.coco import COCO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Split whole json annotation to individual files.")
    parser.add_argument("annofile",
            help = "The file which contains all the annotations for a dataset in json format.")
    parser.add_argument("--out-dir", default = "",
            help = "The output directory where we store the annotation per image.")
    parser.add_argument("--imgset-file", default = "",
            help = "A file where we store all the image names of a dataset.")

    args = parser.parse_args()
    annofile = args.annofile
    if not os.path.exists(annofile):
        print "{} does not exist!".format(annofile)
        sys.exit()

    out_dir = args.out_dir
    if out_dir:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    imgset_file = args.imgset_file
    if imgset_file:
        imgset_dir = os.path.dirname(imgset_file)
        if not os.path.exists(imgset_dir):
            os.makedirs(imgset_dir)

    # initialize COCO api.
    coco = COCO(annofile)

    img_ids = coco.getImgIds()
    img_names = []
    for img_id in img_ids:
        # get image info
        img = coco.loadImgs(img_id)
        file_name = img[0]["file_name"]
        name = os.path.splitext(file_name)[0]
        if out_dir:
            # get annotation info
            anno_ids = coco.getAnnIds(imgIds=img_id, iscrowd=None)
            anno = coco.loadAnns(anno_ids)
            # save annotation to file
            img_anno = dict()
            img_anno["image"] = img[0]
            img_anno["annotation"] = anno
            anno_file = "{}/{}.json".format(out_dir, name)
            with open(anno_file, "w") as f:
                json.dump(img_anno, f, sort_keys=True, indent=2, ensure_ascii=False)
        if imgset_file:
            img_names.append(name)
    if img_names:
        img_names.sort()
        with open(imgset_file, "w") as f:
            f.write("\n".join(img_names))
