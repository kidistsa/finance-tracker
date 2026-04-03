import React, { useState, useEffect } from 'react';
import { useTheme } from '../context/themeContext';
import BackButton from '../components/BackButton';

const Admin = () => {
  const { darkMode } = useTheme();
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState({
    total_users: 0,
    active_users: 0,
    suspended_users: 0,
    premium_users: 0
  });
  const [loading, setLoading] = useState(true);
  const [filterRole, setFilterRole] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    fetchUsers();
    fetchStats();
  }, []);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:9000/api/admin/users', {
        headers: { Authorization: 'Bearer ' + token }
      });
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:9000/api/admin/users/stats', {
        headers: { Authorization: 'Bearer ' + token }
      });
      const data = await response.json();
      
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateUserRole = async (userId, newRole) => {
    try {
      const token = localStorage.getItem('token');
      await fetch('http://localhost:9000/api/admin/users/' + userId, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({ role: newRole })
      });
      fetchUsers();
      fetchStats();
    } catch (error) {
      console.error('Error updating role:', error);
    }
  };

  const updateUserStatus = async (userId, newStatus) => {
    try {
      const token = localStorage.getItem('token');
      await fetch('http://localhost:9000/api/admin/users/' + userId, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({ status: newStatus })
      });
      fetchUsers();
      fetchStats();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const deleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      try {
        const token = localStorage.getItem('token');
        await fetch('http://localhost:9000/api/admin/users/' + userId, {
          method: 'DELETE',
          headers: { Authorization: 'Bearer ' + token }
        });
        fetchUsers();
        fetchStats();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  };

  const filteredUsers = users.filter(user => {
    if (filterRole !== 'all' && user.role !== filterRole) return false;
    if (filterStatus !== 'all' && user.status !== filterStatus) return false;
    return true;
  });

  if (loading) return <div style={{ ...styles.loading, color: darkMode ? '#fff' : '#1a2a4f' }}>Loading admin dashboard...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <BackButton defaultPath="/dashboard" />
        <h1 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Admin Dashboard</h1>
      </div>
      
      <div style={styles.statsGrid}>
        <div style={{ ...styles.statCard, background: darkMode ? '#16213e' : 'white', color: darkMode ? '#eee' : '#333' }}>
          <h3>Total Users</h3>
          <p style={styles.statNumber}>{stats?.total_users || 0}</p>
        </div>
        <div style={{ ...styles.statCard, background: darkMode ? '#16213e' : 'white', color: darkMode ? '#eee' : '#333' }}>
          <h3>Active Users</h3>
          <p style={styles.statNumber}>{stats?.active_users || 0}</p>
        </div>
        <div style={{ ...styles.statCard, background: darkMode ? '#16213e' : 'white', color: darkMode ? '#eee' : '#333' }}>
          <h3>Suspended</h3>
          <p style={styles.statNumber}>{stats?.suspended_users || 0}</p>
        </div>
        <div style={{ ...styles.statCard, background: darkMode ? '#16213e' : 'white', color: darkMode ? '#eee' : '#333' }}>
          <h3>Premium Users</h3>
          <p style={styles.statNumber}>{stats?.premium_users || 0}</p>
        </div>
      </div>
      
      <div style={styles.filters}>
        <select value={filterRole} onChange={(e) => setFilterRole(e.target.value)} style={{ ...styles.filterSelect, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#ddd' }}>
          <option value="all">All Roles</option>
          <option value="user">Users</option>
          <option value="premium">Premium</option>
          <option value="admin">Admins</option>
        </select>
        <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} style={{ ...styles.filterSelect, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#ddd' }}>
          <option value="all">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="suspended">Suspended</option>
        </select>
      </div>
      
      <div style={{ ...styles.tableCard, background: darkMode ? '#16213e' : 'white' }}>
        <table style={styles.table}>
          <thead>
            <tr style={{ borderBottom: darkMode ? '1px solid #2d3748' : '1px solid #e2e8f0' }}>
              <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>ID</th>
              <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Email</th>
              <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Name</th>
              <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Role</th>
              <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Status</th>
              <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Verified</th>
              <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Joined</th>
              <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map(user => (
              <tr key={user.id} style={{ borderBottom: darkMode ? '1px solid #2d3748' : '1px solid #e2e8f0' }}>
                <td style={{ color: darkMode ? '#eee' : '#2d3748' }}>{user.id}</td>
                <td style={{ color: darkMode ? '#eee' : '#2d3748' }}>{user.email}</td>
                <td style={{ color: darkMode ? '#eee' : '#2d3748' }}>{user.full_name || '-'}</td>
                <td>
                  <select value={user.role} onChange={(e) => updateUserRole(user.id, e.target.value)} style={{ ...styles.selectSmall, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#ddd' }}>
                    <option value="user">User</option>
                    <option value="premium">Premium</option>
                    <option value="admin">Admin</option>
                  </select>
                </td>
                <td>
                  <select value={user.status} onChange={(e) => updateUserStatus(user.id, e.target.value)} style={{ ...styles.selectSmall, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#ddd' }}>
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                    <option value="suspended">Suspended</option>
                  </select>
                </td>
                <td style={{ color: darkMode ? '#eee' : '#2d3748' }}>{user.is_verified ? '?' : '?'}</td>
                <td style={{ color: darkMode ? '#eee' : '#2d3748' }}>{new Date(user.created_at).toLocaleDateString()}</td>
                <td>
                  <button onClick={() => deleteUser(user.id)} style={styles.deleteBtn}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '1400px', margin: '0 auto' },
  header: { display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' },
  statsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' },
  statCard: { padding: '1.5rem', borderRadius: '10px', textAlign: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  statNumber: { fontSize: '2rem', fontWeight: 'bold', color: '#d64daf', marginTop: '0.5rem' },
  filters: { display: 'flex', gap: '1rem', marginBottom: '1.5rem' },
  filterSelect: { padding: '0.5rem', borderRadius: '5px', border: '1px solid' },
  tableCard: { borderRadius: '10px', overflow: 'auto', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  table: { width: '100%', borderCollapse: 'collapse' },
  selectSmall: { padding: '0.25rem', borderRadius: '4px', border: '1px solid' },
  deleteBtn: { background: '#ff6384', color: 'white', border: 'none', padding: '0.25rem 0.5rem', borderRadius: '4px', cursor: 'pointer' },
  loading: { textAlign: 'center', padding: '2rem', fontSize: '1.2rem' }
};

export default Admin;


