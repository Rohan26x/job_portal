'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import styles from '../Register.module.css';

export default function RecruiterRegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    company_name: '',
    company_description: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const { registerRecruiter } = useAuth();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 3) {
      setError('Password must be at least 3 characters');
      return;
    }

    setLoading(true);

    const userData = {
      email: formData.email,
      password: formData.password,
      user_type: 'recruiter',
    };

    const recruiterData = {
      company_name: formData.company_name,
      company_description: formData.company_description,
    };

    const result = await registerRecruiter(userData, recruiterData);

    if (result.success) {
      router.push('/auth/login?registered=true');
    } else {
      setError(result.error);
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.formCard}>
        <h1 className={styles.title}>Recruiter Sign Up</h1>
        <p className={styles.subtitle}>Create your recruiter account</p>

        {error && <div className={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="your@email.com"
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="company_name">Company Name *</label>
            <input
              type="text"
              id="company_name"
              name="company_name"
              value={formData.company_name}
              onChange={handleChange}
              required
              placeholder="Your Company"
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="company_description">Company Description</label>
            <textarea
              id="company_description"
              name="company_description"
              value={formData.company_description}
              onChange={handleChange}
              placeholder="Tell us about your company..."
              rows="4"
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="password">Password *</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="••••••••"
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="confirmPassword">Confirm Password *</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              placeholder="••••••••"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            className={styles.submitBtn}
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <p className={styles.footer}>
          Already have an account?{' '}
          <Link href="/auth/login">Sign in here</Link>
        </p>
      </div>
    </div>
  );
}
