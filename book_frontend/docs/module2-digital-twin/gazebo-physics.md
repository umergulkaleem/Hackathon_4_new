# Chapter 1: Gazebo Physics Simulation

## Introduction

Welcome to the first chapter of Module 2: The Digital Twin (Gazebo & Unity). In this chapter, you will learn how to create physics-based simulations of humanoid robots using Gazebo. By the end of this chapter, you will be able to create a simulation environment that accurately models gravity and collision dynamics.

## Learning Objectives

After completing this chapter, you will be able to:
- Install and configure Gazebo for physics simulation
- Create basic humanoid robot models in Gazebo
- Configure gravity and environmental dynamics
- Implement collision detection and response
- Set up and configure various sensor types (LiDAR, Depth Cameras, IMUs)

## Prerequisites

Before starting this chapter, you should have:
- Basic knowledge of ROS 2 concepts (covered in Module 1)
- Understanding of coordinate systems and transformations
- Basic familiarity with 3D modeling concepts

## Gazebo Installation and Setup

### System Requirements

First, ensure your system meets the requirements for running Gazebo:
- Ubuntu 22.04 LTS or Windows 10/11 with WSL2
- At least 4GB RAM (8GB recommended)
- Graphics card with OpenGL 2.1 support
- 10GB free disk space

### Installing Gazebo Garden

On Ubuntu, install Gazebo Garden (Fortress) with the following commands:

```bash
# Update package lists
sudo apt update

# Install Gazebo Garden
sudo apt install gz-harmonic

# Verify installation
gz --version
```

### Setting Up the Environment

After installation, set up your environment by sourcing the appropriate setup files:

```bash
# Add to your .bashrc or .zshrc for permanent setup
source /usr/share/gz/setup.sh
```

## Understanding Gazebo Concepts

### World Files

Gazebo simulations are defined in world files, typically with the .sdf extension. These files define:
- The environment and objects in the simulation
- Physical properties like gravity
- Lighting and visual effects
- Plugins for additional functionality

### Models

Models in Gazebo represent physical objects with:
- Visual representation (how they look)
- Collision properties (how they interact)
- Inertial properties (mass, center of mass)
- Joints (connections between parts)

### Plugins

Gazebo supports various plugins that extend functionality:
- Physics engines (ODE, Bullet, DART)
- Sensors (LiDAR, cameras, IMUs)
- Controllers (for robot actuators)
- Communication interfaces (ROS 2 bridge)

## Creating Your First Simulation Environment

### Basic World Structure

Let's create a simple world file to understand the structure:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="basic_world">
    <!-- Define the physics engine -->
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Add a ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Add a directional light -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Add a simple box -->
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
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.166667</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>0.166667</iyy>
            <iyz>0</iyz>
            <izz>0.166667</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

### Running Your Simulation

Save the above content as `basic_world.sdf` and run it with:

```bash
gz sim -r basic_world.sdf
```

The `-r` flag tells Gazebo to run the simulation immediately without starting the GUI. To start with the GUI:

```bash
gz sim basic_world.sdf
```

## Gravity Simulation

### Understanding Gravity in Gazebo

Gravity in Gazebo is defined as a 3D vector representing acceleration in m/s². The default value is typically `<gravity>0 0 -9.8</gravity>`, representing Earth's gravity pulling objects downward along the negative Z-axis.

### Custom Gravity Settings

You can modify gravity to simulate different environments:

```xml
<physics type="ode">
  <!-- Earth-like gravity -->
  <gravity>0 0 -9.8</gravity>

  <!-- Moon gravity (1/6 of Earth) -->
  <!-- <gravity>0 0 -1.63</gravity> -->

  <!-- Zero gravity (space simulation) -->
  <!-- <gravity>0 0 0</gravity> -->
</physics>
```

### Experiment: Gravity Comparison

Create a world file with multiple boxes that experience different gravity settings to observe the effects:

1. Create a box with Earth gravity
2. Create a second box with reduced gravity
3. Create a third box with zero gravity
4. Observe the different behaviors

## Collision Detection

### Collision Models

Collision detection in Gazebo is handled by collision models that define how objects interact:

- **Primitive Shapes**: Boxes, spheres, cylinders
- **Mesh Shapes**: Complex geometries from 3D models
- **Heightmap Shapes**: Terrain from heightmap images

### Collision Properties

