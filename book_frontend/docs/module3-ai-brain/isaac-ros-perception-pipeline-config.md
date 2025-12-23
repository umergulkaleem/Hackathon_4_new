# Isaac ROS Perception Pipeline Configuration Guide

## Overview

This guide provides essential instructions for configuring Isaac ROS perception pipelines with GPU acceleration. Perception pipelines process sensor data to extract meaningful information for robotics applications.

## Basic Pipeline Setup

### 1. Preprocessing Pipeline

Configure preprocessing nodes for sensor data preparation:

```python
# preprocessing_pipeline.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Isaac ROS Image Rectification
        Node(
            package='isaac_ros_image_proc',
            executable='isaac_ros_image_rectify_node',
            name='image_rectifier',
            parameters=[{
                'input_width': 640,
                'input_height': 480,
                'rectified_images_encoding': 'rgb8'
            }],
            remappings=[
                ('image_raw', 'camera/image_raw'),
                ('camera_info', 'camera/camera_info'),
                ('image_rect', 'camera/image_rect'),
            ]
        )
    ])
```

### 2. Inference Pipeline

Configure neural network inference nodes:

```python
# inference_pipeline.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Isaac ROS DetectNet for object detection
        Node(
            package='isaac_ros_detectnet',
            executable='isaac_ros_detectnet',
            name='object_detector',
            parameters=[{
                'model_name': 'ssd_mobilenet_v2_coco',
                'input_width': 960,
                'input_height': 544,
                'confidence_threshold': 0.5,
                'max_batch_size': 1,
                'gpu_index': 0,
            }],
            remappings=[
                ('image_input', 'camera/image_rect'),
                ('detections_output', 'object_detections'),
            ]
        )
    ])
```

## Complete Pipeline Example

Create a complete perception pipeline combining multiple Isaac ROS packages:

```python
# complete_perception_pipeline.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Image rectification
        Node(
            package='isaac_ros_image_proc',
            executable='isaac_ros_image_rectify_node',
            name='image_rectifier',
            parameters=[{
                'input_width': 640,
                'input_height': 480,
                'rectified_images_encoding': 'rgb8'
            }],
            remappings=[
                ('image_raw', 'camera/color/image_raw'),
                ('camera_info', 'camera/color/camera_info'),
                ('image_rect', 'camera/color/image_rect'),
            ]
        ),

        # Object detection
        Node(
            package='isaac_ros_detectnet',
            executable='isaac_ros_detectnet',
            name='object_detector',
            parameters=[{
                'model_name': 'ssd_mobilenet_v2_coco',
                'input_width': 960,
                'input_height': 544,
                'confidence_threshold': 0.5,
                'max_batch_size': 1,
                'gpu_index': 0,
            }],
            remappings=[
                ('image_input', 'camera/color/image_rect'),
                ('detections_output', 'object_detections'),
            ]
        ),

        # Visual SLAM
        Node(
            package='isaac_ros_visual_slam',
            executable='isaac_ros_visual_slam_node',
            name='visual_slam',
            parameters=[{
                'enable_rectification': True,
                'input_width': 640,
                'input_height': 480,
            }],
            remappings=[
                ('/stereo_camera/left/image', 'camera/left/image_rect'),
                ('/stereo_camera/right/image', 'camera/right/image_rect'),
                ('/stereo_camera/left/camera_info', 'camera/left/camera_info'),
                ('/stereo_camera/right/camera_info', 'camera/right/camera_info'),
            ]
        )
    ])
```

## Performance Optimization

### GPU Configuration

Optimize for GPU acceleration:

```yaml
# perception_pipeline_config.yaml
perception_pipeline:
  ros__parameters:
    # GPU settings
    gpu_index: 0
    enable_memory_pool: true
    memory_pool_size: 1073741824  # 1GB

    # Processing settings
    max_batch_size: 1
    processing_rate: 30
    enable_padding: false
```

### Pipeline Parallelization

Configure pipeline stages to run in parallel:

```python
# parallel_pipeline_config.py
from launch import LaunchDescription
from launch.actions import GroupAction
from launch_ros.actions import Node, PushRosNamespace

def generate_launch_description():
    return LaunchDescription([
        # Parallel preprocessing group
        GroupAction(
            actions=[
                PushRosNamespace('preprocessing'),

                # Image rectification
                Node(
                    package='isaac_ros_image_proc',
                    executable='isaac_ros_image_rectify_node',
                    name='rectifier_1',
                    parameters=[{'processing_rate': 30}],
                    remappings=[
                        ('image_raw', 'camera_1/image_raw'),
                        ('image_rect', 'camera_1/image_rect'),
                    ]
                ),
            ]
        ),

        # Parallel inference group
        GroupAction(
            actions=[
                PushRosNamespace('inference'),

                # Object detection
                Node(
                    package='isaac_ros_detectnet',
                    executable='isaac_ros_detectnet',
                    name='detector_1',
                    parameters=[{
                        'input_width': 640,
                        'input_height': 480,
                        'processing_rate': 15,
                        'gpu_index': 0,
                    }],
                    remappings=[
                        ('image_input', 'preprocessing/camera_1/image_rect'),
                        ('detections_output', 'camera_1/detections'),
                    ]
                ),
            ]
        )
    ])
```

## Quick Setup

### Minimal Pipeline Configuration

For getting started quickly:

```bash
# Launch a basic object detection pipeline
ros2 launch isaac_ros_detectnet isaac_ros_detectnet.launch.py \
  model_name:=ssd_mobilenet_v2_coco \
  input_width:=640 \
  input_height:=480 \
  confidence_threshold:=0.5
```