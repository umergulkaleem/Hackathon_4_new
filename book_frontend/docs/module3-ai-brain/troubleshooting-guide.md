# Troubleshooting Guide: Isaac Sim, Isaac ROS, and Nav2

## Overview

This guide provides solutions to common issues encountered when working with Isaac Sim, Isaac ROS, and Nav2 for humanoid robotics applications.

## Isaac Sim Troubleshooting

### Installation Issues

**Problem**: Isaac Sim fails to launch
- **Solution**:
  1. Check GPU drivers: `nvidia-smi`
  2. Verify CUDA installation: `nvcc --version`
  3. Ensure sufficient VRAM available
  4. Check Isaac Sim logs: `~/isaac_sim_logs/latest.log`

**Problem**: Rendering issues or poor performance
- **Solution**:
  1. Check graphics settings in Isaac Sim preferences
  2. Reduce scene complexity temporarily
  3. Verify GPU memory usage: `nvidia-smi`
  4. Update graphics drivers to latest version

### ROS Bridge Issues

**Problem**: Isaac Sim ROS bridge fails to connect to ROS 2
- **Solution**:
  1. Verify ROS 2 Humble is sourced: `source /opt/ros/humble/setup.bash`
  2. Check network configuration: `echo $ROS_DOMAIN_ID`
  3. Ensure Isaac Sim ROS bridge extension is enabled
  4. Verify topic names and message types match
  5. Check firewall settings if connecting across machines

### Robot Import Problems

**Problem**: URDF robot models fail to import correctly
- **Solution**:
  1. Validate URDF with `check_urdf` tool
  2. Check joint limits and physical properties
  3. Verify mesh file paths and formats
  4. Ensure proper coordinate frame definitions
  5. Check for missing dependencies in URDF

## Isaac ROS Troubleshooting

### Installation Problems

**Problem**: Isaac ROS packages fail to install or are not found
- **Solution**:
  1. Update package lists: `sudo apt update`
  2. Install ROS 2 Humble repositories properly
  3. Check ROS 2 installation: `ros2 --version`
  4. Verify package installation: `apt list --installed | grep isaac_ros`
  5. Check environment setup: `source /opt/ros/humble/setup.bash`

### Performance Issues

**Problem**: Isaac ROS pipelines run slower than real-time
- **Solution**:
  1. Monitor GPU utilization: `nvidia-smi`
  2. Check input data rate matches processing capability
  3. Verify GPU memory is sufficient for model size
  4. Optimize pipeline by reducing input resolution if possible
  5. Check for CPU bottlenecks with `htop`

### Sensor Data Problems

**Problem**: Isaac ROS nodes don't receive expected sensor data
- **Solution**:
  1. Verify sensor topics are publishing: `ros2 topic list`
  2. Check topic names match pipeline configuration
  3. Validate message types with `ros2 topic info`
  4. Ensure proper QoS settings match publisher/subscriber
  5. Check sensor calibration and mounting

## Nav2 Troubleshooting

### Costmap Configuration Problems

**Problem**: Navigation fails due to costmap issues
- **Solution**:
  1. Verify robot footprint is correctly configured
  2. Check costmap resolution and update frequency
  3. Validate sensor data sources for costmap layers
  4. Ensure proper TF tree with all required transforms
  5. Check inflation parameters for humanoid size

### Path Planning Failures

**Problem**: Nav2 cannot find valid paths to goals
- **Solution**:
  1. Verify map quality and resolution
  2. Check global planner configuration for humanoid constraints
  3. Validate robot footprint and clearance requirements
  4. Ensure proper goal tolerance settings
  5. Check for TF timing issues

### Localization Issues

**Problem**: Robot cannot properly localize in map
- **Solution**:
  1. Verify initial pose estimation
  2. Check sensor quality (LiDAR, IMU, odometry)
  3. Validate map quality and features
  4. Check AMCL configuration parameters
  5. Ensure proper TF tree and timing

## Common System Issues

### GPU-Related Problems

