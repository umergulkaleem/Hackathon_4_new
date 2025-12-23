# Chapter 3: Integrating Gazebo & Unity

## Introduction

Welcome to Chapter 3 of Module 2: The Digital Twin (Gazebo & Unity). In this chapter, you will learn how to connect Gazebo physics simulation with Unity rendering to create synchronized environments. By the end of this chapter, you will be able to successfully connect Gazebo and Unity to create environments that accurately represent both physical and visual aspects for AI training and testing.

## Learning Objectives

After completing this chapter, you will be able to:
- Establish communication between Gazebo and Unity using ROS 2
- Implement state synchronization mechanisms between simulators
- Develop coordinate system transformation techniques
- Map data between Gazebo and Unity entities
- Configure communication protocols for real-time synchronization
- Optimize latency for smooth simulation performance
- Create integrated simulation examples for AI testing
- Prepare AI testing environments with synchronized physics and rendering

## Prerequisites

Before starting this chapter, you should have:
- Completed Chapter 1: Gazebo Physics Simulation
- Completed Chapter 2: Unity for High-Fidelity Rendering
- Understanding of ROS 2 concepts (topics, services, actions)
- Basic knowledge of networking and communication protocols
- Familiarity with both Gazebo and Unity environments

## Understanding the Integration Architecture

### The Digital Twin Concept

A digital twin in robotics combines:
- **Physics Simulation**: Accurate physical behavior (Gazebo)
- **Visual Rendering**: High-fidelity visualization (Unity)
- **Real-time Synchronization**: Continuous state exchange between systems

### Integration Approaches

There are several approaches to integrate Gazebo and Unity:

1. **ROS 2 Bridge**: Use ROS 2 as the communication backbone
2. **Direct Communication**: Custom protocols over TCP/UDP
3. **Middleware Solutions**: Specialized tools like Unity Robotics Hub
4. **Cloud Integration**: Remote synchronization services

### Architecture Overview

```
[Unity Scene] ↔ [ROS 2 Bridge] ↔ [Gazebo Simulation]
     ↓              ↓                  ↓
[Visual State]  [State Sync]    [Physics State]
```

## ROS 2 Communication Bridge

### Setting Up the Bridge

The ROS 2 bridge is the most common approach for connecting Gazebo and Unity:

1. **Install ROS 2 Bridge Package**:
   ```bash
   sudo apt install ros-humble-ros-gz-bridge
   # or for newer versions:
   sudo apt install ros-humble-ros-ign-bridge
   ```

2. **Create Bridge Configuration**:
   Define which topics to synchronize between Gazebo and Unity.

### Bridge Implementation

```python
# Python bridge example
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage
import socket
import json

class GazeboUnityBridge(Node):
    def __init__(self):
        super().__init__('gazebo_unity_bridge')

        # Publishers for Unity
        self.unity_tf_publisher = self.create_publisher(TFMessage, '/unity/tf', 10)

        # Subscribers from Gazebo
        self.gazebo_tf_subscriber = self.create_subscription(
            TFMessage,
            '/tf',
            self.tf_callback,
            10
        )

        # Timer for synchronization
        self.timer = self.create_timer(0.033, self.sync_callback) # ~30 Hz

        self.get_logger().info('Gazebo-Unity Bridge initialized')

    def tf_callback(self, msg):
        """Handle transforms from Gazebo"""
        # Process and potentially modify transforms for Unity
        processed_msg = self.process_transforms(msg)

        # Publish to Unity
        self.unity_tf_publisher.publish(processed_msg)

    def process_transforms(self, tf_msg):
        """Process transforms for Unity coordinate system"""
        processed_transforms = []

        for transform in tf_msg.transforms:
            # Convert from Gazebo to Unity coordinate system
            unity_transform = self.convert_to_unity_coords(transform)
            processed_transforms.append(unity_transform)

        tf_msg.transforms = processed_transforms
        return tf_msg

    def convert_to_unity_coords(self, transform):
        """Convert Gazebo coordinates to Unity coordinates"""
        # Gazebo: X=forward, Y=left, Z=up
        # Unity: X=right, Y=up, Z=forward
        new_transform = TransformStamped()
        new_transform.header = transform.header

        # Position conversion
        new_transform.transform.translation.x = transform.transform.translation.y
        new_transform.transform.translation.y = transform.transform.translation.z
        new_transform.transform.translation.z = transform.transform.translation.x

        # Rotation conversion (quaternion)
        new_transform.transform.rotation.w = transform.transform.rotation.w
        new_transform.transform.rotation.x = transform.transform.rotation.x
        new_transform.transform.rotation.y = transform.transform.rotation.y
        new_transform.transform.rotation.z = transform.transform.rotation.z

        return new_transform

    def sync_callback(self):
        """Periodic synchronization callback"""
        self.get_logger().debug('Synchronization tick')

def main(args=None):
    rclpy.init(args=args)
    bridge = GazeboUnityBridge()

    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        bridge.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Unity ROS 2 Integration

To connect Unity to ROS 2, use the Unity Robotics Hub:

1. **Install Unity ROS TCP Connector**:
   - Import the ROS TCP Connector package into Unity
   - Configure the connection settings

2. **Unity Bridge Script**:
```csharp
using UnityEngine;
using Ros2Unity;
using System.Collections;
using System.Collections.Generic;
using System;

