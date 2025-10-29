'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import styles from './Register.module.css';

export default function RegisterPage() {
  const [selectedRole, setSelectedRole] = useState('');
  const router = useRouter();

  const handleRoleSelection = () => {
    if (selectedRole === 'recruiter') {
      router.push('/auth/register/recruiter');
    } else if (selectedRole === 'job-seeker') {
      router.push('/auth/register/job-seeker');
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.formCard}>
        <h1 className={styles.title}>Join Job Portal</h1>
        <p className={styles.subtitle}>Choose how you want to get started</p>

        <div className={styles.roleOptions}>
          <div
            className={`${styles.roleCard} ${selectedRole === 'recruiter' ? styles.selected : ''}`}
            onClick={() => setSelectedRole('recruiter')}
          >
            <div className={styles.roleIcon}>🏢</div>
            <h3>I'm a Recruiter</h3>
            <p>Post job openings and find talented candidates</p>
          </div>

          <div
            className={`${styles.roleCard} ${selectedRole === 'job-seeker' ? styles.selected : ''}`}
            onClick={() => setSelectedRole('job-seeker')}
          >
            <div className={styles.roleIcon}>👤</div>
            <h3>I'm a Job Seeker</h3>
            <p>Find your dream job with AI-powered matching</p>
          </div>
        </div>

        <button
          className={styles.continueBtn}
          onClick={handleRoleSelection}
          disabled={!selectedRole}
        >
          Continue
        </button>

        <p className={styles.footer}>
          Already have an account?{' '}
          <Link href="/auth/login">Sign in here</Link>
        </p>
      </div>
    </div>
  );
}
