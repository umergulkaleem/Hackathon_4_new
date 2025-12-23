# Data Model: Digital Twin Simulation (Gazebo & Unity)

## Overview
Data model for educational content covering Gazebo physics simulation, Unity rendering, and their integration for digital twin applications.

## Entities

### Gazebo Simulation Environment
**Description**: Physics-based simulation platform that models gravity, collisions, and environmental dynamics for humanoid robots

**Attributes**:
- environment_name: string (unique identifier for the simulation environment)
- physics_engine: string (type of physics engine being used, e.g., ODE, Bullet, DART)
- gravity_settings: vector3 (gravity vector in x, y, z directions)
- collision_models: list of CollisionModel objects (models defining collision properties)
- sensor_configurations: list of SensorConfiguration objects (sensor placement and settings)
- world_properties: dictionary (environment-specific properties like friction, damping)

**Validation rules**:
- environment_name must be unique within the system
- physics_engine must be a supported engine type
- gravity_settings must be a valid 3D vector

### Unity Visual Environment
**Description**: High-fidelity rendering platform that provides realistic visual representation of humanoid robots and environments

**Attributes**:
- scene_name: string (unique identifier for the Unity scene)
- rendering_pipeline: string (rendering pipeline used, e.g., URP, HDRP, Built-in)
- lighting_settings: LightingConfiguration object (lighting and shadow settings)
- material_definitions: list of Material objects (visual properties of surfaces)
- camera_configurations: list of Camera objects (viewing angles and properties)
- visual_assets: list of Asset objects (3D models, textures, animations)

**Validation rules**:
- scene_name must be unique within the system
- rendering_pipeline must be a supported pipeline type

### Digital Twin Integration
**Description**: Combined system that synchronizes physics simulation from Gazebo with visual rendering from Unity

**Attributes**:
- integration_name: string (unique identifier for the integration setup)
- synchronization_frequency: number (frequency of state synchronization in Hz)
- data_mapping: list of DataMapping objects (mapping between Gazebo and Unity entities)
- transformation_matrices: list of Matrix4x4 objects (coordinate system conversions)
- communication_protocol: string (method of data transfer between simulators)
- latency_threshold: number (acceptable delay threshold for synchronization)

**Validation rules**:
- integration_name must be unique within the system
- synchronization_frequency must be within acceptable range (typically 10-1000Hz)
- latency_threshold must be within acceptable range for real-time applications

### Sensor Emulation System
**Description**: Virtual sensors (LiDAR, Depth Cameras, IMUs) that generate realistic data for robot perception

**Attributes**:
- sensor_type: string (type of sensor: LiDAR, Depth Camera, IMU, etc.)
- sensor_name: string (unique identifier for the sensor)
- mounting_position: vector3 (position where sensor is mounted on robot)
- mounting_orientation: quaternion (orientation of sensor relative to robot)
- sensor_parameters: dictionary (type-specific parameters like FOV, range, resolution)
- noise_model: NoiseModel object (statistical model for sensor noise)
- calibration_data: Calibration object (data for sensor calibration)

**Validation rules**:
- sensor_name must be unique within the robot
- sensor_type must be a supported sensor type
- mounting_position and orientation must be valid 3D coordinates

### Human-Robot Interaction Scenario
**Description**: Specific use cases that demonstrate realistic interactions between humans and humanoid robots in simulated environments

**Attributes**:
- scenario_name: string (unique identifier for the interaction scenario)
- scenario_description: string (description of the interaction scenario)
- human_behavior_model: BehaviorModel object (model for human actions in scenario)
- robot_response_pattern: ResponsePattern object (how robot responds to human actions)
- interaction_objects: list of GameObject objects (objects involved in interaction)
- success_metrics: list of Metric objects (measures of successful interaction)
- safety_constraints: list of Constraint objects (safety limits for interaction)

**Validation rules**:
- scenario_name must be unique within the system
- success_metrics must be quantifiable measures

### Robot Model
**Description**: Representation of the humanoid robot in both Gazebo and Unity environments

**Attributes**:
- robot_name: string (unique identifier for the robot)
- urdf_definition: string (URDF file path for robot structure)
- sdf_definition: string (SDF file path for Gazebo-specific properties)
- visual_meshes: list of Mesh objects (3D mesh definitions for visual representation)
- collision_geometries: list of Geometry objects (collision shapes for physics)
- joint_definitions: list of Joint objects (robot joint properties)
- link_definitions: list of Link objects (robot link properties)
- actuator_configurations: list of Actuator objects (motor and actuator settings)

**Validation rules**:
- robot_name must be unique within the simulation
- URDF/SDF definitions must be valid and consistent between environments

### Simulation State
**Description**: Container for the synchronized state between Gazebo and Unity

**Attributes**:
- timestamp: datetime (time of state capture)
- robot_states: list of RobotState objects (states of all robots in simulation)
- environment_state: EnvironmentState object (state of the environment)
- sensor_readings: list of SensorReading objects (current sensor values)
- interaction_events: list of Event objects (recent interaction events)
- physics_properties: list of PhysicsProperty objects (physics-related properties)

**Validation rules**:
- timestamp must be current or recent
- all contained states must be consistent with each other