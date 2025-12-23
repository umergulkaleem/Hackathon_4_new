---
sidebar_position: 4
title: Chapter 2 - Cognitive Planning with LLMs
---

# Chapter 2: Cognitive Planning with LLMs

## Overview

This chapter explores how Large Language Models (LLMs) can be used to translate natural language goals into executable ROS 2 action sequences. You'll learn about task decomposition, planning logic, and how to create intelligent robot behaviors that understand high-level human instructions.

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand how LLMs can be integrated with robotic systems for cognitive planning
- Translate natural language goals into ROS 2 action sequences
- Implement task decomposition algorithms for complex robotic tasks
- Design planning logic for multi-step robot operations

## Cognitive Planning Concepts

Cognitive planning in robotics involves translating high-level goals into executable actions. This process requires:

1. **Goal Understanding**: Interpreting the natural language goal
2. **Task Decomposition**: Breaking down complex goals into simpler subtasks
3. **Action Sequencing**: Determining the order of robot actions
4. **Resource Allocation**: Managing robot capabilities and environmental constraints
5. **Execution Monitoring**: Tracking progress and adapting to changes

### Role of LLMs in Cognitive Planning

Large Language Models bring several advantages to cognitive planning:
- **Natural Language Understanding**: LLMs can interpret complex human instructions
- **Common Sense Reasoning**: They understand real-world relationships and constraints
- **Contextual Awareness**: They can maintain context across multiple interactions
- **Flexibility**: They can adapt to novel situations not explicitly programmed

## Natural Language to ROS 2 Action Translation

The process of translating natural language to ROS 2 actions involves several stages:

### 1. Goal Parsing with LLMs

```python
import openai
import json
from typing import List, Dict

class NaturalLanguageToAction:
    def __init__(self):
        self.client = openai.OpenAI()

    def parse_goal(self, natural_language_goal: str) -> Dict:
        """
        Parse natural language goal into structured action plan
        """
        prompt = f"""
        Parse the following natural language goal into a structured action plan for a robot:

        Goal: "{natural_language_goal}"

        Return a JSON object with the following structure:
        {{
            "task_decomposition": [
                {{
                    "step": 1,
                    "action": "action_type",
                    "parameters": {{"param1": "value1", ...}},
                    "description": "Brief description of the action"
                }}
            ],
            "constraints": ["list of any constraints or considerations"],
            "estimated_steps": number of steps,
            "required_capabilities": ["list of robot capabilities needed"]
        }}

        Be specific about action types and parameters that would work with ROS 2.
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        try:
            # Extract JSON from the response
            content = response.choices[0].message.content
            # In practice, you'd need to handle the extraction more robustly
            return json.loads(content)
        except json.JSONDecodeError:
            # Handle case where response isn't valid JSON
            return self.fallback_parse(natural_language_goal)

    def fallback_parse(self, goal: str) -> Dict:
        """
        Simple fallback parser if LLM parsing fails
        """
        # Implement basic keyword matching as fallback
        if "navigate to" in goal.lower():
            location = goal.lower().replace("navigate to", "").strip()
            return {
                "task_decomposition": [
                    {
                        "step": 1,
                        "action": "navigate",
                        "parameters": {"location": location},
                        "description": f"Navigate to {location}"
                    }
                ],
                "constraints": [],
                "estimated_steps": 1,
                "required_capabilities": ["navigation"]
            }
        # ... more fallback rules
        return {
            "task_decomposition": [],
            "constraints": [],
            "estimated_steps": 0,
            "required_capabilities": []
        }
```

### 2. Action Sequence Generation

Once the goal is parsed, generate the corresponding ROS 2 action sequence:

```python
class ActionSequenceGenerator:
    def __init__(self):
        # Initialize ROS 2 action clients
        self.navigation_client = None  # Initialize navigation action client
        self.manipulation_client = None  # Initialize manipulation action client
        self.perception_client = None  # Initialize perception action client

    def execute_action_plan(self, plan: Dict):
        """
        Execute the action plan generated by the LLM
        """
        for task in plan["task_decomposition"]:
            if task["action"] == "navigate":
                self.execute_navigation(task["parameters"])
            elif task["action"] == "manipulate":
                self.execute_manipulation(task["parameters"])
            elif task["action"] == "perceive":
                self.execute_perception(task["parameters"])
            # ... handle other action types

    def execute_navigation(self, params: Dict):
        """
        Execute navigation action
        """
        # Example navigation action
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = self.get_pose_from_location(params["location"])

        # Send goal and wait for result
        future = self.navigation_client.send_goal_async(goal_msg)
        # ... handle result

    def execute_manipulation(self, params: Dict):
        """
        Execute manipulation action
        """
        # Example manipulation action
        goal_msg = ManipulateObject.Goal()
        goal_msg.object_name = params["object"]
        goal_msg.action_type = params["manipulation_type"]

        # Send goal and wait for result
        future = self.manipulation_client.send_goal_async(goal_msg)
        # ... handle result
```

## Task Decomposition Examples

### Simple Task: "Go to the kitchen and bring me a cup"

1. **Navigation Task**: Navigate to kitchen
2. **Perception Task**: Identify cup location
3. **Manipulation Task**: Grasp the cup
4. **Navigation Task**: Return to user location

### Complex Task: "Set the table for dinner with plates and glasses"

