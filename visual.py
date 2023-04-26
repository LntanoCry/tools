#  可视化TXT文件中的boxes到图片上
import json
import shutil
import cv2

def select(txt_path, outpath, image_path):
    with open(txt_path, 'r') as file:
        lines = file.readlines() 
    for line in lines:
        line = line.split()
        img_id = line[0]
        im_path = image_path + "/" + img_id
        img = cv2.imread(im_path)
        
        ann = line[1]
        ann = ann.split(',')
        x, y, w, h = float(ann[0]), float(ann[1]), float(ann[2]), float(ann[3])
        x2, y2 = x + w, y - h
        # object_name = annos[j][""]
        # 将bbox转换为int,会有一点误差
        img = cv2.rectangle(img, (int(x), int(y)), (int(x2), int(y2)), (255, 0, 0), thickness=2)
        img_name = outpath + "/" + img_id
        cv2.imwrite(img_name, img)
        # continue
        print(img_id)

if __name__ == "__main__":
    txt_path = "/root/result.txt"
    out_path = "/root/visual_image"
    image_path = "/root/autodl-tmp/data/visdrone/VisDrone2019-DET-val/images"
    select(txt_path, out_path, image_path)
