# Chapter 2: Unity for High-Fidelity Rendering

## Introduction

Welcome to Chapter 2 of Module 2: The Digital Twin (Gazebo & Unity). In this chapter, you will learn how to create high-fidelity visualizations of humanoid robots using Unity. By the end of this chapter, you will be able to create realistic Unity scenes with humanoid robot models and implement human-robot interaction scenarios.

## Learning Objectives

After completing this chapter, you will be able to:
- Install and configure Unity for robot visualization
- Import and set up humanoid robot 3D models
- Configure Unity's rendering pipeline (URP/HDRP)
- Set up lighting and materials for realistic visualization
- Configure cameras for optimal robot visualization
- Implement basic human-robot interaction scenarios
- Create animations and movement systems in Unity
- Design UI elements for robot control and visualization

## Prerequisites

Before starting this chapter, you should have:
- Basic knowledge of Unity concepts (scenes, game objects, components)
- Understanding of 3D modeling concepts (vertices, meshes, textures)
- Basic programming knowledge in C# (Unity's scripting language)
- Completion of Chapter 1: Gazebo Physics Simulation

## Unity Installation and Setup

### System Requirements

First, ensure your system meets the requirements for running Unity:
- Windows 10/11, macOS 10.14+, or Ubuntu 20.04+
- At least 8GB RAM (16GB recommended for complex scenes)
- Graphics card with OpenGL 3.3 or DirectX 11 support
- 20GB free disk space for Unity installation
- Unity 2022.3 LTS (Long Term Support) version

### Installing Unity Hub

Unity Hub is a management tool that allows you to install and manage multiple Unity versions:

