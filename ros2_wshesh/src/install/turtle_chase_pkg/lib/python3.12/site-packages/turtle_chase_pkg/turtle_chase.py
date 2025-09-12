import rclpy
from rclpy.node import Node
from turtlesim.srv import Kill,Spawn
from functools import partial
from random import random
def random_coords():
    return [random.randint(0.5,10.5),random.randint(0.5,10.5)]
class turtle_chase(Node):
    def __init__(self):
        super().__init__("turtle_chase")
        coords = random_coords()
        self.Spawn_turtle(coords[0],coords[1])
        coords = random_coords()
        self.Spawn_turtle(coords[0],coords[1])
        coords = random_coords()
        self.Spawn_turtle(coords[0],coords[1])


    def Spawn_turtle(self,x,y):
        client=self.create_client(Spawn,"spawn")
        while not client.wait_for_service(1):
            self.get_logger().warn("Waiting...")
        request=Spawn.Request()
        request.x=x
        request.y=y
        request.theta=0.0
        future=client.call_async(request)
        future.add_done_callback(partial(self.spawn_callback,x=x,y=y)) # this will call self.callback when service has replied

    def add_callback(self,future,a,b):
        try:
            response=future.result()
            self.get_logger().info(f"{response.name} has spawned")
        except Exception as e:
            self.get_logger().error("Service call failed: %r" %(e,))


def main():
    rclpy.init()
    node = MyClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()