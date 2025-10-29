'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { jobAPI } from '@/lib/api';
import styles from './PostJob.module.css';

export default function PostJobPage() {
  const [formData, setFormData] = useState({
    job_title: '',
    description: '',
    location: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

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
    if (!formData.job_title.trim()) {
      setError('Job title is required');
      return;
    }
    if (!formData.description.trim()) {
      setError('Job description is required');
      return;
    }
    if (!formData.location.trim()) {
      setError('Location is required');
      return;
    }

    setLoading(true);

    try {
      await jobAPI.createJob(formData);
      router.push('/recruiter/jobs');
    } catch (err) {
      console.error('Error creating job:', err);
      setError(err.response?.data?.detail || 'Failed to create job');
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Post a New Job</h1>

      <div className={styles.formCard}>
        {error && <div className={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="job_title">Job Title *</label>
            <input
              type="text"
              id="job_title"
              name="job_title"
              value={formData.job_title}
              onChange={handleChange}
              required
              placeholder="e.g. Senior React Developer"
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="location">Location *</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
              placeholder="e.g. New York, NY or Remote"
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="description">Job Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              placeholder="Describe the role, responsibilities, requirements..."
              rows="10"
              disabled={loading}
            />
          </div>

          <div className={styles.actions}>
            <button
              type="button"
              className={styles.cancelBtn}
              onClick={() => router.push('/recruiter/dashboard')}
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className={styles.submitBtn}
              disabled={loading}
            >
              {loading ? 'Posting...' : 'Post Job'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
