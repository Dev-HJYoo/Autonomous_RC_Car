# -*- coding: utf-8 -*-

import cv2

import numpy as np

 

 

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): # ROI ����

 

    mask = np.zeros_like(img) # mask = img�� ���� ũ���� �� �̹���

    

    if len(img.shape) > 2: # Color �̹���(3ä��)��� :

        color = color3

    else: # ��� �̹���(1ä��)��� :

        color = color1

        

    # vertices�� ���� ����� �̷��� �ٰ����κ�(ROI �����κ�)�� color�� ä�� 

    cv2.fillPoly(mask, vertices, color)

    

    # �̹����� color�� ä���� ROI�� ��ħ

    ROI_image = cv2.bitwise_and(img, mask)

    return ROI_image

 

 

 

video = cv2.VideoCapture(0) # �̹��� �б�

 

while(True):

    ret, image = video.read()

    height, width = image.shape[:2]

    

    cv2.imshow('results', image)

    vertices = np.array([[(0,height),(0, height/2+100), (width, height/2+100), (width,height)]], dtype=np.int32) # ���� ��, ���� ��, ������ ��, ������ �� 

    ROI_img = region_of_interest(image, vertices)

    cv2.imshow('result', ROI_img)

    

    if cv2.waitKey(1) == ord('q'):

        break