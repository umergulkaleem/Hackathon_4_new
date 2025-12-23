---
sidebar_position: 9
title: Troubleshooting Guide
---

# Troubleshooting Guide: Vision-Language-Action (VLA) Module

This guide helps you diagnose and resolve common issues encountered when implementing Vision-Language-Action systems.

## Voice Recognition Issues

### Problem: Whisper API not responding or returning errors
**Symptoms**:
- Voice commands not being recognized
- API errors or timeouts
- High latency in voice processing

**Solutions**:
1. **Check API Key**: Verify your OpenAI API key is correctly configured
   ```bash
   # Verify API key is set in environment
   echo $OPENAI_API_KEY
   ```

2. **Network Connectivity**: Ensure stable internet connection for API calls
   ```bash
   # Test connectivity to OpenAI
   curl -I https://api.openai.com/v1/models
   ```

3. **Audio Quality**: Improve microphone positioning and reduce background noise
   - Position microphone 6-12 inches from speaker
   - Use a quiet environment
   - Check microphone permissions in your operating system

4. **API Limits**: Check if you've exceeded API rate limits
   - Monitor your usage in the OpenAI dashboard
   - Consider upgrading your plan if needed

### Problem: Speech recognition accuracy is low
**Solutions**:
1. **Use appropriate Whisper model**: Try different models (tiny, base, small, medium, large)
   ```python
   # Use larger model for better accuracy
   transcript = recognizer.recognize_whisper(audio, model="large")
   ```

2. **Audio preprocessing**: Improve audio quality before processing
   - Use noise reduction filters
   - Ensure proper audio sample rate (16kHz recommended)

## LLM Integration Issues

### Problem: LLM generates invalid action plans
**Symptoms**:
- Generated JSON is malformed
- Action plans contain impossible commands
- LLM returns non-action responses

**Solutions**:
1. **Improve prompts**: Use structured prompts with clear output format requirements
   ```python
   prompt = f"""
   Generate a JSON action plan for: {command}
   Response format: {{"action_sequence": [...], "intent": "..."}}
   """
   ```

2. **Validate outputs**: Always validate JSON and action plans before execution
   ```python
   try:
       plan = json.loads(response)
       # Validate required fields exist
       assert "action_sequence" in plan
   except (json.JSONDecodeError, AssertionError):
       # Use fallback plan
   ```

3. **Use response_format**: Specify JSON response format in API calls
   ```python
   response = client.chat.completions.create(
       model="gpt-3.5-turbo",
       response_format={"type": "json_object"}
   )
   ```

### Problem: LLM integration is slow
**Solutions**:
1. **Optimize API calls**: Cache responses for common commands
2. **Use faster models**: Consider gpt-3.5-turbo for faster responses
3. **Implement timeouts**: Add timeout handling to prevent hanging
   ```python
   import signal

   def timeout_handler(signum, frame):
       raise TimeoutError("LLM request timed out")

   signal.signal(signal.SIGALRM, timeout_handler)
   signal.alarm(10)  # 10 second timeout
   ```

## ROS 2 Integration Issues

### Problem: Action clients not connecting to servers
**Symptoms**:
- Timeout errors when sending goals
- "Action server not available" messages
- Goals not being accepted

**Solutions**:
1. **Verify server is running**: Check that action servers are active
   ```bash
   # List available action servers
   ros2 action list
   ros2 action info /navigate_to_pose
   ```

2. **Check network configuration**: Ensure ROS 2 nodes can communicate
   ```bash
   # Verify ROS domain ID
   echo $ROS_DOMAIN_ID
   # Check for multiple ROS networks
   ros2 topic list
   ```

3. **Wait properly for servers**: Implement proper server connection logic
   ```python
   if not self.nav_client.wait_for_server(timeout_sec=10.0):
       self.get_logger().error('Navigation server not available after 10 seconds')
       return False
   ```

### Problem: Robot actions not executing as expected
**Solutions**:
1. **Check action feedback**: Monitor action progress and results
   ```python
   def feedback_callback(self, feedback_msg):
       self.get_logger().info(f'Action progress: {feedback_msg}')
   ```

2. **Validate action parameters**: Ensure all required parameters are set
   ```python
   # Verify pose is properly set before sending navigation goal
   assert goal_msg.pose.header.frame_id == "map"
   ```

3. **Review robot state**: Check robot's current state and capabilities
   ```bash
   # Monitor robot state topics
   ros2 topic echo /robot_state
   ros2 service call /get_robot_status example_interfaces/srv/Trigger
   ```

