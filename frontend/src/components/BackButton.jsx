import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../context/themeContext';

const BackButton = ({ defaultPath = '/dashboard' }) => {
  const navigate = useNavigate();
  const { darkMode } = useTheme();

  const goBack = () => {
    if (window.history.length > 2) {
      navigate(-1);
    } else {
      navigate(defaultPath);
    }
  };

  return (
    <button 
      onClick={goBack} 
      style={{
        ...styles.button,
        background: darkMode ? '#2d3748' : '#e2e8f0',
        color: darkMode ? '#fff' : '#4a5568'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.background = darkMode ? '#4a5568' : '#cbd5e0';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background = darkMode ? '#2d3748' : '#e2e8f0';
      }}
    >
      <span style={{ fontSize: '1.2rem', marginRight: '0.25rem' }}>&larr;</span>
      Back
    </button>
  );
};

const styles = {
  button: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.25rem',
    padding: '0.5rem 1rem',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: '500',
    transition: 'all 0.2s',
    marginBottom: '1rem'
  }
};

export default BackButton;
