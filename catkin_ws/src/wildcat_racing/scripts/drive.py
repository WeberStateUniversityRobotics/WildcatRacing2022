#!/usr/bin/env python
import rospy
from adafruit_servokit import ServoKit
from std_msgs.msg import Float64
from std_msgs.msg import Float32
import numpy as np

kit = ServoKit(channels=16)

class Drive:

    # Steering Servo info:
    # The steering servo as configured above will take range 0-180
    # where 0 is RHS and 180 is LHS.

    def __init__(self):
        self.speed = 0
        self.teleop_speed_subscriber = rospy.Subscriber('/teleop_speed', Float64, self.teleop_callback)
        self.lidar_speed_subscriber = rospy.Subscriber('/lidar_speed', Float32, self.lidar_callback)

    def teleop_callback(self, msg):
        rospy.loginfo(rospy.get_caller_id() + "Latest teleop_speed was: %s\n", msg)
        new_speed = Float64()
        if msg != 0:
            new_speed = msg
            self.speed = msg
            kit.continuous_servo[2].throttle = new_speed
        else:
            self.speed = 0

    def lidar_callback(self, msg):
        rospy.loginfo(rospy.get_caller_id() + "Latest lidar_speed was: %s\n", msg)
        new_speed = Float32()
        #Priority is given to teleop since self.angle is only updated by teleop.
        if self.speed == 0:
            new_speed = msg
            kit.continuous_servo[2].throttle = new_speed

if __name__ == '__main__':
    print("Running drive node.")
    rospy.init_node('drive')
    Drive()
    rospy.spin()
