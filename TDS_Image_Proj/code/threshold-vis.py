#!/usr/bin/env python

# threshold-vis.py - realish-time visualization of threshold adjustment
#                    on a grayscale image

import cv2
import numpy as np
import os

IMAGE_DIR = '/home/jaeger/dev/github.com/tds/Playground/TDS_Image_Proj/images'
IMAGE = 'thefan2.jpg'

# load the original image
img_orig = cv2.imread(os.path.join(IMAGE_DIR, IMAGE))

# save its shape for later use
rows, cols, channels = img_orig.shape

# make a grayscale copy of the original
img_gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)

# make a new empty image (black) of the same shape as the grayscale image
img_new = np.zeros_like(img_gray)

# start with a pixel brightness threshold of 60 (range is 0-255)
threshold = 60

# until the quit signal (q key) is encountered, keep drawing the new image
# and waiting for a keypress
while True:
	# copy the grayscale image to our new image, replacing all values BELOW
	# threshold with 0 and all values ABOVE threshold with 255, thus turning
	# the grayscale image into a black and while map
	for r in range(0, rows):
		for c in range(0, cols):
			if img_gray[r][c] >= threshold:
				img_new[r][c] = 255
			elif img_gray[r][c] < threshold:
				img_new[r][c] = 0

	# write the threshold onto the image so we know what it is currently
	cv2.putText(img_new, "Threshold: %d" % threshold, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 1, cv2.LINE_AA)

	# show the image
	cv2.imshow('new', img_new)

	# wait for a keypress
	key = cv2.waitKey(0)
	if key == 82: # up
		threshold = threshold + 5
	elif key == 84: # down
		threshold = threshold - 5
		if threshold < 0:
			threshold = 0
	elif chr(key & 0xFF) == 'q':
		break

# clean up after myself
cv2.destroyAllWindows()
