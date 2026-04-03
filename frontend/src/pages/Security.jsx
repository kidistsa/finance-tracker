import React, { useState, useEffect } from 'react';
import { useTheme } from '../context/themeContext';
import BackButton from '../components/BackButton';

const Security = () => {
  const { darkMode } = useTheme();
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userRole, setUserRole] = useState(null);
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    fetchUserInfo();
    fetchLogs();
  }, []);

  const fetchUserInfo = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:9000/api/auth/me', {
        headers: { Authorization: 'Bearer ' + token }
      });
      const data = await response.json();
      setUserRole(data.role);
      setUserEmail(data.email);
    } catch (error) {
      console.error('Error fetching user info:', error);
    }
  };

  const fetchLogs = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Try to fetch all logs (admin only)
      try {
        const response = await fetch('http://localhost:9000/api/security/audit-logs', {
          headers: { Authorization: 'Bearer ' + token }
        });
        if (response.ok) {
          const data = await response.json();
          setAuditLogs(data);
        } else {
          // If 403, fetch only user's logs
          const myResponse = await fetch('http://localhost:9000/api/security/my-logs', {
            headers: { Authorization: 'Bearer ' + token }
          });
          const myData = await myResponse.json();
          setAuditLogs(myData);
        }
      } catch (err) {
        // Fallback to user's logs
        const myResponse = await fetch('http://localhost:9000/api/security/my-logs', {
          headers: { Authorization: 'Bearer ' + token }
        });
        const myData = await myResponse.json();
        setAuditLogs(myData);
      }
    } catch (error) {
      console.error('Error fetching logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActionColor = (action) => {
    if (action.includes('login_success')) return { bg: '#4bc0c0', color: '#fff' };
    if (action.includes('login_failed')) return { bg: '#ff6384', color: '#fff' };
    if (action.includes('password_changed')) return { bg: '#36a2eb', color: '#fff' };
    if (action.includes('registered')) return { bg: '#9966ff', color: '#fff' };
    if (action.includes('verified')) return { bg: '#4bc0c0', color: '#fff' };
    if (action.includes('delete')) return { bg: '#ff6384', color: '#fff' };
    return { bg: '#ffce56', color: '#333' };
  };

  const formatAction = (action) => {
    return action
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  if (loading) return <div style={styles.loading}>Loading security logs...</div>;

  const isAdmin = userRole === 'admin';

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <BackButton defaultPath="/dashboard" />
        <h1 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Security & Audit Logs</h1>
      </div>

      {/* User Info Card */}
      <div style={{ ...styles.infoCard, background: darkMode ? '#16213e' : 'white' }}>
        <p><strong>👤 Logged in as:</strong> {userEmail}</p>
        <p><strong>👑 Role:</strong> <span style={{ color: isAdmin ? '#FFD700' : '#4bc0c0', fontWeight: 'bold' }}>{isAdmin ? 'ADMIN' : 'USER'}</span></p>
        {isAdmin && <p><strong>🔓 Viewing:</strong> All user activity (admin access)</p>}
        {!isAdmin && <p><strong>🔒 Viewing:</strong> Only your own activity</p>}
      </div>

      <div style={{ ...styles.card, background: darkMode ? '#16213e' : 'white' }}>
        <h3 style={{ color: darkMode ? '#fff' : '#1a2a4f', marginBottom: '1rem' }}>
          {isAdmin ? '📋 All User Activity' : '📝 My Recent Activity'}
        </h3>
        
        {auditLogs.length === 0 ? (
          <p style={{ color: darkMode ? '#a0aec0' : '#718096', textAlign: 'center', padding: '2rem' }}>
            No activity logs found yet. Your actions will appear here.
          </p>
        ) : (
          <div style={styles.tableWrapper}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Time</th>
                  {isAdmin && <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>User</th>}
                  <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Action</th>
                  <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>IP Address</th>
                  <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Details</th>
                </tr>
              </thead>
              <tbody>
                {auditLogs.map((log, index) => {
                  const actionStyle = getActionColor(log.action);
                  return (
                    <tr key={index}>
                      <td style={{ ...styles.td, borderBottomColor: darkMode ? '#2d3748' : '#e2e8f0', color: darkMode ? '#eee' : '#2d3748' }}>
                        {new Date(log.created_at).toLocaleString()}
                      </td>
                      {isAdmin && (
                        <td style={{ ...styles.td, borderBottomColor: darkMode ? '#2d3748' : '#e2e8f0', color: darkMode ? '#eee' : '#2d3748' }}>
                          {log.user_id}
                        </td>
                      )}
                      <td style={{ ...styles.td, borderBottomColor: darkMode ? '#2d3748' : '#e2e8f0' }}>
                        <span style={{ ...styles.actionBadge, background: actionStyle.bg, color: actionStyle.color }}>
                          {formatAction(log.action)}
                        </span>
                      </td>
                      <td style={{ ...styles.td, borderBottomColor: darkMode ? '#2d3748' : '#e2e8f0', color: darkMode ? '#eee' : '#2d3748' }}>
                        <code style={{ background: darkMode ? '#2d3748' : '#f0f0f0', padding: '2px 6px', borderRadius: '4px' }}>
                          {log.ip_address || 'unknown'}
                        </code>
                      </td>
                      <td style={{ ...styles.td, borderBottomColor: darkMode ? '#2d3748' : '#e2e8f0', color: darkMode ? '#eee' : '#2d3748' }}>
                        {log.details ? JSON.stringify(log.details) : '-'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div style={{ ...styles.card, background: darkMode ? '#16213e' : 'white', marginTop: '1rem' }}>
        <h3 style={{ color: darkMode ? '#fff' : '#1a2a4f', marginBottom: '1rem' }}>🔒 Security Tips</h3>
        <ul style={{ color: darkMode ? '#a0aec0' : '#4a5568', marginLeft: '1.5rem' }}>
          <li>Use a strong, unique password (at least 8 characters with mixed case, numbers, and symbols)</li>
          <li>Never share your password with anyone</li>
          <li>Log out from shared devices</li>
          <li>Monitor your account activity regularly</li>
          <li>If you see suspicious activity, change your password immediately</li>
        </ul>
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '1200px', margin: '0 auto' },
  header: { display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' },
  infoCard: { padding: '1rem', borderRadius: '12px', marginBottom: '1rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  card: { padding: '1.5rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  tableWrapper: { overflowX: 'auto' },
  table: { width: '100%', borderCollapse: 'collapse' },
  td: { padding: '0.75rem', borderBottom: '1px solid' },
  actionBadge: { padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold', display: 'inline-block' },
  loading: { textAlign: 'center', padding: '2rem', fontSize: '1.2rem' }
};

export default Security;
