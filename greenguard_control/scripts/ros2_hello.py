#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Hello(Node):

    def __init__(self):
        super().__init__('greenguard_hello')

        self.timer = self.create_timer(1.0, self.timer_cb)

        self.pub = self.create_publisher(String, '/greenguard_hello', 10)


    def timer_cb(self):
        msg = String()
        msg.data = "Greenguard says Hello!"
        self.pub.publish(msg)
        self.get_logger().info('Just said Hello')


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Hello())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
