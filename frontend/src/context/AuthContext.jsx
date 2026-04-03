import React, { createContext, useState, useContext } from 'react';
import { authService } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchUserInfo = async (accessToken) => {
    try {
      const response = await fetch('http://localhost:9000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        return userData;
      }
    } catch (error) {
      console.error('Error fetching user info:', error);
    }
    return null;
  };

    const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await authService.login({ email, password });
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      setToken(access_token);
      
      // Fetch user info with role
      const userData = await fetchUserInfo(access_token);
      if (userData) {
        setUser(userData);
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, password, fullName) => {
    setLoading(true);
    try {
      const response = await authService.register({ 
        email, 
        password, 
        full_name: fullName 
      });
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      setToken(access_token);
      
      // Fetch user info after registration
      const userData = await fetchUserInfo(access_token);
      if (userData) {
        setUser(userData);
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  // Load user info if token exists on app start
  React.useEffect(() => {
    if (token && !user) {
      fetchUserInfo(token);
    }
  }, [token]);

  return (
    <AuthContext.Provider value={{ token, user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
