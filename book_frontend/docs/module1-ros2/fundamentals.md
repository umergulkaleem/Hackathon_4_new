---
sidebar_label: 'ROS 2 Fundamentals'
sidebar_position: 1
---

# ROS 2 Fundamentals

## What is ROS 2?

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

ROS 2 is the next generation of the Robot Operating System, designed to address the limitations of ROS 1 and provide enhanced features for modern robotics applications, including support for real-time systems, security, and multi-robot systems.

## ROS 2 Architecture

ROS 2 uses a **DDS (Data Distribution Service)** based architecture. Unlike ROS 1 which used a centralized master, ROS 2 implements a distributed architecture where each node can discover other nodes directly.

### Key Architecture Components:

- **Nodes**: A node is a process that performs computation. Nodes are combined together into a ROS graph to do work.
- **DDS Implementation**: ROS 2 uses DDS as the underlying middleware for communication between nodes.
- **RMW (ROS Middleware)**: This layer abstracts the underlying DDS implementation, allowing ROS 2 to work with different DDS vendors.

## The ROS Graph

The ROS graph refers to the network of ROS processes (nodes) that are communicating with each other. This graph is formed by the nodes, topics, services, actions, and parameters that make up your ROS system.

### Components of the ROS Graph:

- **Nodes**: Individual processes that perform computation
- **Topics**: Named buses over which nodes exchange messages
- **Services**: Synchronous request/response communication
- **Actions**: Asynchronous goal-oriented communication with feedback
- **Parameters**: Global configuration values
- **Layers**: Communication layers that enable message passing

## Middleware Role in Physical AI Systems

ROS 2 serves as the middleware in Physical AI systems by:

1. **Abstraction Layer**: Provides a consistent interface for hardware and software components regardless of the underlying implementation
2. **Communication Framework**: Enables seamless communication between AI algorithms and physical robot systems
3. **Modularity**: Allows different components to be developed, tested, and maintained independently
4. **Real-time Capabilities**: Supports time-critical operations required for robot control
5. **Distributed Computing**: Enables multi-robot systems and cloud robotics applications

## DDS Concepts

DDS (Data Distribution Service) is a middleware specification that enables scalable, real-time, dependable, and efficient data exchanges between devices. In ROS 2, DDS provides:

- **Publisher/Subscriber Model**: Data producers publish information to topics, and data consumers subscribe to topics
- **Quality of Service (QoS)**: Configurable policies for reliability, durability, liveliness, and other communication characteristics
- **Discovery**: Automatic discovery of publishers and subscribers
- **Data-Centricity**: The system is organized around data rather than services

### Quality of Service (QoS) Policies

QoS policies allow you to specify how data should be delivered based on your application's requirements:

- **Reliability**: Best effort or reliable delivery
- **Durability**: Volatile or transient local durability
- **History**: Keep last N samples or keep all samples
- **Liveliness**: Automatic, manual by topic, or manual by node

## Interactive Exercise

Try out the following concepts by creating a simple ROS 2 node that demonstrates the publish/subscribe pattern:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HelloWorldPublisher(Node):
    def __init__(self):
        super().__init__('hello_world_publisher')
        self.publisher = self.create_publisher(String, 'hello', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    hello_world_publisher = HelloWorldPublisher()
    rclpy.spin(hello_world_publisher)
    hello_world_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This example demonstrates:
- Creating a ROS 2 node
- Setting up a publisher
- Using a timer to publish messages at regular intervals
- Proper initialization and shutdown procedures