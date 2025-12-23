# Common Assets and Resources for Digital Twin Simulation

This document provides common assets, resources, and references that are useful across all modules of the Digital Twin Simulation course.

## Common Assets

### Robot Models

- **Basic Humanoid Model**: A simple humanoid robot model for initial learning exercises
- **Advanced Humanoid Model**: A more complex humanoid robot with additional joints and sensors
- **Environment Models**: Standard environments for testing and demonstration

### Coordinate System Reference

| System | X Axis | Y Axis | Z Axis |
|--------|--------|--------|--------|
| Gazebo | Forward | Left | Up |
| Unity | Right | Up | Forward |
| ROS | Forward | Left | Up |

### Unit Conventions

- **Length**: Meters (m)
- **Time**: Seconds (s)
- **Angles**: Radians (rad) for internal calculations, Degrees (°) for display
- **Mass**: Kilograms (kg)
- **Force**: Newtons (N)
- **Torque**: Newton-meters (N·m)

## Essential Resources

### Documentation Links

- [Gazebo Documentation](http://gazebosim.org/documentation)
- [Unity Documentation](https://docs.unity3d.com/)
- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Gazebo-ROS Bridge](https://github.com/ros-simulation/gazebo_ros_pkgs)

### Software Requirements

- **Gazebo Garden (Fortress)**: Physics simulation environment
- **Unity 2022.3 LTS**: Visual rendering platform
- **ROS 2 Humble Hawksbill**: Communication framework
- **Python 3.8+**: Scripting and automation
- **Git**: Version control for examples

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Intel i5 / AMD Ryzen 5 | Intel i7 / AMD Ryzen 7 |
| RAM | 8 GB | 16 GB |
| GPU | Integrated Graphics | Dedicated GPU (4GB+ VRAM) |
| Storage | 10 GB | 20 GB |
| OS | Ubuntu 22.04 / Windows 10+ | Ubuntu 22.04 / Windows 11 |

## Common Commands

### Gazebo Commands

```bash
# Launch Gazebo with a world file
gz sim -r world_file.sdf

# Launch with GUI
gz sim -g world_file.sdf
```

### ROS 2 Commands

```bash
# List active topics
ros2 topic list

# Echo a topic
ros2 topic echo /topic_name std_msgs/msg/String
```

### Unity Commands (Command Line)

```bash
# Build project
Unity.exe -batchmode -nographics -buildWindows64Player path/to/build.exe -projectPath path/to/project
```

## Troubleshooting Resources

### Common Issues

1. **Simulation Performance**: Reduce visual quality or physics complexity
2. **Coordinate System Mismatches**: Verify transforms between Gazebo and Unity
3. **Communication Failures**: Check ROS 2 network configuration
4. **Model Import Issues**: Verify URDF/SDF compatibility

### Performance Optimization

- **Gazebo**: Reduce update rate, simplify collision models
- **Unity**: Use Level of Detail (LOD), optimize draw calls
- **Integration**: Reduce synchronization frequency if acceptable

## Assessment Rubric

### Gazebo Physics Simulation

- Environment setup and configuration (25%)
- Gravity and collision implementation (25%)
- Sensor emulation (25%)
- Documentation and code quality (25%)

### Unity Rendering

- Scene setup and configuration (20%)
- Visual quality and realism (30%)
- Human-robot interaction implementation (30%)
- Performance optimization (20%)

### Integration

- State synchronization accuracy (40%)
- Latency management (30%)
- Error handling and robustness (30%)

## Next Steps

These common assets and resources provide a foundation for all modules. Use these references throughout the course to maintain consistency and best practices.