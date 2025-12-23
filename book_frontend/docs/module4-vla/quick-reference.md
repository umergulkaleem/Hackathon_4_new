---
sidebar_position: 10
title: Quick Reference Guide
---

# Quick Reference Guide: Vision-Language-Action (VLA) Systems

## Voice Recognition Commands

### OpenAI Whisper Integration
```python
import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Basic speech recognition
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    transcript = recognizer.recognize_whisper(audio, model="base")
    print(f"Recognized: {transcript}")
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print(f"Error: {e}")
```

### Common Voice Command Patterns
- "Go to the [location]" → Navigation
- "[Action] the [object]" → Manipulation
- "Find the [object]" → Perception
- "Stop" → Emergency stop

## LLM Cognitive Planning

### Basic LLM Integration
```python
import openai
import json

client = openai.OpenAI()

def generate_action_plan(command):
    prompt = f"""
    Convert this command to a robot action plan:
    Command: "{command}"

    Return JSON with:
    {{
        "intent": "...",
        "action_sequence": [
            {{"action_type": "...", "parameters": {{...}}}}
        ]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
```

### Task Decomposition Patterns
- **Simple Navigation**: `navigate → reach goal`
- **Object Interaction**: `perceive → navigate → manipulate`
- **Multi-Step**: `analyze → plan → execute → verify`

## ROS 2 Action Patterns

### Navigation Action Client
```python
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

class NavigationClient:
    def __init__(self, node):
        self.nav_client = ActionClient(node, NavigateToPose, 'navigate_to_pose')

    def navigate_to_pose(self, pose):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose

        if not self.nav_client.wait_for_server(timeout_sec=5.0):
            return False

        future = self.nav_client.send_goal_async(goal_msg)
        return future
```

### Manipulation Action Client
```python
from rclpy.action import ActionClient
from custom_msgs.action import ManipulateObject

class ManipulationClient:
    def __init__(self, node):
        self.manip_client = ActionClient(node, ManipulateObject, 'manipulate_object')

    def manipulate_object(self, obj_name, action_type):
        goal_msg = ManipulateObject.Goal()
        goal_msg.object_name = obj_name
        goal_msg.action_type = action_type

        if not self.manip_client.wait_for_server(timeout_sec=5.0):
            return False

        future = self.manip_client.send_goal_async(goal_msg)
        return future
```

## System Architecture Components

### Core VLA Pipeline
```
Voice Command → Speech Recognition → NLP → LLM Planning → ROS 2 Execution
```

### Component Responsibilities
- **Voice Interface**: Converts speech to text
- **Cognitive Planner**: Translates goals to action sequences
- **Action Executor**: Sends commands to robot hardware
- **Perception System**: Provides environmental awareness
- **Navigation System**: Handles movement planning

## Common ROS 2 Commands

### System Monitoring
```bash
# List all topics
ros2 topic list

# List all actions
ros2 action list

# Check action server
ros2 action info /navigate_to_pose

# Monitor a topic
ros2 topic echo /voice_commands

# Check node status
ros2 node info /autonomous_humanoid
```

### Launch Commands
```bash
# Launch navigation stack
ros2 launch nav2_bringup navigation_launch.py

# Launch your VLA system
ros2 launch your_package vla_system.launch.py
```

## Configuration Files

### Environment Variables
```bash
# Required for OpenAI API
export OPENAI_API_KEY="your-api-key-here"

# ROS 2 configuration
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_cyclonedx_cpp
```

### Sample Navigation Configuration
```yaml
# navigation_params.yaml
amcl:
  ros__parameters:
    use_sim_time: false
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2

controller_server:
  ros__parameters:
    use_sim_time: false
    controller_frequency: 10.0
    max_linear_speed: 0.5
    min_linear_speed: 0.1
```

## Error Handling Patterns

### Safe Command Execution
```python
def execute_command(command):
    try:
        # Validate command
        if not is_command_safe(command):
            raise ValueError("Unsafe command detected")

        # Execute command
        result = send_to_robot(command)

        # Verify success
        if not result.success:
            raise RuntimeError(f"Command failed: {result.error}")

        return True

    except Exception as e:
        log_error(f"Command execution failed: {e}")
        trigger_safety_procedure()
        return False
```

### Fallback Strategies
```python
def fallback_plan(command):
    # Simple keyword-based fallback
    if "go to" in command.lower():
        location = extract_location(command)
        return {"action": "navigate", "params": {"location": location}}
    elif "pick up" in command.lower():
        obj = extract_object(command)
        return {"action": "manipulate", "params": {"object": obj, "action": "grasp"}}

    return None
```

## Performance Optimization

### Caching Strategies
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_location_coordinates(location_name):
    # Expensive lookup operation
    return fetch_coordinates(location_name)

# Preload models at startup
def initialize_models():
    # Load Whisper model
    whisper_model = whisper.load_model("base")
    # Load object detection model
    detection_model = load_detection_model()
    return whisper_model, detection_model
```

### Threading for Responsiveness
```python
import threading
import queue

class AsyncVoiceProcessor:
    def __init__(self):
        self.command_queue = queue.Queue()
        self.processor_thread = threading.Thread(target=self.process_commands)
        self.processor_thread.start()

    def process_commands(self):
        while True:
            command = self.command_queue.get()
            if command is None:
                break
            self.execute_command(command)
```

## Safety Considerations

### Command Validation
```python
def validate_command(command_plan):
    # Check for dangerous actions
    for action in command_plan['action_sequence']:
        if action['action_type'] == 'navigate':
            if not is_path_safe(action['parameters']['pose']):
                return False
        elif action['action_type'] == 'manipulate':
            if not is_manipulation_safe(action['parameters']):
                return False
    return True
```

### Emergency Procedures
```python
def emergency_stop():
    # Send stop command to all action servers
    send_stop_to_navigation()
    send_stop_to_manipulator()
    # Log the emergency event
    log_emergency_event()
    # Wait for confirmation
    wait_for_stop_confirmation()
```

## Testing Commands

### Unit Tests
```bash
# Test individual components
python3 -m pytest test/voice_recognition_test.py
python3 -m pytest test/llm_integration_test.py
python3 -m pytest test/ros_integration_test.py
```

### Integration Tests
```bash
# Test complete VLA pipeline
ros2 launch your_package test_vla_pipeline.launch.py
```

## Useful Resources

### Documentation Links
- [ROS 2 Documentation](https://docs.ros.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Navigation2 Documentation](https://navigation.ros.org/)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)

### Debugging Tools
- `rviz2` - Visualize robot state and navigation
- `rqt` - ROS GUI tools for monitoring
- `ros2 bag` - Record and replay system data
- `plotjuggler` - Plot time series data

## Common API Endpoints

### Voice Interface
- `/voice_commands` - Input for voice commands
- `/voice_status` - Status of voice recognition system

### Planning Interface
- `/plan_request` - Request action plan generation
- `/plan_execution` - Execute generated plans

### Robot Interface
- `/navigate_to_pose` - Navigation action server
- `/manipulate_object` - Manipulation action server
- `/detect_objects` - Perception action server

This quick reference should help you quickly find common patterns, commands, and solutions when working with Vision-Language-Action systems.