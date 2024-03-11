#!/usr/bin/python3
import cv2
import numpy as np
from time import sleep
image = cv2.imread('takeout_cv1/Untitled.jpeg') # 이미지 파일 읽어들이기
# HSV로 색 추출
hsvLower = np.array([50, 0, 0])    # 추출할 색의 하한(HSV)
hsvUpper = np.array([255, 255, 255])    # 추출할 색의 상한(HSV)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # 이미지를 HSV으로 변환
hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)    # HSV에서 마스크를 작성
result = cv2.bitwise_and(image, image, mask=hsv_mask) # 원래 이미지와 마스크를 합성
cv2.imshow('test1', result)
sleep(1)
while True:
       # 키 입력을 1ms기다리고, key가「q」이면 break
    key = cv2.waitKey(1)&0xff
    if key == ord('q'):
        break
cv2.destroyAllWindows()
