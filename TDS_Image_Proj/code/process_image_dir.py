#!/usr/bin/env python

import cv2
import glob
import numpy as np
import os
from PIL import Image
import sys

def processDir(input_dir):
	# iterate through the files in the input directory with a '.jpg' extension
	# and skip anything with oldformat in its path
	for img in glob.iglob(input_dir + '/*/*.jpg'):
		if 'oldformat' not in img:
			print(img)

			# read the image from disk
			in_img = cv2.imread(img)

			# configure blob detector parameters
			params = cv2.SimpleBlobDetector_Params()

			# set it up to filter by minimum area of the blob
			params.filterByArea = True
			params.minArea = 250

			# and by minimum circularity so it hopefully gets only circles
			params.filterByCircularity = True
			params.minCircularity = 0.9

			# work around differences between opencv 2 and 3
			is_v2 = cv2.__version__.startswith('2.')
			if is_v2:
				detector = cv2.SimpleBlobDetector(params)
			else:
				detector = cv2.SimpleBlobDetector_create(params)

			# detect the circles
			keypoints = detector.detect(in_img)
			if len(keypoints) != 4:
				print("Warning: found %d keypoints in '%s'" % (len(keypoints), img))
				continue

			# convert the keypoints to inputs for perspective transformation
			inpts = np.float32([[kp.pt[0], kp.pt[1]] for kp in keypoints])

			# outputs are fixed size, 600x600 pixels - keypoint order matters!
			outpts = np.float32([[600, 600], [0, 600], [600, 0], [0, 0]])

			# calculate the perspective transform matrix
			M = cv2.getPerspectiveTransform(inpts, outpts)

			# do the warp
			img_warp = cv2.warpPerspective(in_img, M, (600, 600))

			# write out the warped image
			out_dir = os.path.join(os.path.dirname(img), 'out')
			if not os.path.isdir(out_dir):
				os.mkdir(out_dir)
			cv2.imwrite(os.path.join(out_dir, os.path.basename(img)), img_warp)

			# write out the individual image cells
			print("Splitting: ", end="")
			cellsize = 100
			for col in range(0, 5):
				for row in range(0, 5):
					print(".", end="")
					#print("%d,%d" % (row + 1, col + 1), end=" ")
					#print("Processing cell %s, %s" % (row + 1, col + 1))
					cell = img_warp[row*cellsize+50:row*cellsize+cellsize+50, col*cellsize+50:col*cellsize+cellsize+50]
					cv2.imwrite(os.path.join(out_dir, os.path.basename(img).replace('.jpg', '-%d-%d.jpg' % (row + 1, col + 1))), cell)
			print()

def usage():
	print("Usage: %s <input directory>" % sys.argv[0])

if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)

	input_dir = os.path.abspath(sys.argv[1])
	print("Processing images in input directory '%s'" % input_dir)
	processDir(input_dir)
