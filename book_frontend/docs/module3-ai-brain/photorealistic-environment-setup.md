# Photorealistic Environment Setup Guide with Lighting Configuration

## Overview

This guide provides detailed instructions for creating photorealistic environments in NVIDIA Isaac Sim with proper lighting configuration. Creating realistic environments is crucial for generating high-quality synthetic data that can be effectively used for AI training and testing.

## Understanding Photorealistic Rendering

### What Makes an Environment Photorealistic?

Photorealistic environments in Isaac Sim require careful attention to several key elements:

1. **Lighting**: Proper simulation of natural and artificial light sources
2. **Materials**: Realistic surface properties and textures
3. **Geometry**: Accurate representation of real-world objects
4. **Atmospherics**: Effects like fog, haze, and atmospheric scattering
5. **Post-processing**: Color grading, depth of field, and other effects

### USD and MaterialX

Isaac Sim uses USD (Universal Scene Description) as its core format and MaterialX for physically-based material definitions. Understanding these technologies is essential for creating photorealistic environments.

## Environment Setup Process

### 1. Creating the Base Scene

Start with a new stage and establish the basic environment:

1. **Create New Stage**:
   - File > New Stage
   - Set appropriate units (meters recommended for robotics)

2. **Add Ground Plane**:
   - Create > Ground Plane
   - Adjust size based on your needs (typically 10x10 to 100x100 units)
   - Apply realistic ground material

3. **Set Up Basic Structure**:
   - Add walls, ceiling, or outdoor terrain as needed
   - Use realistic dimensions based on your application

### 2. Implementing Realistic Lighting

#### Natural Lighting

For outdoor or naturally-lit environments:

1. **Add Distant Light (Sun)**:
   - Create > Light > Distant Light
   - Set intensity to 50,000 lux for direct sunlight
   - Adjust rotation to simulate time of day
   - Enable shadows for realistic effects

2. **Configure Environment Light**:
   - Create > Light > Dome Light
   - Use HDR texture for realistic environmental lighting
   - Adjust exposure to match distant light

#### Artificial Lighting

For indoor or artificially-lit environments:

1. **Add Area Lights**:
   - Create > Light > Rect Light or Disk Light
   - Set appropriate size for realistic shadow softness
   - Adjust intensity (typically 200-2000 lumens per m²)

2. **Configure Light Types**:
   - **Rect Lights**: For panel lights, windows
   - **Disk Lights**: For circular fixtures
   - **Sphere Lights**: For omnidirectional sources
   - **Spot Lights**: For focused illumination

### 3. Advanced Lighting Techniques

#### Three-Point Lighting Setup

Implement professional lighting techniques:

```python
# Example Python code for three-point lighting setup
import omni
from omni.isaac.core.utils.prims import create_prim
from pxr import Gf

# Key Light (main light source)
create_prim(
    prim_path="/World/Lights/KeyLight",
    prim_type="DistantLight",
    position=Gf.Vec3f(5, 5, 5),
    orientation=Gf.Quatf(0.707, -0.707, 0, 0)  # Pointing down and toward center
)

# Adjust key light properties
key_light = omni.usd.get_context().get_stage().GetPrimAtPath("/World/Lights/KeyLight")
key_light.GetAttribute("inputs:intensity").Set(30000)  # Lux
key_light.GetAttribute("inputs:color").Set(Gf.Vec3f(1.0, 0.98, 0.9))  # Warm white

# Fill Light (reduces shadows)
create_prim(
    prim_path="/World/Lights/FillLight",
    prim_type="DistantLight",
    position=Gf.Vec3f(-3, 3, 2),
    orientation=Gf.Quatf(0.924, 0.383, 0, 0)
)

fill_light = omni.usd.get_context().get_stage().GetPrimAtPath("/World/Lights/FillLight")
fill_light.GetAttribute("inputs:intensity").Set(10000)  # Lower intensity than key
fill_light.GetAttribute("inputs:color").Set(Gf.Vec3f(0.9, 0.94, 1.0))  # Cool fill

# Back Light (separates subject from background)
create_prim(
    prim_path="/World/Lights/BackLight",
    prim_type="DistantLight",
    position=Gf.Vec3f(0, -4, 3),
    orientation=Gf.Quatf(0.383, 0.924, 0, 0)
)

back_light = omni.usd.get_context().get_stage().GetPrimAtPath("/World/Lights/BackLight")
back_light.GetAttribute("inputs:intensity").Set(15000)
back_light.GetAttribute("inputs:color").Set(Gf.Vec3f(1.0, 0.98, 0.9))
```

