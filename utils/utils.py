import numpy as np
from PIL import Image
import torch
from torch import nn

#---------------------------------------------------------#
#   将图像转换成RGB图像，防止灰度图在预测时报错。
#   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
#---------------------------------------------------------#
def cvtColor(image):
    if len(np.shape(image)) == 3 and np.shape(image)[2] == 3:
        return image 
    else:
        image = image.convert('RGB')
        return image 

#---------------------------------------------------#
#   对输入图像进行resize
#---------------------------------------------------#
def resize_image(image, size, letterbox_image):
    iw, ih  = image.size
    w, h    = size
    if letterbox_image:
        scale   = min(w/iw, h/ih)
        nw      = int(iw*scale)
        nh      = int(ih*scale)

        image   = image.resize((nw,nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    else:
        new_image = image.resize((w, h), Image.BICUBIC)
    return new_image

#---------------------------------------------------#
#   获得类
#---------------------------------------------------#
def get_classes(classes_path):
    with open(classes_path, encoding='utf-8') as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names, len(class_names)

def preprocess_input(image):
    image   = np.array(image,dtype = np.float32)[:, :, ::-1]
    mean    = [0.40789655, 0.44719303, 0.47026116]
    std     = [0.2886383, 0.27408165, 0.27809834]
    return (image / 255. - mean) / std

def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def download_weights(backbone, model_dir="./model_data"):
    import os
    from torch.hub import load_state_dict_from_url
    
    if backbone == "hourglass":
        raise ValueError("HourglassNet has no pretrained model")
    
    download_urls = {
        'resnet50'      : 'https://s3.amazonaws.com/pytorch/models/resnet50-19c8e357.pth',
    }
    url = download_urls[backbone]
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    load_state_dict_from_url(url, model_dir)

'''
以下为了eval添加
'''

def findnearest(refdata, detdata):
    dis = np.zeros((len(detdata), 1))
    for i in range(len(detdata)):
        dis[i] = abs(refdata[0] - detdata[i][0]) + abs(refdata[1] - detdata[i][1])
    Id = np.argmin(dis)
    point = detdata[Id]
    return Id, point

def pool_nms(heat, kernel=3):
    pad = (kernel - 1) // 2

    hmax = nn.functional.max_pool2d(
        heat, (kernel, kernel), stride=1, padding=pad)
    keep = (hmax == heat).float()
    return heat * keep

# def decode_bbox(pred_hms, pred_offsets, image_size, threshold, cuda=True, topk=100):
#     pred_hms = pool_nms(pred_hms)
#
#     b, c, output_h, output_w = pred_hms.shape
#     detects = []
#     for batch in range(b):
#         heat_map = pred_hms[batch].permute(1, 2, 0).view([-1, c])
#         pred_offset = pred_offsets[batch].permute(1, 2, 0).view([-1, 2])
#         yv, xv = torch.meshgrid(torch.arange(0, output_h), torch.arange(0, output_w))
#         xv, yv = xv.flatten().float(), yv.flatten().float()
#         if cuda:
#             xv = xv.cuda()
#             yv = yv.cuda()
#         class_conf, class_pred = torch.max(heat_map, dim=-1)
#         mask = class_conf > threshold
#         pred_offset_mask = pred_offset[mask]
#         xv_mask = torch.unsqueeze(xv[mask] + pred_offset_mask[..., 0], -1)
#         yv_mask = torch.unsqueeze(yv[mask] + pred_offset_mask[..., 1], -1)
#         bboxes = torch.cat([xv_mask, yv_mask], dim=1)
#         bboxes[:, [0]] /= output_w
#         bboxes[:, [1]] /= output_h
#         detect = torch.cat(
#             [bboxes, torch.unsqueeze(class_conf[mask], -1), torch.unsqueeze(class_pred[mask], -1).float()], dim=-1)
#         arg_sort = torch.argsort(detect[:, -2], descending=True)
#         detect = detect[arg_sort]
#         detects.append(detect.cpu().numpy()[:topk])
#     return detects