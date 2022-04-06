import os
import numpy as np 
import matplotlib.pyplot as plt 

text_only = os.path.join(os.getcwd(),"text_confidence")
multimodal = os.path.join(os.getcwd(),"multimodality_confidence")

print("**************\n\nText-Only case\n**************\n")
f_text = open(text_only,"r").read().split("\n")
Text = []
tmp = []
for i in range(len(f_text)):
    mat = f_text[i]
    # print(mat.split())
    if len(mat.split())!=0:
        if len(mat.split())>1:
            if len(tmp)!=0:
                print(key)
                print(tmp)
                mean_confidence = np.mean(np.array(tmp))
                print(mean_confidence)
                tmp = []
            key = mat
        else:
            tmp.append(int(mat))

print("**************\n\nMultimodal case\n**************\n")
f_text = open(multimodal,"r").read().split("\n")
Text = []
tmp = []
for i in range(len(f_text)):
    mat = f_text[i]
    # print(mat.split())
    if len(mat.split())!=0:
        if len(mat.split())>1:
            if len(tmp)!=0:
                print(key)
                print(tmp)
                mean_confidence = np.mean(np.array(tmp))
                print(mean_confidence)
                tmp = []
            key = mat
        else:
            tmp.append(int(mat))

