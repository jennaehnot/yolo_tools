import os, magic
from PIL import Image
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class Img:
    def __init__(self,filepath):
        # file type
        mime = magic.Magic(mime=True)
        ftype = mime.from_file(filepath)
        self.ftype = ftype.replace('image/','')

        # full img path, img file name
        self.imgpath = filepath
        self.imgname = os.path.basename(filepath)

        # label full path, label name
        idx = self.imgname.index('.')
        self.labelname = self.imgname[:idx] + '.txt'
        labelpath = self.imgpath.replace(self.imgname, self.labelname)
        self.labelpath = labelpath.replace('images', 'labels')

        # init values populated by Img.eval_labels
        self.num_classes = None
        self.class_tally = None
        self.bb_areas = None
        self.bb_areas_n = None

        # is it in train val or test
        data_subsets = ['train', 'test', 'val']
        for subset in data_subsets:
            if subset in filepath:
                self.subset = subset
        
        try: 
            with Image.open(filepath) as img:
                self.img_w, self.img_h = img.size
                self.area = self.img_w * self.img_h
                self.ratio = self.img_w / self.img_h
        except Exception as e:
            print(f"Couldn't open img {filepath}")
            print(e)
    

    def load_labels(self):
        try:
            p = self.labelpath
            lbls = []
            with open(p, 'r') as f:
                for line in f:
                    l = line.strip()
                    l = list(map(float, l.split()))
                    l[0] = int(l[0])
                    lbls.append(l)
            self.labels = lbls 

        except Exception as e:
            print(f"Couldn't open label file {f}")
            print(e)
            self.labels = None



    def eval_labels(self, num_classes):
        # count instances of classes
        self.num_classes = num_classes
        tally = np.zeros(num_classes, int)
        if self.labels is not None:
            for i in range(0,len(self.labels)):
                lbl = self.labels[i]
                c = lbl[0]
                tally[c] += 1
            self.class_tally = tally

        # record areas of boundary boxes
            bb_areas = []
            bb_areas_n = []
            for x in range(0,num_classes):
                x_bbs = []
                x_bbs_n = []
                for l in self.labels:
                    if l[0] == x:
                        a_normal = l[3] * l[4]
                        a = a_normal * self.img_h * self.img_w
                        x_bbs_n.append(a_normal)
                        x_bbs.append(a)
                bb_areas_n.append(x_bbs_n)
                bb_areas.append(x_bbs)

            # write to object
            self.bb_areas = bb_areas
            self.bb_areas_n = bb_areas_n
        return

class Dataset():
    def __init__(self):
        self.num_imgs = 0
        self.class_instances = None
        self.img_sizes = []
        self.img_ratios = []
        self.img_areas = []
        self.bb_area = None


    
def eval_dataset(imgs, num_class):
    # instances of all classes in total
    # instances of all classes by set, ie # in train, # in val
    # list of img sizes
    # pixel area for each class
    dataset = Dataset()
    train = Dataset()
    test = Dataset()
    val = Dataset()
    bb = [[]] * num_class
    bbn = [[]] * num_class
    dataset.class_instances = np.zeros(num_class, int)
    # train.class_instances = np.zeros(num_class)
    # test.class_instances = np.zeros(num_class)
    # val.class_instances = np.zeros(num_class)

    for img in imgs:
        try:
            dataset.num_imgs += 1
            dataset.class_instances = dataset.class_instances + img.class_tally
            sz = (img.img_w, img.img_h)
            dataset.img_sizes.append(sz)
            dataset.img_ratios.append(img.ratio)
            dataset.img_areas.append(img.area)

            for i in range(0,num_class):
                c = img.bb_areas[i]
                cn = img.bb_areas_n[i]
                bb[i] = bb[i] + c
                bbn[i] = bbn[i] + cn            



            # if img.subset == 'train':
            #     train.num_imgs += 1
            #     train.class_instances = train.class_instances + img.class_tally
            #     sz = (img.img_w, img.img_h)
            #     train.img_sizes.append(sz)
            #     train.img_ratios.append(img.ratio)
            #     train.img_areas.append(img.area)
            # elif img.subset == 'test':
            #     test.num_imgs += 1
            #     test.class_instances = test.class_instances + img.class_tally
            #     sz = (img.img_w, img.img_h)
            #     test.img_sizes.append(sz)
            #     test.img_ratios.append(img.ratio)
            #     test.img_areas.append(img.area)
            # elif img.subset == 'val':
            #     val.num_imgs += 1
            #     val.class_instances = val.class_instances + img.class_tally
            #     sz = (img.img_w, img.img_h)
            #     val.img_sizes.append(sz)
            #     val.img_ratios.append(img.ratio)
            #     val.img_areas.append(img.area)
            # # concatenate for full dataset
            # dataset.num_imgs = train.num_imgs + test.num_imgs + val.num_imgs
            # dataset.img_sizes = train.img_sizes + test.img_sizes + val.img_sizes
            # dataset.img_ratios = train.img_ratios + test.img_ratios + val.img_ratios
            # dataset.img_areas = train.img_areas + test.img_areas + val.img_areas



        except Exception as e:
            print(e)
    return(dataset)           

def image_sizes(dataset):
    standards = [(0,0), (320, 320), (640, 640), (960, 960), (1280, 1280), (1600, 1600), (1920, 1920), (2240, 2240), (10000,10000)]
    szs = dataset.img_sizes
    szs.sort()
    count = np.zeros(len(standards)-1, int)


    for q in range(1, len(standards)):
        standard = standards[q]
        for sz in szs: 
            if sz <= standard and sz > standards[q-1]:
                count[q-1] +=1

    xlabels = ['(0,320]', '(320,640]', '(640,960]', '(960,1280]', '(1280,1600]', '(1600,1920]', '(1920,2240]', '2240 and up' ]    
    # plt.figure(figsize=(10,8))
    # plt.bar(range(len(count)), count, tick_label=xlabels)
    # plt.xticks(rotation=45)
    # plt.xlabel('Image widths')
    # plt.ylabel('Frequency')
    # plt.tight_layout()
    # plt.show()

    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(range(len(count)), count, tick_label=xlabels, edgecolor = 'black')

    sz_count = Counter(szs)
    sizes = list(sz_count.keys())
    counts = list(sz_count.values())
    ind_of_5largest = np.argsort(counts)[-5:]
    # big5 = PrettyTable()
    # big5.field_names = ["Image Size", "Number of Images"]
    big5 =[]
    for id in ind_of_5largest[::-1]:
        #big5.add_row([sizes[id], counts[id]])
        big5.append([sizes[id], counts[id]])
    
    columns = ["Five Most Common Image Size", "Number of Images"]
    table = ax.table(cellText=big5, colLabels=columns, loc = 'right', cellLoc='center', bbox=[1.1, 0.1, 0.2, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.auto_set_column_width(col = [range(len(columns))])
    

    plt.subplots_adjust(left=0.1, bottom=0.1)
    plt.tight_layout()
    plt.show()
    print("Five most common image sizes")
    print(big5)

    return