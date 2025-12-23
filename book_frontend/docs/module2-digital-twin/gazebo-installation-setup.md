# Gazebo Installation and Setup with ROS 2 Integration

## Overview

This guide will walk you through the process of installing Gazebo Garden (Fortress) and integrating it with ROS 2 Humble Hawksbill. This setup is essential for creating physics-based simulations of humanoid robots that can communicate with ROS 2 nodes.

## System Requirements

Before installing Gazebo and setting up ROS 2 integration, ensure your system meets the following requirements:

### Minimum Requirements
- **Operating System**: Ubuntu 22.04 LTS or Windows 10/11 with WSL2
- **CPU**: Multi-core processor (Intel i5/Ryzen 5 or better recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space for Gazebo installation
- **Graphics**: OpenGL 2.1 compatible GPU with updated drivers
- **Network**: Internet connection for package installation

### Recommended Requirements
- **Operating System**: Ubuntu 22.04 LTS
- **CPU**: Intel i7 or AMD Ryzen 7 with 8+ cores
- **RAM**: 16GB or more
- **Storage**: 20GB SSD for faster loading
- **Graphics**: Dedicated GPU with 4GB+ VRAM for advanced visualization

## Installing ROS 2 Humble Hawksbill

### Ubuntu Installation

1. **Set up the ROS 2 apt repository**:
```bash
sudo apt update && sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
```

2. **Add the repository to your sources list**:
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

3. **Install ROS 2 packages**:
```bash
sudo apt update
sudo apt install ros-humble-desktop ros-humble-dev-tools
sudo apt install python3-rosdep2 python3-vcstool
```

4. **Initialize rosdep**:
```bash
sudo rosdep init
rosdep update
```

5. **Source the ROS 2 environment**:
```bash
source /opt/ros/humble/setup.bash
```

6. **Make the environment permanent** by adding it to your shell:
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

## Installing Gazebo Garden (Fortress)

### Ubuntu Installation

1. **Add the Gazebo apt repository**:
```bash
sudo apt install ubuntu-keyring
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/gazebo-archive-keyring.gpg --keyserver keyserver.ubuntu.com --recv-keys C3173AA6
```

2. **Add the repository to your sources list**:
```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/gazebo-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo.list > /dev/null
```

3. **Install Gazebo Garden**:
```bash
sudo apt update
sudo apt install gz-harmonic
```

4. **Verify the installation**:
```bash
gz --version
```

## Setting Up ROS 2 Gazebo Integration

### Install Gazebo ROS Packages

1. **Install the Gazebo ROS packages**:
```bash
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-ros2-control
```

2. **Install additional simulation tools**:
```bash
sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers
sudo apt install ros-humble-joint-state-publisher ros-humble-robot-state-publisher
```

### Environment Setup

1. **Create a setup script** to source both ROS 2 and Gazebo environments:
```bash
#!/bin/bash
# Setup script for ROS 2 and Gazebo integration
source /opt/ros/humble/setup.bash
source /usr/share/gz/setup.sh
```

2. **Save this script** as `setup_env.sh` in your home directory:
```bash
nano ~/setup_env.sh
```

3. **Make the script executable**:
```bash
chmod +x ~/setup_env.sh
```

4. **Add to your shell profile**:
```bash
echo "source ~/setup_env.sh" >> ~/.bashrc
```

## Testing the Integration

### Basic Gazebo Launch

1. **Source your environment**:
```bash
source ~/setup_env.sh
```

2. **Launch a basic Gazebo world**:
```bash
gz sim
```

### ROS 2 Communication Test

1. **Open a new terminal** and source the environment:
```bash
source ~/setup_env.sh
```

2. **List available ROS 2 topics**:
```bash
ros2 topic list
```

3. **Check if Gazebo is publishing topics** (in another terminal):
```bash
source ~/setup_env.sh
ros2 topic list | grep gazebo
```

### Launch Gazebo with ROS 2 Bridge

1. **Create a simple world file** (`test_world.sdf`):
```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="test_world">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>

    <model name="box">
      <pose>0 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

2. **Launch the world**:
```bash
gz sim -r test_world.sdf
```

## Creating a Workspace for Simulation Development

### Setting Up a ROS 2 Workspace

1. **Create the workspace directory**:
```bash
mkdir -p ~/gazebo_ros2_ws/src
cd ~/gazebo_ros2_ws
```

2. **Source the ROS 2 environment**:
```bash
source /opt/ros/humble/setup.bash
```

3. **Build the workspace** (even without packages yet):
```bash
colcon build --packages-select
```

4. **Source the workspace**:
```bash
source install/setup.bash
```

### Adding Simulation Packages

1. **Clone common simulation packages**:
```bash
cd ~/gazebo_ros2_ws/src
git clone https://github.com/ros-simulation/gazebo_ros_pkgs.git -b humble
```

2. **Build the packages**:
```bash
cd ~/gazebo_ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select gazebo_ros_pkgs
```

3. **Source the workspace**:
```bash
source install/setup.bash
```

## Troubleshooting Common Issues

### Gazebo Won't Start

**Symptoms**: Gazebo fails to launch or crashes immediately

**Solutions**:
1. Check if your graphics drivers are up to date:
```bash
glxinfo | grep "OpenGL renderer"
```

2. Try running with software rendering:
```bash
export LIBGL_ALWAYS_SOFTWARE=1
gz sim
```

3. Check if the display is properly configured:
```bash
echo $DISPLAY
```

### ROS 2 Topics Not Appearing

**Symptoms**: No Gazebo-related topics appear when running `ros2 topic list`

**Solutions**:
1. Ensure both ROS 2 and Gazebo environments are sourced:
```bash
source ~/setup_env.sh
```

2. Check the ROS domain ID:
```bash
echo $ROS_DOMAIN_ID
```

3. Verify Gazebo plugins are loaded in your world file

### Performance Issues

**Symptoms**: Slow simulation, low FPS, or high CPU usage

**Solutions**:
1. Reduce physics update rate in your world file:
```xml
<physics type="ode">
  <max_step_size>0.004</max_step_size>  <!-- Increase this value -->
  <real_time_factor>1.0</real_time_factor>
</physics>
```

2. Simplify collision models in your robot URDF/SDF

3. Close other CPU-intensive applications

## Verification Steps

To verify that your installation and setup are working correctly:

1. **Check Gazebo version**:
```bash
gz --version
```

2. **Check ROS 2 version**:
```bash
ros2 --version
```

3. **Launch a simple simulation**:
```bash
source ~/setup_env.sh
gz sim -r examples/worlds/shapes.sdf
```

4. **Verify ROS 2 communication** in another terminal:
```bash
source ~/setup_env.sh
ros2 topic list
```

## Next Steps

With Gazebo and ROS 2 properly installed and integrated, you're ready to create more complex simulations. The next steps include:

1. Creating custom robot models in URDF/SDF format
2. Setting up sensors and controllers
3. Implementing robot behavior through ROS 2 nodes
4. Creating humanoid robot simulations

## Additional Resources

- [Gazebo Documentation](http://gazebosim.org/)
- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Gazebo-ROS Integration Tutorials](https://classic.gazebosim.org/tutorials?tut=ros2_overview)
- [Ubuntu Installation Guide for ROS 2](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)