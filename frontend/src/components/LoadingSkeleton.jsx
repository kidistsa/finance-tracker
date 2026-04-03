import React from 'react';
import { useTheme } from '../context/themeContext';

const LoadingSkeleton = () => {
  const { darkMode } = useTheme();
  
  return (
    <div style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ ...styles.skeleton, width: '200px', height: '32px', marginBottom: '2rem' }} />
      <div style={styles.grid}>
        {[1, 2, 3, 4].map(i => (
          <div key={i} style={{ ...styles.skeleton, height: '120px', borderRadius: '10px' }} />
        ))}
      </div>
      <div style={{ ...styles.skeleton, height: '400px', marginTop: '2rem', borderRadius: '10px' }} />
    </div>
  );
};

const styles = {
  skeleton: {
    background: 'linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%)',
    backgroundSize: '200% 100%',
    animation: 'shimmer 1.5s infinite',
    borderRadius: '4px'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '1rem',
    marginBottom: '2rem'
  }
};

// Add keyframes to index.css
const styleSheet = document.createElement('style');
styleSheet.textContent = 
  @keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
;
document.head.appendChild(styleSheet);

export default LoadingSkeleton;
