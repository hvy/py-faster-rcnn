import os
import csv
import json
import shutil


def read_csv(filename, delimiter=','):
    """Return a 2-dimensional list where each row represents a row in the
    csv file and each column represents each value in the row.
    """
    rows = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            rows.append(row)
    return rows


def read_json(filename):
    """Read JSON file as a dict.
    """
    json_as_dict = None
    with open(filename, 'rb') as jsonfile:
        json_as_dict = json.load(jsonfile)
    return json_as_dict


def write_json(filename, data, indent=None):
    """Write dict as JSON.
    Args:
        indent (int): Indentation used for pretty printing.
    """
    with open(filename, 'w') as jsonfile:
        if indent is None:
            json.dump(data, jsonfile, indent=indent)
        else:
            json.dump(data, jsonfile)


def copy_file(src, dst):
    """
    Args:
        src (str): Source file name.
        dst (str): Destination file name.
    """
    shutil.copyfile(src, dst)


def filenames_in(dirname):
    filenames = []
    for filename in os.listdir(dirname):
        filenames.append(filename)
    return filenames


if __name__ == '__main__':
    print('Loading data...')
    # val_data_dict = read_json('/home/ubuntu/data/MSCOCO/annotations/instances_val2014.json')
    val_data_dict = read_json('./new_val_data.json')
    print('Done loading data')

    annotations = val_data_dict['annotations']
    # val_data_dict['annotations'] = ['hey']

    write_json('new_val_data.json', val_data_dict)

    print('Number of annotations: {}'.format(len(annotations)))

