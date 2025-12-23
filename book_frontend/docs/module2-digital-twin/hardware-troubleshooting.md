# Hardware Requirements and Troubleshooting Guide

This document outlines the hardware requirements for the Digital Twin Simulation environment and provides troubleshooting guidance for common issues.

## Hardware Requirements

### Minimum System Requirements

| Component | Minimum Specification | Notes |
|-----------|----------------------|-------|
| **Operating System** | Ubuntu 22.04 LTS or Windows 10/11 | WSL2 recommended for Windows |
| **CPU** | Intel i5 or AMD Ryzen 5 (4 cores) | Multi-core recommended for simulation |
| **RAM** | 8 GB | 16 GB recommended for optimal performance |
| **Storage** | 20 GB free space | For Gazebo, Unity, and simulation assets |
| **GPU** | Integrated graphics | Dedicated GPU required for Unity rendering |
| **Network** | Ethernet or 802.11n WiFi | For distributed simulation scenarios |

### Recommended System Requirements

| Component | Recommended Specification | Notes |
|-----------|---------------------------|-------|
| **Operating System** | Ubuntu 22.04 LTS or Windows 11 | Latest stable version |
| **CPU** | Intel i7 or AMD Ryzen 7 (8 cores) | Better for complex simulations |
| **RAM** | 16-32 GB | For multiple simulation instances |
| **Storage** | 50 GB SSD | Faster loading and simulation |
| **GPU** | Dedicated GPU with 4GB+ VRAM | NVIDIA GTX 1060 or equivalent |
| **Network** | Gigabit Ethernet | For low-latency communication |

### Performance Considerations

#### Gazebo-Specific Requirements
- **Physics Engine**: ODE requires less GPU power than Bullet or DART
- **Simulation Complexity**: More objects and sensors require more CPU power
- **Real-time Performance**: 20-30 FPS requires adequate CPU for physics calculations

#### Unity-Specific Requirements
- **Rendering Pipeline**: URP requires less GPU power than HDRP
- **Visual Quality**: Higher quality settings require more GPU power
- **Real-time Rendering**: 30+ FPS for smooth human-robot interaction

#### Integration-Specific Requirements
- **Synchronization**: Requires both Gazebo and Unity to run simultaneously
- **Memory**: Each application requires significant RAM
- **Latency**: Fast CPU and network reduce synchronization delays

## Installation Prerequisites

### System Preparation

#### Ubuntu Setup
```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Install essential build tools
sudo apt install build-essential cmake pkg-config

# Install graphics drivers (for Unity)
sudo apt install mesa-utils
```

#### Windows Setup
- Enable WSL2 (if using for ROS/Gazebo)
- Install Visual Studio Build Tools
- Update graphics drivers
- Ensure .NET Framework 4.8 or later

### Performance Optimization

#### System Configuration
- Disable unnecessary background applications
- Allocate adequate virtual memory
- Ensure adequate cooling for sustained performance
- Use SSD storage for faster loading

#### Resource Management
- Monitor CPU and GPU usage during simulation
- Close unnecessary applications
- Configure applications for optimal performance
- Use task scheduling to manage resource usage

## Common Issues and Troubleshooting

### Gazebo Issues

#### Gazebo Won't Start
**Symptoms**: Gazebo fails to launch or crashes immediately
**Solutions**:
1. Check system requirements are met
2. Verify ROS 2 environment is sourced: `source /opt/ros/humble/setup.bash`
3. Check graphics drivers are up to date
4. Try running with software rendering: `export LIBGL_ALWAYS_SOFTWARE=1`

#### Poor Physics Performance
**Symptoms**: Slow simulation, low FPS
**Solutions**:
1. Reduce simulation complexity (fewer objects, simpler meshes)
2. Lower physics update rate in world file
3. Use simpler collision models (boxes instead of complex meshes)
4. Close other applications to free up CPU resources

#### Sensor Data Issues
**Symptoms**: Incorrect or missing sensor data
**Solutions**:
1. Verify sensor configuration in SDF/URDF files
2. Check sensor topics are being published: `ros2 topic list`
3. Verify sensor plugins are properly loaded
4. Check sensor parameters (range, resolution, etc.)

