# Isaac Sim Installation and Setup with ROS 2 Integration

## Overview

This guide provides detailed instructions for installing NVIDIA Isaac Sim and setting up integration with ROS 2. This process enables you to create photorealistic simulations of humanoid robots that can communicate with external ROS 2 systems.

## System Requirements

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support (GTX 1060 6GB or better)
  - Compute Capability 6.0 or higher
  - At least 8GB VRAM recommended (10GB+ preferred)
- **CPU**: Intel Core i7 or AMD Ryzen 7 with 8+ cores
- **RAM**: 32GB system memory (16GB minimum)
- **Storage**: 50GB free SSD space
- **OS**: Ubuntu 22.04 LTS (recommended) or Windows 10/11 (64-bit)

### Software Requirements
- **ROS 2**: Humble Hawksbill distribution
- **CUDA**: Version 11.8 or later
- **NVIDIA Drivers**: Version 470 or later
- **Python**: 3.8 to 3.10

## Installation Methods

### Method 1: Omniverse Launcher (Recommended)

The Omniverse Launcher is the easiest way to install Isaac Sim:

1. **Download Omniverse Launcher**:
   - Visit the [NVIDIA Developer website](https://developer.nvidia.com/omniverse/download)
   - Download and install the Omniverse Launcher
   - Create or sign in with your NVIDIA Developer account

2. **Install Isaac Sim**:
   - Launch the Omniverse Launcher
   - Go to the "Extensions" tab
   - Search for "Isaac Sim"
   - Click "Install" to download and install Isaac Sim

3. **Configure Isaac Sim**:
   - Launch Isaac Sim from the launcher
   - Accept the End User License Agreement (EULA)
   - Configure initial settings (graphics quality, paths, etc.)

### Method 2: Docker Installation

For containerized deployment or when you need more control:

```bash
# Pull the latest Isaac Sim Docker image
docker pull nvcr.io/nvidia/isaac-sim:latest

# Create a local directory for Isaac Sim data
mkdir -p ~/isaac_sim_data

# Run Isaac Sim container with GUI support
xhost +local:docker
docker run --gpus all \
  --rm \
  --network=host \
  --env "ACCEPT_EULA=Y" \
  --env "NVIDIA_VISIBLE_DEVICES=all" \
  --env "NVIDIA_DRIVER_CAPABILITIES=all" \
  --volume ~/isaac_sim_data:/isaac_sim_data \
  --volume /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --volume /dev/shm:/dev/shm \
  --env DISPLAY=$DISPLAY \
  nvcr.io/nvidia/isaac-sim:latest
```

### Method 3: Local Installation

For advanced users who want to build from source:

1. **Install Prerequisites**:
   ```bash
   # Install system dependencies
   sudo apt update
   sudo apt install -y build-essential cmake git python3-dev python3-pip

   # Install NVIDIA drivers and CUDA
   sudo apt install -y nvidia-driver-535 nvidia-utils-535
   sudo apt install -y nvidia-cuda-toolkit
   ```

2. **Install Isaac Sim**:
   - Download the Isaac Sim installer from NVIDIA Developer website
   - Run the installer with appropriate permissions
   - Follow the installation wizard

## ROS 2 Integration Setup

### Prerequisites

Before setting up ROS 2 integration, ensure you have:

1. **ROS 2 Humble Hawksbill** installed:
   ```bash
   # Add ROS 2 repository
   sudo apt update && sudo apt install -y curl gnupg lsb-release
   curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo apt-key add -
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/lib/apt/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

   # Install ROS 2 packages
   sudo apt update
   sudo apt install -y ros-humble-desktop
   sudo apt install -y python3-colcon-common-extensions
   sudo apt install -y python3-rosdep
   ```

2. **Source ROS 2 environment**:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

### Isaac ROS Bridge Installation

1. **Install Isaac ROS Packages**:
   ```bash
   # Update package lists
   sudo apt update

   # Install Isaac ROS packages
   sudo apt install -y ros-humble-isaac-ros-*

   # Install specific packages you'll need
   sudo apt install -y \
     ros-humble-isaac-ros-camera \
     ros-humble-isaac-ros-composition \
     ros-humble-isaac-ros-diff-nav \
     ros-humble-isaac-ros-gps-teleop \
     ros-humble-isaac-ros-gxf \
     ros-humble-isaac-ros-manipulation \
     ros-humble-isaac-ros-message-relay \
     ros-humble-isaac-ros-metrics \
     ros-humble-isaac-ros-navigation \
     ros-humble-isaac-ros-ros2-behavior-tree \
     ros-humble-isaac-ros-segmentation-pose-cnn \
     ros-humble-isaac-ros-teleop \
     ros-humble-isaac-ros-visual-slam
   ```

2. **Verify Installation**:
   ```bash
   # Check if Isaac ROS packages are available
   ros2 pkg list | grep isaac_ros

   # Should show a list of Isaac ROS packages
   ```

### ROS Bridge Configuration in Isaac Sim

1. **Enable Extensions**:
   - Launch Isaac Sim
   - Go to Window > Extensions
   - Enable the following extensions:
     - `omni.isaac.ros2_bridge.humble` (or your ROS 2 version)
     - `omni.isaac.ros_bridge` (if needed for specific functionality)

2. **Configure ROS Domain**:
   - Set the ROS domain ID to avoid conflicts with other ROS systems
   - In Isaac Sim, you can set this through the ROS bridge extension settings
   - Or set the environment variable: `export ROS_DOMAIN_ID=0`

3. **Network Configuration**:
   - Ensure proper network setup for multi-machine communication
   - Configure Fast DDS or Cyclone DDS as needed
   - Set up firewall rules if necessary

### Environment Setup Script

Create a setup script to ensure proper environment configuration:

```bash
#!/bin/bash
# isaac_sim_ros_setup.sh

# Source ROS 2
source /opt/ros/humble/setup.bash

# Set Isaac Sim specific environment variables
export ISAACSIM_PATH="/path/to/isaacsim"  # Adjust to your installation path
export OMNI_USER="your_username"
export OMNI_PASS="your_password"  # If required

# Set ROS domain (adjust as needed)
export ROS_DOMAIN_ID=0

# Set Fast DDS configuration
export FASTDDS_DEFAULT_PROFILES_FILE="$ISAACSIM_PATH/dds_config/profiles.xml"

echo "Environment configured for Isaac Sim with ROS 2 integration"
echo "ROS_DOMAIN_ID: $ROS_DOMAIN_ID"
echo "ROS_DISTRO: $ROS_DISTRO"
```

## Testing the Integration

### Basic Connection Test

1. **Launch Isaac Sim**:
   ```bash
   # Source your ROS environment
   source /opt/ros/humble/setup.bash

   # Launch Isaac Sim
   cd ~/isaac-sim
   python3 launcher.py
   ```

2. **Verify ROS Connection**:
   ```bash
   # In a new terminal, after Isaac Sim is running
   source /opt/ros/humble/setup.bash

   # Check for ROS topics
   ros2 topic list

   # You should see Isaac Sim topics if the bridge is working
   ```

### Camera Integration Test

Create a simple test to verify camera data is being published:

1. **In Isaac Sim**:
   - Create a new stage (File > New Stage)
   - Add a camera: Create > Camera
   - Position the camera to view something interesting
   - Add the ROS Camera Bridge component to the camera

2. **In Terminal**:
   ```bash
   # Verify camera topic is available
   ros2 topic list | grep camera

   # Echo camera info
   ros2 topic echo /camera_info

   # Save a camera image
   ros2 run image_view image_saver image:=/rgb_image
   ```

### Robot Integration Test

Test with a simple robot model:

1. **Import a Robot**:
   - In Isaac Sim, go to File > Import > URDF
   - Select a simple robot model (like the default robot)
   - Configure as an Articulation for better physics

2. **Set Up ROS Bridge for Robot**:
   - Add ROS bridge components for joint states
   - Add ROS bridge components for robot state publisher

3. **Verify in Terminal**:
   ```bash
   # Check joint states
   ros2 topic echo /joint_states

   # Check robot description
   ros2 param get /robot_state_publisher robot_description
   ```

## Troubleshooting Common Issues

### Installation Issues

**Problem**: Isaac Sim fails to launch
- **Solution**:
  1. Check GPU drivers: `nvidia-smi`
  2. Verify CUDA installation: `nvcc --version`
  3. Ensure sufficient VRAM available
  4. Check logs in `~/isaac_sim_logs/`

**Problem**: ROS bridge extension not available
- **Solution**:
  1. Verify ROS 2 Humble is properly installed
  2. Check that the correct extension name is used
  3. Ensure Isaac Sim was built with ROS support

### Connection Issues

**Problem**: Isaac Sim topics not appearing in ROS
- **Solution**:
  1. Verify ROS domain IDs match
  2. Check firewall settings
  3. Ensure both systems are on same network (for multi-machine)
  4. Verify ROS bridge components are added to Isaac Sim objects

**Problem**: High latency in data transmission
- **Solution**:
  1. Reduce data resolution if possible
  2. Check network bandwidth
  3. Verify QoS settings match between publisher/subscriber
  4. Monitor system resources

### Performance Issues

**Problem**: Isaac Sim running slowly
- **Solution**:
  1. Reduce rendering quality temporarily
  2. Simplify scene complexity
  3. Check GPU memory usage: `nvidia-smi`
  4. Close unnecessary applications

## Best Practices

### Installation Best Practices
- Use SSD storage for Isaac Sim installation for better performance
- Ensure adequate cooling for sustained GPU usage
- Keep NVIDIA drivers updated for optimal performance
- Install Isaac Sim in a location with sufficient free space

### Integration Best Practices
- Use consistent coordinate frames between Isaac Sim and ROS
- Configure appropriate QoS settings for real-time performance
- Monitor resource usage during simulation
- Use proper error handling in your ROS nodes

### Development Workflow
- Test components individually before integration
- Use version control for your simulation scenes
- Document your ROS interface clearly
- Validate data quality before using in training

## Verification Checklist

Before proceeding, verify the following:

- [ ] Isaac Sim launches without errors
- [ ] ROS 2 Humble is properly installed and sourced
- [ ] Isaac ROS bridge extension is enabled
- [ ] Isaac Sim can publish to ROS topics
- [ ] ROS nodes can subscribe to Isaac Sim topics
- [ ] Camera data is being published correctly
- [ ] Robot joint states are being published
- [ ] TF tree is properly populated

Once all items are verified, you're ready to proceed with more advanced Isaac Sim and ROS integration tasks.