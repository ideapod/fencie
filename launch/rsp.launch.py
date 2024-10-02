import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration,Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.launch_context import LaunchContext
import launch_ros.descriptions

import xacro


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')

    sim_launch_arg = DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true')
    ros_control_launch_arg = DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2 control if true')
    

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('fencie'))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    # robot_description_config = xacro.process_file(xacro_file).toxml()
    
    robot_description_config = Command(
        ['xacro ', xacro_file, ' use_ros2_control:=', use_ros2_control]
    )


    
    # Create a robot_state_publisher node
    params = {
        'robot_description': launch_ros.parameter_descriptions.ParameterValue(robot_description_config, value_type=str), 
        'use_sim_time': use_sim_time
    }

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )


    # Launch!
    return LaunchDescription([
        sim_launch_arg,
        ros_control_launch_arg,
        node_robot_state_publisher
    ])