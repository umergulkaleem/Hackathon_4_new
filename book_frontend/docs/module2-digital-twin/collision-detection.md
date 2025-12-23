# Collision Detection in Gazebo

## Introduction

Collision detection is a critical component of physics simulation in Gazebo. It enables realistic interactions between objects by detecting when they come into contact and computing appropriate response forces. For humanoid robots, accurate collision detection is essential for:

- Safe interaction with the environment
- Proper contact force computation
- Realistic walking and manipulation behaviors
- Accurate sensor simulation

## Understanding Collision Detection

### What is Collision Detection?

Collision detection in Gazebo involves two main phases:

1. **Broad Phase**: Quickly identify pairs of objects that might be colliding
2. **Narrow Phase**: Precisely determine if and where objects are colliding

### Types of Collisions

- **Static Collisions**: Between objects and static environment (e.g., ground)
- **Dynamic Collisions**: Between moving objects
- **Self-Collisions**: Between different parts of the same robot (if not disabled)

## Collision Geometry Types

### Primitive Shapes

Gazebo supports several primitive collision shapes:

#### Box
```xml
<collision name="box_collision">
  <geometry>
    <box>
      <size>1.0 1.0 1.0</size>  <!-- Width, Depth, Height -->
    </box>
  </geometry>
</collision>
```

#### Sphere
```xml
<collision name="sphere_collision">
  <geometry>
    <sphere>
      <radius>0.5</radius>
    </sphere>
  </geometry>
</collision>
```

#### Cylinder
```xml
<collision name="cylinder_collision">
  <geometry>
    <cylinder>
      <radius>0.3</radius>
      <length>0.8</length>
    </cylinder>
  </geometry>
</collision>
```

#### Capsule
```xml
<collision name="capsule_collision">
  <geometry>
    <capsule>
      <radius>0.2</radius>
      <length>0.5</length>
    </capsule>
  </geometry>
</collision>
```

### Mesh Shapes

For complex geometries, you can use mesh files:

```xml
<collision name="mesh_collision">
  <geometry>
    <mesh>
      <uri>file://meshes/complex_shape.stl</uri>
    </mesh>
  </geometry>
</collision>
```

## Collision Properties

### Surface Parameters

Collision surfaces have properties that determine interaction behavior:

#### Friction
```xml
<collision name="collision_with_friction">
  <geometry>
    <box><size>1 1 1</size></box>
  </geometry>
  <surface>
    <friction>
      <ode>
        <mu>0.5</mu>      <!-- Static friction coefficient -->
        <mu2>0.5</mu2>    <!-- Dynamic friction coefficient -->
      </ode>
    </friction>
  </surface>
</collision>
```

#### Bounce (Restitution)
```xml
<collision name="bouncy_collision">
  <geometry>
    <sphere><radius>0.2</radius></sphere>
  </geometry>
  <surface>
    <bounce>
      <restitution_coefficient>0.8</restitution_coefficient>  <!-- 0 = no bounce, 1 = perfect bounce -->
      <threshold>100000</threshold>  <!-- Velocity threshold for bounce -->
    </bounce>
  </surface>
</collision>
```

#### Contact Properties
```xml
<collision name="contact_collision">
  <geometry>
    <box><size>1 1 1</size></box>
  </geometry>
  <surface>
    <contact>
      <ode>
        <soft_cfm>0.000001</soft_cfm>      <!-- Constraint Force Mixing -->
        <soft_erp>0.2</soft_erp>            <!-- Error Reduction Parameter -->
        <kp>1000000000000.0</kp>            <!-- Contact stiffness -->
        <kd>1.0</kd>                        <!-- Contact damping -->
        <max_vel>100.0</max_vel>            <!-- Maximum contact correction velocity -->
        <min_depth>0.001</min_depth>        <!-- Minimum contact depth -->
      </ode>
    </contact>
  </surface>
</collision>
```

## Collision Detection in Humanoid Robots

### Link Collision Design

For humanoid robots, collision shapes should be carefully designed:

#### Torso Collision
```xml
<link name="torso">
  <collision name="torso_collision">
    <geometry>
      <box>
        <size>0.3 0.2 0.5</size>
      </box>
    </geometry>
  </collision>
  <!-- Visual geometry may be more detailed -->
  <visual name="torso_visual">
    <geometry>
      <mesh>
        <uri>file://meshes/torso.dae</uri>
      </mesh>
    </geometry>
  </visual>
</link>
```

