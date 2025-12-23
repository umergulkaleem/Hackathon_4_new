# Isaac ROS Installation and Setup with GPU Acceleration

## Overview

This guide provides detailed instructions for installing and configuring NVIDIA Isaac ROS with GPU acceleration. Isaac ROS packages leverage NVIDIA's GPU computing capabilities to accelerate compute-intensive robotics algorithms for real-time perception and navigation tasks.

## System Requirements

### Hardware Requirements

#### GPU Requirements
- **Minimum**: NVIDIA GPU with compute capability 6.0+ (Pascal architecture or newer)
- **Recommended**: NVIDIA RTX series GPU (RTX 3080 or higher)
- **VRAM**: Minimum 8GB (16GB+ recommended for complex perception tasks)
- **Supported GPUs**:
  - RTX Series: RTX 30xx, RTX 40xx
  - Professional: RTX A-series, Quadro series
  - Data Center: A100, V100
  - Embedded: Jetson AGX Orin, Jetson Xavier NX

#### System Requirements
- **CPU**: Multi-core processor (Intel i7 or AMD Ryzen 7 recommended)
- **RAM**: 16GB minimum, 32GB+ recommended
- **Storage**: 50GB free space for Isaac ROS packages
- **Network**: High-speed connection for Docker image pulls

### Software Requirements

#### Operating System
- **Ubuntu 22.04 LTS** (recommended)
- **Ubuntu 20.04 LTS** (supported)
- **Real-time kernel** (optional, for deterministic applications)

#### Prerequisites
- **ROS 2**: Humble Hawksbill distribution
- **CUDA Toolkit**: Version 11.8 or later
- **NVIDIA Drivers**: Version 470 or later
- **Docker**: Version 20.10 or later (for containerized deployment)
- **Python**: 3.8 to 3.10

## Prerequisites Installation

### 1. Install ROS 2 Humble

```bash
# Set locale
locale  # check for UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 apt repository
sudo apt update && sudo apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros-keyring.gpg | sudo apt-key add -

# Add ROS 2 repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/lib/apt/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update package lists and install ROS 2
sudo apt update
sudo apt install ros-humble-desktop
sudo apt install python3-colcon-common-extensions
sudo apt install python3-rosdep python3-vcstool
```

### 2. Install NVIDIA Drivers and CUDA

```bash
# Update package lists
sudo apt update

# Install NVIDIA drivers
sudo apt install nvidia-driver-535

# Install CUDA toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-0

# Reboot to load drivers
sudo reboot
```

### 3. Install Docker (for containerized deployment)

```bash
# Install Docker
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## Isaac ROS Installation Methods

### Method 1: Package Installation (Recommended)

Install Isaac ROS packages using apt package manager:

```bash
# Update package lists
sudo apt update

# Install Isaac ROS perception meta-package (includes most common packages)
sudo apt install ros-humble-isaac-ros-perception

# Install specific Isaac ROS packages individually
sudo apt install ros-humble-isaac-ros-visual-slam
sudo apt install ros-humble-isaac-ros-detectnet
sudo apt install ros-humble-isaac-ros-segmentation
sudo apt install ros-humble-isaac-ros-stereo-image-proc
sudo apt install ros-humble-isaac-ros-message-filters
sudo apt install ros-humble-isaac-ros-ros2-babel-pipe

# Install navigation-related packages
sudo apt install ros-humble-isaac-ros-navigation
sudo apt install ros-humble-isaac-ros-ros2-control-components
```

### Method 2: Docker Installation

Pull Isaac ROS Docker images for containerized deployment:

```bash
# Pull core Isaac ROS images
docker pull nvcr.io/nvidia/isaac-ros/isaac_ros_visual_slam:latest
docker pull nvcr.io/nvidia/isaac-ros/isaac_ros_detectnet:latest
docker pull nvcr.io/nvidia/isaac-ros/isaac_ros_segmentation:latest
docker pull nvcr.io/nvidia/isaac-ros/isaac_ros_stereo_image_proc:latest
docker pull nvcr.io/nvidia/isaac-ros/isaac_ros_compressed_image_transport:latest

# Pull additional utility images
docker pull nvcr.io/nvidia/isaac-ros/isaac_ros_image_pipeline:latest
docker pull nvcr.io/nvidia/isaac-ros/isaac_ros_apriltag:latest
docker pull nvcr.io/nvidia/isaac-ros/isaac_ros_people_seg_pose:latest
```

### Method 3: Source Installation (Advanced)

For development or custom builds:

```bash
# Create colcon workspace
mkdir -p ~/isaac_ros_ws/src
cd ~/isaac_ros_ws

# Clone Isaac ROS repositories
git clone -b humble https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git src/isaac_ros_common
git clone -b humble https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam.git src/isaac_ros_visual_slam
git clone -b humble https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_detectnet.git src/isaac_ros_detectnet
git clone -b humble https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_segmentation.git src/isaac_ros_segmentation

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build workspace
colcon build --symlink-install
```

## Environment Setup

### 1. ROS 2 Environment Configuration

Create a setup script to ensure proper environment configuration:

```bash
#!/bin/bash
# isaac_ros_setup.sh

