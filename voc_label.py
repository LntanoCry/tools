# -*- coding: utf-8 -*-
# transform YOLO type to txt:
# each line: [class,x,y,w,h]
import xml.etree.ElementTree as ET
import os
from os import getcwd

sets = ['train', 'val', 'test']
classes = ["head", "all"]   # Change to your own classes
abs_path = os.getcwd()
print(abs_path)

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h

def convert_annotation(image_id):
    # path to annotation file with xml type 
    in_file = open('/root/autodl-tmp/inf_voc_fuhe/VOC2007/Annotations/%s.xml' % (image_id), encoding='UTF-8')
    # path to outputflie with annotations in txt type
    out_file = open('/root/autodl-tmp/inf_voc_fuhe/VOC2007/ann_txt/%s.txt' % (image_id), 'w')  # Change here
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = 0
        if  obj.find('Difficult'):
            difficult = obj.find('Difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    out_file.close()  # Close the file

wd = getcwd()
for image_set in sets:
    # Path to train.txt val.txt and test.txt
    image_ids = open('/root/autodl-tmp/inf_voc_fuhe/VOC2007/ImageSets/Main/%s.txt' % (image_set)).read().strip().split()
    for image_id in image_ids:
        convert_annotation(image_id)
