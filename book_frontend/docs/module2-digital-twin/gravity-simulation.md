# Gravity Simulation in Gazebo

## Introduction

Gravity simulation is a fundamental aspect of physics-based robotics simulation in Gazebo. This document explains the concepts behind gravity simulation and how to configure it for humanoid robot applications.

## Understanding Gravity in Physics Simulation

### What is Gravity?

Gravity is a natural phenomenon by which all things with mass or energy are brought toward one another. In robotics simulation, accurately modeling gravity is crucial for:

- Realistic robot movement and behavior
- Proper interaction with the environment
- Accurate sensor data generation
- Validating control algorithms

### Gravity in Gazebo

In Gazebo, gravity is represented as a 3D acceleration vector that affects all objects in the simulation. The default value simulates Earth's gravity: `<gravity>0 0 -9.8</gravity>`, where:
- The X component (0) represents acceleration in the forward/backward direction
- The Y component (0) represents acceleration in the left/right direction
- The Z component (-9.8) represents acceleration in the up/down direction (downward)

## Configuring Gravity in Gazebo

### Basic Gravity Configuration

Gravity is configured in the world file's physics section:

```xml
<sdf version="1.7">
  <world name="gravity_example">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Other world elements -->
  </world>
</sdf>
```

### Different Gravity Environments

#### Earth-like Gravity
```xml
<gravity>0 0 -9.8</gravity>
```
Standard Earth gravity (9.8 m/s² downward)

#### Moon Gravity
```xml
<gravity>0 0 -1.62</gravity>
```
Moon's gravity (1/6 of Earth's gravity)

#### Zero Gravity (Space Simulation)
```xml
<gravity>0 0 0</gravity>
```
No gravitational acceleration (useful for space robotics)

#### Custom Gravity
```xml
<gravity>0 0 -5.0</gravity>
```
Custom gravitational acceleration (e.g., for Mars or experimental scenarios)

## Gravity and Robot Simulation

### Impact on Humanoid Robots

Gravity significantly affects humanoid robot simulation in several ways:

#### Balance and Stability
- Robots must actively maintain balance against gravitational forces
- Control algorithms must account for center of mass positioning
- Walking patterns must consider gravitational effects

#### Joint Loading
- Gravity creates constant forces on joints
- Lower limb joints experience higher loads than upper limbs
- Actuators must overcome gravitational forces

#### Contact Forces
- Feet/ground contact forces are influenced by gravity
- Stability margins change with gravitational acceleration
- Friction calculations depend on gravitational loading

### Gravity-Dependent Behaviors

#### Standing Stability
```xml
<physics type="ode">
  <gravity>0 0 -9.8</gravity>
  <max_step_size>0.001</max_step_size>  <!-- Smaller steps for stability -->
  <real_time_factor>1.0</real_time_factor>
</physics>
```

#### Walking Simulation
For walking robots, gravity affects:
- Center of Mass (CoM) trajectory
- Zero Moment Point (ZMP) calculations
- Foot placement and timing

## Advanced Gravity Concepts

### Gravity Vector Direction

The gravity vector doesn't have to point straight down. For example:

```xml
<!-- Gravity pointing diagonally -->
<gravity>-1.0 0 -9.0</gravity>

<!-- Gravity pointing sideways (for wall-climbing robots) -->
<gravity>9.8 0 0</gravity>
```

### Gravity and Coordinate Systems

Gazebo uses a right-handed coordinate system where:
- X+ points forward
- Y+ points left
- Z+ points up

Therefore, negative Z values in the gravity vector represent downward acceleration.

## Practical Examples

### Example 1: Basic Gravity Setup

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="basic_gravity">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
      <max_step_size>0.002</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>500</real_time_update_rate>
    </physics>

    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Simple box to demonstrate gravity -->
    <model name="falling_box">
      <pose>0 0 2 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.2 0.2 0.2</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.2 0.2 0.2</size>
            </box>
          </geometry>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.006667</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>0.006667</iyy>
            <iyz>0</iyz>
            <izz>0.006667</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

