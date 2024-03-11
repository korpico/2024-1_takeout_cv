#!/usr/bin/env python3
import cv2

def hsv_detection(img, lower_hsv, upper_hsv, color):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # cvtColor 함수를 이용하여 hsv 색공간으로 변환
    img_mask = cv2.inRange(img_hsv, lower_hsv, upper_hsv) # 범위내의 픽셀들은 흰색, 나머지 검은색
    img_result = cv2.bitwise_and(roi, roi, mask = img_mask) 
    # 바이너리 이미지를 마스크로 사용하여 원본이미지에서 범위값에 해당하는 영상부분을 획득
    if img_mask.any()== True:
        print("%s detected from img%d"%(color, num))
    else:
        print("none detection from img%d"%num)
        
    cv2.imshow('img_mask%d'%num, img_mask)
    cv2.imshow('img_result%d'%num, img_result)
 
if __name__=='__main__':
    # 이미지 파일 경로 리스트
    image_paths = ["trafficlight/image/trafficlight1.png", "trafficlight/image/trafficlight2.png", "trafficlight/image/trafficlight3.png"]
    num = 1 
    # 이미지를 차례대로 출력
    for image_path in image_paths:
        # 이미지 로드
        image = cv2.imread(image_path)
        # 이미지 출력
        cv2.imshow("Image%d"%num, image)
        cv2.waitKey(0)
        # 이미지를 블러 처리하여 노이즈 제거
        img_blur = cv2.GaussianBlur(image, (5, 5), 0)
        # 이미지를 grayscale 이미지로 변환
        gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
        # 허프 변환을 사용하여 원 검출
        # 이미지, 변환법, 입력 이미지와의 축척, 인접한 원 중심의 최소 거리,  엣지검출 임계값, 원검출 임계값, 검출할 원의 최소 반지름, 최대반지름
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param2 = 100, minRadius = 10, maxRadius = 70)

        for i in circles[0]:
            x = int(i[0])
            y = int(i[1])
            r = int(i[2])
            cv2.circle(image, (x, y), r, (255, 255  , 255), 2)
            # ROI 좌표 계산
            x1 = max(0, x - r)
            y1 = max(0, y - r)
            x2 = min(image.shape[1], x + r)
            y2 = min(image.shape[0], y + r)
            
            # ROI 그리기
            roi = image[y1:y2, x1:x2]
            lower_red = (0, 30, 30) # hsv 이미지에서 바이너리 이미지로 생성 , 적당한 값 30
            upper_red = (10, 255, 255)

            hsv_detection(roi, lower_red, upper_red, "red")

            # 이미지 출력
            cv2.imshow("ROI%d"%num, roi)
            cv2.waitKey(0)
        num+=1
        # 창 닫기
        cv2.destroyAllWindows()

