---
sidebar_position: 2
title: Chapter 1 - Voice-to-Action Interfaces
---

# Chapter 1: Voice-to-Action Interfaces

## Overview

This chapter introduces you to the fundamental concepts of converting voice commands into robot actions. You'll learn about speech recognition using OpenAI Whisper and how to process voice commands into structured inputs that robotic systems can understand and execute.

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the basics of speech recognition and its applications in robotics
- Implement OpenAI Whisper for converting speech to text
- Process voice commands into structured robot actions
- Create ROS 2 action clients that respond to voice commands

## Speech Recognition Concepts

Speech recognition is a critical component of human-robot interaction. It enables robots to understand natural language commands and respond appropriately. The process typically involves:

1. **Audio Capture**: Recording the user's voice command
2. **Preprocessing**: Cleaning and normalizing the audio signal
3. **Feature Extraction**: Converting audio to features suitable for recognition
4. **Recognition**: Converting features to text
5. **Command Parsing**: Interpreting the text command for robot execution

### OpenAI Whisper

OpenAI Whisper is a state-of-the-art speech recognition system that can transcribe speech to text with high accuracy. It supports multiple languages and can handle various accents and background noise conditions.

## OpenAI Whisper Implementation

Let's implement a basic Whisper-based speech recognition system for our robot:

```python
import openai
import speech_recognition as sr
import rospy
from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatus
from your_robot_msgs.msg import RobotAction, RobotGoal

class VoiceToActionConverter:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('voice_to_action_converter')

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Set up ROS publisher and action client
        self.command_pub = rospy.Publisher('/robot_commands', String, queue_size=10)
        self.action_client = actionlib.SimpleActionClient('robot_action', RobotAction)

        # Wait for action server
        self.action_client.wait_for_server()

    def listen_and_convert(self):
        """Listen to voice command and convert to robot action"""
        with self.microphone as source:
            print("Listening for voice command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            # Use Whisper API to transcribe
            transcript = self.recognizer.recognize_whisper(audio, model="base")
            print(f"Recognized: {transcript}")

            # Parse the command and execute robot action
            self.parse_and_execute(transcript)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error: {e}")

    def parse_and_execute(self, command_text):
        """Parse the command text and execute appropriate robot action"""
        # Simple command parsing - in practice, you'd use more sophisticated NLP
        if "move forward" in command_text.lower():
            self.execute_move_action("forward")
        elif "turn left" in command_text.lower():
            self.execute_move_action("left")
        elif "turn right" in command_text.lower():
            self.execute_move_action("right")
        elif "stop" in command_text.lower():
            self.execute_stop_action()
        else:
            print(f"Unknown command: {command_text}")

    def execute_move_action(self, direction):
        """Execute movement action based on direction"""
        goal = RobotGoal()
        goal.action_type = "move"
        goal.direction = direction
        goal.speed = 0.5  # Default speed

        self.action_client.send_goal(goal)
        self.action_client.wait_for_result()

        result = self.action_client.get_result()
        print(f"Movement result: {result}")

    def execute_stop_action(self):
        """Execute stop action"""
        goal = RobotGoal()
        goal.action_type = "stop"

        self.action_client.send_goal(goal)
        self.action_client.wait_for_result()

        print("Robot stopped successfully")

if __name__ == '__main__':
    converter = VoiceToActionConverter()

    # Continuously listen for commands
    rate = rospy.Rate(1)  # Check for commands every second
    while not rospy.is_shutdown():
        converter.listen_and_convert()
        rate.sleep()
```

## Voice Command to Structured Input

Converting voice commands to structured robot inputs involves several steps:

### 1. Natural Language Understanding (NLU)

The system needs to understand the intent behind the spoken command. For example:
- "Move forward 2 meters" → Intent: Move, Direction: forward, Distance: 2 meters
- "Turn left and grab the red ball" → Intent: Complex action with multiple steps

### 2. Semantic Parsing

Convert the natural language into a structured format that the robot can understand:

```python
def semantic_parse(command_text):
    """
    Parse natural language command into structured format
    """
    # Example structured format
    structured_command = {
        "intent": "move",
        "parameters": {
            "direction": "forward",
            "distance": 2.0,
            "speed": 0.5
        },
        "confidence": 0.95
    }

    # Implementation would involve NLP techniques
    # For now, we'll use simple keyword matching
    if "move forward" in command_text.lower():
        structured_command["intent"] = "move"
        structured_command["parameters"]["direction"] = "forward"
    elif "move backward" in command_text.lower():
        structured_command["intent"] = "move"
        structured_command["parameters"]["direction"] = "backward"
    # ... more parsing logic

    return structured_command
```

### 3. Action Mapping

Map the structured command to specific robot actions:

```python
def map_to_robot_action(structured_command):
    """
    Map structured command to robot-specific action
    """
    if structured_command["intent"] == "move":
        return create_move_action(structured_command["parameters"])
    elif structured_command["intent"] == "grasp":
        return create_grasp_action(structured_command["parameters"])
    # ... more action mappings
```

## ROS 2 Action Client Examples

Here's how to create ROS 2 action clients that respond to voice commands:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from your_robot_interfaces.action import NavigateToPose
from geometry_msgs.msg import PoseStamped

class VoiceControlledNavigation(Node):
    def __init__(self):
        super().__init__('voice_controlled_navigation')
        self._action_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

    def send_goal(self, x, y, theta):
        """Send navigation goal based on voice command"""
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        # Set orientation based on theta

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle result callback"""
        result = future.result().result
        self.get_logger().info(f'Result: {result}')

    def feedback_callback(self, feedback_msg):
        """Handle feedback"""
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {feedback}')
```

## Interactive Exercise

Try implementing a simple voice command parser that can handle these commands:
- "Move forward 1 meter"
- "Turn left 90 degrees"
- "Stop the robot"
- "Navigate to the kitchen"

Create a function that takes a voice command string and returns the appropriate robot action structure.

## Summary

In this chapter, you learned:
- The fundamentals of speech recognition for robotics
- How to implement OpenAI Whisper for voice-to-text conversion
- Techniques for converting voice commands to structured robot inputs
- How to create ROS 2 action clients that respond to voice commands

## Next Steps

[Continue to Chapter 2: Cognitive Planning with LLMs](./chapter2-cognitive-planning.md)

[Take Chapter 1 Quiz](./chapter1-quiz.md)

[Back to Module Overview](./prerequisites.md)