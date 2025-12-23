# Chapter 3: Nav2 for Humanoid Navigation

## Introduction

Welcome to Chapter 3 of Module 3: The AI-Robot Brain (NVIDIA Isaac™). In this chapter, you will learn how to configure and use Navigation2 (Nav2) for humanoid robot navigation. By the end of this chapter, you will be able to set up navigation systems for humanoid robots with special considerations for bipedal locomotion and path planning challenges.

## Learning Objectives

After completing this chapter, you will be able to:
- Install and configure Nav2 for humanoid robot navigation
- Set up costmap configurations for bipedal navigation
- Adapt path planning algorithms for humanoid kinematics
- Configure navigation parameters specific to humanoid movement
- Set up TF tree for humanoid robot navigation
- Test navigation systems with humanoid robots in simulation

## Prerequisites

Before starting this chapter, you should have:
- Basic knowledge of ROS 2 and navigation concepts
- Understanding of humanoid robot kinematics
- Completed Chapters 1 and 2 of this module
- Access to a ROS 2 Humble environment with Nav2 packages

## Understanding Humanoid Navigation

### Differences from Wheeled Navigation

Humanoid navigation presents unique challenges compared to wheeled navigation:

- **Bipedal Locomotion**: Requires discrete footstep planning
- **Balance Requirements**: Maintaining balance during movement
- **Kinematic Constraints**: Complex joint configurations and limitations
- **Foot Placement**: Precise foot placement for stable walking
- **Turning Mechanics**: Different turning radius and mechanics

### Nav2 Architecture for Humanoids

Nav2 for humanoid robots includes:
- **Global Planner**: Creates high-level path considering humanoid kinematics
- **Local Planner**: Executes path following with balance-aware commands
- **Costmap**: Represents environment with humanoid-specific constraints
- **Controller**: Interfaces with humanoid robot's walking controller
- **Behavior Trees**: Manages navigation behaviors and recovery actions

## Nav2 Installation and Setup

### Installation

```bash
# Install Nav2 packages
sudo apt update
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
sudo apt install ros-humble-nav2-common

# Install additional packages for humanoid navigation
sudo apt install ros-humble-footstep-planner
sudo apt install ros-humble-humanoid-navigation
```

### Basic Configuration

```yaml
# nav2_params_humanoid.yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: False
    global_frame_id: "map"
    lambda_short: 0.1
    likelihood_max_dist: 2.0
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: True
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: "map"
    robot_base_frame: "base_link"
    odom_topic: "odom"
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    interrupt_on_battery: False
    battery_topic: "battery_status"

    # Humanoid-specific behavior tree
    default_nav_through_poses_bt_xml: "humanoid_navigate_through_poses_w_replanning_and_recovery.xml"
    default_nav_to_pose_bt_xml: "humanoid_navigate_to_pose_w_replanning_and_recovery.xml"

    # Recovery behaviors for humanoid robots
    recovery_plugins: ["spin", "backup", "wait"]
    spin:
      plugin: "nav2_recoveries/Spin"
      ideal_linear_velocity: 0.0
      ideal_angular_velocity: 0.75
      commanded_linear_velocity: 0.0
      commanded_angular_velocity: 0.5
      time_allowance: 10
    backup:
      plugin: "nav2_recoveries/BackUp"
      desired_distance: 0.3
      target_x_vel: 0.05
    wait:
      plugin: "nav2_recoveries/Wait"
      sleep_duration: 2.0