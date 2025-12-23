---
sidebar_position: 6
title: "Chapter 3 - Capstone: Autonomous Humanoid"
---

# Chapter 3: Capstone Project - Autonomous Humanoid

## Overview

This capstone project integrates all concepts learned in the previous chapters to create a fully autonomous humanoid robot system. You'll implement voice-driven navigation and manipulation with object recognition and path planning capabilities.

## Learning Objectives

By completing this capstone project, you will be able to:
- Integrate voice recognition, cognitive planning, and robotic execution
- Implement voice-driven navigation for humanoid robots
- Create manipulation systems that respond to voice commands
- Combine object recognition with path planning for autonomous behavior
- Design comprehensive systems that demonstrate VLA capabilities

## Project Architecture

The autonomous humanoid system combines three core components:

1. **Voice Interface Layer**: Processes natural language commands using OpenAI Whisper and LLMs
2. **Cognitive Planning Layer**: Translates high-level goals into executable action sequences
3. **Robot Execution Layer**: Executes navigation, manipulation, and perception tasks

### System Integration Diagram

```
[User Voice Command]
        ↓
[Speech Recognition (Whisper)]
        ↓
[Natural Language Processing]
        ↓
[LLM-Based Task Planner]
        ↓
[Action Sequence Generator]
        ↓
[ROS 2 Action Execution]
    ↙        ↘
[Navigation]   [Manipulation & Perception]
```

## Voice-Driven Navigation Implementation

Let's implement the complete voice-driven navigation system:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Point
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import openai
import json
import speech_recognition as sr
import cv2
import numpy as np

