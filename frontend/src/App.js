import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ============================================================================
// TRANSITION COMPONENTS
// ============================================================================

const PageTransition = ({ children, isVisible }) => {
  return (
    <div className={`page-transition ${isVisible ? 'fade-in' : 'fade-out'}`}>
      {children}
    </div>
  );
};

const BridgeTransition = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState("INITIALIZING...");
  const [glitchActive, setGlitchActive] = useState(true);

  const messages = [
    "INITIALIZING RELOCATION MATRIX...",
    "SCANNING REMOTE OPPORTUNITIES...", 
    "CONNECTING TO THRIVE OS...",
    "WELCOME TO YOUR NEW LIFE."
  ];

  useEffect(() => {
    let messageIndex = 0;
    const messageInterval = setInterval(() => {
      if (messageIndex < messages.length) {
        setMessage(messages[messageIndex]);
        messageIndex++;
      }
    }, 700);

    const glitchInterval = setInterval(() => {
      setGlitchActive(prev => !prev);
    }, 200);

    const redirectTimer = setTimeout(() => {
      navigate('/thrive-os');
    }, 3500);

    return () => {
      clearInterval(messageInterval);
      clearInterval(glitchInterval);
      clearTimeout(redirectTimer);
    };
  }, [navigate]);

  return (
    <div className="bridge-container">
      <div className="noir-overlay"></div>
      <div className={`glitch-text ${glitchActive ? 'glitch-active' : ''}`}>
        {message}
      </div>
      <div className="scanning-lines"></div>
    </div>
  );
};

// ============================================================================
// MAIN PAGES
// ============================================================================

