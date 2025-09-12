
import rclpy
from rclpy.node import Node
class timer_node(Node):
    def __init__(self):
        super().__init__('timer')
        self.timer = self.create_timer(1, self.timer_callback)
        self.currtime=10

    def timer_callback(self):
        if(self.currtime >= 0):
            self.get_logger().info(f"{self.currtime}")
        elif(self.currtime == -1):
            self.get_logger().info('Time is up!')
        self.currtime -= 1
        
def main():
    rclpy.init()
    node = timer_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()