#### Limb Collisions

For limbs, consider using capsules which provide good collision detection with reasonable computational cost:

```xml
<link name="upper_arm">
  <collision name="upper_arm_collision">
    <geometry>
      <capsule>
        <radius>0.05</radius>
        <length>0.3</length>
      </capsule>
    </geometry>
  </collision>
</link>
```

### Self-Collision Avoidance

For articulated robots, you may want to disable self-collisions between certain links:

```xml
<!-- In the model or world file -->
<joint name="no_collision_joint" type="revolute">
  <parent>torso</parent>
  <child>head</child>
  <disable_fixed_joint_lumping>true</disable_fixed_joint_lumping>
  <!-- This joint won't cause collisions between parent and child -->
</joint>
```

Or in URDF:
```xml
<disable_collisions link1="torso" link2="head" reason="Adjacent" />
```

## Collision Detection Configuration

### Physics Engine Settings

The physics engine configuration affects collision detection:

```xml
<physics type="ode">
  <gravity>0 0 -9.8</gravity>
  <ode>
    <solver>
      <type>quick</type>
      <iters>10</iters>          <!-- Solver iterations -->
      <sor>1.3</sor>             <!-- Successive Over-Relaxation -->
    </solver>
    <constraints>
      <cfm>0.000001</cfm>        <!-- Constraint Force Mixing -->
      <erp>0.2</erp>            <!-- Error Reduction Parameter -->
      <contact_max_correcting_vel>100</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

### Performance Considerations

#### Collision Layer
```xml
<collision name="collision_with_layer">
  <geometry>
    <box><size>1 1 1</size></box>
  </geometry>
  <surface>
    <contact>
      <ode>
        <max_vel>100.0</max_vel>
        <min_depth>0.001</min_depth>  <!-- Smaller values: more accurate but slower -->
      </ode>
    </contact>
  </surface>
</collision>
```

## Practical Examples

### Example 1: Simple Collision World

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="collision_example">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Falling box -->
    <model name="falling_box">
      <pose>0 0 2 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>0.8</mu>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.0833</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>0.0833</iyy>
            <iyz>0</iyz>
            <izz>0.0833</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Bouncy sphere -->
    <model name="bouncy_sphere">
      <pose>1 0 2 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <sphere>
              <radius>0.2</radius>
            </sphere>
          </geometry>
          <surface>
            <bounce>
              <restitution_coefficient>0.9</restitution_coefficient>
            </bounce>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>0.2</radius>
            </sphere>
          </geometry>
        </visual>
        <inertial>
          <mass>0.5</mass>
          <inertia>
            <ixx>0.004</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>0.004</iyy>
            <iyz>0</iyz>
            <izz>0.004</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

### Example 2: Humanoid Robot with Collision Detection

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_collision">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <include>
      <uri>model://ground_plane</uri>
    </include>

    <model name="humanoid_with_collisions">
      <!-- Base link -->
      <link name="base_link">
        <collision name="base_collision">
          <geometry>
            <box><size>0.1 0.1 0.1</size></box>
          </geometry>
        </collision>
        <visual><geometry><box><size>0.1 0.1 0.1</size></box></geometry></visual>
        <inertial><mass>1.0</mass><inertia><ixx>0.01</ixx><iyy>0.01</iyy><izz>0.01</izz></inertia></inertial>
      </link>

      <!-- Torso -->
      <joint name="torso_joint" type="fixed">
        <parent>base_link</parent>
        <child>torso</child>
        <pose>0 0 0.2 0 0 0</pose>
      </joint>

      <link name="torso">
        <collision name="torso_collision">
          <geometry>
            <box><size>0.3 0.2 0.5</size></box>
          </geometry>
          <surface>
            <friction>
              <ode><mu>0.7</mu></ode>
            </friction>
          </surface>
        </collision>
        <visual><geometry><box><size>0.3 0.2 0.5</size></box></geometry></visual>
        <inertial><mass>10.0</mass><inertia><ixx>0.2</ixx><iyy>0.2</iyy><izz>0.2</izz></inertia></inertial>
      </link>

      <!-- Head -->
      <joint name="neck_joint" type="revolute">
        <parent>torso</parent>
        <child>head</child>
        <pose>0 0 0.4 0 0 0</pose>
        <axis><xyz>0 0 1</xyz></axis>
        <limit><lower>-0.5</lower><upper>0.5</upper></limit>
      </joint>

      <link name="head">
        <collision name="head_collision">
          <geometry>
            <sphere><radius>0.1</radius></sphere>
          </geometry>
        </collision>
        <visual><geometry><sphere><radius>0.1</radius></sphere></geometry></visual>
        <inertial><mass>2.0</mass><inertia><ixx>0.004</ixx><iyy>0.004</iyy><izz>0.004</izz></inertia></inertial>
      </link>

      <!-- Legs with collision detection -->
      <joint name="left_hip_joint" type="revolute">
        <parent>torso</parent>
        <child>left_upper_leg</child>
        <pose>0.1 0 -0.25 0 0 0</pose>
        <axis><xyz>0 1 0</xyz></axis>
        <limit><lower>-1.57</lower><upper>1.57</upper></limit>
      </joint>

      <link name="left_upper_leg">
        <collision name="left_upper_leg_collision">
          <geometry>
            <capsule><radius>0.06</radius><length>0.4</length></capsule>
          </geometry>
        </collision>
        <visual><geometry><cylinder><radius>0.06</radius><length>0.4</length></cylinder></visual>
        <inertial><mass>2.0</mass><inertia><ixx>0.01</ixx><iyy>0.01</iyy><izz>0.002</izz></inertia></inertial>
      </link>
    </model>
  </world>
</sdf>
```

