"""
对文件夹中的文件进行重命名
"""
import os

input_folder = 'E:\Dataset\inf_Integrated\data/t'  # 输入文件夹

# 遍历输入文件夹中的所有文件
for filename in sorted(os.listdir(input_folder)):
    # 获取文件名和文件扩展名
    file_name, file_extension = os.path.splitext(filename)

    # 仅处理特定文件格式（图片和文本）
    if file_extension.lower() in ('.jpg', '.jpeg', '.png', '.bmp', '.txt'):
        # 修改文件名
        new_file_name = file_name + '_2'  # 根据需要修改字符

        # 构造旧文件路径和新文件路径
        old_path = os.path.join(input_folder, filename)
        new_path = os.path.join(input_folder, new_file_name + file_extension)

        # 重命名文件
        os.rename(old_path, new_path)

        print(f'Renamed {file_name} to {new_file_name}')
