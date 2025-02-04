import React, { useState, useRef, useEffect } from "react";
import "./AudioRecorder.css"; // Import CSS file for styling

const AudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioFile, setAudioFile] = useState(null);
  const [uploadFile, setUploadFile] = useState(null);
  const [transcription, setTranscription] = useState("");
  const [report, setReport] = useState(""); 
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // 🎤 Start Recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
        const audioUrl = URL.createObjectURL(audioBlob);
        setAudioFile(audioUrl);
        setUploadFile(new File([audioBlob], "recorded_audio.wav", { type: "audio/wav" }));
        audioChunksRef.current = []; // Reset chunks
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setError(null);
    } catch (err) {
      console.error("Microphone access error:", err);
      setError("Error accessing the microphone: " + err.message);
    }
  };

  // ⏹ Stop Recording
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // 📤 Upload Audio and Get Transcription
  const uploadAndTranscribe = async () => {
    if (!uploadFile) {
      setError("Please record or upload an audio file first!");
      return;
    }
  
    setIsLoading(true);
    setError(null);
  
    const formData = new FormData();
    formData.append("file", uploadFile);
  
    try {
      // Upload the audio file and get the transcription + report
      const response = await fetch("http://127.0.0.1:8000/transcribe/", {
        method: "POST",
        body: formData,
        headers: {
          "Role": "doctor",  // Pass the role dynamically if needed
        },
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Something went wrong.");
      }
  
      const data = await response.json();
  
      // Set the transcription and report in the state
      setTranscription(data.transcription);
      setReport(data.report);  // Ensure this line is present
      console.log("Transcription:", data.transcription);
      console.log("Report:", data.report);
  
    } catch (error) {
      console.error("Error:", error);
      setError(error.message || "Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };
  
  // 🎵 Handle File Selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const audioUrl = URL.createObjectURL(file);
      setUploadFile(file);
      setAudioFile(audioUrl);
    }
  };

  return (
    <div className="container">
      <h1 className="main-heading">DocGenie</h1>
      <h2 className="sub-heading">Medical Report Generator</h2>

      {error && <p className="error-message">{error}</p>}

      <div className="controls">
        {!isRecording ? (
          <button className="record-button" onClick={startRecording}>
            🎤 Start Recording
          </button>
        ) : (
          <button className="stop-button" onClick={stopRecording}>
            ⏹ Stop Recording
          </button>
        )}
      </div>

      <div className="upload-section">
        <h3>Or Upload Pre-recorded Audio</h3>
        <input type="file" accept="audio/*" onChange={handleFileChange} className="file-input" />
      </div>

      {audioFile && (
        <div className="audio-preview">
          <h3>Audio Preview</h3>
          <audio controls src={audioFile} className="audio-player" />
          <button className="upload-button" onClick={uploadAndTranscribe} disabled={isLoading}>
            {isLoading ? "Processing..." : "Upload & Transcribe"}
          </button>
        </div>
      )}

      {transcription && (
        <div className="transcription-section">
          <h3>Transcription</h3>
          <p className="transcription-text">{transcription}</p>
        </div>
      )}
       {/* Generated Report */}
      {report && (
         <div>
          <h3>Medical Report</h3>
          <p>{report}</p>
        </div>
      )}
  </div>

  );
};

export default AudioRecorder;   