Key properties for collision detection include:

- **Surface Parameters**: Friction, restitution (bounciness)
- **Contact Properties**: Contact models, patch radius
- **Collision Filtering**: Which objects can collide with each other

### Example: Collision Configuration

```xml
<collision name="collision">
  <geometry>
    <box>
      <size>1 1 1</size>
    </box>
  </geometry>
  <surface>
    <friction>
      <ode>
        <mu>1.0</mu>
        <mu2>1.0</mu2>
      </ode>
    </friction>
    <bounce>
      <restitution_coefficient>0.5</restitution_coefficient>
      <threshold>100000</threshold>
    </bounce>
  </surface>
</collision>
```

## Environment Dynamics

### Friction and Damping

Environment dynamics include properties that affect how objects move and interact:

- **Static Friction (mu)**: Resistance to initial motion
- **Dynamic Friction (mu2)**: Resistance during motion
- **Linear Damping**: Slows linear motion over time
- **Angular Damping**: Slows rotational motion over time

### Fluid Dynamics (Optional)

For advanced simulations, you can include fluid dynamics:

```xml
<physics type="ode">
  <gravity>0 0 -9.8</gravity>
  <ode>
    <solver>
      <type>quick</type>
      <iters>10</iters>
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0.000001</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

### Advanced Environment Configuration

For more realistic simulations, you can configure additional environmental properties:

#### Air Resistance and Drag

To simulate air resistance, you can apply damping forces to objects:

```xml
<link name="object_with_drag">
  <inertial>
    <mass>1.0</mass>
    <inertia>
      <ixx>0.1</ixx>
      <ixy>0</ixy>
      <ixz>0</ixz>
      <iyy>0.1</iyy>
      <iyz>0</iyz>
      <izz>0.1</izz>
    </inertia>
  </inertial>
  <linear_damping>0.01</linear_damping>
  <angular_damping>0.01</angular_damping>
</link>
```

#### Wind Effects

Wind can be simulated using plugins that apply forces to objects:

```xml
<world name="windy_world">
  <physics type="ode">
    <gravity>0 0 -9.8</gravity>
  </physics>

  <!-- Wind plugin example -->
  <plugin name="wind_plugin" filename="libWindPlugin.so">
    <wind_direction>1 0 0</wind_direction>
    <wind_force>0.5</wind_force>
    <wind_variation>0.1</wind_variation>
  </plugin>
</world>
```

Environment dynamics include properties that affect how objects move and interact:

- **Static Friction (mu)**: Resistance to initial motion
- **Dynamic Friction (mu2)**: Resistance during motion
- **Linear Damping**: Slows linear motion over time
- **Angular Damping**: Slows rotational motion over time

### Fluid Dynamics (Optional)

For advanced simulations, you can include fluid dynamics:

```xml
<physics type="ode">
  <gravity>0 0 -9.8</gravity>
  <ode>
    <solver>
      <type>quick</type>
      <iters>10</iters>
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0.000001</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

## Sensor Emulation in Gazebo

### LiDAR Sensors

LiDAR sensors simulate laser range finders:

```xml
<sensor name="lidar" type="ray">
  <pose>0.5 0 0.3 0 0 0</pose>
  <ray>
    <scan>
      <horizontal>
        <samples>640</samples>
        <resolution>1</resolution>
        <min_angle>-1.570796</min_angle>
        <max_angle>1.570796</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <always_on>1</always_on>
  <update_rate>10</update_rate>
  <visualize>true</visualize>
</sensor>
```

#### Advanced LiDAR Configuration

For more sophisticated LiDAR emulation, you can configure additional parameters:

```xml
<sensor name="advanced_lidar" type="ray">
  <pose>0.5 0 0.5 0 0 0</pose>
  <ray>
    <scan>
      <horizontal>
        <samples>1080</samples>
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>  <!-- 360 degrees -->
        <max_angle>3.14159</max_angle>
      </horizontal>
      <vertical>
        <samples>32</samples>
        <resolution>1</resolution>
        <min_angle>-0.2618</min_angle>    <!-- -15 degrees -->
        <max_angle>0.2618</max_angle>     <!-- 15 degrees -->
      </vertical>
    </scan>
    <range>
      <min>0.08</min>
      <max>30.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <always_on>1</always_on>
  <update_rate>20</update_rate>
  <visualize>false</visualize>
  <plugin name="lidar_control" filename="libRayPlugin.so">
    <always_on>true</always_on>
    <update_rate>20</update_rate>
    <topic>laser_scan</topic>
    <frame_name>lidar_frame</frame_name>
  </plugin>
</sensor>
```

