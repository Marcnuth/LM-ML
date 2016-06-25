import numpy as np
from operator import itemgetter

'''
Return the indexes of max connected array in given array
'''
def max_connected_array(arr, diagonal=True):
    nonzero_arr = np.nonzero(arr)
    nonzero_all = set(map(lambda x, y: (x, y), nonzero_arr[0], nonzero_arr[1]))
    nonzero_walked = set()

    scores = list()
    while nonzero_all - nonzero_walked:
        nonzero_towalk = nonzero_all - nonzero_walked
        neighbor = neighbor_indexs(nonzero_towalk.pop(), arr, diagonal)
        scores.append((len(neighbor), neighbor))

        nonzero_walked = nonzero_walked.union(neighbor)

    scores = sorted(scores, key=itemgetter(0))[::-1]
    
    return scores[0][1]
       
    
def neighbor_indexs(xy, arr, diagonal=True):

    arr_cpy = np.insert(arr, 0, 0, axis=0)
    arr_cpy = np.insert(arr_cpy, 0, 0, axis=1)
    arr_cpy = np.insert(arr_cpy, arr_cpy.shape[0], 0, axis=0)
    arr_cpy = np.insert(arr_cpy, arr_cpy.shape[1], 0, axis=1)

    x, y = xy[0] + 1, xy[1] + 1

    neighbor = set()
    to_walk = set()
    to_walk.add((x, y))
    while to_walk:
        item = to_walk.pop()
        x = item[0]
        y = item[1]

        # neighbor set means the item have been walked, so we donot need to walk again
        if item in neighbor:
            continue

        # not walked, just add to neighbor and walk
        neighbor.add((x, y))

        if arr_cpy[x + 1, y]:
            to_walk.add((x+1, y))
        if arr_cpy[x + 1, y + 1] and diagonal:
            to_walk.add((x+1, y+1))
        if arr_cpy[x, y + 1]:
            to_walk.add((x, y+1))
        if arr_cpy[x - 1, y + 1] and diagonal:
            to_walk.add((x-1, y+1))
        if arr_cpy[x - 1, y]:
            to_walk.add((x-1, y))
        if arr_cpy[x - 1, y - 1] and diagonal:
            to_walk.add((x-1, y-1))
        if arr_cpy[x, y - 1]:
            to_walk.add((x, y-1))
        if arr_cpy[x + 1, y - 1] and diagonal:
            to_walk.add((x+1, y-1))


    return set([(_i[0] - 1, _i[1] - 1) for _i in neighbor])
        



'''
Return an tuple, which is (mins, maxs)
mins: a sorted list of indexs which is minmums
maxs: a sorted list of indexs which is maxmums
'''
def discrete_extremes(arr):

    shrinked = [[arr[0], 1]]
    for i in range(1, arr.shape[0]):
        if arr[i] == shrinked[-1][0]:
            shrinked[-1][1] += 1
        else :
            shrinked.append([arr[i], 1])

    d1_shrinked = np.diff([i[0] for i in shrinked])
    mins_shrinked = [i for i in range(1, d1_shrinked.shape[0]) if d1_shrinked[i] * d1_shrinked[i-1] < 0 and d1_shrinked[i] > 0]
    maxs_shrinked = [i for i in range(1, d1_shrinked.shape[0]) if d1_shrinked[i] * d1_shrinked[i-1] < 0 and d1_shrinked[i] < 0]

    mins, maxs = set(), set()
    hided = 0
    for i in range(len(shrinked)):
        if i in mins_shrinked:
            for j in range(shrinked[i][1]):
                mins.add(i + hided + j)

        if i in maxs_shrinked:
            for j in range(shrinked[i][1]):
                maxs.add(i + hided + j)

        hided += (shrinked[i][1] - 1)



    mins = sorted(list(mins))
    maxs = sorted(list(maxs))

    return (mins, maxs)
    




'''
Main: for test and examples
'''
if __name__ == '__main__':

    # max connected array
    case1 = np.load('xnp.test.array.1')
    print max_connected_array(case1, diagonal=False)

    # tests & examples
    case1 = np.array([1,2,3,4,5,4,3,2,1,2,3,4,5,6,7,8,7,8,9,8,7,3,5,4,5,6,9])
    assert discrete_extremes(case1) == ([8, 16, 21, 23], [4, 15, 18, 22])
    
    case2 = np.array([1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,2,2,2,2,2,3])
    assert discrete_extremes(case2) == ([15, 16, 17, 18, 19], [10, 11, 12, 13, 14])
    
    case3 = np.array([0,0,0,0,1,9,2,1,9,0,0,0])
    assert discrete_extremes(case3) == ([7], [5, 8])

    case4 = np.array([0,1,0,-1,-2,9])
    assert discrete_extremes(case4) == ([4], [1])
    print 'ENJOY!'
