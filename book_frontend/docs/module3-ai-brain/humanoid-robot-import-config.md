# Humanoid Robot Model Import and Configuration Guide for Isaac Sim

## Overview

This guide provides detailed instructions for importing and configuring humanoid robot models in NVIDIA Isaac Sim. Proper robot configuration is essential for realistic simulation, accurate physics behavior, and effective synthetic data generation.

## Understanding Humanoid Robot Models

### Humanoid Robot Characteristics

Humanoid robots have specific characteristics that distinguish them from other robot types:

1. **Anthropomorphic Structure**: Human-like body with head, torso, arms, and legs
2. **Bipedal Locomotion**: Designed for walking on two legs
3. **Degrees of Freedom**: Multiple joints for complex movement
4. **Sensor Placement**: Sensors positioned for human-like perception
5. **Balance Requirements**: Need for active balance control

### Supported Model Formats

Isaac Sim supports several robot model formats:

1. **URDF (Unified Robot Description Format)**: Most common format, XML-based
2. **SDF (Simulation Description Format)**: Gazebo format, XML-based
3. **USD (Universal Scene Description)**: Native Omniverse format
4. **FBX/OBJ**: 3D model formats with additional configuration

## Preparing Robot Models for Import

### URDF Model Requirements

Before importing a humanoid robot from URDF, ensure your model meets these requirements:

1. **Valid URDF Syntax**: Model must pass URDF validation
2. **Complete Kinematic Chain**: Proper parent-child relationships
3. **Physical Properties**: Mass, inertia, and collision properties defined
4. **Joint Limits**: Proper joint limits and ranges specified
5. **Material Definitions**: Visual materials defined for rendering
6. **Sensor Definitions**: Sensor placements defined (optional)

### Example URDF Structure

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.4"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.02"/>
    </inertial>
  </link>

  <!-- Joint connecting base to torso -->
  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.25"/>
  </joint>

  <!-- Additional links and joints for arms, legs, head -->
  <!-- ... -->
</robot>
```

### Model Validation

Before importing, validate your robot model:

```bash
# Validate URDF using check_urdf tool
ros2 run urdfdom check_urdf /path/to/your/robot.urdf

# Check for common issues
urdf_to_graphiz /path/to/your/robot.urdf
```

## Importing Humanoid Robots into Isaac Sim

### Using the Isaac Sim UI

1. **Open Isaac Sim**: Launch Isaac Sim application

2. **Import Robot**:
   - Go to File > Import > URDF
   - Select your robot URDF file
   - Navigate to your URDF file location

3. **Import Settings**:
   - **Import as**: Choose "Articulation" for physics-enabled robots or "Rigid Body" for static objects
   - **Convex Decomposition**: Enable for complex collision meshes
   - **Merge Fixed Joints**: Check to reduce model complexity
   - **Import Visual**: Include visual meshes for rendering
   - **Import Collision**: Include collision meshes for physics

4. **Configure Import**:
   - Set import scale if needed (default is 1.0)
   - Choose parent prim for import
   - Set initial position and orientation

### Using Python API

For more control, import robots programmatically:

```python
# Example Python code for importing humanoid robot
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.importer.urdf import _urdf
import carb

# Get URDF interface
urdf_interface = _urdf.acquire_urdf_interface()

# Import URDF settings
import_config = _urdf.ImportConfig()
import_config.merge_fixed_joints = True
import_config.convex_decomp = False
import_config.import_inertia_tensor = True
import_config.fix_base = False
import_config.make_instanceable = False
import_config.self_collision = False
import_config.create_physics_scene = True
import_config.import_collision_meshes = True
import_config.import_visual_meshes = True
import_config.import_inertia_tensor = True
import_config.default_drive_strength = 20000
import_config.default_position_drive_damping = 100

# Import the robot
robot_path = "/path/to/your/humanoid_robot.urdf"
stage_path = "/World/HumanoidRobot"
urdf_interface.import_file(robot_path, stage_path, import_config)

# Set initial pose
from omni.isaac.core.utils.transformations import set_local_pose
set_local_pose(stage_path, position=[0, 0, 1.0], orientation=[0, 0, 0, 1])
```

### Using Isaac Sim Extensions

For complex humanoid robots, consider using specialized extensions:

```python
# Enable humanoid-specific extensions
from omni.isaac.core.utils.extensions import enable_extension

