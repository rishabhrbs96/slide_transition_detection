import logging
logging.basicConfig(level=logging.DEBUG)
import cv2
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
	max_index_of_slide=19
	matched_slide_number=-1
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



#***************************************** IMAGE COMPARISON USING SIFT *******************************************




def run_sift(n1,n2):
	image1='frame%d.jpg' %n1
	image2='frame%d.jpg' %n2
	sift = cv2.xfeatures2d.SIFT_create() 
	img1 = cv2.imread(image1,0)          # queryImage
	img2 = cv2.imread(image2,0) # trainImage

	# Initiate SIFT detector
	# find the keypoints and descriptors with SIFT
	kp1, des1 = sift.detectAndCompute(img1,None)
	kp2, des2 = sift.detectAndCompute(img2,None)
	#print "frame%d and frame%d" %(frame_number,next_frame_number)
	# FLANN parameters
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)   # or pass empty dictionary

	flann = cv2.FlannBasedMatcher(index_params,search_params)
	del FLANN_INDEX_KDTREE
	del index_params
	del search_params
	matches = flann.knnMatch(des1,des2,k=2)
	del flann
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
	del des2
	del des1
	
	del sift
	
	
	del img1
	del img2
	print n1,n2,
	#print len(matchesMask)
	#print "matched = %d " %feat,
	per1=(float(feat)/len(kp1))*100
	per2=(float(feat)/len(kp2))*100
	del kp1
	del kp2
	print "per1 = %.2f per2 = %.2f " %(per1,per2)
	if per1 < 50 or per2 < 50:	
		#fil.write("%d " %next_frame_number)
		return True                #returns true if there is a doubt of transition
	
	#fil.write("frame%d and frame%d kp1 = %d kp2 = %d matched = %d per1 = %.2f per2 = %.2f \n" %( frame_number, next_frame_number , len(kp1), len(kp2), feat, per1, per2))

	del per1
	del per2
	#draw_params = dict(matchColor = (0,255,0),
	#	               singlePointColor = (255,0,0),
	#	               matchesMask = matchesMask,
	#	               flags = 0)
	#img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
	#print len(matches)
	#plt.imshow(img3,),plt.show()
	





#****************************************** EXTRACTING FRAME PER SECOND ****************************************

video_file_name="video.mp4"
cap = cv2.VideoCapture("%s"%video_file_name);
total_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS))
#print total_frames



cap = cv2.VideoCapture("%s"%video_file_name);
 #int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS))
count = 1;
for i in range(1,total_frames):
	cap.set(cv2.CAP_PROP_POS_MSEC, count*1000)
	ret,image = cap.read()
	#ret,image = cap.read()
	#pos = cap.get(cv2.CAP_PROP_FPS)
	cv2.imwrite("frame%d.jpg" % count, image)
	#print pos
	count=count+1
	#cap.release();'''





#************************************************************** MAIN CODE ***************************************************


'''
gc.disable()                                         #index of the last frame
frame_number=2                                              #starting frame number 
next_frame_number=frame_number+1                              #frame next to the previous frame
check_slide=True                                              #boolean to check whether it is a slide or not
check_next_slide=True                                         #boolean to check whether the next frame is slide or not
#doubtable_frames=[]
#doubt_count=0
while (next_frame_number <= total_frames-1) :                   #iterating through all the frames

	frame1='frame%d.jpg' % frame_number                	#location of frame1 
	frame2='frame%d.jpg' % next_frame_number           	#location of frame2

	check_slide=face_det(frame1)                               #checking whether it is slide or not using the size of the textarea
	check_next_slide=face_det(frame2)                          #checking whether the next frame is slide or not

	if check_next_slide == False:                             #if it contains the instructor then search for the next slide

		while (check_next_slide==False and next_frame_number <= total_frames) :             #end if a slide is found
			next_frame_number=next_frame_number+1
			frame2='frame%d.jpg' % next_frame_number                
			check_next_slide=face_det(frame2)

	fil=open("data.txt","a")
	run_sift(frame1,frame2)                                       #run the sift algorithm
	fil.close()

	frame_number=next_frame_number                              #assign previous frame to the next frame which is a slide 
	next_frame_number=next_frame_number+1                       #increase the next frame by 1


#********************************************************** INDEXING *************************************************

#frame_number=input("Enter frame number :")
#print matching_with_slide(frame_number)'''

logging.basicConfig(level=logging.DEBUG)
frame_number=1                                              #starting frame number 
next_frame_number=frame_number+1                              #frame next to the previous frame
check_slide=True                                              #boolean to check whether it is a slide or not
check_next_slide=True
inter_frame=frame_number
jump=4
while (next_frame_number <= total_frames-1) :                   #iterating through all the frames

	frame1='frame%d.jpg' % frame_number                	#location of frame1 
	frame2='frame%d.jpg' % next_frame_number           	#location of frame2

	check_slide=face_det(frame1)                               #checking whether it is slide or not using the size of the textarea
	check_next_slide=face_det(frame2)                          #checking whether the next frame is slide or not

	if check_next_slide == False:                             #if it contains the instructor then search for the next slide

		while (check_next_slide==False and next_frame_number <= total_frames-1) :             #end if a slide is found
			next_frame_number=next_frame_number+1
			frame2='frame%d.jpg' % next_frame_number                
			check_next_slide=face_det(frame2)
			logging.basicConfig(level=logging.DEBUG)

	
	if run_sift(frame_number,next_frame_number)==True:
		logging.basicConfig(level=logging.DEBUG)
		inter_frame=frame_number+1
		while (inter_frame <=  next_frame_number and inter_frame <= total_frames-1):
			frame1='frame%d.jpg' % frame_number 
			frame2='frame%d.jpg' % inter_frame
			if face_det(frame2)==False:
				inter_frame=inter_frame+1
				continue
			if run_sift(frame_number,inter_frame)==True:
				logging.basicConfig(level=logging.DEBUG)
				fil=open("data.txt","a")
				fil.write("%d\n"% inter_frame)		                                                         #run the sift algorithm
				fil.close()
			frame_number=inter_frame
			inter_frame=inter_frame+1
	
	frame_number=next_frame_number                              #assign previous frame to the next frame which is a slide 
	next_frame_number=next_frame_number+jump                       #increase the next frame by 1

