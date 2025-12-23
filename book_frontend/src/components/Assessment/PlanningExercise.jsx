import React, { useState } from 'react';
import './assessment-styles.css'; // Import assessment styles

const PlanningExercise = () => {
  const [selectedSteps, setSelectedSteps] = useState([]);
  const [feedback, setFeedback] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const exercises = [
    {
      id: 1,
      scenario: "User says: 'Go to the kitchen and bring me a cup'",
      question: "Arrange the correct sequence of actions for this command:",
      steps: [
        { id: 'a', text: "Navigate to kitchen", correctOrder: 1 },
        { id: 'b', text: "Detect cup location", correctOrder: 2 },
        { id: 'c', text: "Grasp the cup", correctOrder: 3 },
        { id: 'd', text: "Return to user", correctOrder: 4 }
      ],
      correctSequence: ['a', 'b', 'c', 'd']
    },
    {
      id: 2,
      scenario: "User says: 'Find the red ball and show it to me'",
      question: "Arrange the correct sequence of actions for this command:",
      steps: [
        { id: 'a', text: "Perceive environment to find red ball", correctOrder: 1 },
        { id: 'b', text: "Navigate to ball location", correctOrder: 2 },
        { id: 'c', text: "Grasp the red ball", correctOrder: 3 },
        { id: 'd', text: "Turn towards user", correctOrder: 4 }
      ],
      correctSequence: ['a', 'b', 'c', 'd']
    },
    {
      id: 3,
      scenario: "User says: 'Clean the living room'",
      question: "Arrange the correct sequence of actions for this complex command:",
      steps: [
        { id: 'a', text: "Analyze living room layout", correctOrder: 1 },
        { id: 'b', text: "Detect objects that need repositioning", correctOrder: 2 },
        { id: 'c', text: "Plan path to each object", correctOrder: 3 },
        { id: 'd', text: "Execute cleaning tasks systematically", correctOrder: 4 }
      ],
      correctSequence: ['a', 'b', 'c', 'd']
    }
  ];

  const [currentExercise, setCurrentExercise] = useState(0);

  const handleStepSelect = (stepId) => {
    if (isSubmitted) return;

    if (selectedSteps.includes(stepId)) {
      // Remove step if already selected
      setSelectedSteps(selectedSteps.filter(id => id !== stepId));
    } else {
      // Add step to the end
      setSelectedSteps([...selectedSteps, stepId]);
    }
  };

  const handleSubmit = () => {
    const currentEx = exercises[currentExercise];
    const isCorrect = JSON.stringify(selectedSteps) === JSON.stringify(currentEx.correctSequence);

    setFeedback(isCorrect
      ? 'Correct! You properly sequenced the cognitive planning steps.'
      : `Incorrect. The correct sequence is: ${currentEx.correctSequence.map(id =>
          currentEx.steps.find(s => s.id === id).text
        ).join(' → ')}.`
    );

    const newScore = isCorrect ? score + 1 : score;
    setScore(newScore);
    setIsSubmitted(true);
  };

  const handleNext = () => {
    if (currentExercise < exercises.length - 1) {
      setCurrentExercise(currentExercise + 1);
      resetExercise();
    }
  };

  const handlePrev = () => {
    if (currentExercise > 0) {
      setCurrentExercise(currentExercise - 1);
      resetExercise();
    }
  };

  const resetExercise = () => {
    setSelectedSteps([]);
    setFeedback('');
    setIsSubmitted(false);
  };

  const currentEx = exercises[currentExercise];

  return (
    <div className="planning-exercise-container">
      <h3>Cognitive Planning Exercise</h3>
      <p>Practice breaking down complex commands into logical action sequences using cognitive planning principles.</p>

      <div className="exercise-info">
        <h4>Exercise {currentExercise + 1} of {exercises.length}</h4>
        <p><strong>Scenario:</strong> {currentEx.scenario}</p>
        <p><strong>Task:</strong> {currentEx.question}</p>
      </div>

      <div className="steps-container">
        <div className="available-steps">
          <h4>Available Actions:</h4>
          {currentEx.steps
            .filter(step => !selectedSteps.includes(step.id))
            .map((step, index) => (
              <div
                key={step.id}
                className="step-option"
                onClick={() => handleStepSelect(step.id)}
              >
                {step.text}
              </div>
            ))}
          {currentEx.steps.filter(step => !selectedSteps.includes(step.id)).length === 0 && (
            <p className="no-steps">All steps have been added to your sequence</p>
          )}
        </div>

        <div className="selected-sequence">
          <h4>Your Action Sequence:</h4>
          {selectedSteps.length > 0 ? (
            <ol className="sequence-list">
              {selectedSteps.map((stepId, index) => {
                const step = currentEx.steps.find(s => s.id === stepId);
                return (
                  <li key={stepId} className="sequence-item">
                    {step.text}
                  </li>
                );
              })}
            </ol>
          ) : (
            <p className="no-selection">Click on actions to add them to your sequence</p>
          )}
        </div>
      </div>

      <div className="exercise-actions">
        <button onClick={handleSubmit} disabled={isSubmitted || selectedSteps.length !== currentEx.steps.length}>
          Submit Sequence
        </button>
        {isSubmitted && (
          <button onClick={resetExercise}>
            Try Again
          </button>
        )}
      </div>

      {feedback && (
        <div className={`feedback-section ${isSubmitted ? (feedback.includes('Correct') ? 'success' : 'error') : ''}`}>
          <p>{feedback}</p>
        </div>
      )}

      <div className="exercise-navigation">
        <button onClick={handlePrev} disabled={currentExercise === 0}>
          Previous
        </button>
        <span>Score: {score}/{exercises.length}</span>
        {currentExercise < exercises.length - 1 ? (
          <button onClick={handleNext} disabled={!isSubmitted}>
            Next
          </button>
        ) : (
          <button onClick={() => { setCurrentExercise(0); resetExercise(); }}>
            Restart Exercises
          </button>
        )}
      </div>

      <div className="exercise-instructions">
        <h4>Instructions:</h4>
        <ul>
          <li>Read the scenario and understand the user's goal</li>
          <li>Drag or click actions to arrange them in the correct sequence</li>
          <li>Consider dependencies between actions (e.g., navigate before grasp)</li>
          <li>Submit your sequence to check your cognitive planning skills</li>
        </ul>
        <p><strong>Tip:</strong> Think about what the robot needs to do first, and what must be completed before subsequent actions.</p>
      </div>
    </div>
  );
};

export default PlanningExercise;