# Source ROS 2
source /opt/ros/humble/setup.bash

# Source Isaac ROS if built from source
if [ -f ~/isaac_ros_ws/install/setup.bash ]; then
    source ~/isaac_ros_ws/install/setup.bash
fi

# Set Isaac ROS specific environment variables
export ISAAC_ROS_WS=~/isaac_ros_ws
export ISAAC_ROS_PACKAGE_PATH=~/isaac_ros_ws/install
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda

# Set ROS domain ID (adjust as needed for multi-robot systems)
export ROS_DOMAIN_ID=0

# Set FastDDS configuration for Isaac ROS
export FASTDDS_DEFAULT_PROFILES_FILE=~/isaac_ros_ws/install/share/isaac_ros_common/config/profiles.xml

echo "Isaac ROS environment configured"
echo "ROS_DISTRO: $ROS_DISTRO"
echo "CUDA_PATH: $CUDA_HOME"
echo "Isaac ROS Workspace: $ISAAC_ROS_WS"
```

### 2. GPU Access Configuration

Ensure GPU access for Isaac ROS applications:

```bash
# Verify GPU access
nvidia-smi

# Check CUDA installation
nvcc --version

# Test CUDA sample (optional)
cd /usr/local/cuda/samples/1_Utilities/deviceQuery
sudo make
./deviceQuery
```

## Verification of Installation

### 1. Check Isaac ROS Packages

Verify that Isaac ROS packages are properly installed:

```bash
# Check for Isaac ROS packages
ros2 pkg list | grep isaac_ros

# Should show output like:
# isaac_ros_visual_slam
# isaac_ros_detectnet
# isaac_ros_segmentation
# isaac_ros_stereo_image_proc
# etc.

# Check specific package information
ros2 pkg info isaac_ros_visual_slam
ros2 pkg info isaac_ros_detectnet
```

### 2. Test GPU Acceleration

Test that GPU acceleration is working:

```bash
# Run a simple Isaac ROS node to test GPU access
ros2 run isaac_ros_visual_slam visual_slam_node --ros-args --log-level info

# Check if GPU memory is allocated
watch -n 1 nvidia-smi
```

### 3. Launch Sample Applications

Test installation with sample launch files:

```bash
# Launch Isaac ROS Visual SLAM demo (if Isaac Sim is available)
ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam.launch.py

# Launch Isaac ROS DetectNet demo
ros2 launch isaac_ros_detectnet isaac_ros_detectnet.launch.py

# Launch stereo image processing demo
ros2 launch isaac_ros_stereo_image_proc isaac_ros_stereo_image_proc.launch.py
```

## GPU Acceleration Configuration

### 1. CUDA Configuration

Ensure CUDA is properly configured for Isaac ROS:

```bash
# Check CUDA device properties
python3 -c "
import torch
print('CUDA available:', torch.cuda.is_available())
print('CUDA device count:', torch.cuda.device_count())
if torch.cuda.is_available():
    print('Current CUDA device:', torch.cuda.current_device())
    print('Device name:', torch.cuda.get_device_name())
"

