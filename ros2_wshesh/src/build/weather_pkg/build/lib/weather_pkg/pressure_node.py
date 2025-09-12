#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random
class pressure_publisher(Node):
    def __init__(self):
        super().__init__('pressure_publisher')
        self.publisher_ = self.create_publisher(Int32, 'pressure', 10)
        self.timer = self.create_timer(3, self.timer_callback)

    def timer_callback(self):
        msg = Int32()
        msg.data = random.randint(900,1100)
        self.publisher_.publish(msg)
        
def main():
    rclpy.init()
    node = pressure_publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()