public class UnityGazeboBridge : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosMasterUri = "http://localhost:11311";
    public string gazeboHost = "127.0.0.1";
    public int gazeboPort = 11345;

    [Header("Synchronization Settings")]
    public float syncRate = 30.0f; // Hz
    public bool enablePhysicsSync = true;
    public bool enableVisualSync = true;

    private Ros2Socket rosSocket;
    private Dictionary<string, GameObject> entityMap;

    void Start()
    {
        // Initialize ROS connection
        Ros2UnityInit.Init();
        rosSocket = Ros2SocketFactory.Create();

        // Connect to ROS master
        rosSocket.Connect(rosMasterUri);

        // Initialize entity mapping
        entityMap = new Dictionary<string, GameObject>();

        // Start synchronization
        StartCoroutine(SynchronizationLoop());
    }

    IEnumerator SynchronizationLoop()
    {
        while (true)
        {
            if (enablePhysicsSync)
            {
                SyncPhysicsStates();
            }

            if (enableVisualSync)
            {
                SyncVisualStates();
            }

            yield return new WaitForSeconds(1.0f / syncRate);
        }
    }

    void SyncPhysicsStates()
    {
        // Send Unity physics states to Gazebo
        foreach (var entity in entityMap)
        {
            var rb = entity.Value.GetComponent<Rigidbody>();
            if (rb != null)
            {
                SendPhysicsState(entity.Key, rb.position, rb.rotation, rb.velocity);
            }
        }
    }

    void SyncVisualStates()
    {
        // Update Unity visuals from Gazebo states
        // This would typically receive TF messages from Gazebo
        ReceiveVisualStates();
    }

    void SendPhysicsState(string entityName, Vector3 position, Quaternion rotation, Vector3 velocity)
    {
        // Send physics state to Gazebo via ROS
        // Implementation depends on specific message types
    }

    void ReceiveVisualStates()
    {
        // Receive visual states from Gazebo
        // Update Unity GameObject positions/rotations
    }

    void OnDestroy()
    {
        if (rosSocket != null)
        {
            rosSocket.Dispose();
        }
    }
}
```

## State Synchronization Mechanisms

### Transform Synchronization

Synchronize positions and orientations between simulators:

```python
# Transform synchronization example
import rclpy
from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage
import tf2_ros
import tf2_geometry_msgs
from rclpy.qos import QoSProfile

class StateSynchronizer:
    def __init__(self, node):
        self.node = node
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, node)

        # Publishers for synchronization
        qos_profile = QoSProfile(depth=10)
        self.gazebo_tf_pub = node.create_publisher(TFMessage, '/gazebo/tf_sync', qos_profile)
        self.unity_tf_pub = node.create_publisher(TFMessage, '/unity/tf_sync', qos_profile)

        # Timer for sync
        self.sync_timer = node.create_timer(0.033, self.synchronize_states)

    def synchronize_states(self):
        """Synchronize states between Gazebo and Unity"""
        try:
            # Get transforms from both systems
            gazebo_transforms = self.get_gazebo_transforms()
            unity_transforms = self.get_unity_transforms()

            # Apply transforms to maintain consistency
            self.apply_transforms_to_gazebo(unity_transforms)
            self.apply_transforms_to_unity(gazebo_transforms)

        except Exception as e:
            self.node.get_logger().error(f'State synchronization error: {e}')

    def get_gazebo_transforms(self):
        """Get current transforms from Gazebo"""
        # Implementation to query Gazebo transforms
        transforms = []
        # This would typically query Gazebo via services or topics
        return transforms

    def get_unity_transforms(self):
        """Get current transforms from Unity"""
        # Implementation to query Unity transforms
        transforms = []
        # This would typically receive from Unity via ROS
        return transforms

    def apply_transforms_to_gazebo(self, transforms):
        """Apply transforms to Gazebo entities"""
        # Send transforms to Gazebo to update physics
        pass

    def apply_transforms_to_unity(self, transforms):
        """Apply transforms to Unity entities"""
        # Send transforms to Unity to update visuals
        pass