## Collision Detection Performance

### Optimization Strategies

1. **Use Simple Geometries**: Prefer boxes, spheres, and capsules over complex meshes
2. **Adjust Physics Parameters**: Balance accuracy with performance
3. **Layer Collisions**: Use contact surface layers appropriately
4. **Disable Unnecessary Collisions**: Use `<disable_collisions>` tags where appropriate

### Performance Monitoring

Monitor simulation performance with collision detection:

```bash
# Check simulation statistics
gz topic -e /statistics

# Monitor real-time factor
gz topic -e /clock
```

## Troubleshooting Collision Issues

### Common Problems

#### Objects Pass Through Each Other
- Check collision geometries are properly defined
- Verify physics engine is active
- Increase solver iterations or adjust ERP/CFM values

#### Excessive Bouncing
- Check restitution coefficients
- Adjust contact parameters (ERP, CFM)
- Verify mass and inertial properties

#### Robot Self-Collisions
- Add `<disable_collisions>` tags in URDF
- Adjust joint limits to prevent self-collision
- Use collision filtering

#### Performance Issues
- Simplify collision geometries
- Reduce solver iterations (may reduce accuracy)
- Use appropriate time steps

## Advanced Collision Features

### Collision Filtering

You can filter collisions between specific objects:

```xml
<collision name="filtered_collision">
  <geometry>
    <box><size>1 1 1</size></box>
  </geometry>
  <surface>
    <contact>
      <collide_without_contact>true</collide_without_contact>  <!-- Detect but don't respond -->
    </contact>
  </surface>
</collision>
```

### Custom Contact Sensors

For detailed collision analysis:

```xml
<sensor name="contact_sensor" type="contact">
  <always_on>1</always_on>
  <update_rate>30</update_rate>
  <contact>
    <collision>collision_name</collision>
  </contact>
</sensor>
```

## Integration with ROS 2

Collision information can be accessed through ROS 2:

- Contact sensor data via ROS 2 topics
- Force/torque information from joint sensors
- Collision events through custom plugins

## Best Practices

### For Humanoid Robots

1. **Use appropriate geometries**: Capsules for limbs, boxes for torso
2. **Tune friction parameters**: Match real-world materials
3. **Validate with simple tests**: Ensure basic collisions work correctly
4. **Monitor performance**: Balance accuracy with simulation speed
5. **Test edge cases**: Ensure stable behavior under various conditions

### General Guidelines

1. **Start simple**: Use basic shapes, increase complexity gradually
2. **Match visual and collision**: Keep them consistent for debugging
3. **Document parameters**: Record why specific values were chosen
4. **Test thoroughly**: Verify behavior under various conditions

## Summary

Collision detection is fundamental to realistic physics simulation in Gazebo. Proper configuration ensures:
- Realistic robot-environment interactions
- Accurate force and contact computations
- Stable simulation behavior
- Valid sensor data generation

Always test collision configurations thoroughly and adjust parameters to balance accuracy with performance.