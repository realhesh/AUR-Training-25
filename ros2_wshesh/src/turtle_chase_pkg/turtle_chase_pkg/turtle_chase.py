import rclpy
from rclpy.node import Node
from turtlesim.srv import Kill,Spawn
from functools import partial
from turtlesim.msg import Pose
from math import sqrt
from std_msgs.msg import Int32
import random
def random_coords():
    return [random.randint(1,10),random.randint(1,10)]

class turtle_chase(Node):
    def __init__(self):
        super().__init__("turtle_chase")
        coords = random_coords()
        self.Spawn_turtle(coords[0],coords[1])
        coords = random_coords()
        self.Spawn_turtle(coords[0],coords[1])
        coords = random_coords()
        self.Spawn_turtle(coords[0],coords[1])
        self.subself = self.create_subscription(Pose,'/turtle1/pose',self.self_callback,10)
        self.sub2 = self.create_subscription(Pose,'/turtle2/pose',self.e0_callback,10)
        self.sub3 = self.create_subscription(Pose,'/turtle3/pose',self.e1_callback,10)
        self.sub4 = self.create_subscription(Pose,'/turtle4/pose',self.e2_callback,10)
        self.publisher_ = self.create_publisher(Int32,'score',10)
        self.enemies = [None,None,None]
        self.mypose = None
        self.score=0
        self.create_timer(0.2,self.timer_callback)
    def timer_callback(self):
        cnt = 1
        for i in self.enemies:
            if self.collision_happened(cnt-1):
                turtle_name = "turtle" + str(cnt+1)
                self.score+=1
                msg = Int32()
                msg.data = self.score
                self.publisher_.publish(msg)
                self.kill_turtle(turtle_name,cnt-1)
            cnt+=1
    def collision_happened(self,other_num):
        if type(self.mypose) is type(None) or type(self.enemies[other_num]) is type(None):
            return False
        distance = sqrt((self.mypose.x-self.enemies[other_num].x)**2 + (self.mypose.y-self.enemies[other_num].y)**2)
        self.get_logger().info(f"distance between me and {other_num+2} is {distance}")
        if distance < 0.5:
            return True
        else:
            return False
    def self_callback(self,msg):
        self.mypose = msg;
    def e0_callback(self,msg):
        self.enemies[0]=msg
        #self.get_logger().warn(f"my position now is : {self.mypose}")
    def e1_callback(self,msg):
        self.enemies[1]=msg
        #self.get_logger().warn(f"my position now is : {self.mypose}")
    def e2_callback(self,msg):
        self.enemies[2]=msg
        #self.get_logger().warn(f"my position now is : {self.mypose}")
    def Spawn_turtle(self,x,y,name=None):
        client=self.create_client(Spawn,"spawn")
        while not client.wait_for_service(1):
            self.get_logger().warn("Waiting...")
        request=Spawn.Request()
        request.x=float(x)
        #request.x = 1.0
        #request.y=1.0
        request.y=float(y)
        request.theta=0.0
        if type(name) is not type(None):
            request.name = name
        future=client.call_async(request)
        future.add_done_callback(partial(self.spawn_callback,x=x,y=y)) # this will call self.callback when service has replied
    def spawn_callback(self,future,x,y):
        try:
            response=future.result()
            self.get_logger().info(f"{response.name} has spawned at {x} , {y}")
        except Exception as e:
            self.get_logger().error("Service call failed: %r" %(e,))
    def kill_turtle(self,name,cnt):
        client=self.create_client(Kill,"kill")
        while not client.wait_for_service(1):
            self.get_logger().warn("Waiting...")
        request=Kill.Request()
        request.name=name
        future=client.call_async(request)
        future.add_done_callback(partial(self.kill_callback,name=name,cnt=cnt)) # this will call self.callback when service has replied
    def kill_callback(self,future,name,cnt):
        try:
            response=future.result()
            self.get_logger().info(f"turtle called {name} has died ,the turtle has died, long live the turtle!")
            self.enemies[cnt]=None
            coords = random_coords()
            self.Spawn_turtle(coords[0],coords[1],name)
        except Exception as e:
            self.get_logger().error("Service call failed: %r" %(e,))
def main():
    rclpy.init()
    node = turtle_chase()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()