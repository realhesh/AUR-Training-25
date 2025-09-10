import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys, select, termios, tty
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
def get_key():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, termios.tcgetattr(sys.stdin.fileno()))
    return key

class controls_publisher(Node):
    def __init__(self):
        super().__init__('controls_publisher')
        self.publisher_ = self.create_publisher(String, 'controls', 10)
        self.timer = self.create_timer(0.1, self.check_key)
        self.get_logger().info(f"Started")
        self.exit_requested=False

    def check_key(self):
        if self.exit_requested:
            return
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = get_key()
            msg = String()
            msg.data = key
            if(key  == 'q'):
                self.exit_requested = True
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                rclpy.shutdown()
            elif key == '\x1b':
                key=get_key()
                key=get_key()
                msg.data = key
            self.publisher_.publish(msg)
            self.get_logger().info(f"I pressed: {msg.data}")
def main():
    rclpy.init()
    node = controls_publisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    rclpy.shutdown()