```

### Physics State Synchronization

Synchronize physics properties like velocity, acceleration, and forces:

```python
# Physics synchronization example
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray
import numpy as np

class PhysicsSynchronizer:
    def __init__(self, node):
        self.node = node

        # Publishers for physics states
        self.gazebo_cmd_pub = node.create_publisher(Float64MultiArray, '/gazebo/joint_commands', 10)
        self.unity_cmd_pub = node.create_publisher(Twist, '/unity/physics_commands', 10)

        # Subscribers for physics feedback
        self.gazebo_state_sub = node.create_subscription(
            Float64MultiArray, '/gazebo/joint_states', self.gazebo_state_callback, 10
        )
        self.unity_state_sub = node.create_subscription(
            Twist, '/unity/physics_states', self.unity_state_callback, 10
        )

        self.last_gazebo_state = None
        self.last_unity_state = None

    def gazebo_state_callback(self, msg):
        """Handle physics state from Gazebo"""
        self.last_gazebo_state = msg.data
        self.synchronize_physics()

    def unity_state_callback(self, msg):
        """Handle physics state from Unity"""
        self.last_unity_state = msg
        self.synchronize_physics()

    def synchronize_physics(self):
        """Synchronize physics states between systems"""
        if self.last_gazebo_state and self.last_unity_state:
            # Calculate physics differences and apply corrections
            self.correct_physics_states()

    def correct_physics_states(self):
        """Apply corrections to maintain physics consistency"""
        # Implementation to maintain physics consistency
        pass
```

## Coordinate System Transformation

### Understanding Coordinate Systems

Gazebo and Unity use different coordinate systems:
- **Gazebo**: X=forward, Y=left, Z=up (right-handed)
- **Unity**: X=right, Y=up, Z=forward (left-handed)

### Transformation Implementation

```python
import numpy as np
from geometry_msgs.msg import Point, Quaternion, Transform
import math

def gazebo_to_unity_position(gz_pos):
    """Convert Gazebo position to Unity position"""
    unity_pos = Point()
    unity_pos.x = gz_pos.y  # Gazebo Y -> Unity X
    unity_pos.y = gz_pos.z  # Gazebo Z -> Unity Y
    unity_pos.z = gz_pos.x  # Gazebo X -> Unity Z
    return unity_pos

def unity_to_gazebo_position(unity_pos):
    """Convert Unity position to Gazebo position"""
    gz_pos = Point()
    gz_pos.x = unity_pos.z  # Unity Z -> Gazebo X
    gz_pos.y = unity_pos.x  # Unity X -> Gazebo Y
    gz_pos.z = unity_pos.y  # Unity Y -> Gazebo Z
    return gz_pos

def gazebo_to_unity_quaternion(gz_quat):
    """Convert Gazebo quaternion to Unity quaternion"""
    # This requires more complex conversion due to coordinate system differences
    # Implementation depends on the specific rotation order
    unity_quat = Quaternion()

    # Simplified conversion - actual implementation may vary
    unity_quat.w = gz_quat.w
    unity_quat.x = gz_quat.x
    unity_quat.y = gz_quat.y
    unity_quat.z = gz_quat.z

    return unity_quat

def transform_point(point, translation, rotation):
    """Apply transform to a point"""
    # Convert to homogeneous coordinates
    p = np.array([point.x, point.y, point.z, 1.0])

    # Create transformation matrix
    # This is a simplified example - full implementation would be more complex
    transform_matrix = create_transform_matrix(translation, rotation)

    # Apply transformation
    transformed_p = transform_matrix @ p

    result = Point()
    result.x = transformed_p[0]
    result.y = transformed_p[1]
    result.z = transformed_p[2]

    return result