# Enable extensions that may be helpful
enable_extension("omni.isaac.humanoid")
enable_extension("omni.isaac.ros2_bridge.humble")  # If using ROS
enable_extension("omni.kit.primitive.mesh")  # For additional primitives
```

## Robot Configuration in Isaac Sim

### Physics Configuration

Configure physics properties for realistic humanoid behavior:

```python
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.physx.scripts import utils
import omni.physx.bindings._physx as physx_bindings

def configure_robot_physics(robot_path):
    """Configure physics properties for humanoid robot"""
    robot_prim = get_prim_at_path(robot_path)

    # Configure mass properties
    configure_mass_properties(robot_path)

    # Configure joint dynamics
    configure_joint_dynamics(robot_path)

    # Configure collision properties
    configure_collision_properties(robot_path)

def configure_mass_properties(robot_path):
    """Set appropriate mass properties for humanoid links"""
    # Example: Set torso mass
    torso_path = f"{robot_path}/torso"
    torso_prim = get_prim_at_path(torso_path)

    # Set mass (adjust values based on your robot)
    from pxr import Gf
    mass_api = utils.get_or_create_physx_api(torso_prim)
    mass_api.mass = 10.0  # kg

def configure_joint_dynamics(robot_path):
    """Configure joint dynamics for natural movement"""
    # Example: Configure hip joint
    hip_joint_path = f"{robot_path}/hip_joint"
    joint_prim = get_prim_at_path(hip_joint_path)

    # Set joint limits and dynamics
    joint_prim.GetAttribute("physics:lowerLimit").Set(-1.57)  # -90 degrees
    joint_prim.GetAttribute("physics:upperLimit").Set(1.57)   # 90 degrees
    joint_prim.GetAttribute("physics:driveDamping").Set(100.0)
    joint_prim.GetAttribute("physics:driveStiffness").Set(1000.0)

def configure_collision_properties(robot_path):
    """Configure collision properties"""
    # Set up collision filtering if needed
    pass
```

### Material and Visual Configuration

Configure materials for realistic rendering:

```python
from pxr import Sdf, UsdShade, Gf

def apply_realistic_materials(robot_path):
    """Apply realistic materials to robot links"""

    # Create metallic material for joints/actuators
    create_metallic_material(robot_path, "joints_material",
                           base_color=Gf.Vec3f(0.7, 0.7, 0.8),
                           metallic=0.8, roughness=0.2)

    # Create plastic material for body parts
    create_plastic_material(robot_path, "body_material",
                          base_color=Gf.Vec3f(0.2, 0.6, 0.8),
                          metallic=0.0, roughness=0.4)

    # Apply materials to appropriate links
    apply_material_to_link(f"{robot_path}/torso", f"{robot_path}/Materials/body_material")
    apply_material_to_link(f"{robot_path}/head", f"{robot_path}/Materials/body_material")
    apply_material_to_link(f"{robot_path}/upper_arm_L", f"{robot_path}/Materials/joints_material")

def create_metallic_material(robot_path, material_name, base_color, metallic, roughness):
    """Create a metallic material"""
    stage = omni.usd.get_context().get_stage()
    material_path = f"{robot_path}/Materials/{material_name}"

    # Create material
    material = UsdShade.Material.Define(stage, Sdf.Path(material_path))

    # Create shader
    shader_path = Sdf.Path(f"{material_path}/Shader")
    shader = UsdShade.Shader.Define(stage, shader_path)
    shader.CreateIdAttr("OmniPBR")

    # Set material properties
    shader.CreateInput("diffuse_tint", Sdf.ValueTypeNames.Color3f).Set(base_color)
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(metallic)
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(roughness)

    # Connect shader to material
    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "out")

def apply_material_to_link(link_path, material_path):
    """Apply material to a specific link"""
    link_prim = get_prim_at_path(link_path)
    material = UsdShade.Material(stage.GetPrimAtPath(material_path))
    UsdShade.MaterialBindingAPI(link_prim).Bind(material)
```

## Humanoid-Specific Configuration

### Balance and Stability Setup

Configure the humanoid robot for stable simulation:

```python
def setup_balance_control(robot_path):
    """Setup for balance control in humanoid robot"""

    # Configure center of mass
    configure_center_of_mass(robot_path)

    # Set up balance-related sensors
    setup_balance_sensors(robot_path)

    # Configure feet for stable standing
    configure_feet(robot_path)

