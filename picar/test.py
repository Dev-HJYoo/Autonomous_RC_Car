# -*- coding: utf-8 -*-

import front_wheels as fw

import back_wheels as bw

import cv2 # 

import numpy as np

import time

from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance1

 

 

 

def grayscale(image): # ����̹����� ��ȯ

    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

 

def canny(img, low_threshold, high_threshold): # Canny �˰���

    return cv2.Canny(img, low_threshold, high_threshold)

 

def gaussian_blur(img, kernel_size): # ����þ� ����

    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

 

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

 

def draw_lines(img, lines, color=[0, 0, 255], thickness=5): # �� �׸���

    for line in lines:

        for x1,y1,x2,y2 in line:

            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

 

def draw_fit_line(img, lines, color=[0, 255, 0], thickness=10): # ��ǥ�� �׸���

        cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)

 

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): # ���� ��ȯ

    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)

    #line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    #draw_lines(line_img, lines)

 

    return lines

 

def weighted_img(img, initial_img, a=1, b=1., c=0.): # �� �̹��� operlap �ϱ�

    return cv2.addWeighted(initial_img, a, img, b, c)

 

def get_fitline(img, f_lines): # ��ǥ�� ���ϱ�   

    lines = np.squeeze(f_lines)

    lines = lines.reshape(lines.shape[0]*2,2)

    rows,cols = img.shape[:2]

    output = cv2.fitLine(lines,cv2.cv.CV_DIST_L2,0, 0.01, 0.01)

    vx, vy, x, y = output[0], output[1], output[2], output[3]

    x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x) , img.shape[0]-1

    x2, y2 = int(((img.shape[0]/2+100)-y)/vy*vx + x) , int(img.shape[0]/2+100)

    

    result = [x1,y1,x2,y2]

    return result

 

 

 

video = cv2.VideoCapture(0) # �̹��� �б�

 

back_wheels = bw.Back_Wheels()

front_wheels = fw.Front_Wheels(channel=0)

UA = Ultrasonic_Avoidance1.Ultrasonic_Avoidance(20)

threshold = 10

 

while(True):

    distance = UA.get_distance()

    print(distance)

    if distance < threshold :

        back_wheels.stop()

        front_wheels.turn_straight()

        continue

 

        

    ret, image = video.read()

    height, width = image.shape[:2] # �̹��� ����, �ʺ�

 

    #cv2.imshow('orgin_image', image)

    gray_img = grayscale(image) # ����̹����� ��ȯ

      

    blur_img = gaussian_blur(image, 3) # Blur ȿ��

    

    #cv2.imshow('blur_image', blur_img)

    

    canny_img = canny(blur_img, 70, 210) # Canny edge �˰���

    

    #cv2.imshow('canny_image', canny_img)

    

    vertices = np.array([[(0,height),(0, height/2+100), (width, height/2+100), (width,height)]], dtype=np.int32) # ���� ��, ���� ��, ������ ��, ������ ��

    ROI_img = region_of_interest(canny_img, vertices) # ROI ����

    #cv2.imshow("ROI_img", ROI_img)

 

    line_arr = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) # ���� ��ȯ

    line_arr = np.squeeze(line_arr)

    

    # ���� ���ϱ�

    slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi

 

    # ���� ���� ����

    line_arr = line_arr[np.abs(slope_degree)<160]

    slope_degree = slope_degree[np.abs(slope_degree)<160]

 

    # ���� ���� ����

    line_arr = line_arr[np.abs(slope_degree)>95]

    slope_degree = slope_degree[np.abs(slope_degree)>95]

 

    # ���͸��� ���� ������

    L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]

    temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    L_lines, R_lines = L_lines[:,None], R_lines[:,None]

 

    # �� �߱� 

##    draw_lines(temp, L_lines)

##    draw_lines(temp, R_lines)

    

    #����, ������ ���� ��ǥ�� ���ϱ�

    left_fit_line = get_fitline(image,L_lines)

    right_fit_line = get_fitline(image,R_lines)

 

    # ���� �и�

    x1 = int(left_fit_line[0])

    y1 = int(left_fit_line[1])

    x2 = int(left_fit_line[2])

    y2 = int(left_fit_line[3])

 

    # ������ �и�

    x3 = int(right_fit_line[0])

    y3 = int(right_fit_line[1])

    x4 = int(right_fit_line[2])

    y4 = int(right_fit_line[3])

 

    Px = int(((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)))

    Py = int(((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)))

    

    

##    # ��ǥ�� �׸���

##    draw_fit_line(temp, left_fit_line)

##    draw_fit_line(temp, right_fit_line)

 

    cv2.circle(image, (Px,Py), 10, (0, 0, 255), -1)

    result = weighted_img(temp, image) # ���� �̹����� ����� �� overlap

    

    back_wheels.backward()

    x = width/2-Px 

    

    if x < 0:

        front_wheels.turn_right()

    elif x > 0:

        front_wheels.turn_left()

    else:

        front_wheels.turn_straight()

    back_wheels.speed = 28

    cv2.circle(result, (x,height/2), 10, (255,0,0), -1)

    time.sleep(0.001)

    cv2.imshow('result',result) # ��� �̹��� ���

    if cv2.waitKey(1) == ord('q'):

        break

 

video.release()

cv2.destroyALLWIndows()

##def test():

##    import random as rd

##    import time

##    back_wheels = bw.Back_Wheels()

##    front_wheels = fw.Front_Wheels(channel=0)

##    x,y = 0,0

##    back_wheels.backward()

##    for i in range(0,100):

##        x = rd.randrange(-1,2)

##        y = rd.randrange(-1,2)

##        if x == -1:

##            front_wheels.turn_right()

##        elif x == 0:

##            front_wheels.turn_straight()

##        else:

##            front_wheels.turn_left()

##        s = rd.randrange(30,70)

##        back_wheels.speed = s

##        print "frontward, speed =", x

##        print "Backward, speed =", s

##        time.sleep(0.5)

##    back_wheels.stop()

##