def create_transform_matrix(translation, rotation):
    """Create a 4x4 transformation matrix"""
    # Implementation of transformation matrix creation
    # This would include rotation matrix and translation
    pass
```

## Data Mapping Between Systems

### Entity Mapping

Map entities between Gazebo and Unity:

```python
class EntityMapper:
    def __init__(self):
        self.gazebo_to_unity_map = {}
        self.unity_to_gazebo_map = {}
        self.next_entity_id = 1

    def register_entity_pair(self, gazebo_name, unity_name):
        """Register a pair of corresponding entities"""
        entity_id = self.next_entity_id
        self.next_entity_id += 1

        self.gazebo_to_unity_map[gazebo_name] = {
            'unity_name': unity_name,
            'entity_id': entity_id
        }
        self.unity_to_gazebo_map[unity_name] = {
            'gazebo_name': gazebo_name,
            'entity_id': entity_id
        }

        return entity_id

    def get_unity_entity(self, gazebo_name):
        """Get Unity name for a Gazebo entity"""
        if gazebo_name in self.gazebo_to_unity_map:
            return self.gazebo_to_unity_map[gazebo_name]['unity_name']
        return None

    def get_gazebo_entity(self, unity_name):
        """Get Gazebo name for a Unity entity"""
        if unity_name in self.unity_to_gazebo_map:
            return self.unity_to_gazebo_map[unity_name]['gazebo_name']
        return None

    def get_entity_id(self, gazebo_name=None, unity_name=None):
        """Get entity ID for synchronization"""
        if gazebo_name and gazebo_name in self.gazebo_to_unity_map:
            return self.gazebo_to_unity_map[gazebo_name]['entity_id']
        elif unity_name and unity_name in self.unity_to_gazebo_map:
            return self.unity_to_gazebo_map[unity_name]['entity_id']
        return None
```

### Sensor Data Mapping

Map sensor data between systems:

```python
from sensor_msgs.msg import LaserScan, Image, Imu
from geometry_msgs.msg import PointStamped

class SensorMapper:
    def __init__(self, entity_mapper):
        self.entity_mapper = entity_mapper
        self.sensor_mapping = {}

    def register_sensor_mapping(self, gazebo_sensor_name, unity_sensor_name, sensor_type):
        """Register mapping between Gazebo and Unity sensors"""
        self.sensor_mapping[gazebo_sensor_name] = {
            'unity_sensor': unity_sensor_name,
            'type': sensor_type,
            'last_data': None
        }

    def process_gazebo_lidar(self, gazebo_sensor_name, scan_data):
        """Process LiDAR data from Gazebo and format for Unity"""
        unity_sensor_name = self.sensor_mapping.get(gazebo_sensor_name, {}).get('unity_sensor')
        if not unity_sensor_name:
            return None

        # Convert Gazebo LiDAR data format to Unity format
        unity_scan = self.convert_lidar_for_unity(scan_data)
        return unity_scan

    def convert_lidar_for_unity(self, scan_data):
        """Convert scan data for Unity visualization"""
        # Implementation to convert LaserScan to Unity-compatible format
        unity_scan = {
            'ranges': list(scan_data.ranges),
            'intensities': list(scan_data.intensities),
            'angle_min': scan_data.angle_min,
            'angle_max': scan_data.angle_max,
            'angle_increment': scan_data.angle_increment,
            'time_increment': scan_data.time_increment,
            'scan_time': scan_data.scan_time,
            'range_min': scan_data.range_min,
            'range_max': scan_data.range_max
        }
        return unity_scan

    def process_unity_camera(self, unity_sensor_name, camera_data):
        """Process camera data from Unity and format for Gazebo/ROS"""
        gazebo_sensor_name = None
        for gz_name, mapping in self.sensor_mapping.items():
            if mapping['unity_sensor'] == unity_sensor_name:
                gazebo_sensor_name = gz_name
                break

        if not gazebo_sensor_name:
            return None

        # Convert Unity camera data to ROS Image message
        ros_image = self.convert_camera_for_ros(camera_data)
        return ros_image
