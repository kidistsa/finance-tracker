import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/authContext';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const { register, loading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const result = await register(email, password, fullName);
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Create Account</h1>
        <p style={styles.subtitle}>Start tracking your finances</p>
        {error && <div style={styles.error}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Full Name</label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              style={styles.input}
              placeholder="Enter your full name"
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={styles.input}
              placeholder="Enter your email"
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={styles.input}
              placeholder="Enter your password"
            />
          </div>
          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'Creating account...' : 'Register'}
          </button>
        </form>
        <p style={styles.link}>
          Already have an account? <Link to="/login" style={styles.linkText}>Login</Link>
        </p>
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
    background: 'linear-gradient(135deg, #e8b4d4 0%, #d48fb3 100%)', 
  },
  card: {
    background: 'white',
    padding: '2.5rem',
    borderRadius: '12px',
    width: '100%',
    maxWidth: '420px',
    boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
  },
  title: { textAlign: 'center', marginBottom: '0.5rem', color: '#333', fontSize: '1.8rem', fontWeight: 'bold' },
  subtitle: { textAlign: 'center', marginBottom: '1.5rem', color: '#666', fontSize: '0.9rem' },
  inputGroup: { marginBottom: '1.2rem' },
  label: { display: 'block', marginBottom: '0.5rem', color: '#555', fontWeight: '500' },
  input: { width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '8px', fontSize: '1rem', boxSizing: 'border-box' },
  button: { width: '100%', padding: '0.75rem', background: 'linear-gradient(135deg, #d64daf 0%, #b83e8f 100%)', color: 'white', border: 'none', borderRadius: '8px', fontSize: '1rem', fontWeight: '600', cursor: 'pointer' },
  error: { background: '#fee', color: '#c62828', padding: '0.75rem', borderRadius: '8px', marginBottom: '1rem', textAlign: 'center' },
  link: { textAlign: 'center', marginTop: '1.5rem', color: '#666' },
  linkText: { color: '#d64daf', textDecoration: 'none', fontWeight: '500' },
};

export default Register;
