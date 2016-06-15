import os
import datasetutil

if __name__ == '__main__':
    yl_root = '/home/ubuntu/data/yamlab/annotations'
    yl_train_csv = os.path.join(yl_root, 'train2014/any_tagInfor.csv')
    yl_val_csv = os.path.join(yl_root, 'val2014/any_tagInfor.csv')

    train_anns, _ = datasetutil.annotations_from_csv(yl_train_csv)
    val_anns, _ = datasetutil.annotations_from_csv(yl_val_csv)

    train_anns_count = [0] * 4
    val_anns_count = [0] * 4

    for ann in train_anns:
        train_anns_count[ann['category_id'] - 1] += 1

    for ann in val_anns:
        val_anns_count[ann['category_id'] - 1] += 1

    print train_anns_count
    print val_anns_count
