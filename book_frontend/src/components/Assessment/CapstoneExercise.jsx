import React, { useState } from 'react';
import './assessment-styles.css'; // Import assessment styles

const CapstoneExercise = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [userSelections, setUserSelections] = useState({});
  const [feedback, setFeedback] = useState('');
  const [isCompleted, setIsCompleted] = useState(false);
  const [score, setScore] = useState(0);

  const capstoneChallenges = [
    {
      id: 1,
      title: "Integrated System Design",
      question: "Which components must be integrated to create a complete VLA system?",
      options: [
        { id: 'a', text: "Voice recognition + Cognitive planning", correct: false },
        { id: 'b', text: "Voice recognition + Robot execution", correct: false },
        { id: 'c', text: "Voice recognition + Cognitive planning + Robot execution", correct: true },
        { id: 'd', text: "Cognitive planning + Robot execution", correct: false }
      ],
      explanation: "A complete VLA system requires all three components: Voice recognition for input, cognitive planning for processing, and robot execution for output."
    },
    {
      id: 2,
      title: "Voice Command Processing Pipeline",
      question: "What is the correct sequence of processing a voice command?",
      options: [
        { id: 'a', text: "Text → Audio → Action", correct: false },
        { id: 'b', text: "Action → Audio → Text", correct: false },
        { id: 'c', text: "Audio → Text → Action", correct: true },
        { id: 'd', text: "Text → Action → Audio", correct: false }
      ],
      explanation: "The correct sequence is Audio (voice) → Text (transcription) → Action (robot execution)."
    },
    {
      id: 3,
      title: "Cognitive Planning with LLMs",
      question: "What is the role of LLMs in cognitive planning?",
      options: [
        { id: 'a', text: "To control the robot's physical movements", correct: false },
        { id: 'b', text: "To interpret natural language goals and generate action plans", correct: true },
        { id: 'c', text: "To store robot operating procedures", correct: false },
        { id: 'd', text: "To replace traditional control systems entirely", correct: false }
      ],
      explanation: "LLMs interpret natural language goals and generate detailed action plans for the robot to execute."
    },
    {
      id: 4,
      title: "System Safety Considerations",
      question: "Which safety measures should be implemented in a VLA system?",
      options: [
        { id: 'a', text: "Validate commands before execution", correct: true },
        { id: 'b', text: "Include emergency stop functionality", correct: true },
        { id: 'c', text: "Ensure movements are within safe parameters", correct: true },
        { id: 'd', text: "All of the above", correct: true }
      ],
      explanation: "All of these safety measures are essential for safe VLA system operation."
    },
    {
      id: 5,
      title: "Capstone Integration Challenge",
      question: "How would you implement a command like 'Go to the kitchen, find the red cup, and bring it to me'?",
      options: [
        { id: 'a', text: "Single complex action", correct: false },
        { id: 'b', text: "Sequence: Navigate → Perceive → Manipulate → Navigate", correct: true },
        { id: 'c', text: "Parallel processing of all tasks", correct: false },
        { id: 'd', text: "Task decomposition with error handling", correct: true }
      ],
      explanation: "This requires task decomposition into a sequence of actions with proper error handling for each step."
    }
  ];

  const handleOptionSelect = (optionId) => {
    if (isCompleted) return;

    const newSelections = {
      ...userSelections,
      [currentStep]: optionId
    };
    setUserSelections(newSelections);
  };

  const handleNext = () => {
    if (currentStep < capstoneChallenges.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = () => {
    let correctAnswers = 0;

    capstoneChallenges.forEach((challenge, index) => {
      const userAnswer = userSelections[index];
      if (userAnswer) {
        const selectedOption = challenge.options.find(opt => opt.id === userAnswer);
        if (selectedOption && selectedOption.correct) {
          correctAnswers++;
        }
      }
    });

    const finalScore = Math.round((correctAnswers / capstoneChallenges.length) * 100);
    setScore(finalScore);
    setIsCompleted(true);

    if (finalScore >= 80) {
      setFeedback(`Excellent work! You scored ${finalScore}%. You've mastered the VLA integration concepts.`);
    } else if (finalScore >= 60) {
      setFeedback(`Good job! You scored ${finalScore}%. You understand the core VLA concepts but could review some areas.`);
    } else {
      setFeedback(`You scored ${finalScore}%. Review the VLA concepts and try again.`);
    }
  };

  const handleRestart = () => {
    setCurrentStep(0);
    setUserSelections({});
    setFeedback('');
    setIsCompleted(false);
    setScore(0);
  };

  const currentChallenge = capstoneChallenges[currentStep];
  const selectedOption = userSelections[currentStep];

  return (
    <div className="capstone-exercise-container">
      <h3>Capstone Integration Exercise</h3>
      <p>Test your comprehensive understanding of Vision-Language-Action systems integration.</p>

      <div className="progress-bar">
        <div className="progress">
          <div
            className="progress-fill"
            style={{ width: `${((currentStep + 1) / capstoneChallenges.length) * 100}%` }}
          />
        </div>
        <span>Question {currentStep + 1} of {capstoneChallenges.length}</span>
      </div>

      <div className="challenge-content">
        <h4>{currentChallenge.title}</h4>
        <p>{currentChallenge.question}</p>

        <div className="options-container">
          {currentChallenge.options.map((option) => (
            <div
              key={option.id}
              className={`option-item ${selectedOption === option.id ? 'selected' : ''}`}
              onClick={() => handleOptionSelect(option.id)}
            >
              <div className="option-radio">
                {selectedOption === option.id ? '●' : '○'}
              </div>
              <div className="option-text">
                {option.text}
              </div>
            </div>
          ))}
        </div>

        {selectedOption && !isCompleted && (
          <div className="selected-feedback">
            <p>You selected: {currentChallenge.options.find(opt => opt.id === selectedOption)?.text}</p>
          </div>
        )}
      </div>

      {isCompleted && currentStep === capstoneChallenges.length - 1 && (
        <div className="final-results">
          <h4>Final Results</h4>
          <p className="score">Your Score: {score}%</p>
          <p className="feedback">{feedback}</p>

          <div className="detailed-review">
            <h5>Detailed Review:</h5>
            {capstoneChallenges.map((challenge, index) => {
              const userAnswer = userSelections[index];
              const selectedOption = challenge.options.find(opt => opt.id === userAnswer);
              const isCorrect = selectedOption ? selectedOption.correct : false;

              return (
                <div key={challenge.id} className="review-item">
                  <p><strong>Question {index + 1}:</strong> {isCorrect ? '✓ Correct' : '✗ Incorrect'}</p>
                  {!isCorrect && selectedOption && (
                    <p className="explanation">{challenge.explanation}</p>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="navigation-controls">
        <button onClick={handlePrev} disabled={currentStep === 0 || isCompleted}>
          Previous
        </button>

        {!isCompleted ? (
          currentStep < capstoneChallenges.length - 1 ? (
            <button onClick={handleNext} disabled={!selectedOption}>
              Next
            </button>
          ) : (
            <button onClick={handleSubmit} disabled={!selectedOption}>
              Submit Answers
            </button>
          )
        ) : (
          <button onClick={handleRestart}>
            Restart Exercise
          </button>
        )}
      </div>

      <div className="exercise-instructions">
        <h4>About This Capstone Exercise:</h4>
        <p>This exercise integrates all concepts from the VLA module:</p>
        <ul>
          <li><strong>Vision:</strong> Object recognition and environment perception</li>
          <li><strong>Language:</strong> Natural language understanding and LLM-based planning</li>
          <li><strong>Action:</strong> Robot execution and control systems</li>
        </ul>
        <p>Successful completion demonstrates your understanding of how these components work together in an autonomous humanoid system.</p>
      </div>
    </div>
  );
};

export default CapstoneExercise;