1. **Task Analysis**: Set table → identify table → get plates → get glasses → place items
2. **Resource Check**: Verify robot has required capabilities
3. **Action Sequence**:
   - Navigate to dining area
   - Identify table location
   - Navigate to dish storage
   - Grasp plates (multiple items)
   - Navigate to table
   - Place plates at settings
   - Navigate back to dish storage
   - Grasp glasses
   - Navigate to table
   - Place glasses at settings

## Planning Logic Implementation

Here's a complete example of cognitive planning with LLMs:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from geometry_msgs.msg import Pose
import openai
import json

class LLMBehaviorPlanner(Node):
    def __init__(self):
        super().__init__('llm_behavior_planner')

        # Initialize OpenAI client
        self.openai_client = openai.OpenAI()

        # Create subscriber for natural language commands
        self.command_sub = self.create_subscription(
            String,
            'natural_language_commands',
            self.command_callback,
            10
        )

        # Initialize action clients for different robot capabilities
        self.navigation_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.manipulation_client = ActionClient(self, ManipulateObject, 'manipulate_object')

        self.get_logger().info('LLM Behavior Planner node started')

    def command_callback(self, msg):
        """
        Handle incoming natural language commands
        """
        command = msg.data
        self.get_logger().info(f'Received command: {command}')

        # Parse the command using LLM
        plan = self.generate_action_plan(command)

        if plan:
            self.execute_plan(plan)
        else:
            self.get_logger().error('Failed to generate action plan')

    def generate_action_plan(self, command: str):
        """
        Generate action plan using LLM
        """
        prompt = f"""
        Generate a detailed action plan for a robot to execute the following command:

        Command: "{command}"

        Consider the robot's capabilities and real-world constraints. Return a JSON plan with:
        1. A sequence of executable actions
        2. Parameters for each action
        3. Potential obstacles or considerations
        4. Success criteria for each step

        Structure the response as a valid JSON object.
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
            self.get_logger().error(f'Error generating action plan: {e}')
            return None

    def execute_plan(self, plan: dict):
        """
        Execute the generated action plan
        """
        for step in plan.get('task_decomposition', []):
            self.get_logger().info(f'Executing step: {step["description"]}')

            success = self.execute_single_action(step)

            if not success:
                self.get_logger().error(f'Step failed: {step["description"]}')
                # Handle failure - could involve replanning or error recovery
                break
            else:
                self.get_logger().info(f'Step completed: {step["description"]}')

    def execute_single_action(self, action: dict) -> bool:
        """
        Execute a single action based on its type
        """
        action_type = action['action']
        parameters = action['parameters']

        if action_type == 'navigate':
            return self.execute_navigation_action(parameters)
        elif action_type == 'manipulate':
            return self.execute_manipulation_action(parameters)
        elif action_type == 'perceive':
            return self.execute_perception_action(parameters)
        else:
            self.get_logger().warn(f'Unknown action type: {action_type}')
            return False

    def execute_navigation_action(self, params: dict) -> bool:
        """
        Execute navigation action
        """
        # Implementation would send navigation goal to action server
        # This is a placeholder implementation
        location = params.get('location', 'unknown')
        self.get_logger().info(f'Navigating to {location}')

        # Wait for navigation action server
        if not self.navigation_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Navigation action server not available')
            return False

        # Create and send navigation goal
        goal_msg = NavigateToPose.Goal()
        # Set pose based on location parameters
        # ... fill in pose details

        send_goal_future = self.navigation_client.send_goal_async(goal_msg)
        # Wait for result and return success status
        # ... handle the future result

        return True  # Placeholder - actual implementation would check results

    def execute_manipulation_action(self, params: dict) -> bool:
        """
        Execute manipulation action
        """
        # Similar implementation for manipulation actions
        object_name = params.get('object', 'unknown')
        self.get_logger().info(f'Attempting to manipulate {object_name}')
        return True  # Placeholder

    def execute_perception_action(self, params: dict) -> bool:
        """
        Execute perception action
        """
        # Similar implementation for perception actions
        target = params.get('target', 'unknown')
        self.get_logger().info(f'Performing perception on {target}')
        return True  # Placeholder

def main(args=None):
    rclpy.init(args=args)
    planner = LLMBehaviorPlanner()

    try:
        rclpy.spin(planner)
    except KeyboardInterrupt:
        pass
    finally:
        planner.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## LLM Integration Best Practices

### 1. Context Management
- Maintain conversation history for context-aware responses
- Clear context when switching between different tasks
- Use system messages to establish robot-specific behavior patterns

### 2. Error Handling
- Implement fallback mechanisms when LLM parsing fails
- Validate action plans before execution
- Provide human-in-the-loop options for ambiguous commands

### 3. Safety Considerations
- Validate that actions are safe before execution
- Implement permission checks for sensitive actions
- Log all decisions for audit and debugging

## Interactive Exercise

Implement a simple task decomposition function that can handle these commands:
- "Clean the living room"
- "Find the red ball and bring it to me"
- "Go to the kitchen, open the fridge, and tell me what's inside"

Create a function that takes a natural language command and returns a list of subtasks that could be executed by a robot.

## Summary

In this chapter, you learned:
- How LLMs can be integrated with robotic systems for cognitive planning
- The process of translating natural language goals into ROS 2 action sequences
- Techniques for task decomposition and planning logic
- Best practices for LLM integration in robotic systems

## Next Steps

[Continue to Chapter 3: Capstone - Autonomous Humanoid](./chapter3-capstone.md)

[Take Chapter 2 Quiz](./chapter2-quiz.md)

[Back to Chapter 1: Voice-to-Action Interfaces](./chapter1-voice-to-action.md)