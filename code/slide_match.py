import logging
logging.basicConfig(level=logging.DEBUG)
import cv2,time
import sys
import os
import gc
import numpy as np
from matplotlib import pyplot as plt
#from textarea import captch_ex
from face import face_det




#****************************************** MATCHING WITH SLIDES ****************************************


def compare_frame_slide(frame,slide):
	sift = cv2.xfeatures2d.SIFT_create() 
	img1 = cv2.imread(frame,0)          # queryImage
	img2 = cv2.imread(slide,0) # trainImage
	
	# Initiate SIFT detector
	# find the keypoints and descriptors with SIFT
	kp1, des1 = sift.detectAndCompute(img1,None)
	kp2, des2 = sift.detectAndCompute(img2,None)
	#print "frame%d and frame%d" %(frame_number,next_frame_number)
	#print image1,image2,
	#print "kp1 = ",len(kp1),
	#print "kp2 = ",len(kp2),
	# FLANN parameters
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)   # or pass empty dictionary

	flann = cv2.FlannBasedMatcher(index_params,search_params)

	matches = flann.knnMatch(des1,des2,k=2)

	# Need to draw only good matches, so create a mask
	matchesMask = [[0,0] for i in xrange(len(matches))]
	feat=0
	per1=0
	per2=0
	# ratio test as per Lowe's paper
	for i,(m,n) in enumerate(matches):
		if m.distance < 0.7*n.distance:
		    matchesMask[i]=[1,0]
		    feat=feat+1
	del matchesMask
	del matches
	del sift
	del FLANN_INDEX_KDTREE
	del des2
	del des1
	del flann
	del index_params
	del search_params
	del img1
	del img2
	#print len(matchesMask)
	#print "matched = %d " %feat,
	per1=(float(feat)/len(kp1))*100
	per2=(float(feat)/len(kp2))*100
	#if per1 < 50 or per2 < 50:
	#	print next_frame_number
	
	#print "per1 = %.2f per2 = %.2f " %(per1,per2)
	#fil.write("%s and %s kp1 = %d kp2 = %d matched = %d per1 = %.2f per2 = %.2f \n" %( image1, image2 , len(kp1), len(kp2), feat, per1, per2))
	del kp1
	del kp2
	del per2
	if per1>5:
		return per1
	else:
		return 0





def matching_with_slide(frame_to_compare):
	count=0
	max_index_of_slide=int(sys.argv[1])
	matched_slide_number=-0
	max_per_match=0
	while (count<=max_index_of_slide):
		frame="frame%d.jpg"%frame_to_compare
		slide="common%d.jpg"%count
		match_percent=compare_frame_slide(frame,slide)
		if max_per_match < match_percent:
			max_per_match=match_percent
			matched_slide_number=count
		count=count+1
	del max_index_of_slide
	del max_per_match
	del frame
	del slide
	del match_percent
	del count
	return matched_slide_number


gc.disable()
'''with open('data.txt') as f:
	content = f.readlines()

fr = content[0].split()'''
fr = [line.rstrip('\n') for line in open('data.txt')]
pre=0
for i in fr:
	fil=open("ans.csv","a")
	j = int(i)
	if j>pre:
		fil.write("%d,%d\n" %(j,matching_with_slide(j)+1))
		pre=j
	#slide_number=matching_with_slide(j)
	#fil.write("%d,%d\n" %(j,matching_with_slide(j)))
	fil.close()
	#time.sleep(1)
