# Quickstart: ROS 2 Fundamentals for Humanoid Robotics

## Prerequisites

1. **System Requirements**:
   - Ubuntu 22.04 LTS or Windows 10/11 with WSL2
   - At least 8GB RAM recommended
   - 20GB free disk space for ROS 2 installation

2. **Software Installation**:
   - ROS 2 Humble Hawksbill
   - Python 3.8 or higher
   - Docusaurus prerequisites (Node.js, npm)

## Installation Steps

### 1. Install ROS 2 Humble Hawksbill

On Ubuntu:
```bash
# Add ROS 2 repository
sudo apt update && sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install ros-humble-desktop
sudo apt install python3-rosdep2
sudo apt install python3-colcon-common-extensions
sudo rosdep init
rosdep update

# Source ROS 2 environment
source /opt/ros/humble/setup.bash
```

### 2. Set up Docusaurus Environment

```bash
# Install Node.js (version 18 or higher)
# Follow instructions at https://nodejs.org/

# Install project dependencies
npm install
```

### 3. Verify Installation

```bash
# Test ROS 2 installation
source /opt/ros/humble/setup.bash
ros2 topic list
# Should return without errors

# Test Python interface
python3 -c "import rclpy; print('rclpy import successful')"
```

## Getting Started with Examples

### 1. Run Basic ROS 2 Node

```bash
# Create a workspace
mkdir -p ~/ros2_workspace/src
cd ~/ros2_workspace

# Source ROS 2
source /opt/ros/humble/setup.bash

# Build workspace
colcon build

# Source the workspace
source install/setup.bash
```

### 2. Launch Example Projects

```bash
# Navigate to the tutorial examples
cd docs/tutorials/python-examples

# Run a basic publisher node
python3 basic_publisher.py

# In another terminal, run a subscriber
python3 basic_subscriber.py
```

## Building the Documentation

```bash
# Navigate to project root
cd /path/to/project

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Running Tests

```bash
# Unit tests for code examples
python3 -m pytest tests/unit/

# Documentation validation
npm run build
```

## Troubleshooting

1. **ROS 2 Commands Not Found**: Ensure you've sourced the ROS 2 environment with `source /opt/ros/humble/setup.bash`

2. **Python Import Errors**: Verify rclpy is installed with `pip3 install rclpy`

3. **Docusaurus Build Issues**: Clear cache with `npm run clear` and reinstall dependencies

## Next Steps

1. Complete the ROS 2 fundamentals chapter
2. Explore communication patterns with topics, services, and actions
3. Create your first URDF model for a humanoid robot
4. Connect AI agents to robot control systems