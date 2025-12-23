// VLA Module Content API
// This API provides access to VLA learning module content and functionality

// Base API configuration
const API_BASE_URL = '/api/vla';
const CONTENT_BASE_URL = '/docs/module4-vla';

// Content API functions
export const VLAContentAPI = {
  // Get module metadata
  getModuleInfo: async () => {
    try {
      // In a real implementation, this would fetch from an actual API
      // For now, we'll return static information
      return {
        moduleId: 'vla-learning-module',
        title: 'Vision-Language-Action (VLA) Learning Module',
        description: 'Learn how voice, vision, and LLMs drive autonomous humanoid behavior end to end',
        chapters: 3,
        estimatedDuration: 8, // hours
        difficulty: 'advanced',
        prerequisites: [
          'ROS 2 fundamentals',
          'Basic robot perception',
          'Simulation experience'
        ]
      };
    } catch (error) {
      console.error('Error fetching module info:', error);
      throw error;
    }
  },

  // Get chapter list
  getChapters: async () => {
    try {
      return [
        {
          id: 'chapter1-voice-to-action',
          title: 'Chapter 1 - Voice-to-Action Interfaces',
          description: 'Learn speech recognition using OpenAI Whisper',
          order: 1,
          estimatedTime: 2 // hours
        },
        {
          id: 'chapter2-cognitive-planning',
          title: 'Chapter 2 - Cognitive Planning with LLMs',
          description: 'Translate natural language goals to ROS 2 actions',
          order: 2,
          estimatedTime: 3 // hours
        },
        {
          id: 'chapter3-capstone',
          title: 'Chapter 3 - Capstone: Autonomous Humanoid',
          description: 'Integrate all VLA concepts in a comprehensive project',
          order: 3,
          estimatedTime: 3 // hours
        }
      ];
    } catch (error) {
      console.error('Error fetching chapters:', error);
      throw error;
    }
  },

  // Get specific chapter content
  getChapter: async (chapterId) => {
    try {
      // This would normally fetch from the actual documentation
      // For now, return a structure with the content path
      return {
        id: chapterId,
        contentPath: `${CONTENT_BASE_URL}/${chapterId}.md`,
        exercisesPath: `${CONTENT_BASE_URL}/${chapterId.replace('chapter', 'chapter')}-quiz.md`,
        examples: [], // Would include interactive examples
        objectives: [] // Would include learning objectives
      };
    } catch (error) {
      console.error(`Error fetching chapter ${chapterId}:`, error);
      throw error;
    }
  },

  // Get interactive examples for a chapter
  getExamples: async (chapterId) => {
    try {
      // Return available interactive examples for the chapter
      const examples = {
        'chapter1-voice-to-action': [
          {
            id: 'whisper-demo',
            title: 'OpenAI Whisper Speech Recognition',
            component: 'WhisperDemo',
            description: 'Demonstrate voice-to-text conversion'
          }
        ],
        'chapter2-cognitive-planning': [
          {
            id: 'planning-demo',
            title: 'LLM-Based Planning',
            component: 'PlanningDemo',
            description: 'Show cognitive planning with LLMs'
          }
        ],
        'chapter3-capstone': [
          {
            id: 'integrated-demo',
            title: 'Complete VLA System',
            component: 'IntegratedDemo',
            description: 'Full VLA pipeline demonstration'
          },
          {
            id: 'simulation-viewer',
            title: 'Robot Simulation',
            component: 'SimulationViewer',
            description: 'Visualize robot behavior in different scenarios'
          }
        ]
      };

      return examples[chapterId] || [];
    } catch (error) {
      console.error(`Error fetching examples for ${chapterId}:`, error);
      throw error;
    }
  },

  // Get assessments for a chapter
  getAssessments: async (chapterId) => {
    try {
      // Return available assessments for the chapter
      const assessments = {
        'chapter1-voice-to-action': [
          {
            id: 'chapter1-quiz',
            title: 'Chapter 1 Quiz',
            type: 'multiple-choice',
            questions: 10
          },
          {
            id: 'voice-command-exercise',
            title: 'Voice Command Parsing Exercise',
            type: 'interactive',
            component: 'VoiceCommandExercise'
          }
        ],
        'chapter2-cognitive-planning': [
          {
            id: 'chapter2-quiz',
            title: 'Chapter 2 Quiz',
            type: 'multiple-choice',
            questions: 12
          },
          {
            id: 'planning-exercise',
            title: 'Cognitive Planning Exercise',
            type: 'interactive',
            component: 'PlanningExercise'
          }
        ],
        'chapter3-capstone': [
          {
            id: 'capstone-assessment',
            title: 'Capstone Project Assessment',
            type: 'comprehensive',
            component: 'CapstoneExercise'
          }
        ]
      };

      return assessments[chapterId] || [];
    } catch (error) {
      console.error(`Error fetching assessments for ${chapterId}:`, error);
      throw error;
    }
  }
};

// Helper functions
export const VLAUtils = {
  // Format chapter content for display
  formatChapterContent: (rawContent) => {
    // In a real implementation, this would process the markdown content
    // for optimal display in the learning interface
    return rawContent || '';
  },

  // Calculate progress based on completed items
  calculateProgress: (completedItems, totalItems) => {
    return totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;
  }
};

export default VLAContentAPI;