class AutonomousHumanoid(Node):
    def __init__(self):
        super().__init__('autonomous_humanoid')

        # Initialize components
        self.openai_client = openai.OpenAI()
        self.recognizer = sr.Recognizer()
        self.cv_bridge = CvBridge()

        # Initialize ROS 2 action clients
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.manip_client = ActionClient(self, ManipulateObject, 'manipulate_object')
        self.perception_client = ActionClient(self, DetectObjects, 'detect_objects')

        # Create subscribers and publishers
        self.voice_sub = self.create_subscription(
            String, 'voice_commands', self.voice_command_callback, 10
        )
        self.image_sub = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10
        )

        # System state
        self.current_location = None
        self.known_objects = {}
        self.navigation_goals = self.define_navigation_goals()

        self.get_logger().info('Autonomous Humanoid system initialized')

    def define_navigation_goals(self):
        """
        Define common navigation goals in the environment
        """
        return {
            "kitchen": self.create_pose(1.0, 2.0, 0.0),
            "living room": self.create_pose(-1.0, 1.0, 1.57),
            "bedroom": self.create_pose(2.0, -1.0, 3.14),
            "dining room": self.create_pose(0.0, -2.0, -1.57),
            "office": self.create_pose(-2.0, 0.0, 0.0)
        }

    def create_pose(self, x, y, theta):
        """
        Create a PoseStamped message
        """
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0

        # Convert theta to quaternion
        from math import sin, cos
        pose.pose.orientation.z = sin(theta / 2.0)
        pose.pose.orientation.w = cos(theta / 2.0)

        return pose

    def voice_command_callback(self, msg):
        """
        Handle voice commands from user
        """
        command = msg.data
        self.get_logger().info(f'Received voice command: {command}')

        # Process command using LLM for cognitive planning
        plan = self.process_voice_command(command)

        if plan:
            self.execute_plan(plan)
        else:
            self.get_logger().error('Failed to process voice command')

    def process_voice_command(self, command: str):
        """
        Process voice command using LLM-based cognitive planning
        """
        # Get environmental context
        context = self.get_environmental_context()

        prompt = f"""
        You are an intelligent robot assistant. Based on the current environmental context and user command, generate a detailed action plan.

        Environmental Context:
        {context}

        User Command: "{command}"

        Generate a JSON action plan with the following structure:
        {{
            "intent": "high-level intent",
            "action_sequence": [
                {{
                    "step": 1,
                    "action_type": "navigate|manipulate|perceive|other",
                    "parameters": {{"param1": "value1", ...}},
                    "description": "What this step does"
                }}
            ],
            "estimated_duration": "in seconds",
            "required_capabilities": ["list", "of", "capabilities"]
        }}

        Consider safety, efficiency, and the robot's current state.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            plan_data = json.loads(response.choices[0].message.content)
            return plan_data

        except Exception as e:
            self.get_logger().error(f'Error processing voice command: {e}')
            return self.fallback_plan(command)

    def get_environmental_context(self):
        """
        Get current environmental context for the LLM
        """
        context = {
            "current_location": str(self.current_location),
            "known_objects": self.known_objects,
            "navigation_goals": list(self.navigation_goals.keys()),
            "robot_capabilities": ["navigation", "manipulation", "perception"]
        }
        return json.dumps(context, indent=2)

    def execute_plan(self, plan: dict):
        """
        Execute the action plan generated by the LLM
        """
        self.get_logger().info(f'Executing plan: {plan["intent"]}')

        for step in plan.get('action_sequence', []):
            self.get_logger().info(f'Executing step: {step["description"]}')

            success = self.execute_action_step(step)

            if not success:
                self.get_logger().error(f'Step failed: {step["description"]}')
                # Attempt recovery or ask for clarification
                self.handle_failure(step, plan)
                break
            else:
                self.get_logger().info(f'Step completed successfully: {step["description"]}')

    def execute_action_step(self, step: dict) -> bool:
        """
        Execute a single action step
        """
        action_type = step['action_type']
        parameters = step['parameters']

        if action_type == 'navigate':
            return self.execute_navigation(parameters)
        elif action_type == 'manipulate':
            return self.execute_manipulation(parameters)
        elif action_type == 'perceive':
            return self.execute_perception(parameters)
        elif action_type == 'wait':
            return self.execute_wait(parameters)
        else:
            self.get_logger().warn(f'Unknown action type: {action_type}')
            return False

    def execute_navigation(self, params: dict) -> bool:
        """
        Execute navigation action
        """
        try:
            # Get target location
            target_location = params.get('location', '').lower()

            if target_location in self.navigation_goals:
                goal_pose = self.navigation_goals[target_location]
            else:
                # Try to parse coordinates if location not predefined
                x = params.get('x')
                y = params.get('y')
                if x is not None and y is not None:
                    goal_pose = self.create_pose(x, y, 0.0)
                else:
                    self.get_logger().error(f'Unknown navigation target: {target_location}')
                    return False

            # Wait for navigation server
            if not self.nav_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error('Navigation server not available')
                return False

            # Send navigation goal
            goal_msg = NavigateToPose.Goal()
            goal_msg.pose = goal_pose

            future = self.nav_client.send_goal_async(goal_msg)
            rclpy.spin_until_future_complete(self, future)

            result = future.result()
            if result and result.success:
                self.current_location = target_location
                self.get_logger().info(f'Navigation to {target_location} completed successfully')
                return True
            else:
                self.get_logger().error(f'Navigation failed')
                return False

        except Exception as e:
            self.get_logger().error(f'Navigation execution error: {e}')
            return False

    def execute_manipulation(self, params: dict) -> bool:
        """
        Execute manipulation action
        """
        try:
            # Wait for manipulation server
            if not self.manip_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error('Manipulation server not available')
                return False

            # Create manipulation goal
            goal_msg = ManipulateObject.Goal()
            goal_msg.object_name = params.get('object', '')
            goal_msg.action_type = params.get('action', 'grasp')
            goal_msg.target_pose = self.get_object_pose(params.get('object', ''))

            future = self.manip_client.send_goal_async(goal_msg)
            rclpy.spin_until_future_complete(self, future)

            result = future.result()
            if result and result.success:
                self.get_logger().info(f'Manipulation completed successfully')
                return True
            else:
                self.get_logger().error(f'Manipulation failed')
                return False

        except Exception as e:
            self.get_logger().error(f'Manipulation execution error: {e}')
            return False

    def execute_perception(self, params: dict) -> bool:
        """
        Execute perception action
        """
        try:
            # Wait for perception server
            if not self.perception_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error('Perception server not available')
                return False

            # Create perception goal
            goal_msg = DetectObjects.Goal()
            goal_msg.target_object = params.get('target', '')
            goal_msg.search_area = params.get('area', 'current_view')

            future = self.perception_client.send_goal_async(goal_msg)
            rclpy.spin_until_future_complete(self, future)

            result = future.result()
            if result and result.found_objects:
                # Update known objects
                for obj in result.found_objects:
                    self.known_objects[obj.name] = obj.pose
                self.get_logger().info(f'Perception completed, found {len(result.found_objects)} objects')
                return True
            else:
                self.get_logger().info(f'Perception completed, no target objects found')
                return True  # Perception itself succeeded, even if target not found

        except Exception as e:
            self.get_logger().error(f'Perception execution error: {e}')
            return False

    def execute_wait(self, params: dict) -> bool:
        """
        Execute wait action
        """
        try:
            duration = params.get('duration', 1.0)  # Default 1 second
            self.get_logger().info(f'Waiting for {duration} seconds')

            # Simple sleep - in real implementation, use ROS timers
            import time
            time.sleep(duration)

            return True
        except Exception as e:
            self.get_logger().error(f'Wait execution error: {e}')
            return False

    def handle_failure(self, failed_step: dict, original_plan: dict):
        """
        Handle failure of a step in the plan
        """
        # Log failure
        self.get_logger().error(f'Step failed: {failed_step}')

        # Optionally, ask user for clarification or try alternative
        # This could involve sending a message back to the user
        feedback_msg = String()
        feedback_msg.data = f"I encountered an issue with: {failed_step['description']}. Could you please clarify?"

        # Publish feedback (assuming there's a feedback publisher)
        # self.feedback_pub.publish(feedback_msg)

    def fallback_plan(self, command: str):
        """
        Create a simple fallback plan if LLM processing fails
        """
        # Simple keyword-based fallback
        if "go to" in command.lower():
            location = command.lower().replace("go to", "").strip()
            return {
                "intent": f"navigate to {location}",
                "action_sequence": [
                    {
                        "step": 1,
                        "action_type": "navigate",
                        "parameters": {"location": location},
                        "description": f"Navigate to {location}"
                    }
                ],
                "estimated_duration": "30",
                "required_capabilities": ["navigation"]
            }
        # Add more fallback patterns as needed
        return None

    def image_callback(self, msg):
        """
        Process incoming images for object recognition
        """
        try:
            # Convert ROS image to OpenCV format
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Perform basic object detection (placeholder - in practice, use YOLO, etc.)
            # objects = self.detect_objects(cv_image)

            # Update known objects if needed
            # self.update_known_objects(objects)

        except Exception as e:
            self.get_logger().error(f'Image processing error: {e}')

    def get_object_pose(self, object_name: str):
        """
        Get the pose of a known object
        """
        if object_name in self.known_objects:
            return self.known_objects[object_name]
        else:
            # Return a default pose or trigger perception to find the object
            return self.create_pose(0.0, 0.0, 0.0).pose


def main(args=None):
    rclpy.init(args=args)
    humanoid = AutonomousHumanoid()

    try:
        rclpy.spin(humanoid)
    except KeyboardInterrupt:
        pass
    finally:
        humanoid.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Object Recognition and Path Planning

### Object Recognition Integration

The system integrates object recognition to identify and locate objects in the environment:

```python
class ObjectRecognition:
    def __init__(self):
        # Initialize object detection model (e.g., YOLO, SSD, etc.)
        self.detection_model = self.load_detection_model()
        self.object_database = self.load_object_database()

    def detect_objects(self, image):
        """
        Detect objects in the provided image
        """
        # Run object detection
        detections = self.detection_model(image)

        # Filter and process detections
        recognized_objects = []
        for detection in detections:
            if detection.confidence > 0.5:  # Confidence threshold
                obj_info = {
                    'name': detection.class_name,
                    'confidence': detection.confidence,
                    'bbox': detection.bbox,
                    'pose_3d': self.estimate_3d_pose(detection.bbox, image)
                }
                recognized_objects.append(obj_info)

        return recognized_objects

    def estimate_3d_pose(self, bbox, image):
        """
        Estimate 3D pose of object from 2D bounding box
        """
        # Use depth information or geometric estimation
        # This is a simplified approach
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2

        # Convert to 3D coordinates (simplified)
        x_3d = (center_x - image.shape[1]/2) * 0.001  # Simplified conversion
        y_3d = (center_y - image.shape[0]/2) * 0.001
        z_3d = 1.0  # Placeholder depth

        return {'x': x_3d, 'y': y_3d, 'z': z_3d}
```

### Path Planning Integration

The system uses path planning to navigate safely around obstacles:

```python
class PathPlanner:
    def __init__(self):
        # Initialize path planning (e.g., A*, RRT, etc.)
        self.map = None
        self.planner = self.initialize_planner()

    def plan_path(self, start_pose, goal_pose, obstacles):
        """
        Plan a safe path from start to goal avoiding obstacles
        """
        # Update map with current obstacles
        self.update_map_with_obstacles(obstacles)

        # Plan path using chosen algorithm
        path = self.planner.plan(start_pose, goal_pose, self.map)

        return path

    def update_map_with_obstacles(self, obstacles):
        """
        Update the occupancy map with detected obstacles
        """
        # Integrate obstacle information into the map
        for obstacle in obstacles:
            self.map.set_occupied(obstacle.pose, obstacle.size)
```

## Complete Integration Example

Here's how all components work together in the complete system:

```python
class CompleteVLASystem:
    def __init__(self):
        # Initialize all subsystems
        self.voice_interface = VoiceInterface()
        self.cognitive_planner = CognitivePlanner()
        self.robot_executor = RobotExecutor()
        self.object_recognizer = ObjectRecognition()
        self.path_planner = PathPlanner()

        # Connect components
        self.voice_interface.on_command_received = self.on_voice_command
        self.robot_executor.on_task_completed = self.on_task_completed

    def on_voice_command(self, command):
        """
        Handle voice command through the complete pipeline
        """
        # 1. Process voice command (V - Voice)
        text = self.voice_interface.speech_to_text(command)

        # 2. Cognitive planning (L - Language)
        action_plan = self.cognitive_planner.plan_from_command(text)

        # 3. Execute robot actions (A - Action)
        self.robot_executor.execute_plan(action_plan)

    def on_task_completed(self, task_result):
        """
        Handle task completion, potentially triggering perception or planning updates
        """
        # Update world model based on task completion
        self.update_world_model(task_result)

        # Check if additional actions are needed
        self.check_for_follow_up_actions()
```

## Testing the Complete System

To test the complete autonomous humanoid system:

1. **Environment Setup**: Configure your simulation or real robot environment
2. **Component Integration**: Ensure all components are properly connected
3. **Command Testing**: Test various voice commands to verify the complete pipeline
4. **Edge Case Handling**: Test scenarios with ambiguous commands or failed actions
5. **Performance Evaluation**: Measure response time and accuracy

## Interactive Exercise

Implement a simplified version of the autonomous humanoid that can handle these commands:
- "Go to the kitchen and bring me the red cup"
- "Find the ball and show it to me"
- "Move to the living room and wait there"

Your implementation should demonstrate the integration of voice recognition, cognitive planning, and robot execution.

## Summary

In this capstone project, you have:
- Integrated voice recognition, cognitive planning, and robotic execution
- Implemented voice-driven navigation and manipulation
- Combined object recognition with path planning
- Created a comprehensive autonomous humanoid system

This completes the Vision-Language-Action learning module, demonstrating how these three components work together to create intelligent robotic systems that can understand and respond to natural human commands.

## Next Steps

[Complete Capstone Assessment](./capstone-assessment.md)

[View Module Summary](./summary.md)

[Back to Chapter 2: Cognitive Planning with LLMs](./chapter2-cognitive-planning.md)