import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import styles from './assessment.module.css';

// Generic Assessment Component for multiple choice questions
const AssessmentComponent = ({ question, options, correctAnswer, explanation }) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const handleSubmit = (option) => {
    if (!submitted) {
      setSelectedOption(option);
      const correct = option === correctAnswer;
      setIsCorrect(correct);
      setSubmitted(true);
    }
  };

  const resetQuiz = () => {
    setSelectedOption(null);
    setSubmitted(false);
    setIsCorrect(false);
  };

  return (
    <div className={styles.assessmentContainer}>
      <h4>{question}</h4>
      <div className={styles.optionsContainer}>
        {options.map((option, index) => (
          <div
            key={index}
            className={`${styles.optionItem} ${
              submitted && option === correctAnswer ? styles.correct :
              submitted && option === selectedOption && option !== correctAnswer ? styles.incorrect : ''
            }`}
            onClick={() => !submitted && handleSubmit(option)}
          >
            <div className={styles.optionRadio}>
              {submitted ? (
                option === correctAnswer ? '✓' :
                (option === selectedOption ? '✗' : '')
              ) : (
                `${String.fromCharCode(65 + index)}.`
              )}
            </div>
            <div className={styles.optionText}>
              {option}
            </div>
          </div>
        ))}
      </div>

      {submitted && (
        <div className={`${styles.feedbackSection} ${isCorrect ? styles.success : styles.error}`}>
          <p><strong>{isCorrect ? 'Correct!' : 'Incorrect.'}</strong></p>
          <div className={styles.explanation}>
            <p><strong>Explanation:</strong> {explanation}</p>
          </div>
          <button onClick={resetQuiz} className={styles.resetButton}>
            Try Again
          </button>
        </div>
      )}
    </div>
  );
};

// Wrapper to handle SSR properly
const Assessment = (props) => {
  return (
    <BrowserOnly>
      {() => <AssessmentComponent {...props} />}
    </BrowserOnly>
  );
};

export default Assessment;