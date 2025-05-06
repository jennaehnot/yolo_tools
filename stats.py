'''
For a dataset:
-number of images, broken up by jpg, png, maybe even codec
-for each image:
    -height, width
    -ratio
-find for each class:
    - number of images with class in it
    - number of occurences
    - area of all occurences

''' 
import os, imghdr
from PIL import Image
import numpy as np
import yolo_tools
from collections import Counter
import matplotlib.pyplot as plt

#path to dataset
'''
list dir on dset
for each folder in list dir

'''
def is_image(filename):
    try:
        with Image.open(filename) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False

def eval_img(filename):

    with Image.open(filename) as img:
        img_w, img_h = img.size
        area = img_w * img_h
        ratio = img_w / img_h

    return (img_w, img_h, ratio, area)

# def eval_label(imgpath, num_classes):
    
#     f_type = imghdr.what(imgpath)
#     f_end = '.' + f_type
#     lbl_path = imgpath.replace('images','labels')
#     lbl_path = lbl_path.replace(f_end, '.txt')
#     try:
#         with open(lbl_path,'r') as f:
#             for line in f:
#                 # read lines
#                 pass
#     except Exception as e:
#         print(f'Error reading label file {lbl_path}')
#         print(e)
        
#     return

ds_dir = '/home/jennaehnot/Desktop/dalian_dataset/dataset_v3'
num_classes = 3

valid_sets = ['test', 'train', 'val']
dataset = []
try:
    img_dir = os.path.join(ds_dir, 'images')
    img_sets = os.listdir(img_dir) 
    for set in img_sets:
        if set in valid_sets: # only looking for test, train, val images
            img_num = 0
            if set == 'train':
                pth = os.path.join(img_dir, set)
                #yolo_tools.image_check(pth)
                train_imgs = os.listdir(os.path.join(img_dir,set))

                for file in train_imgs: # for imgs in train set
                    fullimgpath = os.path.join(img_dir,set,file)
                    if is_image(fullimgpath): # verify its an image file
                        img = yolo_tools.Img(fullimgpath)
                        img.load_labels()
                        img.eval_labels(num_classes=3)
                        #print(img.class_tally)
                        dataset.append(img)
                train = yolo_tools.eval_dataset(dataset, 3)
    
    szs = train.img_sizes
    szs.sort()
    sz_count = Counter(szs)
    sizes = list(sz_count.keys())
    counts = list(sz_count.values())
    yolo_tools.image_sizes(train)
    # plt.figure(figsize=(10,6))
    # plt.bar(range(len(sizes)), counts, tick_label=[f"{size[0]}x{size[1]}" for size in sizes])
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()                  
                        

    pass

            
except Exception as e:
    print(e)


