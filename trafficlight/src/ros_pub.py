#!/usr/bin/env python3
import cv2
import rospy
from std_msgs.msg import String


def hsv_detection(img, lower_hsv, upper_hsv, color, imgnum):
    global ros_str
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # cvtColor 함수를 이용하여 hsv 색공간으로 변환
    img_mask = cv2.inRange(img_hsv, lower_hsv, upper_hsv) # 범위내의 픽셀들은 흰색, 나머지 검은색
    img_result = cv2.bitwise_and(img, img, mask = img_mask) 

    # 바이너리 이미지를 마스크로 사용하여 원본이미지에서 범위값에 해당하는 영상부분을 획득
    if img_mask.any()== True:
        print("%s detected from img%d"%(color, imgnum))
        # contour_image, area = find_contour_and_area(img_result)
        ros_str = color
    else:
        print("none detection from img%d"%imgnum)    
        ros_str = "none detection from img%d"%imgnum
        
    cv2.imshow('img_mask%d'%imgnum, img_mask)
    cv2.imshow('img_result%d'%imgnum, img_result)
    return ros_str


def find_contour_and_area(image):
    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 이진화
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # 컨투어 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 컨투어 그리기
    contour_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)
    # 컨투어 영역 계산
    areas = []
    for contour in contours:
        area = cv2.contourArea(contour)
        areas.append(area)
    # 결과 출력
    i = 0
    for i, area in enumerate(areas):
        i+=1
    print("영역 크기 : %d"%i)
    
    return contour_image, areas


def cvpub():
    # 이미지 파일 경로 리스트
    image_paths = ["study_cv/image/trafficlight1.png", "study_cv/image/trafficlight2.png", "study_cv/image/trafficlight3.png"]

    num = 1
    ros_str = ""
    # 이미지를 차례대로 출력
    for image_path in image_paths:
        # 이미지 로드
        image = cv2.imread(image_path)

        # 이미지 출력
        cv2.imshow("Image%d"%num, image)
        cv2.waitKey(0)
        # 이미지를 블러 처리하여 노이즈 제거
        img_blur = cv2.GaussianBlur(image, (5, 5), 0)
        gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param2 = 100, minRadius = 5, maxRadius = 70)

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
            upper_red = (5, 255, 255)

            ros_str = hsv_detection(roi, lower_red, upper_red, "red", num)
            pub = rospy.Publisher('cv_detection', String, queue_size=10)
            pub.publish(ros_str)
            # 이미지 출력
            cv2.imshow("ROI%d"%num, roi)
            cv2.waitKey(0)
        num+=1
        
        # 창 닫기
        cv2.destroyAllWindows()


if __name__=='__main__':
    rospy.init_node('study_cv')
    rate = rospy.Rate(30) #30hz
    while not rospy.is_shutdown():
        try:
            cvpub()
        except rospy.ROSInitException:
            pass
        rate.sleep()


