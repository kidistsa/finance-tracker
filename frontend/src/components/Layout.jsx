import React, { useState, useEffect } from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';
import { useTheme } from '../context/themeContext';

const Layout = () => {
  const { logout, user, token } = useAuth();
  const { darkMode, toggleDarkMode } = useTheme();
  const navigate = useNavigate();
  const [isAdmin, setIsAdmin] = useState(false);
  const [userRole, setUserRole] = useState(null);

  useEffect(() => {
    const checkAdminStatus = async () => {
      if (token) {
        try {
          const response = await fetch('http://localhost:9000/api/auth/me', {
            headers: {
              'Authorization': 'Bearer ' + token
            }
          });
          if (response.ok) {
            const userData = await response.json();
            setUserRole(userData.role);
            setIsAdmin(userData.role === 'admin');
          }
        } catch (error) {
          console.error('Error checking admin status:', error);
        }
      }
    };
    
    checkAdminStatus();
  }, [token]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={{
      ...styles.layout,
      background: darkMode ? '#1a1a2e' : '#f5f7fa'
    }}>
      <nav style={styles.navbar}>
        <div style={styles.navBrand}>
          <Link to="/dashboard" style={styles.link}>
            <span style={styles.logo}>🇪🇹</span>
            <span style={styles.brandText}>Birr Finance</span>
          </Link>
        </div>
        <div style={styles.navLinks}>
          <Link to="/dashboard" style={styles.link}>Dashboard</Link>
          <Link to="/transactions" style={styles.link}>Transactions</Link>
          <Link to="/budgets" style={styles.link}>Budgets</Link>
          <Link to="/upload" style={styles.link}>Upload</Link>
          <Link to="/recurring" style={styles.link}>Recurring</Link>
          {isAdmin && <Link to="/admin" style={styles.adminLink}>👑 Admin</Link>}
          <Link to="/security" style={styles.link}>🔒 Security</Link>
        </div>
        <div style={styles.navUser}>
          <button onClick={toggleDarkMode} style={styles.themeBtn}>
            {darkMode ? '☀️' : '🌙'}
          </button>
          <div style={styles.userInfo}>
            <span style={styles.userEmail}>{user?.email || 'User'}</span>
            {userRole && (
              <span style={{
                ...styles.roleBadge,
                background: userRole === 'admin' ? '#FFD700' : userRole === 'premium' ? '#4bc0c0' : '#a0aec0'
              }}>
                {userRole === 'admin' ? 'ADMIN' : userRole === 'premium' ? 'PREMIUM' : 'USER'}
              </span>
            )}
          </div>
          <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
        </div>
      </nav>
      <main style={styles.main}>
        <Outlet />
      </main>
    </div>
  );
};

const styles = {
  layout: {
    minHeight: '100vh',
    transition: 'background 0.3s'
  },
  navbar: {
    background: 'linear-gradient(135deg, #d64daf 0%, #b83e8f 100%)',
    color: 'white',
    padding: '0.6rem 1.5rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: '0.5rem'
  },
  navBrand: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.25rem'
  },
  logo: {
    fontSize: '1.3rem'
  },
  brandText: {
    fontSize: '1rem',
    fontWeight: 'bold'
  },
  navLinks: {
    display: 'flex',
    gap: '1rem',
    flexWrap: 'wrap',
    alignItems: 'center',
    fontSize: '0.9rem'
  },
  navUser: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem'
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.4rem'
  },
  userEmail: {
    color: 'white',
    fontSize: '0.85rem'
  },
  link: {
    color: 'white',
    textDecoration: 'none',
    transition: 'opacity 0.3s',
    padding: '0.2rem 0.4rem',
    borderRadius: '4px'
  },
  adminLink: {
    color: '#FFD700',
    textDecoration: 'none',
    fontWeight: 'bold',
    border: '1px solid #FFD700',
    padding: '0.2rem 0.6rem',
    borderRadius: '20px',
    fontSize: '0.8rem',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.2rem'
  },
  roleBadge: {
    fontSize: '0.6rem',
    padding: '0.15rem 0.4rem',
    borderRadius: '12px',
    fontWeight: 'bold',
    color: '#1a1a2e'
  },
  themeBtn: {
    background: 'rgba(255,255,255,0.2)',
    border: 'none',
    color: 'white',
    padding: '0.3rem 0.6rem',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '0.9rem'
  },
  logoutBtn: {
    background: 'rgba(255,255,255,0.2)',
    border: 'none',
    color: 'white',
    padding: '0.3rem 0.6rem',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '0.75rem'
  },
  main: {
    padding: '1.5rem',
    maxWidth: '1400px',
    margin: '0 auto'
  }
};

export default Layout;