### Example 2: Variable Gravity Experiment

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="variable_gravity">
    <physics type="ode">
      <!-- This will be changed programmatically -->
      <gravity>0 0 -9.8</gravity>
    </physics>

    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Multiple boxes at different gravity settings -->
    <model name="earth_box">
      <pose>-2 0 2 0 0 0</pose>
      <link name="link">
        <collision><geometry><box><size>0.2 0.2 0.2</size></box></geometry></collision>
        <visual><geometry><box><size>0.2 0.2 0.2</size></box></geometry></visual>
        <inertial><mass>1.0</mass><inertia><ixx>0.006667</ixx><iyy>0.006667</iyy><izz>0.006667</izz></inertia></inertial>
      </link>
    </model>

    <model name="moon_box">
      <pose>0 0 2 0 0 0</pose>
      <link name="link">
        <collision><geometry><box><size>0.2 0.2 0.2</size></box></geometry></collision>
        <visual><geometry><box><size>0.2 0.2 0.2</size></box></geometry></visual>
        <inertial><mass>1.0</mass><inertia><ixx>0.006667</ixx><iyy>0.006667</iyy><izz>0.006667</izz></inertia></inertial>
      </link>
    </model>

    <model name="zero_gravity_box">
      <pose>2 0 2 0 0 0</pose>
      <link name="link">
        <collision><geometry><box><size>0.2 0.2 0.2</size></box></geometry></collision>
        <visual><geometry><box><size>0.2 0.2 0.2</size></box></geometry></visual>
        <inertial><mass>1.0</mass><inertia><ixx>0.006667</ixx><iyy>0.006667</iyy><izz>0.006667</izz></inertia></inertial>
      </link>
    </model>
  </world>
</sdf>
```

## Gravity and Simulation Performance

### Time Step Considerations

Gravity simulation accuracy depends on the physics engine's time step:

```xml
<physics type="ode">
  <gravity>0 0 -9.8</gravity>
  <max_step_size>0.001</max_step_size>  <!-- Smaller steps: more accurate but slower -->
  <!-- or -->
  <max_step_size>0.01</max_step_size>   <!-- Larger steps: faster but less accurate -->
</physics>
```

### Stability Considerations

For humanoid robots, especially when standing or walking, consider:

- Using smaller time steps for better stability
- Adjusting solver parameters for gravity-related forces
- Ensuring sufficient update rates for balance control

## Testing Gravity Configuration

### Simple Test Procedure

1. Create a world with a simple object at height
2. Set a specific gravity value
3. Run the simulation and measure the object's fall
4. Verify the acceleration matches expected values

### Verification Code Example

```python
import math

def calculate_gravitational_acceleration(initial_height, fall_time):
    """
    Calculate gravity from fall time and height
    h = 0.5 * g * t^2 => g = 2h / t^2
    """
    if fall_time > 0:
        calculated_g = (2 * initial_height) / (fall_time ** 2)
        return calculated_g
    return 0

# Example: Object falls 1 meter in 0.45 seconds
# Expected: g ≈ 9.8 m/s²
actual_g = calculate_gravitational_acceleration(1.0, 0.45)
print(f"Calculated gravity: {actual_g} m/s²")
```

## Troubleshooting Gravity Issues

### Common Problems

#### Objects Don't Fall
- Check that gravity is set in the world file
- Verify the physics engine is enabled
- Ensure collision properties are defined

#### Objects Fall Too Fast/Slow
- Verify gravity vector values
- Check time step settings
- Confirm mass and inertial properties

#### Robot Instability
- Consider reducing time step for better accuracy
- Check joint limits and friction parameters
- Verify center of mass calculations

## Best Practices

### For Humanoid Robots

1. **Use appropriate gravity**: Earth gravity (9.8 m/s²) for Earth-based robots
2. **Match simulation to reality**: Use same gravity as the target environment
3. **Consider control algorithms**: Gravity affects balance control strategies
4. **Test stability**: Ensure robots can maintain balance under gravity
5. **Validate sensor data**: Gravity affects IMU and force sensor readings

### Performance Tips

1. **Balance accuracy and performance**: Choose time steps appropriately
2. **Use stable physics parameters**: Ensure consistent behavior
3. **Monitor simulation speed**: Adjust parameters if real-time performance is needed

## Integration with ROS 2

When using ROS 2 with Gazebo, gravity affects:
- IMU sensor readings
- Force/torque sensor values
- Robot state estimation
- Control algorithm performance

Gravity can be modified during simulation through ROS 2 services or parameters, allowing for dynamic experiments.

## Summary

Gravity simulation is fundamental to realistic humanoid robot simulation in Gazebo. Proper configuration ensures:
- Realistic robot behavior
- Accurate sensor data
- Valid control algorithm testing
- Meaningful performance evaluation

Always verify that your gravity settings match the intended operating environment for your humanoid robot.