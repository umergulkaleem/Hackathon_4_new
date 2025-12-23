import React, { useState } from 'react';
import './vla-styles.css'; // Import the styles

const IntegratedDemo = () => {
  const [command, setCommand] = useState('');
  const [systemState, setSystemState] = useState('idle');
  const [transcript, setTranscript] = useState('');
  const [plan, setPlan] = useState(null);
  const [executionLog, setExecutionLog] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const processCommand = async () => {
    if (!command.trim()) return;

    setIsLoading(true);
    setExecutionLog([]);
    setSystemState('processing');

    try {
      // Step 1: Simulate voice recognition
      await new Promise(resolve => setTimeout(resolve, 1000));
      setTranscript(command); // In demo, we just echo the input
      addLog('Voice Recognition: Command received and transcribed');

      // Step 2: Simulate cognitive planning
      await new Promise(resolve => setTimeout(resolve, 1500));
      const samplePlan = generateSamplePlan(command);
      setPlan(samplePlan);
      addLog('Cognitive Planning: Action plan generated');
      setSystemState('planning');

      // Step 3: Simulate execution
      await executePlan(samplePlan);
      addLog('Execution: Plan completed successfully');
      setSystemState('completed');
    } catch (error) {
      addLog(`Error: ${error.message}`);
      setSystemState('error');
    } finally {
      setIsLoading(false);
    }
  };

  const generateSamplePlan = (command) => {
    // Generate a sample plan based on the command
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
      estimatedDuration: actionSequence.length * 10,
      requiredCapabilities: ['navigation', 'manipulation', 'perception']
    };
  };

  const extractLocation = (cmd) => {
    const locations = ['kitchen', 'living room', 'bedroom', 'office', 'dining room'];
    for (const loc of locations) {
      if (cmd.toLowerCase().includes(loc)) {
        return loc;
      }
    }
    return 'unknown location';
  };

  const extractObject = (cmd) => {
    const objects = ['cup', 'ball', 'book', 'box', 'chair'];
    for (const obj of objects) {
      if (cmd.toLowerCase().includes(obj)) {
        return obj;
      }
    }
    return 'unknown object';
  };

  const executePlan = async (plan) => {
    for (const action of plan.actionSequence) {
      addLog(`Executing: ${action.description}`);
      setSystemState(`executing-${action.step}`);

      // Simulate action execution time
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  };

  const addLog = (message) => {
    const timestamp = new Date().toLocaleTimeString();
    setExecutionLog(prev => [...prev, `[${timestamp}] ${message}`]);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      processCommand();
    }
  };

  const getStatusColor = () => {
    switch (systemState) {
      case 'processing': return '#007acc';
      case 'planning': return '#ffc107';
      case 'completed': return '#28a745';
      case 'error': return '#dc3545';
      default: return '#6c757d';
    }
  };

  return (
    <div className="integrated-demo-container">
      <h3>Integrated VLA System Demo</h3>
      <p>Experience the complete Vision-Language-Action pipeline: Voice recognition, Cognitive Planning, and Robot Execution.</p>

      <div className="system-status">
        <div className="status-indicator" style={{ backgroundColor: getStatusColor() }}>
          System Status: <strong>{systemState}</strong>
        </div>
      </div>

      <div className="input-section">
        <label htmlFor="vla-command-input">Enter Voice Command:</label>
        <input
          id="vla-command-input"
          type="text"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="e.g., 'Go to the kitchen and pick up the red cup'"
          className="command-input"
          disabled={isLoading}
        />
        <button
          onClick={processCommand}
          disabled={isLoading}
          className="process-button"
        >
          {isLoading ? 'Processing...' : 'Process Command'}
        </button>
      </div>

      <div className="vla-pipeline">
        <div className="pipeline-stage">
          <h4>🗣️ Voice Recognition</h4>
          <div className="stage-content">
            {transcript ? (
              <div className="transcript-output">{transcript}</div>
            ) : (
              <div className="stage-placeholder">Waiting for voice input...</div>
            )}
          </div>
        </div>

        <div className="pipeline-stage">
          <h4>🧠 Cognitive Planning</h4>
          <div className="stage-content">
            {plan ? (
              <div>
                <p><strong>Intent:</strong> {plan.intent}</p>
                <p><strong>Actions:</strong> {plan.actionSequence.length}</p>
              </div>
            ) : (
              <div className="stage-placeholder">Generating plan...</div>
            )}
          </div>
        </div>

        <div className="pipeline-stage">
          <h4>🤖 Robot Execution</h4>
          <div className="stage-content">
            <div className="execution-status">
              {plan ? (
                <ol>
                  {plan.actionSequence.map((action, index) => (
                    <li key={index} className={systemState.includes(`executing-${action.step}`) ? 'executing' : ''}>
                      {action.description}
                    </li>
                  ))}
                </ol>
              ) : (
                <div className="stage-placeholder">Waiting for execution...</div>
              )}
            </div>
          </div>
        </div>
      </div>

      {executionLog.length > 0 && (
        <div className="execution-log">
          <h4>Execution Log:</h4>
          <div className="log-content">
            {executionLog.map((log, index) => (
              <div key={index} className="log-entry">{log}</div>
            ))}
          </div>
        </div>
      )}

      <div className="demo-info">
        <h4>Complete VLA Pipeline:</h4>
        <ol>
          <li><strong>Voice Recognition:</strong> Converting speech to text</li>
          <li><strong>Language Processing:</strong> Understanding the command intent</li>
          <li><strong>Cognitive Planning:</strong> Generating action sequences</li>
          <li><strong>Robot Execution:</strong> Performing the physical actions</li>
        </ol>
        <p><strong>Note:</strong> This demo simulates the complete VLA pipeline. In a real implementation, this would connect to actual voice recognition, LLM, and robot systems.</p>
      </div>
    </div>
  );
};

export default IntegratedDemo;