import argparse
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

height = 1900
width = 1240


parser = argparse.ArgumentParser()
parser.add_argument("inputFile", type=str)

args = parser.parse_args()

img = cv.imread(args.inputFile)

assert img is not None, "file could not be read"
rows, cols, ch = img.shape

pts1 = np.float32([[40, 90], [552, 34], [780, 834], [248, 933]])
pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

M = cv.getPerspectiveTransform(pts1, pts2)
dst = cv.warpPerspective(img, M, (width, height))

cv.imwrite("transformed.png", dst)

plt.subplot(121), plt.imshow(img), plt.title("Input")
plt.subplot(122), plt.imshow(dst), plt.title("Output")
plt.show()
