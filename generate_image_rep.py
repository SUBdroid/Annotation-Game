import torch
from matplotlib import pyplot as plt
import cv2
from PIL import Image
import os
import numpy as np
from sklearn.preprocessing import LabelBinarizer
import pandas as pd

def create_one_hot():
    feat = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush'] 
    features = list(map(str.lower,feat))
    ids = np.arange(0,len(features))

    df = pd.DataFrame(list(zip(ids,features)),columns=['Ids','Categories'])
    y = pd.get_dummies(df.Categories)
    return y
    
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

data_loc = os.path.join(os.getcwd(),os.path.join("model_datasets","coco_general"))
# train_loc = os.path.join(data_loc,os.path.join("train2017"))
# data_dic = os.path.join(data_loc,"data_dictionary_train")
# img_list = []

# data_annotation = os.path.join(os.getcwd(),"Train_Image_Obj_Annotation")
# # auto_annotation_file = open(data_annotation,"w")
# open(data_annotation,"w")

# img_rep_folder = os.path.join(os.getcwd(),"img_rep")

# data_path = open(data_dic).read().split("\n")
# for line in data_path:
#     if len(line.split("\t"))==2:
#         text = line.split("\t")[0]
#         img_name = line.split("\t")[1]
#         img_path = os.path.join(train_loc,img_name)
#         if not os.path.exists(img_path):
#             print("Not found: %s"%img_path)
#         else:
#             results = model(img_path)
#             results.save()
#             # print(results.pandas().xyxy[0])
#             df = (results.pandas().xyxy[0])["name"].tolist()
#             one_hot = create_one_hot()
#             # pred = ['car', 'traffic light', 'car', 'car', 'traffic light']
#             pred = df
#             model_preds = list(set(pred))
#             f_ =  open(data_annotation,"a") 
#             h = text+"\t"
#             for obj in model_preds:
#                 h+=obj+","
#             print(h)
#             print(h,file=f_)
#             f_.close()
#             emb = []
#             for item in range(len(model_preds)):
#                 emb.append(one_hot[model_preds[item]].to_numpy())
#             image_embedding = np.sum(emb,axis=0)
#             print(image_embedding)
#             file_name = os.path.join(img_rep_folder,img_name+".npy")
#             with open(file_name, 'wb') as f:
#                 np.save(f,image_embedding)
#                 print("saved image representation successfully")

val_loc = os.path.join(data_loc,os.path.join("val2017"))
data_dic = os.path.join(data_loc,"data_dictionary_val")
img_list = []

data_annotation = os.path.join(os.getcwd(),"Val_Image_Obj_Annotation")
# auto_annotation_file = open(data_annotation,"w")
open(data_annotation,"w")

img_rep_folder = os.path.join(os.getcwd(),"img_rep_val")

data_path = open(data_dic).read().split("\n")
for line in data_path:
    if len(line.split("\t"))==2:
        text = line.split("\t")[0]
        img_name = line.split("\t")[1]
        img_path = os.path.join(val_loc,img_name)
        if not os.path.exists(img_path):
            print("Not found: %s"%img_path)
        else:
            results = model(img_path)
            results.save()
            # print(results.pandas().xyxy[0])
            df = (results.pandas().xyxy[0])["name"].tolist()
            one_hot = create_one_hot()
            # pred = ['car', 'traffic light', 'car', 'car', 'traffic light']
            pred = df
            model_preds = list(set(pred))
            f_ =  open(data_annotation,"a") 
            h = text+"\t"
            for obj in model_preds:
                h+=obj+","
            print(h)
            print(h,file=f_)
            f_.close()
            emb = []
            for item in range(len(model_preds)):
                emb.append(one_hot[model_preds[item]].to_numpy())
            image_embedding = np.sum(emb,axis=0)
            print(image_embedding)
            file_name = os.path.join(img_rep_folder,img_name+".npy")
            with open(file_name, 'wb') as f:
                np.save(f,image_embedding)
                print("saved image representation successfully")
   



# for root, dirs, files in os.walk(train_loc):
#     for f in files:
#         img_list.append(os.path.join(train_loc,f))


# img_list = ['/home/bhattacharya/personal_work_troja/MML/New/s1.jpg','/home/bhattacharya/personal_work_troja/MML/New/s2.jpg']

# for img in img_list:
#     results = model(img)
#     results.save()
#     # print(results.pandas().xyxy[0])
#     df = (results.pandas().xyxy[0])["name"].tolist()
#     one_hot = create_one_hot()
#     # pred = ['car', 'traffic light', 'car', 'car', 'traffic light']
#     pred = df
#     model_preds = list(set(pred))
#     emb = []
#     for item in range(len(model_preds)):
#         emb.append(one_hot[model_preds[item]].to_numpy())
#     print(model_preds)
#     print(np.sum(emb,axis=0))
   