# For non-PyTorch CUDA checks
nvidia-ml-py3 -c "import pynvml; pynvml.nvmlInit(); print('NVML initialized successfully')"
```

### 2. Isaac ROS Parameter Configuration

Configure Isaac ROS nodes for optimal GPU usage:

```yaml
# isaac_ros_gpu_config.yaml
/**:
  ros__parameters:
    # GPU device index (0 for first GPU, 1 for second, etc.)
    gpu_index: 0

    # Memory pool configuration
    enable_memory_pool: true
    memory_pool_size: 1073741824  # 1GB pool size

    # Batch processing configuration
    max_batch_size: 1
    batch_timeout_us: 1000

    # Precision settings
    precision_mode: 'FP16'  # or 'FP32' depending on GPU capability
```

### 3. Performance Optimization Settings

Configure performance settings for Isaac ROS:

```bash
# Set environment variables for performance optimization
export CUDA_CACHE_MAXSIZE=2147483648  # 2GB cache
export CUDA_CACHE_PATH=/tmp/.nv/ComputeCache
export __GL_SHADER_DISK_CACHE_PATH=/tmp/.nv/GLCache

# Set up memory management
ulimit -l unlimited  # Remove memory lock limit for shared memory
```

## Troubleshooting Common Issues

### Installation Issues

**Problem**: Isaac ROS packages not found after installation
- **Solution**:
  ```bash
  # Verify ROS 2 Humble is sourced
  source /opt/ros/humble/setup.bash

  # Check if packages are installed
  dpkg -l | grep ros-humble-isaac-ros

  # If not installed, reinstall
  sudo apt update
  sudo apt install ros-humble-isaac-ros-perception
  ```

**Problem**: CUDA not found or GPU not detected
- **Solution**:
  ```bash
  # Check NVIDIA driver installation
  nvidia-smi

  # Check CUDA installation
  which nvcc
  nvcc --version

  # Reinstall CUDA if needed
  sudo apt install cuda-toolkit-12-0
  ```

### GPU Access Issues

**Problem**: Isaac ROS nodes fail with GPU memory errors
- **Solution**:
  1. Check available GPU memory: `nvidia-smi`
  2. Reduce input resolution or batch size
  3. Close other GPU-intensive applications
  4. Verify GPU compute capability is sufficient

**Problem**: Permission denied accessing GPU
- **Solution**:
  ```bash
  # Add user to video group
  sudo usermod -aG video $USER

  # Add user to render group (for some systems)
  sudo usermod -aG render $USER

  # Log out and log back in for changes to take effect
  ```

### Docker Issues

**Problem**: Docker containers fail to access GPU
- **Solution**:
  ```bash
  # Verify nvidia-container-toolkit is installed and configured
  sudo nvidia-ctk runtime configure --runtime=docker

  # Restart Docker daemon
  sudo systemctl restart docker

  # Test GPU access in container
  docker run --rm --gpus all nvidia/cuda:12.0-base-ubuntu22.04 nvidia-smi
  ```

### Performance Issues

**Problem**: Isaac ROS nodes running slowly
- **Solution**:
  1. Check GPU utilization: `nvidia-smi`
  2. Verify input data rate matches processing capability
  3. Check for CPU bottlenecks with `htop`
  4. Optimize pipeline by reducing input resolution if possible

**Problem**: High memory usage
- **Solution**:
  1. Monitor memory usage: `nvidia-smi` and `htop`
  2. Reduce pipeline buffer sizes
  3. Optimize data transport settings
  4. Consider using compressed image transport

## Best Practices

### Installation Best Practices

1. **Use Package Installation**: For production systems, use apt packages
2. **Maintain Clean Environment**: Keep system updated and clean
3. **Monitor Resources**: Regularly monitor GPU and system resources
4. **Document Configuration**: Keep records of working configurations

### Performance Best Practices

1. **Match Hardware to Requirements**: Ensure GPU capabilities match application needs
2. **Optimize Pipeline**: Configure pipelines for your specific use case
3. **Monitor Performance**: Use Isaac ROS performance monitoring tools
4. **Plan for Scalability**: Design systems that can scale with hardware

### Development Workflow

1. **Test Incrementally**: Start with simple configurations
2. **Monitor Metrics**: Track performance and resource usage
3. **Validate Results**: Verify output quality and accuracy
4. **Document Changes**: Keep track of configuration changes

## Testing the Installation

### Basic Functionality Test

Create a simple test to verify Isaac ROS is working:

```bash
#!/bin/bash
# test_isaac_ros_installation.sh

echo "Testing Isaac ROS Installation..."

# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Check for Isaac ROS packages
echo "Checking Isaac ROS packages..."
PACKAGES=$(ros2 pkg list | grep isaac_ros | wc -l)
echo "Found $PACKAGES Isaac ROS packages"

if [ $PACKAGES -gt 0 ]; then
    echo "✓ Isaac ROS packages detected"
else
    echo "✗ No Isaac ROS packages found"
    exit 1
fi

# Check GPU access
echo "Checking GPU access..."
if nvidia-smi > /dev/null 2>&1; then
    echo "✓ GPU accessible"
else
    echo "✗ GPU not accessible"
    exit 1
fi

# Test CUDA
echo "Checking CUDA..."
if nvcc --version > /dev/null 2>&1; then
    echo "✓ CUDA available"
else
    echo "✗ CUDA not available"
    exit 1
fi

echo "Installation test completed successfully!"
echo "Isaac ROS is ready for use."
```

### Performance Test

Run a basic performance test:

```bash
# Run Isaac ROS Visual SLAM node briefly to test functionality
timeout 10s ros2 run isaac_ros_visual_slam visual_slam_node --ros-args --log-level warn

# Check if node ran without errors
if [ $? -eq 0 ]; then
    echo "✓ Isaac ROS node executed successfully"
else
    echo "✗ Isaac ROS node execution failed"
fi
```

## Verification Checklist

Before proceeding, verify the following:

- [ ] ROS 2 Humble is properly installed and sourced
- [ ] NVIDIA drivers and CUDA are properly installed
- [ ] Isaac ROS packages are installed via apt
- [ ] GPU is accessible and detected by system
- [ ] Isaac ROS nodes can be launched successfully
- [ ] Docker and nvidia-container-toolkit are configured (if using containers)
- [ ] Environment variables are properly set
- [ ] Performance benchmarks meet requirements

## Next Steps

After successful installation and configuration:

1. **Explore Examples**: Run Isaac ROS example applications
2. **Configure Pipelines**: Set up perception pipelines for your application
3. **Integrate with Navigation**: Connect perception to navigation systems
4. **Optimize Performance**: Fine-tune for your specific requirements

This installation guide provides the foundation for using Isaac ROS with GPU acceleration, enabling you to build high-performance robotics perception applications.