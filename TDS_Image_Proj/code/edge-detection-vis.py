#!/usr/bin/env python

# edge-detection-vis.py - realish-time visualization of adjustment of
#                         thresholds for Canny edge detection

import cv2
import numpy as np
import os

IMAGE_DIR = '/home/jaeger/dev/github.com/tds/Playground/TDS_Image_Proj/images'
IMAGE = 'thefan2.jpg'

# load the original image
img_orig = cv2.imread(os.path.join(IMAGE_DIR, IMAGE))

# save its shape for later use
rows, cols, channels = img_orig.shape

# rotate the image
M = cv2.getRotationMatrix2D((cols/2, rows/2), -90, 1)
img_rot = cv2.warpAffine(img_orig, M, (cols, rows))

# convert it to grayscale
img_gray = cv2.cvtColor(img_rot, cv2.COLOR_BGR2GRAY)

# start with both thresholds at 0 (produces a lot of graphical noise)
t1 = 0
t2 = 0

# until the quit signal (q key) is encountered, keep drawing the new image
# and waiting for a keypress
while True:
	# run the Canny edge detection algorithm on the image with the supplied
	# thresholds
	edges = cv2.Canny(img_gray, t1, t2)

	# write the thresholds onto the image so we know what they are currently
	cv2.putText(edges, "T1: %d, T2: %d" % (t1, t2), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1, cv2.LINE_AA)

	# show the image
	cv2.imshow('edges', edges)

	# wait for a keypress
	key = cv2.waitKey(0)
	if key == 82: # up
		t1 = t1 + 5
	elif key == 84: # down
		t1 = t1 - 5
		if t1 < 0:
			t1 = 0
	elif key == 81: # left
		t2 = t2 - 5
		if t2 < 0:
			t2 = 0
	elif key == 83: # right
		t2 = t2 + 5
	elif chr(key & 0xFF) == 's':
		t1, t2 = t2, t1
	elif chr(key & 0xFF) == 'q':
		break

# clean up after myself
cv2.destroyAllWindows()
