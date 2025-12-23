# Quickstart Guide: Digital Twin Simulation (Gazebo & Unity)

## Prerequisites

### System Requirements
- **Operating System**: Ubuntu 22.04 LTS or Windows 10/11 with WSL2
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 20GB free space for Gazebo and Unity installations
- **GPU**: Integrated graphics sufficient for Gazebo; Dedicated GPU (4GB+ VRAM) required for Unity rendering
- **Processor**: Multi-core processor (Intel i5/Ryzen 5 or better recommended)

### Software Prerequisites
1. **ROS 2 Humble Hawksbill** (with development tools)
2. **Gazebo Garden** (Fortress version recommended)
3. **Unity Hub** with Unity 2022.3 LTS
4. **Python 3.8+** with pip
5. **Git** for version control
6. **Node.js** (v18+) and npm for Docusaurus

## Installation Steps

### 1. Install ROS 2 Humble Hawksbill
```bash
# On Ubuntu
sudo apt update && sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install ros-humble-desktop ros-humble-dev-tools
sudo apt install python3-rosdep2 python3-vcstool

# Source ROS 2 environment
source /opt/ros/humble/setup.bash
```

### 2. Install Gazebo Garden
```bash
# On Ubuntu
sudo apt install ubuntu-keyring
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/gazebo-archive-keyring.gpg --keyserver keyserver.ubuntu.com --recv-keys C3173AA6

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/gazebo-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo.list > /dev/null

sudo apt update
sudo apt install gz-harmonic
```

### 3. Install Unity
1. Download and install Unity Hub from [Unity's website](https://unity.com/download)
2. Through Unity Hub, install Unity 2022.3 LTS
3. Install the following modules during installation:
   - Android Build Support (if targeting mobile)
   - iOS Build Support (if targeting iOS)
   - Windows Build Support (if targeting Windows)
   - Visual Studio integration

### 4. Set up the Educational Environment
```bash
# Clone the repository
git clone https://github.com/[your-org]/digital-twin-course.git
cd digital-twin-course

# Install Docusaurus dependencies
npm install

# Install Python dependencies for simulation examples
pip3 install rclpy transforms3d numpy matplotlib
```

## Getting Started with Examples

### 1. Run Basic Gazebo Simulation
```bash
# Source ROS 2 and Gazebo
source /opt/ros/humble/setup.bash
source /usr/share/gazebo/setup.sh

# Launch a basic humanoid simulation
gz sim -r examples/humanoid_basic.sdf
```

### 2. Launch Unity Visualization
1. Open Unity Hub
2. Click "Open" and navigate to the `unity-scenes` directory in the project
3. Open the "BasicHumanoid" scene
4. Press Play to see the visualization

### 3. Integrate Gazebo and Unity
For integration examples, see the integration tutorial in the documentation which demonstrates how to connect Gazebo physics with Unity rendering using ROS 2 communication.

## Running the Documentation Locally
```bash
# From the project root
npm start
```
This will start the Docusaurus development server at http://localhost:3000

## Building for Production
```bash
# Create a production build
npm run build

# Serve the production build locally for testing
npm run serve
```

## Troubleshooting Common Issues

### Gazebo Won't Start
- Ensure your system meets the minimum requirements
- Check that ROS 2 environment is sourced: `source /opt/ros/humble/setup.bash`
- Verify Gazebo installation: `gz --version`

### Unity Scenes Not Loading
- Make sure you have the correct Unity version (2022.3 LTS)
- Check that all required packages are installed in Unity
- Ensure your GPU meets the minimum requirements

### Docusaurus Build Errors
- Verify Node.js version is 18 or higher: `node --version`
- Clear Docusaurus cache: `npm run clear`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## Next Steps

1. Complete the Gazebo Physics Simulation chapter (Module 2, Chapter 1)
2. Explore Unity Rendering techniques (Module 2, Chapter 2)
3. Learn Integration techniques (Module 2, Chapter 3)
4. Practice with the provided exercises and examples
5. Test your knowledge with the assessment tools