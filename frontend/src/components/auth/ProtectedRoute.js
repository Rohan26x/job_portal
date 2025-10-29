'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

export default function ProtectedRoute({ children, requiredRole }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push('/auth/login');
      } else if (requiredRole && user.user_type !== requiredRole) {
        // Redirect to appropriate dashboard if wrong role
        const redirectPath = user.user_type === 'recruiter'
          ? '/recruiter/dashboard'
          : '/job-seeker/dashboard';
        router.push(redirectPath);
      }
    }
  }, [user, loading, requiredRole, router]);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        fontSize: '1.2rem',
        color: '#667eea'
      }}>
        Loading...
      </div>
    );
  }

  if (!user || (requiredRole && user.user_type !== requiredRole)) {
    return null;
  }

  return children;
}