```

## Communication Protocols for Real-Time Synchronization

### Message Rate Optimization

Optimize communication rates for real-time performance:

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, target_rate_hz):
        self.target_rate = target_rate_hz
        self.target_interval = 1.0 / target_rate_hz
        self.last_publish_time = 0
        self.publish_history = deque(maxlen=100)

    def can_publish(self):
        """Check if enough time has passed to publish"""
        current_time = time.time()
        elapsed = current_time - self.last_publish_time
        return elapsed >= self.target_interval

    def record_publish(self):
        """Record a publish event"""
        current_time = time.time()
        if self.last_publish_time > 0:
            self.publish_history.append(current_time - self.last_publish_time)
        self.last_publish_time = current_time

    def get_actual_rate(self):
        """Get the actual publish rate over the last N messages"""
        if len(self.publish_history) < 2:
            return 0
        avg_interval = sum(self.publish_history) / len(self.publish_history)
        return 1.0 / avg_interval if avg_interval > 0 else 0

class SynchronizationManager:
    def __init__(self, node):
        self.node = node

        # Rate limiters for different data types
        self.position_rate_limiter = RateLimiter(60)  # 60 Hz for positions
        self.physics_rate_limiter = RateLimiter(100)  # 100 Hz for physics
        self.sensor_rate_limiter = RateLimiter(30)    # 30 Hz for sensors
        self.ui_rate_limiter = RateLimiter(10)       # 10 Hz for UI updates

    def publish_position_update(self, msg):
        """Publish position update with rate limiting"""
        if self.position_rate_limiter.can_publish():
            # Publish the message
            self.position_publisher.publish(msg)
            self.position_rate_limiter.record_publish()
            return True
        return False

    def publish_physics_update(self, msg):
        """Publish physics update with rate limiting"""
        if self.physics_rate_limiter.can_publish():
            self.physics_publisher.publish(msg)
            self.physics_rate_limiter.record_publish()
            return True
        return False
```

### Quality of Service (QoS) Configuration

Configure QoS settings for reliable communication:

```python
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy

class QoSConfig:
    @staticmethod
    def get_sync_qos():
        """QoS profile for synchronization messages"""
        return QoSProfile(
            depth=1,  # Only keep the most recent message
            reliability=QoSReliabilityPolicy.RELIABLE,  # Ensure delivery
            history=QoSHistoryPolicy.KEEP_LAST,  # Keep only last message
            durability=QoSDurabilityPolicy.VOLATILE  # Don't keep after disconnect
        )

    @staticmethod
    def get_sensor_qos():
        """QoS profile for sensor data"""
        return QoSProfile(
            depth=10,  # Keep more sensor messages
            reliability=QoSReliabilityPolicy.BEST_EFFORT,  # Allow some loss
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE
        )

    @staticmethod
    def get_control_qos():
        """QoS profile for control commands"""
        return QoSProfile(
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE
        )
```

## Latency Optimization Techniques

### Network Optimization

Minimize network latency between simulators:

```python
import socket
import struct
from threading import Thread
import queue

class OptimizedNetworkBridge:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)  # Increase send buffer
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)  # Increase receive buffer

        # Use non-blocking I/O
        self.socket.setblocking(False)

        self.send_queue = queue.Queue(maxsize=100)
        self.receive_queue = queue.Queue(maxsize=100)

    def send_data(self, data):
        """Send data with optimization"""
        try:
            # Pack data efficiently
            packed_data = self.pack_data(data)
            self.socket.sendto(packed_data, (self.host, self.port))
        except queue.Full:
            print("Send queue full, dropping packet")
        except Exception as e:
            print(f"Send error: {e}")

    def receive_data(self):
        """Receive data with optimization"""
        try:
            data, addr = self.socket.recvfrom(65536)
            unpacked_data = self.unpack_data(data)
            return unpacked_data
        except BlockingIOError:
            # No data available
            return None
        except Exception as e:
            print(f"Receive error: {e}")
            return None

    def pack_data(self, data):
        """Efficiently pack data for transmission"""
        # Implementation depends on data type
        # Use struct for basic types, or custom serialization
        pass

    def unpack_data(self, packed_data):
        """Efficiently unpack received data"""
        # Implementation depends on data type
        pass
```

### Prediction and Interpolation

Implement prediction to compensate for latency:

```python
import numpy as np
from collections import deque

class StatePredictor:
    def __init__(self, max_history=10):
        self.position_history = deque(maxlen=max_history)
        self.timestamp_history = deque(maxlen=max_history)
        self.velocity_history = deque(maxlen=max_history)

    def update_state(self, position, timestamp):
        """Update with new state information"""
        if len(self.position_history) > 0:
            # Calculate velocity from position change
            last_pos = self.position_history[-1]
            last_time = self.timestamp_history[-1]
            dt = timestamp - last_time

            if dt > 0:
                velocity = (position - last_pos) / dt
                self.velocity_history.append(velocity)

        self.position_history.append(position)
        self.timestamp_history.append(timestamp)

    def predict_state(self, future_time):
        """Predict state at future time"""
        if len(self.position_history) < 2:
            return self.position_history[-1] if self.position_history else np.array([0, 0, 0])

        # Use last known position and velocity for prediction
        current_pos = self.position_history[-1]
        current_vel = self.velocity_history[-1] if self.velocity_history else np.array([0, 0, 0])

        dt = future_time - self.timestamp_history[-1]
        predicted_pos = current_pos + current_vel * dt

        return predicted_pos

    def compensate_for_latency(self, latency_ms):
        """Compensate for network latency"""
        latency_s = latency_ms / 1000.0
        current_time = time.time()
        future_time = current_time + latency_s
        return self.predict_state(future_time)
```

## Integrated Simulation Examples

### Simple Robot Integration Example

Create a complete example integrating a simple robot:

```python
#!/usr/bin/env python3
# integrated_robot_example.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, Twist
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import tf2_ros
import math
import time

class IntegratedRobotExample(Node):
    def __init__(self):
        super().__init__('integrated_robot_example')

        # TF broadcaster for Unity
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        # Publishers for Unity
        self.unity_joint_pub = self.create_publisher(JointState, '/unity/joint_states', 10)
        self.unity_cmd_pub = self.create_publisher(Twist, '/unity/cmd_vel', 10)

        # Subscribers from Gazebo
        self.gazebo_joint_sub = self.create_subscription(
            JointState, '/gazebo/joint_states', self.joint_state_callback, 10
        )

        # Timer for synchronization
        self.timer = self.create_timer(0.033, self.sync_callback)  # ~30 Hz

        # Robot state
        self.robot_position = [0.0, 0.0, 0.0]
        self.robot_orientation = [0.0, 0.0, 0.0, 1.0]  # quaternion
        self.joint_positions = {}

        self.get_logger().info('Integrated Robot Example started')

    def joint_state_callback(self, msg):
        """Handle joint states from Gazebo"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_positions[name] = msg.position[i]

    def sync_callback(self):
        """Synchronization callback"""
        # Update robot state (simulated movement)
        self.update_robot_state()

        # Broadcast transforms to Unity
        self.broadcast_transforms()

        # Publish joint states to Unity
        self.publish_joint_states()

    def update_robot_state(self):
        """Update robot state for simulation"""
        # Simple movement pattern for demonstration
        current_time = time.time()
        self.robot_position[0] = math.sin(current_time * 0.5) * 2.0  # Move in X
        self.robot_position[1] = math.cos(current_time * 0.5) * 1.0  # Move in Y

    def broadcast_transforms(self):
        """Broadcast transforms to Unity"""
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'robot_base'

        t.transform.translation.x = self.robot_position[0]
        t.transform.translation.y = self.robot_position[1]
        t.transform.translation.z = self.robot_position[2]

        t.transform.rotation.x = self.robot_orientation[0]
        t.transform.rotation.y = self.robot_orientation[1]
        t.transform.rotation.z = self.robot_orientation[2]
        t.transform.rotation.w = self.robot_orientation[3]

        self.tf_broadcaster.sendTransform(t)

    def publish_joint_states(self):
        """Publish joint states to Unity"""
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'robot_base'

        # Add joint names and positions
        for joint_name, position in self.joint_positions.items():
            msg.name.append(joint_name)
            msg.position.append(position)
            # Add velocity and effort if available
            msg.velocity.append(0.0)  # Placeholder
            msg.effort.append(0.0)    # Placeholder

        self.unity_joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = IntegratedRobotExample()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### AI Testing Environment

Create an environment for AI testing with synchronized simulation:

```python
# ai_testing_environment.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, Twist
from sensor_msgs.msg import LaserScan, Image
from std_msgs.msg import Float32
import numpy as np
import random