#### HDRI Environment Lighting

Use High Dynamic Range Images for realistic environmental lighting:

1. **Import HDRI**:
   - Download or create HDRI textures
   - Import into Isaac Sim's asset library
   - Apply to Dome Light as texture

2. **Configure HDRI Settings**:
   - Adjust exposure to match scene lighting
   - Rotate to align with sun position
   - Enable multiple importance sampling for better performance

### 4. Material Configuration

#### Physically-Based Materials

Create realistic materials using MaterialX:

1. **Basic Material Properties**:
   - **Base Color**: Albedo or diffuse color
   - **Normal Map**: Surface detail without geometry
   - **Roughness**: Surface microfacet distribution
   - **Metallic**: Metallic vs. dielectric properties
   - **Specular**: Reflectance properties

2. **Advanced Material Features**:
   - **Subsurface Scattering**: For skin, wax, marble
   - **Anisotropy**: For brushed metals, hair
   - **Sheen**: For fabrics and skin
   - **Clearcoat**: For varnished surfaces

#### Example Material Setup

```python
# Example material setup in Python
import omni
from pxr import Sdf, UsdShade, Gf

def create_realistic_material(stage, prim_path, material_name):
    """Create a realistic material with common properties"""

    # Create material prim
    material_path = Sdf.Path(prim_path)
    material = UsdShade.Material.Define(stage, material_path)

    # Create shader
    shader_path = material_path.AppendChild("Surface")
    shader = UsdShade.Shader.Define(stage, shader_path)
    shader.CreateIdAttr("OmniPBR")

    # Set material properties
    shader.CreateInput("diffuse_tint", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.8, 0.8, 0.8))
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    shader.CreateInput("specular_level", Sdf.ValueTypeNames.Float).Set(0.5)

    # Connect shader to material
    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "out")

    return material

# Usage example
stage = omni.usd.get_context().get_stage()
create_realistic_material(stage, "/World/Materials/GroundMaterial", "Ground")
```

## Specific Environment Types

### Indoor Environments

#### Office Environment
1. **Flooring**: Use realistic carpet or tile materials
2. **Walls**: Paint with appropriate reflectance (0.6-0.8)
3. **Furniture**: Add realistic office furniture with proper materials
4. **Lighting**: Mix of overhead lighting and task lighting
5. **Windows**: Add for natural light if needed

#### Industrial Environment
1. **Flooring**: Concrete or metal with appropriate textures
2. **Walls**: Industrial materials like concrete, metal panels
3. **Equipment**: Add industrial machinery and equipment
4. **Lighting**: High-intensity discharge (HID) or LED industrial lights
5. **Atmospherics**: Consider adding dust or fog effects

### Outdoor Environments

#### Urban Environment
1. **Ground**: Asphalt, concrete, or mixed materials
2. **Buildings**: Realistic architectural models
3. **Vegetation**: Trees, bushes, and landscaping
4. **Lighting**: Natural lighting with shadows
5. **Atmospherics**: Consider weather conditions

#### Natural Environment
1. **Terrain**: Use height maps or procedural terrain
2. **Ground Cover**: Grass, dirt, rocks with realistic materials
3. **Vegetation**: Trees, plants, and natural elements
4. **Water**: Lakes, rivers, or puddles if applicable
5. **Sky**: Realistic sky dome with atmospheric effects

## Lighting Configuration Best Practices

### Time of Day Simulation

Simulate different times of day for varied lighting conditions:

1. **Morning**: Warm, low-angle lighting
2. **Noon**: Harsh, overhead lighting
3. **Evening**: Warm, long shadows
4. **Night**: Artificial lighting dominance

### Weather Conditions

Create different weather scenarios:

1. **Clear Day**: Direct sunlight, sharp shadows
2. **Overcast**: Soft, even lighting
3. **Rain**: Wet surfaces, reduced visibility
4. **Snow**: Bright, reflective surfaces

### Dynamic Lighting

Implement time-varying lighting for more realistic environments:

