import numpy as np
from skimage import io, color
from skimage.morphology import skeletonize
from operator import itemgetter
import matplotlib.pyplot as plt
import xnp, xplt
from skimage.transform import rotate
from skimage import io




'''
Rotate image to be vertical
This require the input img has black back and white foreground
Also, img should be 2D array

Parameter:
angels: a tuple of the minial angel, max angel and step for rotate
'''
def erect(img, angels=(-45, 45, 5), split=4):

    assert img[0][0] == 0

    scores = []
    for i in range(angels[0], angels[1], angels[2]):
        tmp = rotate(img, i, resize=True)

        best_split = select_best_split(tmp, split=split)
        tmp_1 = tmp[:, 0: best_split[0]]
        tmp_2 = tmp[:, best_split[0]: best_split[1]]
        tmp_3 = tmp[:, best_split[1]: best_split[2]]
        tmp_4 = tmp[:, best_split[2]:]

        #calculate the max connected array
        scores.append((i,
                       _max_connected_ratio(tmp_1),
                       _max_connected_ratio(tmp_2),
                       _max_connected_ratio(tmp_3),
                       _max_connected_ratio(tmp_4)
        ))

    print '====>'
    print sorted(scores, key=lambda s : np.std([s[1], s[2], s[3], s[4]]))
    print sorted(scores, key=lambda s : np.mean([s[1], s[2], s[3], s[4]]), reverse = True)
    return sorted(scores, key=lambda s : np.mean([s[1], s[2], s[3], s[4]]), reverse = True)[0][0]

def _max_connected_ratio(img):
    indexes = xnp.max_connected_array(img, diagonal=False)
    max_connected_sum = 0
    for cooridnate in indexes:
        max_connected_sum += img[cooridnate[0], cooridnate[1]]
        
    return max_connected_sum * 1.0 / np.sum(img)



'''
This require the input img is black(0) background and white(1) foreground
'''
def select_best_split(img, split=4, skel=False):

    # The image should be 2-D arrary, and with black background & white foreground
    assert img[0][0] == 0
    
    # convert img
    img_bw = img
    img_bw_sum = np.sum(img, axis=0)

    print img_bw_sum

    start_index = np.nonzero(img_bw_sum)[0][0]
    end_index = np.nonzero(img_bw_sum)[0][-1]

    mins = xnp.discrete_extremes(img_bw_sum)[0]
  
    loc_interval = (end_index - start_index) * 1.0 / split
    proper_loc = [i * 1.0 * loc_interval + start_index for i in range(1, split)]
    
    # find best split point
    best_split = []
    for i in range(len(mins) - 1):
        if len(best_split) == split - 1 :
            break

        if mins[i] < proper_loc[len(best_split)]:
            if mins[i + 1] >= proper_loc[len(best_split)]:
                best_split.append(mins[i] if mins[i+1] - proper_loc[len(best_split)] > proper_loc[len(best_split)] - mins[i] else mins[i+1])


    return best_split
    

if __name__ == '__main__':
    img = io.imread('../data/3.jpeg')
    img_gray = color.rgb2gray(img)
    img_bw = np.where(img_gray > np.mean(img_gray),0.0 ,1.0)
    print img_bw
    img_rotate = rotate(img_bw, 10, resize=True)
    print select_best_split(img_rotate)

    xplt.show([img, img_gray, img_rotate, img_bw], 2, 2)

    
    print 'ENJOY!'
