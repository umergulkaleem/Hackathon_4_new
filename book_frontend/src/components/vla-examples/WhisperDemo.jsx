import React, { useState, useRef } from 'react';
import './vla-styles.css'; // Import the styles

const WhisperDemo = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await sendAudioToWhisper(audioBlob);
        // Stop all tracks to turn off microphone
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setTranscript('');
      setResult('');
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const sendAudioToWhisper = async (audioBlob) => {
    setIsLoading(true);
    try {
      // In a real implementation, you would send the audio to OpenAI Whisper API
      // For this demo, we'll simulate the API response
      await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API delay

      // Simulated response - in real implementation, this would come from Whisper API
      const simulatedTranscript = "This is a simulated transcription of your voice command. In a real implementation, this would be the actual text from Whisper API.";
      setTranscript(simulatedTranscript);

      // Simulate processing the command
      await processCommand(simulatedTranscript);
    } catch (error) {
      console.error('Error processing audio:', error);
      setResult('Error processing audio. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const processCommand = async (command) => {
    // Simulate processing the voice command
    await new Promise(resolve => setTimeout(resolve, 1000));
    setResult(`Command "${command}" would be processed by the robot in a real implementation.`);
  };

  return (
    <div className="whisper-demo-container">
      <h3>OpenAI Whisper Demo</h3>
      <p>Click the button below to start speaking. Your voice will be converted to text using OpenAI Whisper technology.</p>

      <div className="recording-controls">
        <button
          className={`record-button ${isRecording ? 'recording' : ''}`}
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isLoading}
        >
          {isRecording ? '⏹ Stop Recording' : '🎤 Start Recording'}
        </button>

        {isLoading && <div className="loading-indicator">Processing audio...</div>}
      </div>

      {transcript && (
        <div className="transcript-section">
          <h4>Transcript:</h4>
          <div className="transcript-output">
            {transcript}
          </div>
        </div>
      )}

      {result && (
        <div className="result-section">
          <h4>Result:</h4>
          <div className="result-output">
            {result}
          </div>
        </div>
      )}

      <div className="demo-info">
        <h4>How it works:</h4>
        <ol>
          <li>Click "Start Recording" and speak your command</li>
          <li>Your voice is captured and sent to OpenAI Whisper API</li>
          <li>Whisper converts your speech to text</li>
          <li>The text command is processed by the robot system</li>
        </ol>
        <p><strong>Note:</strong> This is a demonstration interface. In a real implementation, you would need to configure your OpenAI API key and handle the actual API calls.</p>
      </div>
    </div>
  );
};

export default WhisperDemo;