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
    # if os.path.isfile(dst_json_filename):
    #     print('File already converted to {}'.format(dst_json_filename))
    #     return

    print('Converting csv file {} to {}'.format(src_csv_filename, dst_json_filename))

    # Parse the csv file assuming that it contains the annotation data
    #  in a valid format.
    src_as_json, image_filenames = datasetutil.annotations_from_csv(src_csv_filename)

    fileutil.write_json(dst_json_filename, src_as_json)

    return image_filenames


def replace_annotations(original, modified):
    original['annotations'] = modified
    return original


def extract_images(original, filenames):
    imgs = original['images']
    imgs_subset = []
    for img in imgs:
        if img['file_name'] in filenames:
            imgs_subset.append(img)
    original['images'] = imgs_subset

    assert len(filenames) == len(original['images'])

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
    coco_root = '/home/ubuntu/data/yamlab/MSCOCO'
    coco_ann = os.path.join(coco_root, 'annotations')
    coco_train_json = os.path.join(coco_ann, 'instances_train2014.json')
    coco_val_json = os.path.join(coco_ann, 'instances_val2014.json')

    # 1. Convert the Yamlab CSV annotations to JSON files
    train_img_filenames = convert_annotation_file(yl_train_csv, yl_train_dst)
    val_img_filenames = convert_annotation_file(yl_val_csv, yl_val_dst)

    # 2. Load the Yamlab JSON files
    yl_train = fileutil.read_json(yl_train_dst)
    yl_val = fileutil.read_json(yl_val_dst)

    # 3. Load the MSCOCO JSON files
    coco_train = fileutil.read_json(coco_train_json)
    coco_val = fileutil.read_json(coco_val_json)

    # 4. Replace the MSCOCO JSON annotations with the Yamlab annotations
    replaced_train = replace_annotations(coco_train, yl_train)
    replaced_val = replace_annotations(coco_val, yl_val)

    # 5. Replace the MSCOCO JSON images in the annotations with the images
    # that we want to use.
    replaced_train = extract_images(replaced_train, train_img_filenames)
    replaced_val = extract_images(replaced_val, val_img_filenames)

    # 6. Write the new MSCOCO JSON annotations to disk
    fileutil.write_json(coco_train_json, replaced_train)
    fileutil.write_json(coco_val_json, replaced_val)

    # 7. Extract only the images that we want to use from the original MSCOCO
    """
    mscoco_val_img = os.path.join(coco_root, 'val2014')
    yamlab_val_img = os.path.join(coco_root, 'val2014_yamlab')

    for val_img in val_img_filenames:
        mscoco_val_img_filename = os.path.join(mscoco_val_img, val_img)
        yamlab_val_img_filename = os.path.join(yamlab_val_img, val_img)
        fileutil.copy_file(src=mscoco_val_img_filename, dst=yamlab_val_img_filename)

    mscoco_train_img = os.path.join(coco_root, 'train2014')
    yamlab_train_img = os.path.join(coco_root, 'train2014_yamlab')

    for train_img in train_img_filenames:
        mscoco_train_img_filename = os.path.join(mscoco_train_img, train_img)
        yamlab_train_img_filename = os.path.join(yamlab_train_img, train_img)
        fileutil.copy_file(src=mscoco_train_img_filename, dst=yamlab_train_img_filename)
        i += 1
        print(i)
    """
