#本程序只能实现一个文件夹下的txt文件合并

import os

#获取目标文件夹的路径
filedir = os.getcwd()+'/runs/detect/exp5/labels' # 输入和程序在同一个文件夹下的文件夹目录

#获取当前文件夹中的文件名称列表
filenames=os.listdir(filedir)

#打开当前目录下的result.txt文件，如果没有则创建
f=open('result.txt','w',encoding='utf-8')

# 先遍历文件名
for filename in filenames:
    filepath = filedir+'/'+filename
    #遍历单个文件，读取行数
    for line in open(filepath,encoding='utf-8'):
        f.writelines(filename + ' '+ line)

#关闭文件
f.close()
