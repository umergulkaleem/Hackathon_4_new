# Quickstart Guide: VLA Learning Module

**Feature**: VLA Learning Module
**Created**: 2025-12-17
**Status**: Complete

## Overview

This guide helps you get started with the Vision-Language-Action (VLA) learning module. The module teaches how voice, vision, and LLMs drive autonomous humanoid behavior end to end using Docusaurus-based documentation with interactive examples.

## Prerequisites

Before starting the VLA learning module, ensure you have:

- Basic understanding of ROS 2 concepts
- Familiarity with robot simulation environments
- Basic knowledge of computer vision and perception
- Access to a computer with Docker installed

## Environment Setup

### Option 1: Docker Setup (Recommended)

1. **Install Docker**
   ```bash
   # For Windows/Mac: Install Docker Desktop
   # For Linux:
   sudo apt update
   sudo apt install docker.io docker-compose
   sudo usermod -aG docker $USER
   ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

3. **Start the development environment**
   ```bash
   cd book_frontend
   npm install
   npm run start
   ```

4. **Start the ROS 2 simulation environment**
   ```bash
   cd simulation
   docker-compose up -d ros2-humanoid-sim
   ```

### Option 2: Native Setup

1. **Install ROS 2 Humble Hawksbill**
   Follow the official installation guide: https://docs.ros.org/en/humble/Installation.html

2. **Install required packages**
   ```bash
   sudo apt update
   sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-navigation2 ros-humble-nav2-bringup
   ```

3. **Install Python dependencies**
   ```bash
   pip install openai speech-recognition numpy matplotlib
   ```

## Accessing the Learning Module

1. **Start the Docusaurus server**
   ```bash
   cd book_frontend
   npm start
   ```

2. **Open your browser** to `http://localhost:3000`

3. **Navigate to the VLA Learning Module** in the sidebar

## Chapter Structure

The VLA learning module consists of three main chapters:

### Chapter 1: Voice-to-Action Interfaces
- Learn speech recognition concepts using OpenAI Whisper
- Practice converting voice commands into structured inputs
- Implement audio processing pipelines

**Start here**: Navigate to "Modules" → "Module 4: VLA" → "Chapter 1: Voice-to-Action Interfaces"

### Chapter 2: Cognitive Planning with LLMs
- Understand how LLMs translate natural language to ROS 2 actions
- Learn task decomposition and planning logic
- Implement cognitive planning algorithms

**Prerequisite**: Complete Chapter 1

### Chapter 3: Capstone - Autonomous Humanoid
- Integrate voice, vision, and LLM components
- Implement voice-driven navigation and manipulation
- Complete the comprehensive capstone project

**Prerequisites**: Complete Chapters 1 and 2

## Interactive Examples

Each chapter includes interactive examples that you can run directly in your browser:

1. **Code Editor**: Modify example code and see results instantly
2. **Simulation Viewer**: Visualize robot behavior in simulated environments
3. **Audio Input**: Test voice recognition with your microphone (where supported)
4. **Step-by-Step Guidance**: Follow along with detailed instructions

## Running Simulations

### Starting a Simulation

1. Navigate to an example that includes simulation
2. Click "Start Simulation" button
3. Wait for the Docker container to initialize
4. Use the controls to interact with the simulated robot

### Common Simulation Commands

```bash
# Check simulation status
docker-compose ps

# View simulation logs
docker-compose logs ros2-humanoid-sim

# Stop simulation
docker-compose down
```

## Assessment and Progress Tracking

- Complete exercises at the end of each section
- Take chapter quizzes to test your understanding
- Track your progress through the module
- Access the capstone project after completing prerequisites

## Troubleshooting

### Common Issues

**Problem**: Simulation won't start
- Solution: Ensure Docker is running and you have sufficient memory (8GB+ recommended)

**Problem**: Audio examples not working
- Solution: Check microphone permissions in your browser settings

**Problem**: Code examples not executing
- Solution: Ensure all dependencies are installed and restart the development server

### Getting Help

- Check the FAQ section in each chapter
- Review the troubleshooting guide in the documentation
- Join the community forum for additional support

## Next Steps

1. Complete the prerequisite assessment to ensure you're ready
2. Start with Chapter 1: Voice-to-Action Interfaces
3. Work through each chapter sequentially
4. Complete the capstone project to demonstrate your knowledge
5. Explore additional resources and advanced topics

## Support

For technical issues or questions about the VLA learning module:
- Create an issue in the GitHub repository
- Join our Discord community
- Check the documentation for detailed explanations

---

**Ready to begin?** Navigate to the VLA Learning Module in your Docusaurus documentation site and start with Chapter 1!