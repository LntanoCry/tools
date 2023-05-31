# tools
some useful tools for data processing

## visual.py:
可以在图片中可视化txt文件中的bbox信息

## convert.py:
可以train.txt中的训练文件编号对应的图片提取出来

## getbox.py:
提取mask文件的最小外接矩形和最大内接矩形

## merge.py:
将多个txt文件合并为一个1

## voc2coco.py
将voc格式转换为coco格式

有两种转换方式:

- 通过txt

  其文件格式为

  ----VOC2007

  ---------Annotations

  ---------ImageSetss

  ----------------Main

  -----------------------train.txt

  -----------------------test.txt

  -----------------------val.txt

  ---------JEPGImages

  转换时按照train.txt，val.txt，test.txt生成三个.json文件

- 通过文件夹

  需要分别使用3个Annotations文件生成3个对应的.json文件

