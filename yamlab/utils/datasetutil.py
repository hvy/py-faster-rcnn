import fileutil


def filename_to_id(filename):
    # TODO: Use regexp (re module) instead of splits
    id_str = filename.split('.')[0].split('_')[2]
    id_int = int(id_str)
    return id_int


def row_to_annotations(row):
    """Take a list of values in a csv file row and return a list of annotations.
    """
    image_filename = row.pop(0)
    image_id = filename_to_id(image_filename)

    n_props = 6  # annotation id, category id, upper left x, upper left y, bottom right x, bottom right y
    assert len(row) % n_props == 0
    n_anns = len(row) / n_props

    annotations = []

    for ann_i in range(n_anns):
        offset = ann_i * n_props
        subrow = row[offset:offset + n_props]
        subrow = map(int, subrow)

        ann_id = subrow[0]
        category_id = subrow[1]
        upper_left_x = subrow[2]
        upper_left_y = subrow[3]
        bottom_right_x = subrow[4]
        bottom_right_y = subrow[5]

        assert (isinstance(upper_left_x, int) and upper_left_x >= 0)
        assert (isinstance(upper_left_y, int) and upper_left_y >= 0)
        assert (isinstance(bottom_right_x, int) and bottom_right_x > 0)
        assert (isinstance(bottom_right_y, int) and bottom_right_y > 0)

        assert bottom_right_x > upper_left_x
        assert bottom_right_y > upper_left_y

        width = bottom_right_x - upper_left_x
        height = bottom_right_y - upper_left_y
        area = width * height

        assert area > 0

        bbox = [upper_left_x, upper_left_y, width, height]

        # TODO: Add 'segmentation' to each annotation, if necessary
        # See format here http://mscoco.org/dataset/#download
        annotation = {'id': ann_id, 'image_id': image_id, 'category_id': category_id, 'area': area, 'bbox': bbox, 'iscrowd': 0}

        annotations.append(annotation)

    return annotations, image_filename


def annotations_from_csv(filename):
    # Read the csv file
    csvfile = fileutil.read_csv(filename)

    # Process the csv file
    image_filenames = []
    annotations = []
    for row in csvfile:
        trailing = row.pop()  # Remove last value from each row caused by trailing comma
        assert trailing == ''

        # Parse the row to an annotation
        annotations_in_row, image_filename = row_to_annotations(row)
        annotations += annotations_in_row
        image_filenames.append(image_filename)

    print 'Total annotations: {}'.format(len(annotations))

    return annotations, image_filenames
