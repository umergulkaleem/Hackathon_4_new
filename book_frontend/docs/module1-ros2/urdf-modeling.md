---
sidebar_label: 'Humanoid Modeling with URDF'
sidebar_position: 3
---

# Humanoid Modeling with URDF

## Introduction to URDF

URDF (Unified Robot Description Format) is an XML-based format used in ROS to describe robot models. It defines the physical and visual properties of a robot, including links, joints, and their relationships.

## Links

A link represents a rigid component of a robot. It contains information about the visual and collision properties of the component.

### Link Structure

```xml
<link name="link_name">
  <inertial>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <mass value="1.0"/>
    <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
  </inertial>
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="1 1 1"/>
    </geometry>
  </visual>
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="1 1 1"/>
    </geometry>
  </collision>
</link>
```

### Key Properties:
- **name**: Unique identifier for the link
- **inertial**: Physical properties like mass and inertia
- **visual**: How the link appears visually
- **collision**: How the link behaves in collision detection

## Joints

Joints connect two links and define how they can move relative to each other.

### Joint Types:
- **fixed**: No movement between links
- **revolute**: Rotational movement around an axis
- **continuous**: Unlimited rotational movement
- **prismatic**: Linear sliding movement
- **floating**: 6 degrees of freedom
- **planar**: Movement on a plane

### Joint Structure

```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link_name"/>
  <child link="child_link_name"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
</joint>
```

### Key Properties:
- **name**: Unique identifier for the joint
- **type**: Type of joint (fixed, revolute, etc.)
- **parent/child**: Links connected by the joint
- **origin**: Position and orientation of the joint
- **axis**: Movement axis for revolute/prismatic joints
- **limit**: Movement constraints for revolute/prismatic joints

## Coordinate Frames

ROS uses the right-handed coordinate system where:
- **X**: Forward
- **Y**: Left
- **Z**: Up

This standardization ensures consistent orientation across all robot models.

## Creating a Basic Humanoid Model

Here's a simplified example of a humanoid robot with a torso, head, two arms, and two legs:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Torso -->
  <link name="torso">
    <inertial>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <mass value="10.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.3 0.6"/>
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.3 0.6"/>
      </geometry>
    </collision>
  </link>

  <!-- Head -->
  <link name="head">
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="2.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
    </collision>
  </link>

  <!-- Neck joint -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.6" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.785" upper="0.785" effort="10" velocity="1"/>
  </joint>

  <!-- Left upper arm -->
  <link name="left_upper_arm">
    <inertial>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <mass value="2.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
  </link>

  <!-- Left shoulder joint -->
  <joint name="left_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.2 0 0.4" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>
</robot>
```

## Best Practices for Humanoid URDF Models

1. **Consistent Naming**: Use descriptive names for links and joints
2. **Proper Inertial Properties**: Accurate mass and inertia values for realistic simulation
3. **Collision vs Visual**: Use simpler geometries for collision to improve performance
4. **Kinematic Chains**: Organize joints to form proper kinematic chains
5. **Joint Limits**: Set appropriate limits to prevent impossible configurations
6. **Fixed Joints**: Use fixed joints for attachments that don't move relative to each other

## Validation and Troubleshooting

### Common Issues:
- Missing parent links
- Incorrect joint types
- Invalid XML syntax
- Inconsistent units

### Validation Tools:
- `check_urdf` command to verify URDF structure
- RViz for visual inspection
- Gazebo for physics simulation testing

This structure provides the foundation for creating complex humanoid robot models that can be used in ROS 2 systems for simulation and control.