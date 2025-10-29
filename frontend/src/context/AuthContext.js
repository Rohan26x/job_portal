'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, userAPI } from '@/lib/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      const savedUser = localStorage.getItem('user');

      if (token && savedUser) {
        try {
          setUser(JSON.parse(savedUser));
        } catch (error) {
          console.error('Error parsing saved user:', error);
          localStorage.removeItem('user');
          localStorage.removeItem('access_token');
        }
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      console.log('Starting login...');
      const response = await authAPI.login({ email, password });
      console.log('Login response:', response.data);

      const { access_token } = response.data;
      console.log('Access token:', access_token);

      // Save token
      localStorage.setItem('access_token', access_token);
      console.log('Token saved to localStorage');

      // Small delay to ensure token is saved
      await new Promise(resolve => setTimeout(resolve, 100));

      // Get user data
      console.log('Fetching user data...');
      try {
        const userResponse = await userAPI.getCurrentUser();
        console.log('User response:', userResponse.data);

        const userData = userResponse.data;

        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);

        console.log('Login successful! User type:', userData.user_type);
        return { success: true, userType: userData.user_type };
      } catch (userError) {
        console.error('Error fetching user data:', userError);
        console.error('Error response:', userError.response?.data);

        // Clear the token if user fetch fails
        localStorage.removeItem('access_token');

        return {
          success: false,
          error: 'Failed to fetch user data. Please try again.'
        };
      }
    } catch (error) {
      console.error('Login error:', error);
      console.error('Error response:', error.response?.data);
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      };
    }
  };

  const registerRecruiter = async (userData, recruiterData) => {
    try {
      await authAPI.registerRecruiter(userData, recruiterData);
      return { success: true };
    } catch (error) {
      console.error('Registration error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Registration failed'
      };
    }
  };

  const registerJobSeeker = async (userData, jobSeekerData) => {
    try {
      await authAPI.registerJobSeeker(userData, jobSeekerData);
      return { success: true };
    } catch (error) {
      console.error('Registration error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Registration failed'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    registerRecruiter,
    registerJobSeeker,
    loading,
    isAuthenticated: !!user,
    isRecruiter: user?.user_type === 'recruiter',
    isJobSeeker: user?.user_type === 'job_seeker',
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