### Unity Issues

#### Unity Scenes Won't Load
**Symptoms**: Unity editor crashes or scenes fail to load
**Solutions**:
1. Verify Unity 2022.3 LTS is installed
2. Check GPU drivers are up to date
3. Try running Unity in safe mode
4. Verify project files are not corrupted

#### Poor Rendering Performance
**Symptoms**: Low FPS, laggy interaction
**Solutions**:
1. Reduce rendering quality in Unity settings
2. Use Level of Detail (LOD) for complex models
3. Reduce lighting complexity
4. Close other GPU-intensive applications

#### Import/Export Issues
**Symptoms**: Problems importing robot models or exporting scenes
**Solutions**:
1. Verify model format compatibility (FBX, OBJ, etc.)
2. Check model scale and coordinate system
3. Ensure textures and materials are properly linked
4. Verify file permissions and paths

### Integration Issues

#### Synchronization Problems
**Symptoms**: Physics and rendering become out of sync
**Solutions**:
1. Check ROS 2 communication between systems
2. Verify coordinate system transformations
3. Adjust synchronization frequency
4. Implement interpolation for smoother updates

#### Communication Failures
**Symptoms**: Data not flowing between Gazebo and Unity
**Solutions**:
1. Verify ROS 2 network configuration
2. Check topic names and message types match
3. Ensure both systems are on same ROS domain
4. Test communication with simple publisher/subscriber

#### High Latency
**Symptoms**: Delay between physics simulation and visual update
**Solutions**:
1. Optimize data transmission frequency
2. Reduce data payload size
3. Use faster communication method (shared memory)
4. Profile and optimize bridge performance

## Performance Optimization

### Gazebo Optimization
- Use simpler collision models (collision vs visual can be different)
- Reduce physics engine iterations
- Use fixed step size for consistent performance
- Limit the number of active sensors

### Unity Optimization
- Implement Level of Detail (LOD) for models
- Use occlusion culling
- Optimize draw calls and batching
- Use appropriate texture compression

### Integration Optimization
- Minimize data transmission frequency
- Use delta updates instead of full state
- Implement efficient serialization
- Profile and optimize bridge code

## Diagnostic Tools

### System Monitoring
- **htop/top**: Monitor CPU and memory usage
- **nvidia-smi**: GPU monitoring (if NVIDIA GPU)
- **ROS 2 tools**: `ros2 topic echo`, `ros2 node info`

### Performance Profiling
- **Gazebo**: Built-in statistics and logging
- **Unity**: Built-in profiler for performance analysis
- **Network**: Tools like Wireshark for communication analysis

## Hardware-Specific Issues

### NVIDIA GPUs
- Ensure proprietary drivers are installed
- Check CUDA compatibility if using GPU acceleration
- Monitor GPU temperature during extended use

### AMD GPUs
- Verify OpenCL support for compute operations
- Check Mesa drivers on Linux systems
- Monitor for driver-specific issues

### Intel Integrated Graphics
- May struggle with Unity rendering
- Consider using URP instead of HDRP
- Lower quality settings may be necessary

## Recovery Procedures

### System Restore Points
- Create system restore points before major installations
- Keep backups of working configurations
- Document successful installation procedures

### Troubleshooting Checklist
1. Verify all prerequisites are installed and working
2. Check system meets minimum requirements
3. Test individual components (Gazebo, Unity) separately
4. Verify communication between components
5. Test with minimal example before complex scenarios

## Support Resources

### Documentation
- Gazebo: http://gazebosim.org/tutorials
- Unity: https://docs.unity3d.com/
- ROS 2: https://docs.ros.org/en/humble/

### Community Support
- Gazebo Answers: https://answers.gazebosim.org/
- Unity Forum: https://forum.unity.com/
- ROS Answers: https://answers.ros.org/

## Next Steps

This hardware requirements and troubleshooting guide provides essential information for setting up and maintaining the digital twin simulation environment. Use this guide to optimize your system for the best possible performance and to resolve common issues quickly.