1. Download Unity Hub from the [Unity website](https://unity.com/download)
2. Install Unity Hub following the platform-specific instructions
3. Sign in with your Unity ID or create a new account
4. Use Unity Hub to install Unity 2022.3 LTS

### Setting Up Unity for Robotics

When creating a new project in Unity, consider these settings for robotics applications:

1. Choose the "3D (Built-in Render Pipeline)" or "3D (URP)" template
2. For high-fidelity rendering, URP (Universal Render Pipeline) is recommended
3. Set the project name to reflect your robotics focus (e.g., "HumanoidRobotVisualization")

## Understanding Unity Concepts for Robotics

### GameObjects and Components

In Unity, everything is a GameObject. For robotics, common GameObjects include:
- Robot parts (torso, limbs, sensors)
- Environment objects (ground, obstacles, lighting)
- Controllers and managers

Each GameObject is composed of Components:
- Transform: Position, rotation, scale
- Mesh Renderer: Visual representation
- Colliders: Physics interactions
- Scripts: Custom behavior

### Coordinate Systems

Unity uses a left-handed coordinate system:
- X: Right
- Y: Up
- Z: Forward

This may differ from ROS coordinate conventions, so pay attention to coordinate transformations when integrating.

### Prefabs

Prefabs are reusable GameObject templates. For robotics, create prefabs for:
- Robot components (limbs, sensors)
- Complete robot models
- Common environment objects
- UI elements

## Importing Humanoid Robot Models

### Supported 3D Model Formats

Unity supports several 3D model formats:
- FBX: Most common and recommended format
- OBJ: Simple mesh format
- DAE: Collada format
- 3DS: 3D Studio format

### Model Preparation

Before importing robot models, ensure they are properly prepared:

1. **Scale**: Models should be appropriately scaled (typically 1-2 meters for humanoid robots)
2. **Pivot Points**: Center pivot points for easy positioning and rotation
3. **Mesh Quality**: Balance between visual quality and performance
4. **Materials**: Include basic materials and textures

### Importing a Robot Model

1. Place your robot model file (e.g., `humanoid_robot.fbx`) in the `Assets/Models/` folder
2. Unity will automatically import and create a GameObject
3. Configure import settings in the Inspector:
   - Scale Factor: Adjust if model is incorrectly scaled
   - Import Materials: Enable for material preservation
   - Animation Type: None, Legacy, or Humanoid for rigged models

### Example Robot Model Setup

Here's an example of how to structure a humanoid robot in Unity:

```csharp
using UnityEngine;

public class HumanoidRobot : MonoBehaviour
{
    [Header("Robot Components")]
    public Transform torso;
    public Transform head;
    public Transform leftArm;
    public Transform rightArm;
    public Transform leftLeg;
    public Transform rightLeg;

    [Header("Sensor Mounts")]
    public Transform lidarMount;
    public Transform cameraMount;
    public Transform imuMount;

    [Header("Movement Parameters")]
    public float walkSpeed = 2.0f;
    public float turnSpeed = 100.0f;

    // Animation rigging for realistic movement
    Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        // Movement logic would go here
    }
}
```

## Rendering Pipeline Setup

### Universal Render Pipeline (URP)

URP provides a modern, lightweight rendering pipeline that's efficient for robotics visualization:

1. Install URP from the Package Manager (Window > Package Manager)
2. Create a new URP Asset (Assets > Create > Rendering > Universal Render Pipeline > Pipeline Asset)
3. In Project Settings > Graphics, assign the new URP asset to Scriptable Render Pipeline Settings

### High Definition Render Pipeline (HDRP)

For maximum visual quality (at the cost of performance):
1. Install HDRP from the Package Manager
2. Create HDRP Asset (Assets > Create > Rendering > High Definition Render Pipeline > HDRP Asset)
3. Configure the HDRP asset settings

### Basic URP Configuration

For robotics applications, use these URP settings:
- Renderer: Forward renderer (good balance of features and performance)
- Lighting: Forward+, which handles multiple lights efficiently
- Anti-aliasing: FXAA for performance or TAA for quality
- Shadow resolution: Medium to High depending on needs

## Lighting and Material Configuration

### Light Types in Unity

For realistic robot visualization, use appropriate light types:

1. **Directional Light**: Simulates sunlight or main light source
2. **Point Light**: Local light sources on the robot or in the environment
3. **Spot Light**: Focused lighting for specific areas
4. **Area Light**: Soft lighting for realistic shadows (baked only in URP)

### Creating Realistic Materials

Create materials that match the robot's physical properties:

```csharp
// Example material configuration script
using UnityEngine;

public class RobotMaterialSetup : MonoBehaviour
{
    [Header("Material Properties")]
    public Material metalMaterial;
    public Material plasticMaterial;
    public Material rubberMaterial;

    void Start()
    {
        ConfigureMetalMaterial();
        ConfigurePlasticMaterial();
        ConfigureRubberMaterial();
    }

    void ConfigureMetalMaterial()
    {
        if (metalMaterial != null)
        {
            metalMaterial.SetColor("_BaseColor", Color.gray);
            metalMaterial.SetFloat("_Metallic", 0.9f);
            metalMaterial.SetFloat("_Smoothness", 0.8f);
        }
    }

    void ConfigurePlasticMaterial()
    {
        if (plasticMaterial != null)
        {
            plasticMaterial.SetColor("_BaseColor", Color.blue);
            metalMaterial.SetFloat("_Metallic", 0.1f);
            metalMaterial.SetFloat("_Smoothness", 0.3f);
        }
    }

    void ConfigureRubberMaterial()
    {
        if (rubberMaterial != null)
        {
            rubberMaterial.SetColor("_BaseColor", Color.black);
            metalMaterial.SetFloat("_Metallic", 0.0f);
            metalMaterial.SetFloat("_Smoothness", 0.1f);
        }
    }
}
```

### Lighting Setup for Robotics

Create a balanced lighting setup for robot visualization:

1. **Main Light**: Directional light representing primary illumination
2. **Fill Light**: Softer light to reduce harsh shadows
3. **Back Light**: Light from behind to separate the robot from the background
4. **Environment Lighting**: Ambient lighting from the skybox

## Camera Configuration for Visualization

### Camera Types for Robotics

Different camera perspectives serve different purposes in robotics:

1. **Third-Person Camera**: Overview of robot and environment
2. **First-Person Camera**: Robot's perspective (with sensors)
3. **Follow Camera**: Tracks robot movement
4. **Static Cameras**: Fixed viewpoints for monitoring

### Creating a Robot-Following Camera

```csharp
using UnityEngine;

public class RobotCameraController : MonoBehaviour
{
    [Header("Target Setup")]
    public Transform target; // The robot to follow
    public Vector3 offset = new Vector3(0, 2, -5); // Camera offset from robot

    [Header("Camera Settings")]
    public float smoothSpeed = 0.125f;
    public float rotationSpeed = 2.0f;

    [Header("Constraints")]
    public float minDistance = 2.0f;
    public float maxDistance = 10.0f;

    void LateUpdate()
    {
        if (target == null) return;

        // Calculate desired position
        Vector3 desiredPosition = target.position + offset;
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed);

        transform.position = smoothedPosition;
        transform.LookAt(target);
    }
}
```

### Multiple Camera Setup

For comprehensive robot monitoring:

```csharp
using UnityEngine;

public class MultiCameraSetup : MonoBehaviour
{
    [Header("Camera References")]
    public Camera[] cameras;
    public int activeCameraIndex = 0;

    void Start()
    {
        ActivateCamera(0);
    }

    void Update()
    {
        // Switch cameras with number keys
        for (int i = 0; i < cameras.Length; i++)
        {
            if (Input.GetKeyDown(KeyCode.Alpha1 + i))
            {
                ActivateCamera(i);
            }
        }
    }

    void ActivateCamera(int index)
    {
        for (int i = 0; i < cameras.Length; i++)
        {
            cameras[i].gameObject.SetActive(i == index);
        }
        activeCameraIndex = index;
    }
}
```

## Human-Robot Interaction Scenarios

### Basic Interaction System

Create a system for users to interact with the robot:

```csharp
using UnityEngine;
using UnityEngine.UI;

public class RobotInteractionSystem : MonoBehaviour
{
    [Header("UI References")]
    public Button moveForwardButton;
    public Button moveBackwardButton;
    public Button turnLeftButton;
    public Button turnRightButton;
    public Slider speedSlider;

    [Header("Robot Reference")]
    public HumanoidRobot robot;

    void Start()
    {
        SetupUI();
    }

    void SetupUI()
    {
        if (moveForwardButton != null)
            moveForwardButton.onClick.AddListener(() => MoveRobot(Vector3.forward));

        if (moveBackwardButton != null)
            moveBackwardButton.onClick.AddListener(() => MoveRobot(Vector3.back));

        if (turnLeftButton != null)
            turnLeftButton.onClick.AddListener(() => RotateRobot(-1));

        if (turnRightButton != null)
            turnRightButton.onClick.AddListener(() => RotateRobot(1));
    }

    void MoveRobot(Vector3 direction)
    {
        if (robot != null)
        {
            float speed = speedSlider != null ? speedSlider.value : 1.0f;
            robot.transform.Translate(direction * speed * Time.deltaTime);
        }
    }

    void RotateRobot(int direction)
    {
        if (robot != null)
        {
            float rotationSpeed = speedSlider != null ? speedSlider.value * 50 : 50.0f;
            robot.transform.Rotate(Vector3.up, direction * rotationSpeed * Time.deltaTime);
        }
    }
}
```

### Sensor Visualization

Create visualizations for robot sensors:

```csharp
using UnityEngine;

public class SensorVisualization : MonoBehaviour
{
    [Header("Sensor References")]
    public Transform lidarTransform;
    public Transform cameraTransform;
    public Transform imuTransform;

    [Header("Visualization Settings")]
    public float lidarRange = 10.0f;
    public float cameraFOV = 60.0f;
    public LineRenderer lidarRay;
    public GameObject cameraFrustum;

    void Update()
    {
        VisualizeLidar();
        VisualizeCamera();
    }

    void VisualizeLidar()
    {
        if (lidarRay != null)
        {
            lidarRay.SetPosition(0, lidarTransform.position);
            lidarRay.SetPosition(1, lidarTransform.position + lidarTransform.forward * lidarRange);
        }
    }

    void VisualizeCamera()
    {
        if (cameraFrustum != null)
        {
            // Update camera frustum visualization based on FOV
            // This would typically be handled with custom mesh or gizmo rendering
        }
    }
}
```

## Animation and Movement Systems

### Robot Animation Controller

Set up animations for robot movement:

1. Create an Animator Controller (Assets > Create > Animator Controller)
2. Set up states for different movements (idle, walk, turn, etc.)
3. Create transitions between states based on parameters
4. Assign the controller to your robot's Animator component

### Simple Robot Walking Animation

```csharp
using UnityEngine;

public class RobotWalkController : MonoBehaviour
{
    [Header("Animation Parameters")]
    public Animator animator;
    public float walkSpeed = 2.0f;
    public float turnSpeed = 100.0f;

    [Header("Animation Triggers")]
    public string speedParameter = "Speed";
    public string turnParameter = "Turn";

    void Update()
    {
        HandleMovement();
    }

    void HandleMovement()
    {
        if (animator == null) return;

        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        // Calculate movement parameters
        float speed = Mathf.Clamp01(vertical);
        float turn = Mathf.Clamp(horizontal, -1f, 1f);

        // Apply to animator
        animator.SetFloat(speedParameter, speed);
        animator.SetFloat(turnParameter, turn);

        // Apply actual movement
        transform.Translate(Vector3.forward * speed * walkSpeed * Time.deltaTime);
        transform.Rotate(Vector3.up, turn * turnSpeed * Time.deltaTime);
    }
}
```

## UI Elements for Robot Control

### Creating Robot Status UI

```csharp
using UnityEngine;
using UnityEngine.UI;

public class RobotStatusUI : MonoBehaviour
{
    [Header("UI Text Elements")]
    public Text positionText;
    public Text statusText;
    public Text batteryText;
    public Slider healthSlider;

    [Header("Robot Reference")]
    public HumanoidRobot robot;

    void Update()
    {
        UpdateRobotStatus();
    }

    void UpdateRobotStatus()
    {
        if (robot != null)
        {
            // Update position
            if (positionText != null)
            {
                positionText.text = $"Position: {robot.transform.position}";
            }

            // Update status
            if (statusText != null)
            {
                statusText.text = "Status: Active";
            }

            // Update battery
            if (batteryText != null)
            {
                batteryText.text = "Battery: 100%";
            }

            // Update health
            if (healthSlider != null)
            {
                healthSlider.value = 1.0f; // Robot health value
            }
        }
    }
}
```

## Practical Exercise: Complete Robot Visualization

Create a complete robot visualization scene with:

1. Import a humanoid robot model
2. Set up appropriate materials and lighting
3. Create a camera system to view the robot
4. Implement basic movement controls
5. Add sensor visualization
6. Create UI elements to monitor robot status

### Exercise Steps:

1. **Model Setup**: Import a humanoid robot model and organize it hierarchically
2. **Material Assignment**: Apply appropriate materials to different robot parts
3. **Lighting**: Set up 3-point lighting for good robot visibility
4. **Camera**: Create a camera that can orbit around the robot
5. **Controls**: Implement keyboard controls to move and rotate the robot
6. **Visualization**: Add visual indicators for sensor ranges and fields of view

## Optimization Recommendations

### Performance Optimization

For real-time robot visualization:

1. **LOD (Level of Detail)**: Use lower-poly models when the camera is far away
2. **Occlusion Culling**: Hide objects not visible to the camera
3. **Texture Compression**: Use compressed textures to save memory
4. **Batching**: Combine similar meshes to reduce draw calls
5. **Shader Complexity**: Use simpler shaders for performance-critical applications

### Quality Settings for Robotics

Consider these quality settings for robotics applications:

```csharp
// Quality settings for robot visualization
using UnityEngine;

public class RobotQualitySettings : MonoBehaviour
{
    void Start()
    {
        // Set quality level based on hardware capabilities
        QualitySettings.SetQualityLevel(3); // Medium quality as default

        // Enable anti-aliasing for smooth edges
        QualitySettings.antiAliasing = 2;

        // Optimize shadows for performance
        QualitySettings.shadowDistance = 20.0f;
        QualitySettings.shadowResolution = ShadowResolution.Medium;
    }
}
```

## Troubleshooting Common Issues

### Model Import Issues
- **Incorrect Scale**: Check model units and adjust import scale factor
- **Missing Textures**: Ensure texture files are in the same directory or properly referenced
- **Missing Materials**: Reassign materials after import

### Performance Issues
- **Low Frame Rate**: Reduce draw distance, use simpler shaders, optimize meshes
- **High Memory Usage**: Compress textures, use object pooling
- **Stuttering**: Check for heavy scripts running every frame

### Lighting Issues
- **Dark Models**: Ensure lights are enabled and properly positioned
- **Overexposed**: Adjust light intensity and camera exposure
- **No Shadows**: Check shadow settings in both lights and quality settings

## Summary

In this chapter, you've learned:
- How to install and set up Unity for robotics visualization
- How to import and configure humanoid robot models
- How to set up rendering pipelines for high-fidelity visualization
- How to configure lighting and materials for realistic rendering
- How to set up camera systems for optimal robot visualization
- How to implement human-robot interaction scenarios
- How to create animations and movement systems
- How to design UI elements for robot control

## Next Steps

In the next chapter, you'll learn how to integrate Gazebo physics simulation with Unity rendering to create synchronized environments for AI training and testing.