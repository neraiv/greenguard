import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'greenguard_description'
    file_subpath = 'urdf/greenguard.urdf.xacro'
    rviz_subpath = 'rviz/greenguard.rviz'
    world_path = 'worlds/deneme.world'
    robot_position = [-6.850161, -5.289750, 0.033333, 0.0, 0.0, 0.0]  # Add robot position here


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    world_file = os.path.join(get_package_share_directory(pkg_name),world_path)
    rviz_file = os.path.join(get_package_share_directory(pkg_name),rviz_subpath)
    robot_description_raw = xacro.process_file(xacro_file, substitutions={'robot_position': robot_position}).toxml()
    
    remappings = [('/tf', 'tf'),
                ('/tf_static', 'tf_static')]
    
    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        remappings = remappings,
        parameters=[{'robot_description': robot_description_raw,
        'use_sim_time': True}] # add other parameters here if required
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
            launch_arguments={'world': world_file}.items(),
        )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'greenguard',
                                '-x', str(robot_position[0]),
                                '-y', str(robot_position[1]),
                                '-z', str(robot_position[2]),
                                '-R', str(robot_position[3]),
                                '-P', str(robot_position[4]),
                                '-Y', str(robot_position[5])],           
                    output='screen')
    
    start_rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_file])

    # Run the node
    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        start_rviz_cmd
    ])