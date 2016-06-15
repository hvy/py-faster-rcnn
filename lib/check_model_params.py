import caffe


if __name__ == '__main__':
    print 'Running...'

    model_file = '/home/ubuntu/code/forked/py-faster-rcnn/output/faster_rcnn_end2end/coco_2014_train/vgg16_faster_rcnn_iter_5000.caffemodel'
    proto_file = '/home/ubuntu/code/forked/py-faster-rcnn/models/coco/VGG16/faster_rcnn_end2end/test.prototxt'

    net = caffe.Net(proto_file, model_file, caffe.TEST)


    for name, param in net.params.iteritems():
        print name, param[0].data.shape, param[1].data.shape


