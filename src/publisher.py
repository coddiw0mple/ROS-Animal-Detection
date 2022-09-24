#!/usr/bin/env python3
from ast import arg
import rospy
import numpy as np
import airsim
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def main(args):
  image_pub = rospy.Publisher("image_topic_pub",Image, queue_size=10)
  rospy.init_node('image_pub', anonymous=True)
  rate = rospy.Rate(10)

  bridge = CvBridge()
  
  client = airsim.MultirotorClient(ip = args[1])
  client.confirmConnection()

  while not rospy.is_shutdown():
    responses = client.simGetImages([airsim.ImageRequest("front_center_custom", airsim.ImageType.Scene, False, False)])
    response = responses[0]

    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img = img1d.reshape(response.height, response.width, 3)

    img_msg = bridge.cv2_to_imgmsg(img, encoding="passthrough")
    rospy.loginfo("Publishing!")
    try:
      image_pub.publish(img_msg)
    except CvBridgeError as e:
      print(e)
    rate.sleep()

if __name__ == '__main__':
    try:
        main(sys.argv)
    except rospy.ROSInterruptException:
        pass