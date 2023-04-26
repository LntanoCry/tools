import xml.etree.ElementTree as ET  # 读取xml。
import os, cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def parse_rec(filename):
    if filename == 'E:\\Dataset\\detector\\last_ann\\Annotations\\30.xml':
        print(" 30.xml ")
    tree = ET.parse(filename)  # 解析读取xml函数
    objects = []
    img_dir = []
    for xml_name in tree.findall('filename'):
        img_path = os.path.join(pic_path, xml_name.text)
        img_dir.append(img_path)
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['pose'] = obj.find('pose').text
        obj_struct['truncated'] = float(obj.find('truncated').text)
        obj_struct['difficult'] = float(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [float(bbox.find('xmin').text),
                              float(bbox.find('ymin').text),
                              float(bbox.find('xmax').text),
                              float(bbox.find('ymax').text)]
        objects.append(obj_struct)

    return objects, img_dir


fontPath = "C:\Windows\Fonts\Consolas\consola.ttf"  # 字体路径

ann_path = r'E:\Dataset\detector\last_ann\Annotations'  # xml文件所在路径
pic_path = r'E:\Dataset\detector\image_all_jpg'  # 样本图片路径
label_img_path = r'E:\Dataset\detector\last_ann\mask'
if not os.path.exists(label_img_path):  # 判断是否存在文件夹如果不存在则创建为文件夹
    os.makedirs(label_img_path)
font = ImageFont.truetype(fontPath, 16)

for filename in os.listdir(ann_path):
    xml_path = os.path.join(ann_path, filename)
    objects, img_dir = parse_rec(xml_path)
    # print('img_dir:',img_dir)
    for img_path in img_dir:
        img = cv2.imread(img_path)
        (w, h, c) = img.shape
        # SIZE:PIL宽高，numpy.ndarray_img.size为 高x宽x通道数 的总个数，arry_img.shape为（高，宽，通道数）
        mask = np.zeros([h, w], dtype=np.uint8)
        # draw = ImageDraw.Draw(mask)
        for a in objects:
            xmin = int(a['bbox'][0])
            ymin = int(a['bbox'][1])
            xmax = int(a['bbox'][2])
            ymax = int(a['bbox'][3])
            label = a['name']
            SAVE = cv2.rectangle(mask, (xmin, ymin), (xmax, ymax), (255, 255, 255), -1)
            cv2.imwrite(label_img_path + '//' + os.path.basename(img_path), SAVE)  # 写入label_img
        if objects == []:
            cv2.imwrite(label_img_path + '//' + os.path.basename(img_path), mask)

# # 运行单个文件
# idnum = 5
# ann_path = 'data'+str(idnum)  # xml文件所在路径
# pic_path = r'D:\Research direction\data set\data'+str(idnum)  # 样本图片路径
# label_img_path = r'C:\Users\11046\Desktop\mask\Newdata'+str(idnum) # 输出GT路径
# if not os.path.exists(label_img_path):  # 判断是否存在文件夹如果不存在则创建为文件夹
#     os.makedirs(label_img_path)
# # font = ImageFont.truetype(fontPath, 16)
#
# for filename in os.listdir(ann_path):
#     xml_path = os.path.join(ann_path, filename)
#     objects, img_dir = parse_rec(xml_path)
#     # print('img_dir:',img_dir)
#     for img_path in img_dir:
#         img = cv2.imread(img_path)
#         (w, h, c) = img.shape  # SIZE:PIL宽高，numpy.ndarray_img.size为 高x宽x通道数 的总个数，arry_img.shape为（高，宽，通道数）
#         mask = np.zeros([h, w], dtype=np.uint8)
#         # draw = ImageDraw.Draw(mask)
#         for a in objects:
#             xmin = int(a['bbox'][0])
#             ymin = int(a['bbox'][1])
#             xmax = int(a['bbox'][2])
#             ymax = int(a['bbox'][3])
#             label = a['name']
#
#             SAVE = cv2.rectangle(mask, (xmin, ymin), (xmax, ymax), (255, 255, 255), -1)
#             cv2.imwrite(label_img_path + '//' + os.path.basename(img_path), SAVE)  # 写入label_img
