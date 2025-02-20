import cv2
import matplotlib.pyplot as plt

def view_annotations(img_path, lbl_path):
    try:
        # read image
        image = cv2.imread(img_path)
        if image is None:
            raise FileNotFoundError(f"This img file doesn't exist silly: \n {img_path} ")
    
    except FileNotFoundError as e:
        print(f'\n{e}')
        print('no soup for you')
        return None
    
    # CONVERT TO RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_h, img_w, _ = image.shape

    try: 
        with open(lbl_path,'r') as file:

            # plot image !
            plt.figure(figsize = (20,20))
            
            plt.imshow(image)
            ax = plt.gca()


            # read annotations, then draw them on img
            for line in file:
                annotn = line.strip().split()
                class_id = int(annotn[0])
                x_center, y_center, w, h = map(float, annotn[1:5])
                # normalize to pixel values
                x_center = int(x_center * img_w)
                y_center = int(y_center * img_h)
                w = int(w * img_w)
                h = int(h * img_h)

                #calc top-left and bottom-right coord
                x1 = x_center - w/2
                y1 = y_center - h/2
                x2 = x_center + w/2
                y2 = y_center + h/2

                # draw box on img
                ax.add_patch(plt.Rectangle((x1,y1), x2 - x1, y2 - y1, linewidth = 2, edgecolor = 'r', facecolor ='none'))
                ax.text(x1, y1, f'Class {class_id}', color='r', fontsize=12, weight='bold')

            plt.show()

                    
    except Exception as e:
        print(f"\nAn error occured! {e}")
        print(f"no boxes for you loser")
        return None

view_annotations('/home/jennaehnot/Desktop/model_testing/images/val/rb150_1775.png', '/home/jennaehnot/Desktop/model_testing/labels/val/rb150_1775.txt')