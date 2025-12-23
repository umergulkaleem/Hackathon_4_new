---
sidebar_position: 11
title: Setup Requirements
---

# Setup Requirements: Vision-Language-Action (VLA) Module

This document outlines the setup requirements and dependencies needed to implement and run the Vision-Language-Action systems covered in this module.

## System Requirements

### Hardware Requirements
- **CPU**: Multi-core processor (4+ cores recommended)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB free space for development environment
- **Network**: Stable internet connection for OpenAI API access
- **Microphone**: For voice command input (USB or built-in)
- **Camera**: For object recognition (optional for simulation)

### Software Requirements
- **Operating System**: Ubuntu 22.04 LTS or Windows 10/11
- **Docker**: Version 20.10 or higher
- **Python**: Version 3.8-3.11
- **ROS 2**: Humble Hawksbill distribution

## Development Environment Setup

### 1. ROS 2 Installation
```bash
# For Ubuntu
sudo apt update && sudo apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo apt-key add -
echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install ros-humble-desktop
sudo apt install python3-rosdep2 python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
```

### 2. Python Dependencies
```bash
pip install openai speech-recognition numpy matplotlib opencv-python cv-bridge
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 3. OpenAI API Configuration
```bash
# Set your OpenAI API key as an environment variable
export OPENAI_API_KEY="your-api-key-here"

# Or add to your shell profile (~/.bashrc or ~/.zshrc)
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
```

## Docker Environment Setup

### 1. ROS 2 Docker Image
```dockerfile
FROM ros:humble-ros-base

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install openai speech-recognition numpy matplotlib opencv-python

# Set ROS environment
ENV ROS_DISTRO=humble
ENV ROS_ROOT=/opt/ros/humble
ENV PATH=/opt/ros/humble/bin:$PATH
ENV PYTHONPATH=/opt/ros/humble/lib/python3.10/site-packages:$PYTHONPATH
ENV LD_LIBRARY_PATH=/opt/ros/humble/lib:$LD_LIBRARY_PATH

WORKDIR /workspace
```

### 2. Docker Compose for Simulation
```yaml
version: '3.8'
services:
  ros2-core:
    image: ros:humble-ros-base
    volumes:
      - ./src:/workspace/src
    environment:
      - ROS_DOMAIN_ID=4
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    network_mode: host
    command: >
      bash -c "source /opt/ros/humble/setup.bash &&
               cd /workspace &&
               bash"

  simulation:
    image: osrf/ros:humble-desktop-full
    environment:
      - DISPLAY=${DISPLAY}
      - QT_X11_NO_MITSHM=1
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
      - ./models:/root/.gazebo/models
    network_mode: host
    command: >
      bash -c "source /opt/ros/humble/setup.bash &&
               gazebo --verbose"
```

## Project Structure Setup

### 1. Create Workspace
```bash
mkdir -p ~/vla_ws/src
cd ~/vla_ws
colcon build
source install/setup.bash
```

### 2. Package Structure
```
vla_ws/
├── src/
│   ├── vla_voice_interface/
│   ├── vla_cognitive_planner/
│   ├── vla_robot_executor/
│   └── vla_examples/
├── build/
├── install/
└── log/
```

### 3. Example Package Creation
```bash
cd ~/vla_ws/src
ros2 pkg create --build-type ament_python vla_voice_interface
ros2 pkg create --build-type ament_python vla_cognitive_planner
ros2 pkg create --build-type ament_python vla_robot_executor
```

## API Keys and Authentication

### 1. OpenAI API Key
- Visit https://platform.openai.com/api-keys
- Create a new secret key
- Save it securely and set as environment variable

### 2. Rate Limits and Costs
- Check your OpenAI usage at https://platform.openai.com/usage
- Monitor costs at https://platform.openai.com/settings/organization/billing/usage
- Consider using fine-tuned models for cost optimization

## Simulation Environment

### 1. Gazebo Setup
```bash
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-ros2-control
sudo apt install ros-humble-gazebo-ros2-control-demos
```

### 2. Navigation2 Setup
```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
sudo apt install ros-humble-slam-toolbox
```

### 3. Create Simulation World
```bash
# Create a simple world file for testing
mkdir -p ~/vla_ws/src/vla_examples/worlds
# Add your world file content here
```

## Testing and Validation Setup

### 1. Unit Testing
```bash
pip install pytest pytest-ros
```

### 2. Integration Testing
```bash
# Example test structure
mkdir -p ~/vla_ws/src/vla_tests/test
# Add test files
```

### 3. Performance Testing
```bash
# Install ROS 2 testing tools
sudo apt install ros-humble-test-msgs ros-humble-launch-testing
```

## Troubleshooting Common Setup Issues

### 1. ROS 2 Environment Not Sourced
```bash
# Add to ~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 2. Python Package Import Errors
```bash
# Ensure packages are installed in the correct Python environment
python3 -c "import openai; print(openai.__version__)"
```

### 3. Docker Permission Issues
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and log back in for changes to take effect
```

## Optional: Development Tools

### 1. VS Code Extensions
- ROS
- Python
- Docker
- Remote - Containers

### 2. Additional Tools
```bash
# ROS 2 command line tools
sudo apt install python3-ros2cli
sudo apt install ros-humble-rqt*

# Visualization tools
sudo apt install ros-humble-rviz2
```

## Quick Start Verification

After completing the setup, verify your installation with:

```bash
# Check ROS 2 installation
ros2 --version

# Check Python packages
python3 -c "import openai, speech_recognition, cv2; print('All packages imported successfully')"

# Source workspace
cd ~/vla_ws && source install/setup.bash

# Run a simple test
ros2 run demo_nodes_py talker
```

## Next Steps

Once your environment is set up, proceed with:

1. [Chapter 1: Voice-to-Action Interfaces](./chapter1-voice-to-action.md)
2. [Chapter 2: Cognitive Planning with LLMs](./chapter2-cognitive-planning.md)
3. [Chapter 3: Capstone - Autonomous Humanoid](./chapter3-capstone.md)

Remember to regularly update your packages and monitor your API usage to ensure smooth development experience.