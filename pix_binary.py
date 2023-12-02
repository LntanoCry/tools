import os
import cv2

def convert_images_to_binary_mask(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有图像
    for filename in os.listdir(input_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # 构建输入和输出文件路径
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 读取图像
            image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

            # 将只含有0和255像素值的图像转换为0和1的二值掩码图像
            # _, binary_mask = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)
            _, binary_mask = cv2.threshold(image, 0, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            # 保存二值掩码图像
            cv2.imwrite(output_path, binary_mask)

input_folder_path = "/root/Pytorch-UNet/data/res_png"

# 输出二值掩码图像文件夹路径
output_folder_path = "/root/Pytorch-UNet/data/res"

# 转换图像为二值掩码
convert_images_to_binary_mask(input_folder_path, output_folder_path)