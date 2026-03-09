from setuptools import find_packages, setup

package_name = 'agv_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/agv_control']),
        ('share/agv_control', ['package.xml']),
        ('share/agv_control/launch', ['launch/agv_system.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='strsph',
    maintainer_email='strsph@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'hand_gesture_node = agv_control.hand_gesture_node:main',
            'gesture_command_node = agv_control.gesture_command_node:main',
            'motion_control_node = agv_control.motion_control_node:main',
            'obstacle_detection_node = agv_control.obstacle_detection_node:main',
            'control_service_node = agv_control.control_service_node:main',
        ],
    },
)
