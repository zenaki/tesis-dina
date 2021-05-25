# python3 -m pip install matplotlib

# (C) 2021
# aviezab
#  Gunakan Program ini Untuk Memastikan Gambar Yolov3 nya sudah benar bboxnya

# imports
import os, sys

# 3rd Party Imports
import matplotlib.pyplot as plt
import cv2


def clean_list(listx):
    for i, word in enumerate(listx):
        if word == '\n' or word == '\r':
            words[i] = ''
    return listx

def clean_list_as_str(listx):
    strx=""
    listy=[]
    strx=str(listx[0])
    strx = strx.replace("\n", "")
    strx= strx.replace("\r", "")
    # print(strx)
    listy = strx.split()
    # listy = json.loads(strx)
    return listy

# Gambarnya
img = cv2.imread("/home/dina/test_yolov3/images/train/20.jpeg")
dh, dw, _ = img.shape
# Labelnya
fl = open("/home/dina/test_yolov3/labels/train/20.txt", 'r')

data = fl.readlines()

data = clean_list_as_str(data) # Comment baris ini kalau multilabel
print(data, type(data))

fl.close()

for dt in data:
    # Split string to float
    print (dt, print(type(dt)))

    # _, x, y, w, h = map(float, dt.split(' ')) # Kalau multilabel pakai ini.
    # Kalau single label, pakai baris 53 sampai 56
    x = float(data[1])
    y = float(data[2])
    w = float(data[3])
    h = float(data[4])

    # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
    # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
    l = int((x - w / 2) * dw)
    r = int((x + w / 2) * dw)
    t = int((y - h / 2) * dh)
    b = int((y + h / 2) * dh)
    
    if l < 0:
        l = 0
    if r > dw - 1:
        r = dw - 1
    if t < 0:
        t = 0
    if b > dh - 1:
        b = dh - 1

    cv2.rectangle(img, (l, t), (r, b), (255, 255, 0), 3)

plt.imshow(img)
plt.show()
#plt.savefig("yolov3.png")
