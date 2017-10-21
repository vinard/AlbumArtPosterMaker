import os
from os.path import isfile, join
import sys
import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math

_PRIOR = 1
mypath = ''

def debug(prior, str):
    if(prior <= _PRIOR):
        print(str)

def magnitude(arr):
    squared_sum = math.sqrt(arr[0]**2 + arr[1]**2 + arr[2]**2)
    return squared_sum

def dom_color():
    cwd = os.getcwd()
    onlyfiles = [f for f in os.listdir(cwd) if isfile(join(cwd, f))]
    onlyfiles = [x for x in onlyfiles if '.jpg' in x]
    onlyfiles.sort()

    # Run k-means on all images to find dominant colors
    dominant_colors = []
    for jpg in onlyfiles:
        debug(1, "Assessing {0}".format(jpg))
        image = cv2.imread(jpg)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
        image = cv2.resize(image, (300,300))

        image = image.reshape((image.shape[0] * image.shape[1], 3))
        clt = KMeans(n_clusters = 1)
        clt.fit(image)

        color = clt.cluster_centers_[0]
        dominant_colors.append(color)

    dominant_colors = np.array(dominant_colors)
    magnitudes      = np.apply_along_axis(magnitude, 1, dominant_colors)
    magnitudes      = magnitudes.reshape(magnitudes.shape[0],1)

    data            = np.hstack((dominant_colors, magnitudes))
    data            = np.hstack((data, np.array(onlyfiles).reshape(len(onlyfiles),1)))
    data            = data[data[:,-2].argsort()]

    return data

def rename(data):
    for i in range(data.shape[0]):
        os.rename(data[i,-1], "{:02d}.jpg".format(i))

def collage():
    cwd = os.getcwd()
    onlyfiles = [f for f in os.listdir(cwd) if isfile(join(cwd, f))]
    onlyfiles = [x for x in onlyfiles if '.jpg' in x]
    onlyfiles.sort()

    images = []
    for jpg in onlyfiles:
        img = cv2.imread(jpg)
        img = cv2.resize(img, (700, 700))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)

    final = []
    x = 6
    y = 4
    for i in range(0,y):
        for j in range(0,x):
            if j > 0:
                row = np.hstack((row, images[x*i+j]))
            else:
                row = images[x*i+j]

        if i > 0:
            final = np.vstack((final, row))
        else:
            final = row

    plot = plt.figure()
    plt.axis("off")
    plt.imshow(final)
    final = cv2.cvtColor(final, cv2.COLOR_RGB2BGR)
    cv2.imwrite("collage.png",final)
    plt.show()

    cv2.imshow('final', final)

def main():
    if (len(sys.argv) != 2):
        print("Usage: python3 art.py <dir>")
        return

    # Get all images in a folder
    mypath = sys.argv[1]
    os.chdir(mypath)

    data = dom_color()
    rename(data)
    collage()
    # reference_collage() TODO


if __name__ == '__main__':
    main()
