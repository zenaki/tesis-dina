# python3 -m pip install tqdm

# (C) 2021
# aviezab
#  Gunakan Program ini Untuk Convert LabelMe ke Yolov3

# imports
from pathlib import Path
import PIL.Image as Image
import json

# 3rd party import
from tqdm import tqdm

# Fungsi Convert
def convertLtoY5(size, box):
    """
    Convert Labelme format to Yolov5 format.
    """
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def create_yolov5_dataset(tag, categories, dataset_type):
    """
    Create Ultralytics Dataset. dataset_type = "train" or "val"
    """
    images_path = Path(f"images/{dataset_type}")
    images_path.mkdir(parents=True, exist_ok=True)

    labels_path = Path(f"labels/{dataset_type}")
    labels_path.mkdir(parents=True, exist_ok=True)

    for img_id, row in enumerate(tqdm(tag)):
        image_name = f"{img_id}.jpeg" 
        img = dataset_path + "/" + row["imagePath"]
        img = Image.open(img)
        img = img.convert("RGB")
        img.save(str(images_path / image_name), "JPEG") # Kalau mau bagus, bisa ganti JPEG ke PNG
        label_name = f"{img_id}.txt"
        with (labels_path / label_name).open(mode="w") as label_file:
            for a in row['shapes']:
                category_idx = categories.index(a["label"])
                points = a['points']
                x1 = points[0][0]
                y1 = points[0][1]
                x2 = points[1][0]
                y2 = points[1][1]
                xmin = min(x1,x2)
                xmax = max(x1,x2)
                ymin = min(y1,y2)
                ymax = max(y1,y2)
                w= int(img.size[0])
                h= int(img.size[1])
                b = (xmin, xmax, ymin, ymax)
                bb = convertLtoY5((w,h), b)
                label_file.write(f"{category_idx} {str(bb[0])} {str(bb[1])} {str(bb[2])} {str(bb[3])} \n")  
# Variables
# dataset_path = "path" # Contoh Path: "/run/media/aviezab/ai/projects/practices/facial-expression/dataset/yolov3"
dataset_path = "/home/dina/test_yolov3/dataset"
json_array   = []
_tag = []
anotasi      = []
print(dataset_path)
for path in Path(dataset_path).rglob('*.json'):
    print(path)
    json_array.append(dataset_path + "/" +path.name)
    f = open(dataset_path + "/" +path.name)
    _tag.append(json.load(f))

for item in _tag:
    pre_len = item["shapes"]
    banyak_ano = len(pre_len)
    for i in range(banyak_ano):
        anotasi.append(pre_len[i]["label"])

anotasi = list(set(anotasi))
anotasi.sort()

print(anotasi) #print Kelas

# Jalankan program
if (__name__ ==  "__main__") :
    create_yolov5_dataset(_tag, anotasi, "train")