def configure_center_of_mass(robot_path):
    """Configure center of mass for stable balance"""
    # The torso should have appropriate mass distribution
    torso_path = f"{robot_path}/torso"
    # Ensure torso has realistic mass and inertia properties
    # Center of mass should be within the torso volume

def setup_balance_sensors(robot_path):
    """Setup sensors for balance feedback"""
    # Add IMU to torso for orientation sensing
    add_imu_to_link(f"{robot_path}/torso", "balance_imu")

    # Add force/torque sensors to feet
    add_force_torque_sensor(f"{robot_path}/left_foot", "left_foot_sensor")
    add_force_torque_sensor(f"{robot_path}/right_foot", "right_foot_sensor")

def configure_feet(robot_path):
    """Configure feet for stable contact"""
    # Ensure feet have appropriate collision geometry
    # Set up friction coefficients for stable standing
    left_foot_path = f"{robot_path}/left_foot"
    right_foot_path = f"{robot_path}/right_foot"

    # Configure contact properties
    set_friction_coefficient(left_foot_path, 0.8)  # High friction for grip
    set_friction_coefficient(right_foot_path, 0.8)
```

### Sensor Configuration

Configure sensors for humanoid perception:

```python
def configure_robot_sensors(robot_path):
    """Configure sensors for humanoid robot perception"""

    # Head-mounted camera for vision
    configure_head_camera(robot_path)

    # IMU for orientation and acceleration
    configure_imu(robot_path)

    # Joint position sensors
    configure_joint_sensors(robot_path)

def configure_head_camera(robot_path):
    """Configure head-mounted camera"""
    from omni.isaac.sensor import Camera
    import numpy as np

    camera = Camera(
        prim_path=f"{robot_path}/head_camera",
        position=np.array([0.0, 0.0, 0.1]),  # Offset from head center
        frequency=30,
        resolution=(640, 480),
        orientation=np.array([0, 0, 0, 1])  # Looking forward
    )

    # Add to world scene
    world = World()
    world.scene.add_sensor("head_camera", camera)

def configure_imu(robot_path):
    """Configure IMU sensor"""
    # IMU typically placed in torso for center of mass
    torso_imu_path = f"{robot_path}/torso_imu"
    # Implementation depends on Isaac Sim's IMU capabilities

def configure_joint_sensors(robot_path):
    """Configure joint position/velocity sensors"""
    # This is handled automatically by Isaac Sim for articulations
    # The joint states will be available through the articulation API
```

## Testing Robot Configuration

### Basic Functionality Test

Test that the robot imports and functions correctly:

```python
def test_robot_import(robot_path):
    """Test basic robot import functionality"""
    try:
        # Check if robot exists in stage
        robot_prim = get_prim_at_path(robot_path)
        if not robot_prim.IsValid():
            raise Exception(f"Robot prim not found at {robot_path}")

        # Check for basic links
        required_links = ["torso", "head", "left_leg", "right_leg", "left_arm", "right_arm"]
        for link in required_links:
            link_path = f"{robot_path}/{link}"
            link_prim = get_prim_at_path(link_path)
            if not link_prim.IsValid():
                print(f"Warning: Expected link {link} not found")

        # Test joint functionality
        test_joint_movement(robot_path)

        # Test physics simulation
        test_physics_stability(robot_path)

        print(f"Robot import test passed for {robot_path}")
        return True

    except Exception as e:
        print(f"Robot import test failed: {str(e)}")
        return False

def test_joint_movement(robot_path):
    """Test that joints can move properly"""
    # Implementation to test joint ranges and movement
    pass

def test_physics_stability(robot_path):
    """Test physics stability"""
    # Implementation to test if robot maintains stable pose
    pass
```

### ROS Integration Test

If using ROS integration, test the connection:

```python
def test_ros_integration(robot_path):
    """Test ROS integration for the imported robot"""
    import rclpy
    from sensor_msgs.msg import JointState
    from geometry_msgs.msg import TransformStamped
    import time

    # Initialize ROS
    if not rclpy.ok():
        rclpy.init()

    # Create node to test communication
    node = rclpy.Node('robot_tester')

    # Subscribe to joint states
    joint_state_sub = node.create_subscription(
        JointState,
        '/joint_states',
        lambda msg: print(f"Received joint states: {len(msg.name)} joints"),
        10
    )

    # Test TF publishing
    tf_publisher = node.create_publisher(
        TransformStamped,
        '/tf',
        10
    )

    # Allow some time for messages to be processed
    time.sleep(1)

    # Spin to process messages
    rclpy.spin_once(node, timeout_sec=0.1)

    node.destroy_node()
