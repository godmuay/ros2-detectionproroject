from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='agv_control',
            executable='gesture_command_node',
            name='gesture_command_node'
        ),

        Node(
            package='agv_control',
            executable='motion_control_node',
            name='motion_control_node'
        ),

        Node(
            package='agv_control',
            executable='obstacle_detection_node',
            name='obstacle_detection_node'
        ),

        Node(
            package='agv_control',
            executable='control_service_node',
            name='control_service_node'
        )

    ])