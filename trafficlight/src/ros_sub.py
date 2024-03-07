#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def callback(msg):
    if msg.data == "red":
        print("stop")
    elif msg.data == "green":
        print("go")
    elif msg.data == "yellow":
        print("wait")

def listener():
    rospy.init_node('study_sub')
    rospy.Subscriber("cv_detection", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()