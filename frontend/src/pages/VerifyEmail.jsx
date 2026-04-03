import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const VerifyEmail = () => {
  const [status, setStatus] = useState('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = new URLSearchParams(window.location.search).get('token');
    
    if (!token) {
      setStatus('error');
      setMessage('No verification token found');
      return;
    }

    fetch(`http://localhost:9000/api/auth/verify-email?token=${token}`)
      .then(res => res.json())
      .then(data => {
        if (data.message) {
          setStatus('success');
          setMessage(data.message);
        } else {
          setStatus('error');
          setMessage(data.detail || 'Verification failed');
        }
      })
      .catch(() => {
        setStatus('error');
        setMessage('Something went wrong');
      });
  }, []);

  if (status === 'loading') {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h2>Verifying your email...</h2>
          <p>Please wait...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        {status === 'success' ? (
          <>
            <div style={styles.successIcon}>?</div>
            <h2>Email Verified!</h2>
            <p>{message}</p>
            <Link to="/login" style={styles.button}>Go to Login</Link>
          </>
        ) : (
          <>
            <div style={styles.errorIcon}>?</div>
            <h2>Verification Failed</h2>
            <p>{message}</p>
            <Link to="/login" style={styles.button}>Back to Login</Link>
          </>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #d64daf 0%, #b83e8f 100%)',
  },
  card: {
    background: 'white',
    padding: '2rem',
    borderRadius: '12px',
    textAlign: 'center',
    maxWidth: '400px',
    width: '90%',
  },
  successIcon: { fontSize: '3rem', marginBottom: '1rem' },
  errorIcon: { fontSize: '3rem', marginBottom: '1rem' },
  button: {
    display: 'inline-block',
    background: '#d64daf',
    color: 'white',
    padding: '0.75rem 1.5rem',
    borderRadius: '8px',
    textDecoration: 'none',
    marginTop: '1rem',
  },
};

export default VerifyEmail;