### Depth Camera Sensors

Depth cameras provide 3D point cloud data:

```xml
<sensor name="depth_camera" type="depth">
  <pose>0.5 0 0.5 0 0 0</pose>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>10</far>
    </clip>
  </camera>
  <always_on>1</always_on>
  <update_rate>30</update_rate>
  <visualize>true</visualize>
</sensor>
```

#### Advanced Depth Camera Configuration

For more realistic depth camera simulation:

```xml
<sensor name="advanced_depth_camera" type="depth">
  <pose>0.5 0 0.5 0 0 0</pose>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>1280</width>
      <height>720</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.05</near>
      <far>15</far>
    </clip>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev>
    </noise>
  </camera>
  <always_on>1</always_on>
  <update_rate>30</update_rate>
  <visualize>true</visualize>
  <plugin name="camera_controller" filename="libDepthCameraPlugin.so">
    <alwaysOn>true</alwaysOn>
    <updateRate>30.0</updateRate>
    <cameraName>depth_camera</cameraName>
    <imageTopicName>image_raw</imageTopicName>
    <depthImageTopicName>depth/image_raw</depthImageTopicName>
    <pointCloudTopicName>points</pointCloudTopicName>
    <cameraInfoTopicName>camera_info</cameraInfoTopicName>
    <frameName>depth_camera_frame</frameName>
    <baseline>0.1</baseline>
    <distortion_k1>0.0</distortion_k1>
    <distortion_k2>0.0</distortion_k2>
    <distortion_k3>0.0</distortion_k3>
    <distortion_t1>0.0</distortion_t1>
    <distortion_t2>0.0</distortion_t2>
  </plugin>
</sensor>
```

### IMU Sensors

IMU sensors measure linear acceleration and angular velocity:

```xml
<sensor name="imu" type="imu">
  <pose>0 0 0.5 0 0 0</pose>
  <always_on>1</always_on>
  <update_rate>100</update_rate>
  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </z>
    </angular_velocity>
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
        </noise>
      </z>
    </linear_acceleration>
  </imu>
</sensor>
```

#### Advanced IMU Configuration

For more realistic IMU simulation with custom noise characteristics:

```xml
<sensor name="advanced_imu" type="imu">
  <pose>0 0 0.8 0 0 0</pose>
  <topic>imu</topic>
  <always_on>1</always_on>
  <update_rate>100</update_rate>
  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-3</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0</bias_stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-3</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0</bias_stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-3</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0</bias_stddev>
        </noise>
      </z>
    </angular_velocity>
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0</bias_stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0</bias_stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0</bias_stddev>
        </noise>
      </z>
    </linear_acceleration>
  </imu>
  <plugin name="imu_plugin" filename="libImuPlugin.so">
    <alwaysOn>true</alwaysOn>
    <topic>imu</topic>
    <serviceName>imu_service</serviceName>
    <gaussianNoise>0.0</gaussianNoise>
    <frameName>imu_link</frameName>
    <initialOrientationAsReference>false</initialOrientationAsReference>
  </plugin>
</sensor>
```

### Sensor Best Practices

When implementing sensors in Gazebo, consider these best practices:

1. **Update Rates**: Balance between realism and performance
   - LiDAR: 10-20 Hz is typical for 360° scanners
   - Cameras: 30 Hz for standard video, 60+ Hz for high-speed applications
   - IMU: 100-1000 Hz for accurate motion tracking

2. **Noise Modeling**: Include realistic noise to match real sensor behavior
   - Use Gaussian noise for most sensors
   - Consider bias and drift for long-term simulations
   - Calibrate noise parameters to match real sensor specifications

3. **Visualization**: Enable visualization during development but disable in production runs to improve performance

4. **Topic Names**: Use consistent, descriptive topic names that match ROS conventions

## Practical Exercise: Simple Humanoid Robot

Now let's create a simple humanoid robot model with basic physics properties:

