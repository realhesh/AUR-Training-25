from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld=LaunchDescription()
    
    turtlesim_node=Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        )
    logic_node= Node(
        package='turtle_chase_pkg',
        executable='turtle_chase',
        name='logic'
    )
    ld.add_action(turtlesim_node)
    ld.add_action(logic_node)
    return ld