```

## Troubleshooting Common Issues

### Import Issues

**Problem**: Robot fails to import or crashes Isaac Sim
- **Solution**:
  1. Validate URDF with `check_urdf`
  2. Check for invalid characters in link/joint names
  3. Verify all referenced mesh files exist
  4. Try importing with different settings (merge fixed joints, etc.)

**Problem**: Robot appears in incorrect position or orientation
- **Solution**:
  1. Check URDF origin definitions
  2. Verify Isaac Sim import scale settings
  3. Manually adjust pose after import

**Problem**: Robot has missing visual or collision geometry
- **Solution**:
  1. Verify mesh file paths in URDF
  2. Check that mesh files are in correct format
  3. Ensure Isaac Sim can access the mesh files

### Physics Issues

**Problem**: Robot falls through the ground
- **Solution**:
  1. Check that ground plane exists and is properly configured
  2. Verify robot has collision meshes defined
  3. Check mass properties are reasonable

**Problem**: Robot joints behave erratically
- **Solution**:
  1. Check joint limits and ranges
  2. Verify mass properties are physically realistic
  3. Adjust joint damping and stiffness parameters

**Problem**: Robot doesn't maintain balance
- **Solution**:
  1. Verify center of mass is correctly positioned
  2. Check that feet have appropriate contact properties
  3. Ensure proper mass distribution

### Performance Issues

**Problem**: Slow simulation performance with robot
- **Solution**:
  1. Simplify collision meshes
  2. Reduce number of complex joints
  3. Optimize mass and inertia properties
  4. Check for joint loops or problematic kinematic structures

## Advanced Configuration

### Custom Controllers

Implement custom controllers for humanoid locomotion:

```python
class HumanoidController:
    def __init__(self, robot_path):
        self.robot_path = robot_path
        self.articulation_controller = None

    def setup_controller(self):
        """Setup articulation controller for humanoid"""
        from omni.isaac.core.articulations import Articulation

        # Get the imported robot as an articulation
        robot_articulation = Articulation(prim_path=self.robot_path)

        # Create controller
        self.articulation_controller = robot_articulation.get_articulation_controller()

    def move_to_pose(self, joint_positions):
        """Move robot to specific joint configuration"""
        if self.articulation_controller:
            self.articulation_controller.apply_position_targets(joint_positions)

    def setup_walking_controller(self):
        """Setup specialized controller for bipedal walking"""
        # Implementation for walking pattern generation
        pass
```

### Animation and Motion Capture

Import motion capture data for realistic humanoid movement:

```python
def import_motion_capture(robot_path, motion_file):
    """Import motion capture data for humanoid robot"""
    # Parse motion capture file (BVH, FBX, or custom format)
    motion_data = parse_motion_file(motion_file)

    # Map motion data to robot joints
    joint_mapping = create_joint_mapping(robot_path, motion_data)

    # Apply motion data to robot
    apply_motion_to_robot(robot_path, motion_data, joint_mapping)

def create_joint_mapping(robot_path, motion_data):
    """Create mapping between motion capture joints and robot joints"""
    # Implementation to map motion capture joint names to Isaac Sim joint paths
    pass
```

## Verification Checklist

Before using the imported humanoid robot, verify:

- [ ] Robot imports without errors
- [ ] All links and joints are present
- [ ] Physics properties are realistic
- [ ] Collision meshes are properly configured
- [ ] Visual materials are applied correctly
- [ ] Robot maintains stable pose when idle
- [ ] Joints move within expected ranges
- [ ] Sensors are properly configured (if applicable)
- [ ] ROS integration works (if applicable)
- [ ] Performance is acceptable for simulation

## Best Practices

1. **Start Simple**: Begin with basic humanoid models before complex ones
2. **Validate Early**: Check URDF validity before import
3. **Iterative Testing**: Test functionality incrementally
4. **Realistic Properties**: Use physically realistic mass and inertia values
5. **Proper Scaling**: Ensure model is correctly scaled for your application
6. **Documentation**: Keep track of import settings and configurations used

This guide provides comprehensive instructions for importing and configuring humanoid robots in Isaac Sim, ensuring they are properly set up for realistic simulation and synthetic data generation.