## Object Recognition Issues

### Problem: Object detection is unreliable
**Symptoms**:
- Objects not detected consistently
- False positives in detection
- Slow detection performance

**Solutions**:
1. **Improve lighting conditions**: Ensure adequate lighting for camera
   - Use consistent lighting
   - Avoid glare and shadows
   - Consider additional lighting for low-light environments

2. **Tune detection parameters**: Adjust confidence thresholds and NMS parameters
   ```python
   # Lower confidence threshold for better detection
   detections = model(image, conf=0.3, iou=0.5)
   ```

3. **Use appropriate models**: Select models based on your specific objects
   - Train custom models for specific objects
   - Use pre-trained models for common objects

### Problem: 3D pose estimation is inaccurate
**Solutions**:
1. **Use depth information**: Integrate depth camera data for better 3D estimation
   ```python
   # Combine RGB and depth data for accurate 3D poses
   pose_3d = self.estimate_pose_with_depth(rgb_image, depth_image)
   ```

2. **Calibrate cameras**: Ensure proper camera calibration
   ```bash
   # Use ROS camera calibration tools
   ros2 run camera_calibration cameracalibrator --size 8x6 --square 0.108 image:=/camera/image_raw
   ```

## Navigation Issues

### Problem: Robot gets stuck or fails to navigate
**Symptoms**:
- Navigation goals never complete
- Robot oscillates in place
- Collision avoidance not working

**Solutions**:
1. **Check costmaps**: Verify costmap configuration and updates
   ```bash
   # Visualize costmaps in RViz
   ros2 run rviz2 rviz2
   ```

2. **Tune navigation parameters**: Adjust controller and planner settings
   ```yaml
   # In navigation configuration
   controller_frequency: 10.0
   max_linear_speed: 0.5
   min_linear_speed: 0.1
   ```

3. **Verify transforms**: Ensure all TF transforms are publishing correctly
   ```bash
   ros2 run tf2_tools view_frames
   ros2 run tf2_ros tf2_echo map base_link
   ```

## Performance Optimization

### Problem: System response time is too slow
**Solutions**:
1. **Parallel processing**: Process multiple components simultaneously
   ```python
   # Use threading for non-blocking operations
   import threading

   def process_voice_in_background():
       # Voice processing in separate thread
       pass

   voice_thread = threading.Thread(target=process_voice_in_background)
   voice_thread.start()
   ```

2. **Caching**: Cache frequently used data and computations
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=128)
   def get_location_pose(location_name):
       return self.navigation_goals.get(location_name)
   ```

3. **Preprocessing**: Precompute common operations
   - Preload models at startup
   - Cache frequently accessed data
   - Precompute static transforms

## Debugging Strategies

### Enable detailed logging
```python
# Add detailed logging to your nodes
self.get_logger().set_level(rclpy.logging.LoggingSeverity.DEBUG)
```

### Use ROS 2 tools for diagnosis
```bash
# Monitor system performance
ros2 topic hz /voice_commands
ros2 run plotjuggler plotjuggler

# Check system resources
ros2 run top top_node
```

### Implement health checks
```python
def check_system_health(self):
    """Check if all required components are available"""
    checks = {
        'voice_recognition': self.check_voice_service(),
        'llm_connection': self.check_openai_connection(),
        'navigation_server': self.nav_client.wait_for_server(timeout_sec=1.0),
        'manipulation_server': self.manip_client.wait_for_server(timeout_sec=1.0)
    }
    return all(checks.values())
```

## Common Error Messages and Solutions

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "No speech detected" | Microphone issues or silence | Check microphone, ambient noise, speaking distance |
| "Action server not available" | Server not running or network issues | Verify server status, check ROS network |
| "JSON decode error" | Invalid LLM response format | Add response validation, use response_format |
| "Navigation failed" | Invalid goal or obstacles | Check goal validity, update costmaps |
| "Object not found" | Detection parameters or lighting | Adjust thresholds, improve lighting |

## Getting Help

If you encounter issues not covered in this guide:

1. **Check ROS 2 documentation**: https://docs.ros.org/
2. **OpenAI support**: https://help.openai.com/
3. **Community forums**: ROS Answers, GitHub issues
4. **Create detailed bug reports** with:
   - Exact error messages
   - Steps to reproduce
   - System configuration
   - Expected vs actual behavior

Remember: Start with simple test cases and gradually add complexity. This approach helps isolate issues quickly.