### Robot Model File (simple_humanoid.sdf)

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_humanoid">
    <!-- Torso -->
    <link name="torso">
      <pose>0 0 1 0 0 0</pose>
      <collision name="torso_collision">
        <geometry>
          <box>
            <size>0.3 0.2 0.5</size>
          </box>
        </geometry>
      </collision>
      <visual name="torso_visual">
        <geometry>
          <box>
            <size>0.3 0.2 0.5</size>
          </box>
        </geometry>
      </visual>
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.2</ixx>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyy>0.2</iyy>
          <iyz>0</iyz>
          <izz>0.2</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Head -->
    <link name="head">
      <pose>0 0 1.4 0 0 0</pose>
      <collision name="head_collision">
        <geometry>
          <sphere>
            <radius>0.1</radius>
          </sphere>
        </geometry>
      </collision>
      <visual name="head_visual">
        <geometry>
          <sphere>
            <radius>0.1</radius>
          </sphere>
        </geometry>
      </visual>
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.004</ixx>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyy>0.004</iyy>
          <iyz>0</iyz>
          <izz>0.004</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Joint connecting torso and head -->
    <joint name="neck_joint" type="revolute">
      <parent>torso</parent>
      <child>head</child>
      <axis>
        <xyz>0 0 1</xyz>
        <limit>
          <lower>-0.5</lower>
          <upper>0.5</upper>
        </limit>
      </axis>
    </joint>
  </model>
</sdf>
```

### World File with Robot

Create a world file that includes your simple humanoid:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_world">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Include your robot -->
    <include>
      <uri>file://path/to/simple_humanoid.sdf</uri>
    </include>
  </world>
</sdf>
```

## Practical Exercises for Physics Simulation

### Exercise 1: Multi-Object Physics Simulation
Create a simulation with multiple objects of different materials and observe their interactions:

1. Create a world with:
   - A sloped surface (ramp)
   - Objects of different materials (wood, metal, rubber)
   - Objects of different shapes (sphere, cube, cylinder)
   - Different friction coefficients for each material

2. Observe how objects behave differently based on their properties:
   - Which objects roll vs. slide?
   - How do different friction values affect motion?
   - How do different masses affect collisions?

### Exercise 2: Sensor Integration Challenge
Create a robot that uses multiple sensor types to navigate:

1. Build a robot with:
   - LiDAR for obstacle detection
   - IMU for orientation tracking
   - Depth camera for detailed environment mapping

2. Create a maze environment with:
   - Walls of different heights
   - Moving obstacles
   - Multiple paths to a goal

3. Program the robot to navigate using sensor feedback to avoid obstacles and reach the goal.

### Exercise 3: Realistic Humanoid Physics
Create a more realistic humanoid model with joint constraints:

1. Design a humanoid with:
   - Articulated joints (revolute joints for arms/legs)
   - Realistic mass distribution
   - Proper inertial properties for each link

2. Implement basic movement:
   - Standing balance
   - Simple walking gait
   - Basic arm movements

3. Test the model under different gravity conditions and observe how physics affects movement.

## Assessment Questions for Gazebo Physics Concepts

### Basic Concepts
1. What is the primary purpose of collision detection in Gazebo simulations?
2. Explain the difference between static friction and dynamic friction in physics simulation.
3. What role does the physics engine play in Gazebo, and what are the common options available?

### Configuration and Implementation
4. How would you configure a world in Gazebo to simulate lunar gravity conditions?
5. Describe the key components needed to create a sensor in Gazebo and explain their purposes.
6. What are the important parameters to consider when setting up a collision model for a robot link?

### Advanced Applications
7. Explain how you would implement a realistic wind effect in a Gazebo simulation.
8. What are the trade-offs between visual quality and performance when configuring physics parameters?
9. How would you synchronize sensor data rates to match real-world sensor specifications?
10. Describe the process of calibrating noise parameters for realistic sensor simulation.

## Hands-On Exercise

Create a simulation environment with:
1. A ground plane
2. A simple humanoid robot
3. A few obstacles (boxes, spheres)
4. At least one sensor (LiDAR, camera, or IMU)

Observe how the robot interacts with the environment under gravity and how sensors respond to the environment.

## Summary

In this chapter, you've learned:
- How to install and set up Gazebo
- The basic structure of world and model files
- How to configure gravity and collision detection
- How to add various sensor types to your simulation
- How to create a simple humanoid robot model

## Next Steps

In the next chapter, you'll learn about Unity for high-fidelity rendering and how to visualize your simulated robots in a realistic environment.