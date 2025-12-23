import React, { useState } from 'react';
import './assessment-styles.css'; // Import assessment exercise styles

const VoiceCommandExercise = () => {
  const [userInput, setUserInput] = useState('');
  const [result, setResult] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const exercises = [
    {
      id: 1,
      description: "Convert the voice command 'Move forward 2 meters' to a structured robot command",
      expectedAction: "move",
      expectedParams: { direction: "forward", distance: 2.0 }
    },
    {
      id: 2,
      description: "Convert the voice command 'Turn left 90 degrees' to a structured robot command",
      expectedAction: "turn",
      expectedParams: { direction: "left", angle: 90 }
    },
    {
      id: 3,
      description: "Convert the voice command 'Stop the robot immediately' to a structured robot command",
      expectedAction: "stop",
      expectedParams: {}
    }
  ];

  const [currentExercise, setCurrentExercise] = useState(0);

  const handleSubmit = () => {
    // Parse user input (simplified parsing for demo)
    const input = userInput.toLowerCase();
    let detectedAction = '';
    let detectedParams = {};

    if (input.includes('move') || input.includes('forward') || input.includes('backward')) {
      detectedAction = 'move';
      detectedParams.direction = input.includes('forward') ? 'forward' : 'backward';
      const distanceMatch = input.match(/(\d+(?:\.\d+)?)\s*(meters|meter|m)/);
      if (distanceMatch) {
        detectedParams.distance = parseFloat(distanceMatch[1]);
      }
    } else if (input.includes('turn') || input.includes('left') || input.includes('right')) {
      detectedAction = 'turn';
      detectedParams.direction = input.includes('left') ? 'left' : 'right';
      const angleMatch = input.match(/(\d+(?:\.\d+)?)\s*(degrees|degree|deg)/);
      if (angleMatch) {
        detectedParams.angle = parseFloat(angleMatch[1]);
      }
    } else if (input.includes('stop')) {
      detectedAction = 'stop';
    }

    // Check if the action matches expected
    const expected = exercises[currentExercise];
    const isCorrect = detectedAction === expected.expectedAction;

    setResult({
      userAction: detectedAction,
      userParams: detectedParams,
      expectedAction: expected.expectedAction,
      expectedParams: expected.expectedParams,
      isCorrect
    });

    setFeedback(isCorrect
      ? 'Correct! You successfully parsed the voice command.'
      : 'Incorrect. Try to identify the action type and parameters more carefully.'
    );

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
    setUserInput('');
    setResult(null);
    setFeedback('');
    setIsSubmitted(false);
  };

  const currentEx = exercises[currentExercise];

  return (
    <div className="voice-command-exercise-container">
      <h3>Voice Command Parsing Exercise</h3>
      <p>Practice converting natural language voice commands into structured robot commands.</p>

      <div className="exercise-info">
        <h4>Exercise {currentExercise + 1} of {exercises.length}</h4>
        <p><strong>Task:</strong> {currentEx.description}</p>
      </div>

      <div className="exercise-input">
        <label htmlFor="voice-command-input">Enter the structured command format:</label>
        <input
          id="voice-command-input"
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="e.g., move forward 2 meters, turn left 90 degrees, stop"
          disabled={isSubmitted}
        />
        <button onClick={handleSubmit} disabled={isSubmitted || !userInput.trim()}>
          Submit Answer
        </button>
      </div>

      {result && (
        <div className={`result-section ${result.isCorrect ? 'correct' : 'incorrect'}`}>
          <h4>Result:</h4>
          <div className="result-details">
            <p><strong>Your Parse:</strong> Action: {result.userAction}, Params: {JSON.stringify(result.userParams)}</p>
            <p><strong>Expected:</strong> Action: {result.expectedAction}, Params: {JSON.stringify(result.expectedParams)}</p>
            <p className={`feedback ${result.isCorrect ? 'success' : 'error'}`}>
              {feedback}
            </p>
          </div>
        </div>
      )}

      <div className="exercise-navigation">
        <button onClick={handlePrev} disabled={currentExercise === 0}>
          Previous
        </button>
        <span>Exercise {currentExercise + 1} of {exercises.length}</span>
        {currentExercise < exercises.length - 1 ? (
          <button onClick={handleNext} disabled={!isSubmitted}>
            Next
          </button>
        ) : (
          <button onClick={resetExercise} disabled={!isSubmitted}>
            Restart Exercises
          </button>
        )}
      </div>

      <div className="exercise-instructions">
        <h4>Instructions:</h4>
        <ul>
          <li>Listen to or read the voice command</li>
          <li>Identify the main action (move, turn, stop, etc.)</li>
          <li>Determine the parameters (direction, distance, angle, etc.)</li>
          <li>Enter the structured command in the input field</li>
        </ul>
        <p><strong>Tip:</strong> Focus on extracting the core action and its parameters from the natural language.</p>
      </div>
    </div>
  );
};

export default VoiceCommandExercise;