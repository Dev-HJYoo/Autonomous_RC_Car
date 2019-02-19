# -*- coding: utf-8 -*-

import cv2

import numpy as np

 

 

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): # ROI 셋팅

 

    mask = np.zeros_like(img) # mask = img와 같은 크기의 빈 이미지

    

    if len(img.shape) > 2: # Color 이미지(3채널)라면 :

        color = color3

    else: # 흑백 이미지(1채널)라면 :

        color = color1

        

    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움 

    cv2.fillPoly(mask, vertices, color)

    

    # 이미지와 color로 채워진 ROI를 합침

    ROI_image = cv2.bitwise_and(img, mask)

    return ROI_image

 

 

 

video = cv2.VideoCapture(0) # 이미지 읽기

 

while(True):

    ret, image = video.read()

    height, width = image.shape[:2]

    

    cv2.imshow('results', image)

    vertices = np.array([[(0,height),(0, height/2+100), (width, height/2+100), (width,height)]], dtype=np.int32) # 왼쪽 밑, 왼쪽 위, 오른쪽 위, 오른쪽 밑 

    ROI_img = region_of_interest(image, vertices)

    cv2.imshow('result', ROI_img)

    

    if cv2.waitKey(1) == ord('q'):

        break