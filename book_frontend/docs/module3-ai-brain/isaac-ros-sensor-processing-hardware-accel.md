# Isaac ROS Sensor Processing with Hardware Acceleration

## Overview

This guide provides essential instructions for processing various sensor types using Isaac ROS packages with GPU acceleration. Isaac ROS leverages NVIDIA's GPU computing capabilities to accelerate sensor data processing for real-time robotics applications.

## Supported Sensor Types

### Camera Sensors
- RGB cameras
- Stereo cameras
- Fish-eye cameras
- Thermal cameras

### LiDAR Sensors
- 2D LiDAR
- 3D LiDAR
- Solid-state LiDAR

### Other Sensors
- IMU sensors
- GPS sensors
- Depth cameras

## Basic Sensor Processing Pipeline

### Camera Processing

Configure camera processing with hardware acceleration:

```python
# camera_processing_pipeline.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Isaac ROS Image Processing
        Node(
            package='isaac_ros_image_proc',
            executable='isaac_ros_image_rectify_node',
            name='image_processor',
            parameters=[{
                'input_width': 640,
                'input_height': 480,
                'rectified_images_encoding': 'rgb8',
                'interpolation': 1,  # Linear interpolation
            }],
            remappings=[
                ('image_raw', 'camera/image_raw'),
                ('camera_info', 'camera/camera_info'),
                ('image_rect', 'camera/image_rect'),
            ]
        )
    ])
```

### Stereo Processing

Configure stereo processing for depth estimation:

```python
# stereo_processing_pipeline.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Isaac ROS Stereo Processing
        Node(
            package='isaac_ros_stereo_image_proc',
            executable='isaac_ros_stereo_rectify_node',
            name='stereo_processor',
            parameters=[{
                'alpha': 0.0,  # Fully rectified images
                'use_color': True,
                'queue_size': 5
            }],
            remappings=[
                ('left/image_raw', 'camera/left/image_raw'),
                ('right/image_raw', 'camera/right/image_raw'),
                ('left/camera_info', 'camera/left/camera_info'),
                ('right/camera_info', 'camera/right/camera_info'),
                ('left/image_rect', 'camera/left/image_rect'),
                ('right/image_rect', 'camera/right/image_rect'),
            ]
        )
    ])
```

## Hardware Acceleration Setup

### GPU Configuration

Ensure proper GPU configuration for sensor processing:

```yaml
# sensor_processing_config.yaml
sensor_processing:
  ros__parameters:
    # GPU settings
    gpu_index: 0
    enable_cuda_stream: True
    cuda_stream_priority: 0

    # Memory settings
    enable_memory_pool: True
    memory_pool_size: 1073741824  # 1GB

    # Processing settings
    max_batch_size: 1
    processing_rate: 30
    enable_padding: False
```

### Performance Optimization

Optimize sensor processing for real-time performance:

```python
# optimized_sensor_processing.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Optimized camera processing
        Node(
            package='isaac_ros_image_proc',
            executable='isaac_ros_image_rectify_node',
            name='optimized_image_processor',
            parameters=[{
                'input_width': 640,
                'input_height': 480,
                'rectified_images_encoding': 'rgb8',

                # Performance optimizations
                'gpu_index': 0,
                'enable_cuda_stream': True,
                'max_batch_size': 1,
                'processing_rate': 30,
            }],
            remappings=[
                ('image_raw', 'camera/image_raw'),
                ('camera_info', 'camera/camera_info'),
                ('image_rect', 'camera/image_rect'),
            ]
        )
    ])
```

## Multi-Sensor Fusion

### Sensor Data Synchronization

Synchronize multiple sensor streams:

```python
# sensor_fusion_pipeline.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Camera processing
        Node(
            package='isaac_ros_image_proc',
            executable='isaac_ros_image_rectify_node',
            name='camera_processor',
            parameters=[{'processing_rate': 30}],
            remappings=[
                ('image_raw', 'camera/image_raw'),
                ('image_rect', 'camera/image_rect'),
            ]
        ),

        # LiDAR processing
        Node(
            package='isaac_ros_pointcloud_utils',
            executable='isaac_ros_pointcloud_to_laserscan_node',
            name='lidar_processor',
            parameters=[{'scan_height': 1}],
            remappings=[
                ('cloud_in', 'lidar/points'),
                ('scan', 'lidar/scan'),
            ]
        )
    ])
```

## Quick Setup

### Minimal Sensor Processing

For getting started quickly with sensor processing:

```bash
# Launch basic camera processing
ros2 launch isaac_ros_image_proc isaac_ros_image_rectify.launch.py \
  input_width:=640 \
  input_height:=480 \
  rectified_images_encoding:=rgb8

# Launch stereo processing
ros2 launch isaac_ros_stereo_image_proc isaac_ros_stereo_rectify.launch.py \
  alpha:=0.0 \
  use_color:=true
```