```python
# Example dynamic lighting based on time
import omni
from pxr import Gf
import math

def update_dynamic_lighting(time_of_day):
    """
    Update lighting based on time of day (0-24 hours)
    """
    # Calculate sun position based on time
    hour_angle = (time_of_day - 12) * 15  # 15 degrees per hour
    sun_altitude = 90 - 23.5 * math.cos(math.radians(hour_angle))

    # Calculate sun direction
    sun_azimuth = hour_angle
    x = math.cos(math.radians(sun_altitude)) * math.sin(math.radians(sun_azimuth))
    y = math.sin(math.radians(sun_altitude))
    z = math.cos(math.radians(sun_altitude)) * math.cos(math.radians(sun_azimuth))

    sun_direction = Gf.Vec3f(x, y, z).GetNormalized()

    # Update distant light direction
    distant_light = omni.usd.get_context().get_stage().GetPrimAtPath("/World/DistantLight")
    if distant_light.IsValid():
        distant_light.GetAttribute("xformOp:rotateXYZ").Set(Gf.Vec3f(
            math.degrees(math.asin(sun_direction[1])),  # Pitch
            math.degrees(math.atan2(sun_direction[0], sun_direction[2])),  # Yaw
            0  # Roll
        ))

    # Adjust intensity based on sun angle
    intensity = max(0, sun_direction[1] * 50000)  # Maximum 50,000 lux at noon
    distant_light.GetAttribute("inputs:intensity").Set(intensity)
```

## Performance Optimization

### Rendering Performance

Optimize photorealistic environments for real-time performance:

1. **Level of Detail (LOD)**:
   - Create simplified versions of complex objects
   - Use distance-based switching
   - Reduce polygon count where possible

2. **Texture Optimization**:
   - Use appropriate texture resolution
   - Implement texture streaming
   - Use texture compression where appropriate

3. **Lighting Optimization**:
   - Limit number of dynamic lights
   - Use light baking for static lighting
   - Use light probes for indirect lighting

### Scene Complexity Management

Balance realism with performance:

1. **Object Density**: Don't overcrowd scenes
2. **Material Complexity**: Use simpler materials when possible
3. **Lighting Complexity**: Limit dynamic lighting calculations
4. **Post-processing**: Use effects judiciously

## Quality Validation

### Visual Quality Checks

Validate the quality of your photorealistic environment:

1. **Shadow Quality**: Check for realistic shadow shapes and softness
2. **Lighting Consistency**: Ensure all lighting is consistent
3. **Material Realism**: Verify materials look realistic
4. **Color Accuracy**: Check for proper color temperature

### Technical Validation

Ensure technical correctness:

1. **Performance**: Maintain target frame rate (typically 30+ FPS)
2. **Memory Usage**: Monitor GPU and system memory
3. **Render Quality**: Check for artifacts or errors
4. **Consistency**: Ensure consistent lighting across scenes

## Troubleshooting Common Issues

### Lighting Issues

**Problem**: Scene appears too dark or too bright
- **Solution**: Check light intensities and camera exposure settings

**Problem**: Shadows appear incorrect
- **Solution**: Verify light directions and shadow settings

**Problem**: Lighting doesn't appear realistic
- **Solution**: Check light colors, intensities, and physical properties

### Material Issues

**Problem**: Materials appear unrealistic
- **Solution**: Verify material properties and textures

**Problem**: Materials don't respond to lighting properly
- **Solution**: Check material shader configuration

### Performance Issues

**Problem**: Slow rendering performance
- **Solution**: Optimize scene complexity, lighting, and materials

**Problem**: GPU memory overflow
- **Solution**: Reduce texture resolution or scene complexity

## Advanced Techniques

### Procedural Environment Generation

Create environments programmatically for variation:

1. **Randomization**: Randomize object placement and properties
2. **Parametric Design**: Use parameters to control environment generation
3. **Modular Assets**: Create reusable environment components

### Synthetic Data Diversity

Enhance synthetic data quality through environmental variation:

1. **Lighting Variation**: Multiple lighting conditions
2. **Material Variation**: Different materials for same object types
3. **Object Placement**: Randomized object arrangements
4. **Weather Simulation**: Different atmospheric conditions

## Verification Checklist

Before finalizing your photorealistic environment, verify:

- [ ] Lighting appears realistic and physically accurate
- [ ] Materials respond correctly to lighting
- [ ] Shadows are properly cast and softness is appropriate
- [ ] Color temperature is consistent throughout scene
- [ ] Performance meets real-time requirements
- [ ] Environment is suitable for intended application
- [ ] Synthetic data quality meets requirements
- [ ] Scene is properly optimized for performance

This guide provides the foundation for creating photorealistic environments in Isaac Sim. With proper lighting and material configuration, you can generate high-quality synthetic data that effectively supports AI training and testing for humanoid robots.