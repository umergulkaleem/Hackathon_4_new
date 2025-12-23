# Data Model: ROS 2 Fundamentals for Humanoid Robotics

## Overview
Data model for educational content covering ROS 2 fundamentals, communication patterns, and URDF modeling for humanoid robotics.

## Entities

### ROS 2 Node
**Description**: A process that performs computation in the ROS 2 system, implementing robot functionality and communicating with other nodes

**Attributes**:
- node_name: string (unique identifier for the node)
- node_namespace: string (optional namespace for organization)
- publishers: list of Publisher objects (outgoing communication)
- subscribers: list of Subscriber objects (incoming communication)
- services: list of Service objects (request/response communication)
- actions: list of Action objects (goal-based communication)

**Validation rules**:
- node_name must be unique within namespace
- node_name must follow ROS naming conventions

### Publisher
**Description**: Component that sends messages to topics in ROS 2 communication system

**Attributes**:
- topic_name: string (name of the topic to publish to)
- message_type: string (ROS message type being published)
- qos_profile: QoS object (Quality of Service settings)

### Subscriber
**Description**: Component that receives messages from topics in ROS 2 communication system

**Attributes**:
- topic_name: string (name of the topic to subscribe to)
- message_type: string (ROS message type being subscribed to)
- callback_function: function (function to process incoming messages)
- qos_profile: QoS object (Quality of Service settings)

### Service
**Description**: Component that provides request/response communication in ROS 2

**Attributes**:
- service_name: string (name of the service)
- service_type: string (ROS service type definition)
- callback_function: function (function to process service requests)

### Action
**Description**: Component that handles goal-based communication with feedback in ROS 2

**Attributes**:
- action_name: string (name of the action)
- action_type: string (ROS action type definition)
- goal_callback: function (function to process action goals)
- feedback_callback: function (function to send feedback)
- result_callback: function (function to send results)

### URDF Model
**Description**: Unified Robot Description Format files that define the physical structure of robots including links, joints, and visual properties

**Attributes**:
- model_name: string (name of the robot model)
- links: list of Link objects (physical components of the robot)
- joints: list of Joint objects (connections between links)
- materials: list of Material objects (visual properties)
- gazebo_extensions: list of Gazebo objects (simulation-specific extensions)

### Link
**Description**: A rigid component of a robot in URDF representation

**Attributes**:
- link_name: string (unique name for the link)
- visual: Visual object (visual representation)
- collision: Collision object (collision detection properties)
- inertial: Inertial object (mass and inertia properties)

### Joint
**Description**: Connection between two links in URDF representation

**Attributes**:
- joint_name: string (unique name for the joint)
- joint_type: string (type of joint: revolute, continuous, prismatic, fixed, etc.)
- parent_link: string (name of parent link)
- child_link: string (name of child link)
- origin: Pose object (position and orientation relative to parent)

### AI Agent
**Description**: Software components that implement artificial intelligence logic and interact with robot systems through ROS 2 interfaces

**Attributes**:
- agent_name: string (unique identifier for the agent)
- behavior_logic: function (core AI logic implementation)
- ros_interfaces: list of ROS Interface objects (connections to ROS 2 system)
- input_sources: list of string (topics/services/actions the agent subscribes to)
- output_targets: list of string (topics/services/actions the agent publishes to)

### Humanoid Robot
**Description**: A robot with human-like characteristics including limbs and structure that can be controlled through the ROS 2 system

**Attributes**:
- robot_name: string (name of the humanoid robot)
- urdf_model: URDF Model object (physical structure definition)
- joint_controllers: list of Controller objects (actuator control systems)
- sensor_configurations: list of Sensor objects (sensor setups)
- kinematic_chain: list of Joint objects (limb structure definitions)