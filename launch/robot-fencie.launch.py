import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
import launch_ros.descriptions
import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'fencie'
    file_subpath = 'description/robot.urdf.xacro'


    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(pkg_name), 'launch','rsp.launch.py'
            )]), 
        launch_arguments={'use_sim_time':'true', 'use_ros2_control': 'true'}.items()
    )

    controller_params_file = os.path.join(get_package_share_directory(pkg_name),'config','my_bot_controllers.yaml')
    
    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])



    # use this when ros2 control in use
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {'robot_description': 
            launch_ros.parameter_descriptions.ParameterValue(
                robot_description, value_type=str)
            },
            controller_params_file
        ]
    )

    delayed_controller_manager = TimerAction(period=3.0, actions=[controller_manager])

    # use this when ros2 control in use
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )

    # Run the node
    return LaunchDescription([
        rsp,
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner
    ])


