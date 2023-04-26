# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 21:03:44 2018
@author: Fsl
"""
import shutil
 
 
# 这个库复制文件比较省事
 
def objFileName():
    '''
    生成文件名列表
    :return:
    '''
    local_file_name_list = r'E:\Dataset\detector\last_ann\ImageSets\Main/train.txt'
    # 指定名单
    obj_name_list = []
    for i in open(local_file_name_list, 'r'):
        obj_name_list.append(i.replace('\n', ''))
    return obj_name_list
 
 
def copy_img():
    '''
    复制、重命名、粘贴文件
    :return:
    '''
    local_img_name = r'E:\Dataset\detector\last_ann/mask_bmp'
    # 指定要复制的图片路径
    path = r'E:\Dataset\detector\last_ann/train_mask'
    # 指定存放图片的目录
    for i in objFileName():
        new_obj_name = i + '.bmp'
        shutil.copy(local_img_name + '/' + new_obj_name, path + '/' + new_obj_name)
 
 
if __name__ == '__main__':
    copy_img()