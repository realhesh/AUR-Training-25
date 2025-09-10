#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Int32
class monitor_node(Node):
    def __init__(self):
        super().__init__('monitor_node')
        self.temp=0
        self.hum=0
        self.pressure=0
        self.TempSub = self.create_subscription(
            Int32,
            'temperature',
            self.TempUpdate_callback,
            10)
        self.HumSub = self.create_subscription(
            Int32,
            'humidity',
            self.HumUpdate_callback,
            10)
        self.PressureSub = self.create_subscription(
            Int32,
            'pressure',
            self.PressureUpdate_callback,
            10)
        with open("output.txt", "w") as f:
            ...
        self.timer = self.create_timer(1.0, self.timer_callback)
    def TempUpdate_callback(self, msg):
        self.temp=msg.data
        #self.get_logger().info(f'I heard: "{msg.data}"')
    def HumUpdate_callback(self, msg):
        self.hum=msg.data
        #self.get_logger().info(f'I heard: "{msg.data}"')
    def PressureUpdate_callback(self, msg):
        self.pressure=msg.data
        #self.get_logger().info(f'I heard: "{msg.data}"')
    def timer_callback(self):
        data = f'Temp = {self.temp} ◦ C, Humidity = {self.hum} %, Pressure = {self.pressure} hPa.'
        with open("output.txt", "a") as f:
            f.write(data+"\n")
        self.get_logger().info(data)

def main():
    rclpy.init()
    node = monitor_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()