class AITestingEnvironment(Node):
    def __init__(self):
        super().__init__('ai_testing_environment')

        # Publishers for AI agent
        self.laser_pub = self.create_publisher(LaserScan, '/ai/laser_scan', 10)
        self.camera_pub = self.create_publisher(Image, '/ai/camera', 10)
        self.odom_pub = self.create_publisher(Pose, '/ai/odometry', 10)

        # Subscribers from AI agent
        self.cmd_sub = self.create_subscription(
            Twist, '/ai/cmd_vel', self.ai_command_callback, 10
        )

        # Environment state
        self.robot_pose = Pose()
        self.environment_objects = []
        self.ai_score = 0.0

        # Timer for environment updates
        self.env_timer = self.create_timer(0.1, self.update_environment)
        self.sensor_timer = self.create_timer(0.033, self.publish_sensors)

        self.get_logger().info('AI Testing Environment initialized')

    def update_environment(self):
        """Update the testing environment"""
        # Move obstacles randomly
        for obj in self.environment_objects:
            # Random movement for dynamic obstacles
            obj.position.x += random.uniform(-0.1, 0.1)
            obj.position.y += random.uniform(-0.1, 0.1)

        # Update robot pose based on physics simulation
        # This would typically receive from Gazebo
        pass

    def publish_sensors(self):
        """Publish sensor data to AI agent"""
        # Publish laser scan
        laser_msg = self.generate_laser_scan()
        self.laser_pub.publish(laser_msg)

        # Publish camera image
        camera_msg = self.generate_camera_image()
        self.camera_pub.publish(camera_msg)

        # Publish odometry
        self.odom_pub.publish(self.robot_pose)

    def generate_laser_scan(self):
        """Generate simulated laser scan data"""
        scan = LaserScan()
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = 'laser_frame'

        scan.angle_min = -np.pi / 2
        scan.angle_max = np.pi / 2
        scan.angle_increment = np.pi / 180  # 1 degree
        scan.time_increment = 0.0
        scan.scan_time = 0.1
        scan.range_min = 0.1
        scan.range_max = 10.0

        # Generate ranges based on environment
        num_ranges = int((scan.angle_max - scan.angle_min) / scan.angle_increment) + 1
        ranges = []

        for i in range(num_ranges):
            angle = scan.angle_min + i * scan.angle_increment
            # Simulate distance to nearest obstacle
            distance = self.calculate_distance_to_obstacle(angle)
            ranges.append(min(distance, scan.range_max))

        scan.ranges = ranges
        return scan

    def calculate_distance_to_obstacle(self, angle):
        """Calculate distance to nearest obstacle at given angle"""
        # Simplified calculation - in reality this would use raycasting
        # or collision detection against environment objects
        return random.uniform(1.0, 5.0)

    def ai_command_callback(self, msg):
        """Handle commands from AI agent"""
        # Apply command to robot simulation in Gazebo
        # This would send commands to Gazebo physics engine
        linear_vel = msg.linear.x
        angular_vel = msg.angular.z

        # Update robot state based on command
        self.update_robot_from_command(linear_vel, angular_vel)

    def update_robot_from_command(self, linear, angular):
        """Update robot state from velocity commands"""
        # Update position based on velocity
        dt = 0.1  # Time step from timer
        self.robot_pose.position.x += linear * dt
        self.robot_pose.position.y += angular * dt * 0.1  # Simplified turning

        # Update orientation
        current_yaw = self.quaternion_to_euler(self.robot_pose.orientation)[2]
        new_yaw = current_yaw + angular * dt
        self.robot_pose.orientation = self.euler_to_quaternion(0, 0, new_yaw)

    def quaternion_to_euler(self, quat):
        """Convert quaternion to Euler angles"""
        # Simplified conversion
        import math
        sinr_cosp = 2 * (quat.w * quat.z + quat.x * quat.y)
        cosr_cosp = 1 - 2 * (quat.y * quat.y + quat.z * quat.z)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (quat.w * quat.y - quat.z * quat.x)
        pitch = math.asin(sinp)

        siny_cosp = 2 * (quat.w * quat.x + quat.y * quat.z)
        cosy_cosp = 1 - 2 * (quat.x * quat.x + quat.y * quat.y)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return (roll, pitch, yaw)

    def euler_to_quaternion(self, roll, pitch, yaw):
        """Convert Euler angles to quaternion"""
        from geometry_msgs.msg import Quaternion
        import math

        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        q = Quaternion()
        q.w = cr * cp * cy + sr * sp * sy
        q.x = sr * cp * cy - cr * sp * sy
        q.y = cr * sp * cy + sr * cp * sy
        q.z = cr * cp * sy - sr * sp * cy

        return q

def main(args=None):
    rclpy.init(args=args)
    node = AITestingEnvironment()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Practical Exercise: Complete Integration

