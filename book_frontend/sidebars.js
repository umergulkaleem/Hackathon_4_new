// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module1-ros2/fundamentals',
        'module1-ros2/communication',
        'module1-ros2/urdf-modeling',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module2-digital-twin/gazebo-physics',
        'module2-digital-twin/unity-rendering',
        'module2-digital-twin/integration',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module3-ai-brain/isaac-sim',
        'module3-ai-brain/isaac-ros',
        'module3-ai-brain/nav2-humanoid-navigation',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module4-vla/prerequisites',
        'module4-vla/setup-requirements',
        'module4-vla/chapter1-voice-to-action',
        'module4-vla/chapter1-quiz',
        'module4-vla/chapter2-cognitive-planning',
        'module4-vla/chapter2-quiz',
        'module4-vla/chapter3-capstone',
        'module4-vla/capstone-assessment',
        'module4-vla/summary',
        'module4-vla/troubleshooting',
        'module4-vla/quick-reference',
      ],
    },
    {
      type: 'category',
      label: 'Assessments',
      items: [
        'assessments/ros_fundamentals_quiz',
      ],
    },
    {
      type: 'category',
      label: 'Resources',
      items: [
        'accessibility_checklist',
        'success_criteria_review',
      ],
    },
  ],
};

module.exports = sidebars;