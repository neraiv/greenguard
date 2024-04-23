#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Mover(Node):

    def __init__(self):
        super().__init__('mover')
        self.twist_publisher = self.create_publisher(Twist, '/greenguard/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.twist_values_x_z = [(2,2),(5,1),(-5,-1),(-2,-2)]
        self.increment = 0
        self.total_values = len(self.twist_values_x_z)

    def timer_callback(self):
        msg = Twist()

        msg.linear.x = float(self.twist_values_x_z[self.increment][0])
        msg.angular.z = float(self.twist_values_x_z[self.increment][1])

        self.get_logger().info('Publishing message')
        self.twist_publisher.publish(msg)
        self.increment += 1
        if(self.total_values <= self.increment):
            self.increment = 0

def main(args=None):
    
    try:    
        rclpy.init(args=args)
        node = Mover()   
        rclpy.spin(node)
    except KeyboardInterrupt:
        msg = Twist()
        node.twist_publisher.publish(msg)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