const RelocateDashboard = () => {
  const navigate = useNavigate();
  const [locations, setLocations] = useState([]);
  const [searchData, setSearchData] = useState({
    current_location: "",
    target_cities: [],
    budget_range: { min: 2000, max: 5000 }
  });

  const featuredLocations = [
    { name: "Phoenix, AZ", score: 8.2, highlight: "Low cost, tech growth" },
    { name: "Austin, TX", score: 9.1, highlight: "Thriving startup scene" },
    { name: "Peak District, UK", score: 9.2, highlight: "Remote-first culture" }
  ];

  const handleLocationSearch = async () => {
    if (!searchData.current_location) return;
    
    try {
      const response = await axios.post(`${API}/search-locations`, {
        user_id: "user_001",
        ...searchData,
        preferences: { climate: "moderate", cost_of_living: "medium" }
      });
      console.log("Search created:", response.data);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  const initiateTransition = () => {
    navigate('/bridge');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="logo-section">
          <h1 className="main-title">RELOCATE<span className="accent">ME</span></h1>
          <p className="subtitle">MISSION: PHOENIX ➔ PEAK DISTRICT</p>
        </div>
        <div className="status-indicator">
          <span className="status-dot"></span>
          <span>SYSTEM OPERATIONAL</span>
        </div>
      </header>

      <main className="dashboard-main">
        <section className="hero-section">
          <div className="hero-content">
            <h2 className="hero-title">Your Cinematic Relocation Journey</h2>
            <p className="hero-description">
              Discover the perfect location for your remote career. Our AI analyzes 
              thousands of data points to match you with opportunities that align 
              with your lifestyle and professional goals.
            </p>
          </div>
        </section>

        <section className="search-section">
          <div className="search-form">
            <h3>Begin Your Location Search</h3>
            <div className="form-grid">
              <input
                type="text"
                placeholder="Current Location"
                value={searchData.current_location}
                onChange={(e) => setSearchData({...searchData, current_location: e.target.value})}
                className="location-input"
              />
              <input
                type="text"
                placeholder="Target Cities (comma separated)"
                onChange={(e) => setSearchData({
                  ...searchData, 
                  target_cities: e.target.value.split(',').map(s => s.trim())
                })}
                className="location-input"
              />
              <div className="budget-range">
                <label>Budget Range</label>
                <div className="range-inputs">
                  <input
                    type="number"
                    placeholder="Min"
                    value={searchData.budget_range.min}
                    onChange={(e) => setSearchData({
                      ...searchData, 
                      budget_range: {...searchData.budget_range, min: parseInt(e.target.value)}
                    })}
                    className="budget-input"
                  />
                  <input
                    type="number"
                    placeholder="Max"
                    value={searchData.budget_range.max}
                    onChange={(e) => setSearchData({
                      ...searchData, 
                      budget_range: {...searchData.budget_range, max: parseInt(e.target.value)}
                    })}
                    className="budget-input"
                  />
                </div>
              </div>
            </div>
            <button onClick={handleLocationSearch} className="search-button">
              Analyze Locations
            </button>
          </div>
        </section>

        <section className="featured-locations">
          <h3>Featured Opportunities</h3>
          <div className="locations-grid">
            {featuredLocations.map((location, index) => (
              <div key={index} className="location-card">
                <div className="location-score">{location.score}</div>
                <h4 className="location-name">{location.name}</h4>
                <p className="location-highlight">{location.highlight}</p>
                <button className="explore-button">Explore</button>
              </div>
            ))}
          </div>
        </section>

        <section className="transition-section">
          <div className="transition-prompt">
            <h3>Ready to Connect with Remote Opportunities?</h3>
            <p>Access ThriveRemoteOS to discover jobs tailored to your new location</p>
            <button onClick={initiateTransition} className="transition-button">
              INITIATE CONNECTION
            </button>
          </div>
        </section>
      </main>
    </div>
  );
};

const ThriveRemoteOS = () => {
  const [systemStatus, setSystemStatus] = useState(null);
  const [jobRecommendations, setJobRecommendations] = useState([]);
  const [userProfile, setUserProfile] = useState(null);

  useEffect(() => {
    const fetchSystemData = async () => {
      try {
        const [statusRes, jobsRes] = await Promise.all([
          axios.get(`${API}/system/status`),
          axios.get(`${API}/jobs/recommendations/user_001`)
        ]);
        
        setSystemStatus(statusRes.data);
        setJobRecommendations(jobsRes.data.recommendations);
      } catch (error) {
        console.error("Failed to fetch system data:", error);
      }
    };

    fetchSystemData();
  }, []);

  return (
    <div className="thrive-container">
      <header className="thrive-header">
        <div className="thrive-logo">
          <h1>THRIVE<span className="remote-accent">REMOTE</span>OS</h1>
          <span className="version">v{systemStatus?.version || '5.5'}</span>
        </div>
        <div className="system-status">
          <div className="status-grid">
            <div className="status-item">
              <span className="status-label">Uptime</span>
              <span className="status-value">{systemStatus?.uptime || '99.8%'}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Services</span>
              <span className="status-value">Online</span>
            </div>
          </div>
        </div>
      </header>

      <main className="thrive-main">
        <section className="welcome-section">
          <h2 className="welcome-title">AI Job Platform V5.5</h2>
          <p className="welcome-subtitle">
            Your relocation data has been processed. Here are personalized 
            remote opportunities that match your new location preferences.
          </p>
        </section>

        <section className="recommendations-section">
          <h3>Curated Job Matches</h3>
          <div className="jobs-grid">
            {jobRecommendations.map((job, index) => (
              <div key={index} className="job-card">
                <div className="job-header">
                  <h4 className="job-title">{job.title}</h4>
                  <span className="company-name">{job.company}</span>
                </div>
                <div className="job-details">
                  <div className="location-tag">
                    <span className={job.remote_friendly ? 'remote-friendly' : 'hybrid'}>
                      {job.location}
                    </span>
                  </div>
                  <div className="salary-range">
                    ${job.salary_range.min.toLocaleString()} - ${job.salary_range.max.toLocaleString()}
                  </div>
                  <div className="skills-required">
                    {job.required_skills.slice(0, 3).map((skill, idx) => (
                      <span key={idx} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                  <p className="job-description">{job.description}</p>
                </div>
                <div className="job-actions">
                  <button className="apply-button">Apply Now</button>
                  <button className="save-button">Save</button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="ai-insights">
          <h3>AI Location Insights</h3>
          <div className="insights-grid">
            <div className="insight-card">
              <h4>Market Analysis</h4>
              <p>Based on your skills, the remote job market in your target locations shows 23% growth in opportunities.</p>
            </div>
            <div className="insight-card">
              <h4>Salary Optimization</h4>
              <p>Relocating to your selected area could increase your effective income by 15-20% due to cost of living differences.</p>
            </div>
            <div className="insight-card">
              <h4>Network Expansion</h4>
              <p>3 professional communities and 12 networking events identified in your target locations.</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

// ============================================================================
// MAIN APP COMPONENT
// ============================================================================

function App() {
  const [isTransitioning, setIsTransitioning] = useState(false);

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RelocateDashboard />} />
          <Route path="/relocate" element={<RelocateDashboard />} />
          <Route path="/bridge" element={<BridgeTransition />} />
          <Route path="/thrive-os" element={<ThriveRemoteOS />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;