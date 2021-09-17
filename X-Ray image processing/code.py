import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import math

def scale(threat_image,scale=80):
	'''
	this function scale down the threat image.
	'''
	width = int(threat_image.shape[1] * scale/100)
	height = int(threat_image.shape[0] * scale/100)

	dim = (width,height)
	resized_img = cv2.resize(threat_image,dim)
	img_copy = np.copy(resized_img)
	print('size of the scaled image : ',img_copy.shape)
	return img_copy




def mask(rotated_and_resized,background_image,scaled):
	'''
	this function generates the mask and crops the background image.
	'''

	lower_white = np.array([200,200,200])
	upper_white = np.array([255,255,255])
	mask = cv2.inRange(rotated_and_resized,lower_white,upper_white)
	#cv2.imshow('threat image',rotated_and_resized)
	#cv2.imshow('mask',mask)

	masked_img = np.copy(rotated_and_resized)
	masked_img[mask!=0] = [0,0,0]
	bag_img =background_image
	crop_back = bag_img
	#crop_back[mask == 0]=[255,255,255]
	#cv2.imshow('masked',masked_img)
	#cv2.imshow('crop_back',crop_back)
	return masked_img




def padding(masked_img,top,bottom,left,right):
	'''
	this functions adds white border to the image.
	'''

	#border=cv2.copyMakeBorder(masked_img,top+150,bottom,left,right-70,cv2.BORDER_CONSTANT,value=[255,255,255]) #this is for 4th number image 

	border=cv2.copyMakeBorder(masked_img,top,bottom,left,right,cv2.BORDER_CONSTANT,value=[255,255,255])
	border_resized = cv2.resize(border,(original_width,original_height))
	return border_resized




def rotate(border_resized):
	'''
	this function rotates the image by 45 degrees.
	'''

	rotated = ndimage.rotate(border_resized, 45)
	black_pix = np.where((rotated[:,:,0]==0)&(rotated[:,:,1]==0)&(rotated[:,:,2]==0))
	rotated[black_pix] = [255,255,255]
	rotated_resized=cv2.resize(rotated,(original_width,original_height))
	return rotated_resized





def final_image(background_image,threat_image):

	scaled=scale(threat_image)
	
	left = (threat_image.shape[1] - scaled.shape[1]) // 2
	right = left
	top = (threat_image.shape[0] - scaled.shape[0]) // 2
	bottom = top
	print('left',left)
	padded=padding(scaled,top,bottom,left,right)
	rotated_and_resized = rotate(padded)
	masked=mask(rotated_and_resized,background_image,scaled)
	final_output = cv2.addWeighted(background_image,0.5,masked,0.5,0) 
	#final_output = background_image + masked
	#final_output = masked - background_image
	return final_output 




background_image = cv2.imread('/home/lenovo/baggage/BaggageAI_CV_Hiring_Assignment/background_images/S0320365070_20180821160850_L-12_5.jpg')
img2 = cv2.imread('/home/lenovo/baggage/BaggageAI_CV_Hiring_Assignment/threat_images/BAGGAGE_20170524_075554_80428_B.jpg')
save_dir_path = "/home/lenovo/baggage/output images"

original_width = background_image.shape[1]
original_height = background_image.shape[0]
threat_image = cv2.resize(img2,(original_width,original_height))
final_img = final_image(background_image,threat_image)
cv2.imwrite("/home/lenovo/baggage/output images/5th.jpg",final_img)

cv2.imshow('threat image',threat_image)
cv2.imshow('background image',background_image) 
cv2.imshow('final image',final_img)

if cv2.waitKey(0) == 27:
	cv2.destroyAllWindows()























