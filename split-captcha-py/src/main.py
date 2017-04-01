import numpy as np
from skimage import io, color
from skimage.morphology import skeletonize
from skimage.transform import rotate
from operator import itemgetter
import matplotlib.pyplot as plt
import cracker as xc
import xplt


def split_and_show(filename):
    img = io.imread(filename)

    #convert to 2-D array first
    img_gray = color.rgb2gray(img)


    # using 200 as the threshold
    #convert to black background & white foreground
    #in skimage array, black is 0
    img_bw = np.where(img_gray > np.mean(img_gray),0.0 ,1.0)

    to_rotate = xc.erect(img_bw)
    img_rotate = rotate(img_bw, to_rotate, resize=True)

    #split the original image and rotate one
    best_split = xc.select_best_split(img_bw)
    img1_1 = img_bw[:, 0: best_split[0]]
    img2_1 = img_bw[:, best_split[0]: best_split[1]]
    img3_1 = img_bw[:, best_split[1]: best_split[2]]
    img4_1 = img_bw[:, best_split[2]: ]

    
    best_split = xc.select_best_split(img_rotate)
    img1_2 = img_rotate[:, 0: best_split[0]]
    img2_2 = img_rotate[:, best_split[0]: best_split[1]]
    img3_2 = img_rotate[:, best_split[1]: best_split[2]]
    img4_2 = img_rotate[:, best_split[2]: ]


    #show the result
    xplt.show([img, skeletonize(img_bw), img_bw, img_rotate,
               img1_2, img2_2, img3_2, img4_2], 2, 4)


'''
Manually, I test the images:
1,2,3,4,5,6,7,8,9,10,15,25,35,65, 165,170,270,298,398,499,599


The rotate results are:
Better for splitting:2,3,4,6,8,65,170,298,398,499,599
Worse for splitting :5,10,25,35
Stay the same       :1,7,9,15,165,270


The splited results using rotate one are:
GOOD :1,2,3,4,8,298,398,499,599
BAD_1:5,6,10,15,25,65,170
BAD_2:270
BAD_3:7,9
BAD_4:35,165


Guess conclusion:
This algorithm is good for unconnected captcha or connected but no coincide lines.

''' 
if __name__ == '__main__':
    split_and_show('../data/2257.jpeg')
