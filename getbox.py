'''得到mask的最大内接矩形和最小外接矩形的bbox信息并取平均后输出到bbox'''

import cv2
import os
import numpy as np

mask_path = 'E:/my_python/detect_result/MDvsFA_cGAN/res'
get_txt = True
# choice = 'max_internel'
# choice = 'average'
choice = 'min_rect'

# 最大内接矩形
def maximum_internal_rectangle(mask_img):
    img = cv2.imread(mask_img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, img_bin = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(img_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if contours == ():
        return 0
    contour = contours[0].reshape(len(contours[0]), 2)

    rect = []

    for i in range(len(contour)):
        x1, y1 = contour[i]
        for j in range(len(contour)):
            x2, y2 = contour[j]
            area = abs(y2 - y1) * abs(x2 - x1)
            rect.append(((x1, y1), (x2, y2), area))

    all_rect = sorted(rect, key=lambda x: x[2], reverse=True)

    if all_rect:
        best_rect_found = False
        index_rect = 0
        nb_rect = len(all_rect)

        while not best_rect_found and index_rect < nb_rect:

            rect = all_rect[index_rect]
            (x1, y1) = rect[0]
            (x2, y2) = rect[1]

            valid_rect = True

            x = min(x1, x2)
            while x < max(x1, x2) + 1 and valid_rect:
                if any(img[y1, x]) == 0 or any(img[y2, x]) == 0:
                    valid_rect = False
                x += 1

            y = min(y1, y2)
            while y < max(y1, y2) + 1 and valid_rect:
                if any(img[y, x1]) == 0 or any(img[y, x2]) == 0:
                    valid_rect = False
                y += 1

            if valid_rect:
                best_rect_found = True

            index_rect += 1

        if best_rect_found:
            # 如果要在灰度图img_gray上画矩形，请用黑色画（0,0,0）
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 1)
            # cv2.imshow("rec", img)
            # cv2.waitKey(0)
            if get_txt:
                return [x1,y1,x2,y2]


        else:
            print("No rectangle fitting into the area")

    else:
        print("No rectangle found")

# 最小外接矩形
def draw_min_rect_rectangle(mask_img):
    image = cv2.imread(mask_img, 0)

    thresh = cv2.Canny(image, 256, 256)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img = np.copy(image)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # # 绘制矩形
        # cv2.rectangle(img, (x, y + h), (x + w, y), (0, 255, 255))
        if get_txt == True:
            return [x, y+h, x+w, y]


if __name__ == '__main__':
    # f = open("out_path", "w")
    if choice == 'average':
        for filename in os.listdir(mask_path):
            # 返回对顶角坐标
            inter = maximum_internal_rectangle(mask_path+'/'+filename)
            if inter != 0:
                recter = draw_min_rect_rectangle(mask_path+'/'+filename)
                [x1, y1, x2, y2] = [(inter[0]+recter[0])/2,(inter[1]+recter[3])/2,(inter[2]+recter[2])/2,(inter[3]+recter[1])/2]
                res = [min(x1,x2), min(y1,y2), abs(x2 - x1), abs(y2 - y1)]
                with open("result.txt", 'a') as f:
                    f.write(filename)
                    for i in res:
                        f.write(' '+str(i))
                    f.write('\n')
            else:
                with open("result.txt", 'a') as f:
                    f.write(filename)
                    f.write('\n')
    if choice == 'max_internel':
        for filename in os.listdir(mask_path):
            # 返回对顶角坐标
            if filename == '10109.bmp':
                print('10109')
            inter = maximum_internal_rectangle(mask_path + '/' + filename)
            if inter != 0:
                [x1, y1, x2, y2] = inter
                res = [min(x1,x2), min(y1,y2), abs(x2 - x1), abs(y2 - y1)]
                with open("result.txt", 'a') as f:
                    f.write(filename)
                    for i in res:
                        f.write(' ' + str(i))
                    f.write('\n')
            else:
                with open("result.txt", 'a') as f:
                    f.write(filename)
                    f.write('\n')
    if choice == 'min_rect':
        for filename in os.listdir(mask_path):
            # 返回对顶角坐标
            inter = maximum_internal_rectangle(mask_path + '/' + filename)
            if inter != 0:
                recter = draw_min_rect_rectangle(mask_path+'/'+filename)
                [x1, y1, x2, y2] = recter
                res = [min(x1,x2), min(y1,y2), abs(x2 - x1), abs(y2 - y1)]
                with open("result.txt", 'a') as f:
                    f.write(filename)
                    for i in res:
                        f.write(' '+str(i))
                    f.write('\n')
            else:
                with open("result.txt", 'a') as f:
                    f.write(filename)
                    f.write('\n')