**Problem**: GPU memory errors
- **Solution**:
  1. Reduce input resolution of sensor data
  2. Lower batch processing size
  3. Close other GPU-intensive applications
  4. Check available GPU memory: `nvidia-smi`

**Problem**: GPU not utilized
- **Solution**:
  1. Verify Isaac ROS GPU parameters are set correctly
  2. Check that Isaac ROS packages are properly installed
  3. Ensure GPU index is correctly specified in parameters
  4. Verify CUDA and NVIDIA driver compatibility

### Network and Communication Issues

**Problem**: Topics not connecting between nodes
- **Solution**:
  1. Check ROS domain IDs match: `echo $ROS_DOMAIN_ID`
  2. Verify network connectivity if using multi-machine setup
  3. Check QoS settings match between publishers and subscribers
  4. Ensure all nodes are on same network segment

### Performance Optimization

**Problem**: Low frame rates or high latency
- **Solution**:
  1. Monitor system resources: `htop`, `nvidia-smi`
  2. Reduce input data resolution or rate
  3. Optimize pipeline configuration for specific hardware
  4. Check for bottlenecks in processing chain

## Humanoid-Specific Troubleshooting

### Balance and Locomotion Issues

**Problem**: Humanoid robot fails to maintain balance during navigation
- **Solution**:
  1. Verify balance controller is properly configured
  2. Check footstep planner parameters
  3. Validate walking pattern generator settings
  4. Ensure proper center of mass estimation
  5. Check sensor calibration for balance feedback

### Footstep Planning Problems

**Problem**: Footstep planner cannot find safe foot placements
- **Solution**:
  1. Verify terrain representation quality
  2. Check footstep planner parameters
  3. Validate robot kinematic constraints
  4. Ensure proper ground detection
  5. Check obstacle representation in costmap

## Quick Diagnostic Commands

### System Health Check
```bash
# Check GPU status
nvidia-smi

# Check ROS 2 topics
ros2 topic list

# Check ROS 2 nodes
ros2 node list

# Check Isaac Sim logs
tail -f ~/isaac_sim_logs/latest.log

# Monitor system resources
htop
```

### Network Troubleshooting
```bash
# Check ROS 2 network
ros2 topic list
ros2 node list

# Check network connectivity
ping <target_ip>

# Monitor bandwidth
iftop
```

### Performance Profiling
```bash
# Profile Isaac Sim performance
nsys profile --trace=cuda,nvtx ros2 launch ...

# Profile ROS 2 nodes
ros2 run tracetools_trace trace -p <process_name>

# Monitor real-time performance
ros2 topic hz /performance_metrics
```

## Common Error Messages and Solutions

### Isaac Sim Errors
- **"Failed to create OpenGL context"**: Update graphics drivers or reduce rendering settings
- **"CUDA error: out of memory"**: Reduce scene complexity or increase GPU memory limits
- **"ROS bridge connection failed"**: Check ROS 2 installation and network configuration

### Isaac ROS Errors
- **"Package not found"**: Verify Isaac ROS installation and environment setup
- **"GPU memory allocation failed"**: Reduce input resolution or model size
- **"Message queue overflow"**: Increase queue size or reduce input rate

### Nav2 Errors
- **"No valid path found"**: Check map quality, robot footprint, and goal validity
- **"TF timeout"**: Verify TF tree and timing configuration
- **"Controller failed"**: Check robot controller and safety systems

## Prevention Tips

### Before Starting Projects
1. Verify all prerequisites are installed and working
2. Test basic functionality before complex implementations
3. Create backup configurations for known working states
4. Document your setup and configuration for reproducibility

### During Development
1. Test components individually before integration
2. Monitor resource usage continuously
3. Keep incremental backups of working configurations
4. Use version control for all configurations and code

### Performance Monitoring
1. Regularly check GPU and CPU utilization
2. Monitor memory usage patterns
3. Verify data rates match processing capabilities
4. Track performance metrics over time

This troubleshooting guide provides solutions for common issues encountered when working with Isaac Sim, Isaac ROS, and Nav2 for humanoid robotics applications. When encountering issues not covered in this guide, check the official documentation and community forums for additional resources.