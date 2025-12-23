import React, { useState } from 'react';
import './vla-styles.css'; // Import the styles

const PlanningDemo = () => {
  const [command, setCommand] = useState('');
  const [plan, setPlan] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const generatePlan = async () => {
    if (!command.trim()) {
      setError('Please enter a command');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Simulate API call to LLM for planning
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate API delay

      // Generate a sample plan based on the command
      const samplePlan = generateSamplePlan(command);
      setPlan(samplePlan);
    } catch (err) {
      setError('Error generating plan. Please try again.');
      console.error('Planning error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const generateSamplePlan = (command) => {
    // This would be replaced with actual LLM call in real implementation
    const actionSequence = [];

    if (command.toLowerCase().includes('go to') || command.toLowerCase().includes('navigate')) {
      actionSequence.push({
        step: 1,
        action: 'navigate',
        parameters: { location: extractLocation(command) },
        description: `Navigate to ${extractLocation(command)}`
      });
    }

    if (command.toLowerCase().includes('pick up') || command.toLowerCase().includes('grasp')) {
      actionSequence.push({
        step: actionSequence.length + 1,
        action: 'manipulate',
        parameters: { object: extractObject(command) },
        description: `Grasp the ${extractObject(command)}`
      });
    }

    if (command.toLowerCase().includes('find') || command.toLowerCase().includes('look for')) {
      actionSequence.push({
        step: actionSequence.length + 1,
        action: 'perceive',
        parameters: { target: extractObject(command) },
        description: `Detect ${extractObject(command)}`
      });
    }

    // Add a default action if no specific actions were identified
    if (actionSequence.length === 0) {
      actionSequence.push({
        step: 1,
        action: 'understand',
        parameters: { command: command },
        description: `Process command: ${command}`
      });
    }

    return {
      intent: command,
      actionSequence: actionSequence,
      estimatedDuration: actionSequence.length * 10, // Estimated duration in seconds
      requiredCapabilities: ['navigation', 'manipulation', 'perception']
    };
  };

  const extractLocation = (cmd) => {
    // Simple location extraction - in real implementation, use NLP
    const locations = ['kitchen', 'living room', 'bedroom', 'office', 'dining room'];
    for (const loc of locations) {
      if (cmd.toLowerCase().includes(loc)) {
        return loc;
      }
    }
    return 'unknown location';
  };

  const extractObject = (cmd) => {
    // Simple object extraction - in real implementation, use NLP
    const objects = ['cup', 'ball', 'book', 'box', 'chair'];
    for (const obj of objects) {
      if (cmd.toLowerCase().includes(obj)) {
        return obj;
      }
    }
    return 'unknown object';
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      generatePlan();
    }
  };

  return (
    <div className="planning-demo-container">
      <h3>Cognitive Planning Demo</h3>
      <p>Enter a natural language command and see how it gets converted to a robot action plan using LLM-based cognitive planning.</p>

      <div className="input-section">
        <label htmlFor="command-input">Enter Robot Command:</label>
        <input
          id="command-input"
          type="text"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="e.g., 'Go to the kitchen and pick up the red cup'"
          className="command-input"
        />
        <button
          onClick={generatePlan}
          disabled={isLoading}
          className="generate-button"
        >
          {isLoading ? 'Generating Plan...' : 'Generate Plan'}
        </button>
        {error && <div className="error-message">{error}</div>}
      </div>

      {plan && (
        <div className="plan-output">
          <h4>Generated Action Plan:</h4>
          <div className="plan-details">
            <p><strong>Intent:</strong> {plan.intent}</p>
            <p><strong>Estimated Duration:</strong> {plan.estimatedDuration} seconds</p>
            <p><strong>Required Capabilities:</strong> {plan.requiredCapabilities.join(', ')}</p>
          </div>

          <h5>Action Sequence:</h5>
          <ol className="action-sequence">
            {plan.actionSequence.map((action, index) => (
              <li key={index} className="action-item">
                <strong>Step {action.step}:</strong> {action.description}
                <div className="action-params">
                  <em>Action:</em> {action.action} |
                  <em>Parameters:</em> {JSON.stringify(action.parameters)}
                </div>
              </li>
            ))}
          </ol>
        </div>
      )}

      <div className="demo-info">
        <h4>How Cognitive Planning Works:</h4>
        <ol>
          <li>User provides a natural language command</li>
          <li>LLM interprets the command and identifies intent</li>
          <li>Complex tasks are decomposed into simpler actions</li>
          <li>Action sequence is generated with proper dependencies</li>
          <li>Plan is validated for feasibility before execution</li>
        </ol>
        <p><strong>Note:</strong> This demo simulates the planning process. In a real implementation, this would connect to an LLM API for actual cognitive planning.</p>
      </div>
    </div>
  );
};

export default PlanningDemo;