import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'greenguard_description'
    file_subpath = 'urdf/greenguard.urdf.xacro'
    rviz_subpath = 'rviz/greenguard.rviz'


    # Use xacro to process the file
    rviz_file = os.path.join(get_package_share_directory(pkg_name),rviz_subpath)
    
    start_rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_file])
    
    return LaunchDescription([
        start_rviz_cmd
    ])
