import os
import json
from utils import datasetutil
from utils import fileutil


# Example: How to obtain ta filepath relative to a file
#
# root_path = os.path.dirname(os.path.realpath(__file__))
# train2014_path = os.path.join(root_path, 'data/annotations/train2014/any_tagInfor.csv')
# val2014_path = os.path.join(root_path, 'data/annotations/val2014/any_tagInfor.csv')


def convert_annotation_file(src_csv_filename, dst_json_filename):
    if os.path.isfile(dst_json_filename):
        print('File already converted to {}'.format(dst_json_filename))
        return

    print('Converting csv file {} to {}'.format(src_csv_filename, dst_json_filename))

    # Parse the csv file assuming that it contains the annotation data
    #  in a valid format.
    src_as_json = datasetutil.annotations_from_csv(src_csv_filename)

    fileutil.write_json(dst_json_filename, src_as_json)


def replace_annotations(original, modified):
    original['annotations'] = modified
    return original


if __name__ == '__main__':
    print 'Running setup...'

    # Yamlab file paths
    yl_root = '/home/ubuntu/data/yamlab/annotations'
    yl_train_csv = os.path.join(yl_root, 'train2014/any_tagInfor.csv')
    yl_train_dst = os.path.join(yl_root, 'train2014/train_annotations.json')
    yl_val_csv = os.path.join(yl_root, 'val2014/any_tagInfor.csv')
    yl_val_dst = os.path.join(yl_root, 'val2014/val_annotations.json')

    # MSCOCO file paths
    coco_root = '/home/ubuntu/data/yamlab/MSCOCO/annotations'
    coco_train_json = os.path.join(coco_root, 'instances_train2014.json')
    coco_val_json = os.path.join(coco_root, 'instances_val2014.json')

    # 1. Convert the Yamlab CSV annotations to JSON files
    convert_annotation_file(yl_train_csv, yl_train_dst)
    convert_annotation_file(yl_val_csv, yl_val_dst)

    # 2. Load the Yamlab JSON files
    yl_train = fileutil.read_json(yl_train_dst)
    yl_val = fileutil.read_json(yl_val_dst)

    # 3. Load the MSCOCO JSON files
    coco_train = fileutil.read_json(coco_train_json)
    coco_val = fileutil.read_json(coco_val_json)

    # 4. Replace the MSCOCO JSON annotations with the Yamlab annotations
    replaced_train = replace_annotations(coco_train, yl_train)
    replaced_val = replace_annotations(coco_val, yl_val)

    # 5. Write the new MSCOCO JSON annotations to disk
    fileutil.write_json(coco_train_json, replaced_train)
    fileutil.write_json(coco_val_json, replaced_val)
