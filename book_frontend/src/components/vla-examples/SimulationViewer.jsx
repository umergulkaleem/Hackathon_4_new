import React, { useState, useEffect } from 'react';
import './vla-styles.css'; // Import the styles

const SimulationViewer = () => {
  const [selectedScenario, setSelectedScenario] = useState('navigation');
  const [isRunning, setIsRunning] = useState(false);
  const [robotPosition, setRobotPosition] = useState({ x: 50, y: 50 });
  const [objects, setObjects] = useState([
    { id: 1, type: 'cup', x: 200, y: 150, label: 'Red Cup' },
    { id: 2, type: 'ball', x: 300, y: 250, label: 'Blue Ball' },
    { id: 3, type: 'box', x: 150, y: 300, label: 'Cardboard Box' }
  ]);
  const [path, setPath] = useState([]);
  const [status, setStatus] = useState('Ready');

  const scenarios = {
    navigation: {
      name: 'Navigation Demo',
      description: 'Simulate robot navigation to different locations',
      actions: ['Go to Kitchen', 'Go to Living Room', 'Go to Bedroom']
    },
    manipulation: {
      name: 'Manipulation Demo',
      description: 'Simulate robot manipulation tasks',
      actions: ['Pick up Red Cup', 'Grasp Blue Ball', 'Move Cardboard Box']
    },
    perception: {
      name: 'Perception Demo',
      description: 'Simulate robot object recognition',
      actions: ['Detect All Objects', 'Find Red Cup', 'Locate Blue Ball']
    }
  };

  const environmentMap = {
    kitchen: { x: 350, y: 100 },
    living: { x: 100, y: 350 },
    bedroom: { x: 350, y: 350 }
  };

  const runScenario = (action) => {
    if (isRunning) return;

    setIsRunning(true);
    setStatus(`Running: ${action}`);

    // Simulate robot movement based on scenario
    if (selectedScenario === 'navigation') {
      simulateNavigation(action);
    } else if (selectedScenario === 'manipulation') {
      simulateManipulation(action);
    } else if (selectedScenario === 'perception') {
      simulatePerception(action);
    }
  };

  const simulateNavigation = (action) => {
    let targetX, targetY;

    if (action.includes('Kitchen')) {
      targetX = 350; targetY = 100;
    } else if (action.includes('Living')) {
      targetX = 100; targetY = 350;
    } else if (action.includes('Bedroom')) {
      targetX = 350; targetY = 350;
    } else {
      // Default: move to center
      targetX = 250; targetY = 200;
    }

    // Calculate path (simplified as straight line)
    const steps = 50; // Number of steps for smooth movement
    const pathPoints = [];

    for (let i = 0; i <= steps; i++) {
      const progress = i / steps;
      const x = robotPosition.x + (targetX - robotPosition.x) * progress;
      const y = robotPosition.y + (targetY - robotPosition.y) * progress;
      pathPoints.push({ x, y });
    }

    setPath(pathPoints);

    // Animate the movement
    let step = 0;
    const interval = setInterval(() => {
      if (step < pathPoints.length) {
        setRobotPosition(pathPoints[step]);
        step++;
      } else {
        clearInterval(interval);
        setStatus(`Arrived at destination. ${action} completed.`);
        setIsRunning(false);
      }
    }, 50); // Update every 50ms for smooth animation
  };

  const simulateManipulation = (action) => {
    const objectName = action.split(' ')[2]; // Extract object name from "Pick up X"
    const targetObject = objects.find(obj => obj.label.toLowerCase().includes(objectName.toLowerCase()));

    if (targetObject) {
      // Move robot to object location
      const steps = 30;
      const pathPoints = [];

      for (let i = 0; i <= steps; i++) {
        const progress = i / steps;
        const x = robotPosition.x + (targetObject.x - robotPosition.x) * progress;
        const y = robotPosition.y + (targetObject.y - robotPosition.y) * progress;
        pathPoints.push({ x, y });
      }

      setPath(pathPoints);

      let step = 0;
      const interval = setInterval(() => {
        if (step < pathPoints.length) {
          setRobotPosition(pathPoints[step]);
          step++;
        } else {
          clearInterval(interval);
          setStatus(`${action} completed. Object picked up.`);
          setIsRunning(false);
        }
      }, 50);
    }
  };

  const simulatePerception = (action) => {
    setStatus(`Perception running: ${action}`);

    // Simulate perception by highlighting objects
    setTimeout(() => {
      setStatus(`Perception completed. Found ${objects.length} objects.`);
      setIsRunning(false);
    }, 3000);
  };

  const resetSimulation = () => {
    setRobotPosition({ x: 50, y: 50 });
    setPath([]);
    setStatus('Ready');
    setIsRunning(false);
  };

  return (
    <div className="simulation-viewer-container">
      <h3>Simulation Viewer</h3>
      <p>Visualize and simulate robot behavior for different VLA scenarios.</p>

      <div className="simulation-controls">
        <div className="scenario-selector">
          <label>Select Scenario:</label>
          <select
            value={selectedScenario}
            onChange={(e) => setSelectedScenario(e.target.value)}
            disabled={isRunning}
          >
            {Object.entries(scenarios).map(([key, scenario]) => (
              <option key={key} value={key}>{scenario.name}</option>
            ))}
          </select>
        </div>

        <div className="scenario-info">
          <h4>{scenarios[selectedScenario].name}</h4>
          <p>{scenarios[selectedScenario].description}</p>
        </div>

        <div className="action-buttons">
          {scenarios[selectedScenario].actions.map((action, index) => (
            <button
              key={index}
              onClick={() => runScenario(action)}
              disabled={isRunning}
              className="action-button"
            >
              {action}
            </button>
          ))}
        </div>

        <button
          onClick={resetSimulation}
          disabled={isRunning}
          className="reset-button"
        >
          Reset Simulation
        </button>
      </div>

      <div className="simulation-status">
        <div className="status-indicator">
          Status: <strong>{status}</strong>
        </div>
      </div>

      <div className="simulation-canvas-container">
        <h4>Simulation Environment</h4>
        <div className="simulation-canvas">
          {/* Robot */}
          <div
            className="robot"
            style={{
              left: `${robotPosition.x}px`,
              top: `${robotPosition.y}px`,
              backgroundColor: isRunning ? '#ff6b6b' : '#4ec9b0'
            }}
          >
            🤖
          </div>

          {/* Path */}
          {path.map((point, index) => (
            <div
              key={index}
              className="path-point"
              style={{
                left: `${point.x}px`,
                top: `${point.y}px`,
              }}
            />
          ))}

          {/* Objects */}
          {objects.map((obj) => (
            <div
              key={obj.id}
              className={`object object-${obj.type}`}
              style={{
                left: `${obj.x}px`,
                top: `${obj.y}px`,
              }}
            >
              {obj.type === 'cup' ? '☕' : obj.type === 'ball' ? '⚽' : '📦'}
              <div className="object-label">{obj.label}</div>
            </div>
          ))}

          {/* Environment markers */}
          <div className="environment-marker" style={{ left: '350px', top: '100px' }}>
            🏹 Kitchen
          </div>
          <div className="environment-marker" style={{ left: '100px', top: '350px' }}>
            🛋️ Living Room
          </div>
          <div className="environment-marker" style={{ left: '350px', top: '350px' }}>
            🛏️ Bedroom
          </div>
        </div>
      </div>

      <div className="demo-info">
        <h4>About Simulation:</h4>
        <p>This simulation demonstrates how a robot might navigate, manipulate objects, and perceive its environment in response to voice commands.</p>
        <ul>
          <li><strong>Navigation:</strong> Robot moves to specified locations</li>
          <li><strong>Manipulation:</strong> Robot picks up and moves objects</li>
          <li><strong>Perception:</strong> Robot detects and identifies objects</li>
        </ul>
        <p><strong>Note:</strong> This is a simplified simulation. Real robot simulation would use more sophisticated physics and environment modeling.</p>
      </div>
    </div>
  );
};

export default SimulationViewer;