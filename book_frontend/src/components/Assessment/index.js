// VLA Assessment Components Index
// This file exports all VLA-specific assessment components for easy import

export { default as VoiceCommandExercise } from './VoiceCommandExercise';
export { default as PlanningExercise } from './PlanningExercise';
export { default as CapstoneExercise } from './CapstoneExercise';

// Additional assessment utilities could be added here
export const AssessmentUtils = {
  // Utility functions for assessments
  calculateScore: (correct, total) => {
    return Math.round((correct / total) * 100);
  },

  validateAnswer: (userAnswer, correctAnswer) => {
    return userAnswer.toLowerCase().trim() === correctAnswer.toLowerCase().trim();
  },

  provideFeedback: (isCorrect, correctAnswer, userAnswer = null) => {
    if (isCorrect) {
      return "Correct! Well done.";
    } else {
      return `Incorrect. The correct answer is: ${correctAnswer}`;
    }
  }
};

export default {
  VoiceCommandExercise,
  PlanningExercise,
  CapstoneExercise,
  AssessmentUtils
};