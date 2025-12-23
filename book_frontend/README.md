# ROS 2 Fundamentals for Humanoid Robotics

This educational module teaches Computer Science students with Python and basic AI knowledge how to use ROS 2 as middleware connecting AI agents to humanoid robot control systems.

## Overview

This course covers:
- ROS 2 fundamentals: architecture, ROS graph, and middleware concepts
- ROS 2 communication patterns: nodes, topics, services, and actions
- Python AI agents using rclpy for robot control
- Humanoid modeling with URDF (Unified Robot Description Format)
- Digital twin simulation with Gazebo and Unity
- Advanced perception and navigation with NVIDIA Isaac technologies

## Prerequisites

- Basic Python programming knowledge
- Fundamental understanding of AI concepts
- Interest in robotics

## Getting Started

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## Course Structure

The course is organized into multiple modules:

1. **Module 1: The Robotic Nervous System (ROS 2)**: Learn the core concepts of ROS 2 architecture, communication patterns, and URDF modeling
2. **Module 2: The Digital Twin (Gazebo & Unity)**: Understand physics simulation with Gazebo and high-fidelity rendering with Unity, plus integration techniques for digital twin applications
3. **Module 3: The AI-Robot Brain (NVIDIA Isaac™)**: Explore advanced perception, navigation, and training of humanoid robots using NVIDIA Isaac technologies, including Isaac Sim for photorealistic simulation, Isaac ROS for hardware-accelerated perception, and Nav2 for humanoid navigation

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)

This module covers:
- **Chapter 1: NVIDIA Isaac Sim** - Photorealistic simulation and synthetic data generation
- **Chapter 2: Isaac ROS** - Hardware-accelerated perception and visual SLAM
- **Chapter 3: Nav2 for Humanoid Navigation** - Path planning and navigation for bipedal robots

#### Key Topics in Module 3:
- Isaac Sim for photorealistic simulation environments
- Isaac ROS for hardware-accelerated perception pipelines
- Visual SLAM implementation with Isaac ROS packages
- Sensor processing with GPU acceleration
- Nav2 configuration for humanoid robots with bipedal locomotion
- Performance optimization techniques for perception pipelines
- Integration of perception and navigation systems

## Interactive Examples

The course includes practical examples in various directories:
- Python examples in `docs/tutorials/python-examples/`
- Isaac Sim examples in `docs/tutorials/isaac-sim-examples/`
- Isaac ROS examples in `docs/tutorials/isaac-ros-examples/`
- Nav2 examples in `docs/tutorials/nav2-examples/`
- URDF models in `docs/tutorials/urdf-examples/`

## Assessment

Test your knowledge with interactive assessments throughout the course to validate your understanding of ROS 2, simulation, perception, and navigation concepts.

## Deployment

This site is built with Docusaurus and can be deployed to GitHub Pages or any static hosting service.

## Contributing

This educational module is designed for students learning ROS 2 for humanoid robotics applications. Contributions to improve the content or add new examples are welcome.