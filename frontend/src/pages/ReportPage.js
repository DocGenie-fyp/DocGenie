import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./ReportPage.css"; // Import CSS file for styling

const ReportPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { report, transcription } = location.state || {};

  return (
    <div className="container">
      <h1 className="main-heading">Medical Report</h1>

      {transcription && (
        <div className="transcription-section">
          <h3>Transcription</h3>
          <p className="transcription-text">{transcription}</p>
        </div>
      )}

      {report ? (
        <div className="report-section">
          <h3>Generated Medical Report</h3>
          <p className="report-text">{report}</p>
        </div>
      ) : (
        <p className="error-message">No report available. Please upload and process an audio file first.</p>
      )}

      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
    </div>
  );
};

export default ReportPage;
