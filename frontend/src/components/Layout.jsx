
import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';

const Layout = () => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => { logout(); navigate('/login'); };

  return (
    <div style={styles.layout}>
      <nav style={styles.navbar}>
        <div style={styles.navBrand}><Link to="/dashboard" style={styles.link}>💰 Finance Tracker</Link></div>
        <div style={styles.navLinks}>
          <Link to="/dashboard" style={styles.link}>Dashboard</Link>
          <Link to="/transactions" style={styles.link}>Transactions</Link>
          <Link to="/budgets" style={styles.link}>Budgets</Link>
          <Link to="/upload" style={styles.link}>Upload CSV</Link>
        </div>
        <div style={styles.navUser}>
          <span>{user?.email || 'User'}</span>
          <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
        </div>
      </nav>
      <main style={styles.main}><Outlet /></main>
    </div>
  );
};

const styles = {
  layout: { minHeight: '100vh', background: '#f5f7fa' },
  navbar: { background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', padding: '1rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  navBrand: { fontSize: '1.5rem', fontWeight: 'bold' },
  navLinks: { display: 'flex', gap: '2rem' },
  navUser: { display: 'flex', alignItems: 'center', gap: '1rem' },
  link: { color: 'white', textDecoration: 'none' },
  logoutBtn: { background: 'rgba(255,255,255,0.2)', border: 'none', color: 'white', padding: '0.5rem 1rem', borderRadius: '5px', cursor: 'pointer' },
  main: { padding: '2rem', maxWidth: '1400px', margin: '0 auto' },
};

export default Layout;
