import os
from PIL import Image

# 输入文件夹路径和输出文件夹路径
input_folder = 'E:\Dataset\inf_Integrated\data/t2'  # 输入文件夹
output_folder = 'E:\Dataset\inf_Integrated\data/t'  # 输出文件夹

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        # 构造输入文件路径和输出文件路径
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.replace('.jpg', '.bmp'))

        # 检查原始文件是否为BMP格式，如果是则跳过转换
        if os.path.splitext(input_path)[1] == '.bmp':
            continue

        # 打开JPEG图片
        image = Image.open(input_path)

        # 将图片转换为BMP格式并保存
        image.save(output_path, 'BMP')

        # 关闭图片
        image.close()
