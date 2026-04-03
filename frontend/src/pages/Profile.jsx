import React, { useState } from 'react';
import { useAuth } from '../context/authContext';
import { useTheme } from '../context/ThemeContext';

const Profile = () => {
  const { user, token } = useAuth();
  const { darkMode } = useTheme();
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showVerificationMsg, setShowVerificationMsg] = useState(false);

  const handleChangePassword = async (e) => {
    e.preventDefault();
    
    if (newPassword !== confirmPassword) {
      setError('New passwords do not match');
      return;
    }
    
    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }
    
    setLoading(true);
    setError('');
    setMessage('');
    
    try {
      const response = await fetch('http://localhost:9000/api/auth/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': Bearer 
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword
        }),
      });
      
      const data = await response.json();
      if (response.ok) {
        setMessage('Password changed successfully!');
        setCurrentPassword('');
        setNewPassword('');
        setConfirmPassword('');
      } else {
        setError(data.detail || 'Failed to change password');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const sendVerification = async () => {
    try {
      const response = await fetch('http://localhost:9000/api/auth/send-verification', {
        method: 'POST',
        headers: { 'Authorization': Bearer  }
      });
      const data = await response.json();
      setShowVerificationMsg(true);
      setTimeout(() => setShowVerificationMsg(false), 5000);
    } catch (error) {
      alert('Failed to send verification email');
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Profile Settings</h1>
      
      <div style={{ ...styles.card, background: darkMode ? '#16213e' : 'white' }}>
        <h2>Account Information</h2>
        <div style={styles.infoRow}>
          <strong>Email:</strong> {user?.email}
        </div>
        <div style={styles.infoRow}>
          <strong>Role:</strong> {user?.role || 'user'}
        </div>
        <div style={styles.infoRow}>
          <strong>Status:</strong> {user?.is_verified ? '? Verified' : '?? Not verified'}
        </div>
        {!user?.is_verified && (
          <button onClick={sendVerification} style={styles.verifyBtn}>
            ?? Send Verification Email
          </button>
        )}
        {showVerificationMsg && (
          <div style={styles.successMsg}>Verification email sent! Check your inbox.</div>
        )}
      </div>
      
      <div style={{ ...styles.card, background: darkMode ? '#16213e' : 'white' }}>
        <h2>Change Password</h2>
        {error && <div style={styles.error}>{error}</div>}
        {message && <div style={styles.success}>{message}</div>}
        <form onSubmit={handleChangePassword}>
          <div style={styles.inputGroup}>
            <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Current Password</label>
            <input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              required
              style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#e2e8f0' }}
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>New Password</label>
            <input
              type="password"
              placeholder="Minimum 6 characters"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#e2e8f0' }}
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Confirm New Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#e2e8f0' }}
            />
          </div>
          <button type="submit" disabled={loading} style={styles.changeBtn}>
            {loading ? 'Changing...' : 'Change Password'}
          </button>
        </form>
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '800px', margin: '0 auto' },
  card: { padding: '1.5rem', borderRadius: '12px', marginBottom: '2rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  infoRow: { marginBottom: '0.75rem', padding: '0.5rem', borderBottom: '1px solid #e2e8f0' },
  inputGroup: { marginBottom: '1rem' },
  input: { width: '100%', padding: '0.75rem', border: '1px solid', borderRadius: '8px', fontSize: '1rem', boxSizing: 'border-box' },
  changeBtn: { width: '100%', padding: '0.75rem', background: '#d64daf', color: 'white', border: 'none', borderRadius: '8px', fontSize: '1rem', cursor: 'pointer', marginTop: '0.5rem' },
  verifyBtn: { marginTop: '1rem', padding: '0.5rem 1rem', background: '#ffce56', color: '#333', border: 'none', borderRadius: '5px', cursor: 'pointer' },
  error: { background: '#ffebee', color: '#c62828', padding: '0.75rem', borderRadius: '8px', marginBottom: '1rem', textAlign: 'center' },
  success: { background: '#e8f5e9', color: '#2e7d32', padding: '0.75rem', borderRadius: '8px', marginBottom: '1rem', textAlign: 'center' },
  successMsg: { marginTop: '1rem', padding: '0.5rem', background: '#e8f5e9', color: '#2e7d32', borderRadius: '5px', textAlign: 'center' },
};

export default Profile;