Create a complete integration example with:

1. Gazebo simulation environment
2. Unity visualization environment
3. ROS 2 bridge for communication
4. Synchronized state management
5. AI testing capabilities

### Exercise Steps:

1. **Environment Setup**: Configure both Gazebo and Unity with the same scene
2. **Bridge Configuration**: Set up ROS 2 bridge for communication
3. **State Synchronization**: Implement position and physics synchronization
4. **Coordinate Conversion**: Handle coordinate system differences
5. **Sensor Mapping**: Connect sensors between systems
6. **AI Interface**: Create interface for AI testing

## Performance Considerations

### Synchronization Performance

Monitor and optimize synchronization performance:

```python
import time
from collections import deque
import statistics

class PerformanceMonitor:
    def __init__(self):
        self.sync_times = deque(maxlen=100)
        self.latency_measurements = deque(maxlen=100)
        self.last_sync_time = time.time()

    def start_sync(self):
        """Record start of synchronization"""
        self.last_sync_time = time.time()

    def end_sync(self):
        """Record end of synchronization and calculate performance"""
        current_time = time.time()
        sync_duration = current_time - self.last_sync_time
        self.sync_times.append(sync_duration)

        return sync_duration

    def get_avg_sync_time(self):
        """Get average synchronization time"""
        if not self.sync_times:
            return 0
        return statistics.mean(self.sync_times)

    def get_max_sync_time(self):
        """Get maximum synchronization time"""
        if not self.sync_times:
            return 0
        return max(self.sync_times)

    def get_sync_frequency(self):
        """Get actual synchronization frequency"""
        if len(self.sync_times) < 2:
            return 0
        avg_time = self.get_avg_sync_time()
        return 1.0 / avg_time if avg_time > 0 else 0

    def report_performance(self):
        """Report current performance metrics"""
        avg_time = self.get_avg_sync_time()
        max_time = self.get_max_sync_time()
        frequency = self.get_sync_frequency()

        print(f"Sync Performance: Avg={avg_time*1000:.2f}ms, "
              f"Max={max_time*1000:.2f}ms, "
              f"Freq={frequency:.2f}Hz")
```

## Troubleshooting Integration Issues

### Common Problems and Solutions

1. **Synchronization Drift**
   - **Problem**: Systems gradually fall out of sync
   - **Solution**: Implement periodic full-state synchronization

2. **Coordinate System Mismatches**
   - **Problem**: Objects appear in wrong positions/orientations
   - **Solution**: Verify coordinate transformation matrices

3. **Network Latency Issues**
   - **Problem**: Delayed responses between systems
   - **Solution**: Optimize message rates and implement prediction

4. **Physics Inconsistencies**
   - **Problem**: Different physics behaviors in each system
   - **Solution**: Ensure consistent physics parameters

5. **Performance Degradation**
   - **Problem**: Low frame rates or high CPU usage
   - **Solution**: Optimize update rates and data processing

### Debugging Tools

```python
class IntegrationDebugger:
    def __init__(self, node):
        self.node = node
        self.debug_publisher = node.create_publisher(String, '/integration/debug', 10)

    def log_sync_state(self, gazebo_state, unity_state, diff_threshold=0.1):
        """Log synchronization state for debugging"""
        diff = self.calculate_state_difference(gazebo_state, unity_state)

        if diff > diff_threshold:
            debug_msg = String()
            debug_msg.data = f"Synchronization drift detected: {diff:.3f}"
            self.debug_publisher.publish(debug_msg)
            self.node.get_logger().warn(f"Synchronization drift: {diff:.3f}")

    def calculate_state_difference(self, state1, state2):
        """Calculate difference between two states"""
        # Implementation depends on state structure
        # This is a simplified example
        return abs(state1.position.x - state2.position.x)
```

## Summary

In this chapter, you've learned:
- How to establish communication between Gazebo and Unity using ROS 2
- How to implement state synchronization mechanisms between simulators
- How to develop coordinate system transformation techniques
- How to map data between Gazebo and Unity entities
- How to configure communication protocols for real-time synchronization
- How to optimize latency for smooth simulation performance
- How to create integrated simulation examples for AI testing

## Next Steps

With all three chapters complete, you now have a comprehensive understanding of digital twin simulation using Gazebo and Unity. You can apply these concepts to create sophisticated simulation environments for robotics research and AI development.