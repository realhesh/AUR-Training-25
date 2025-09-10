#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
def input_to_movement(movement):
    command = Twist()
    if movement == 'w' or movement =='A':        # forward
        command.linear.x = 1.0
    elif movement == 's' or movement =='B':      # backward
        command.linear.x = -1.0
    elif movement == 'a' or movement == 'D':      # rotate left
        command.angular.z = 1.0
    elif movement == 'd' or movement == 'C':      # rotate right
        command.angular.z = -1.0
    return command
class turtle_controller(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.subscription = self.create_subscription(
            String,
            'controls',
            self.listener_callback,
            10)
        self.pub1 = self.create_publisher(Twist, f'/turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist ,f'/turtle2/cmd_vel',10)
    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')
        movement = Twist()
        if msg.data in ['w','a','s','d']:
            self.pub1.publish(input_to_movement(msg.data))
        elif msg.data in ['A','B','C','D']:
            self.pub2.publish(input_to_movement(msg.data))

def main():
    rclpy.init()
    node = turtle_controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()