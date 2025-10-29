'use client';

import { useState, useEffect, use } from 'react';
import { useRouter } from 'next/navigation';
import { jobAPI, applicationAPI } from '@/lib/api';
import styles from './JobDetails.module.css';

export default function JobDetailsPage({ params }) {
  const resolvedParams = use(params);
  const jobId = resolvedParams.id;

  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const router = useRouter();

  useEffect(() => {
    fetchJobDetails();
  }, [jobId]);

  const fetchJobDetails = async () => {
    try {
      const response = await jobAPI.getById(jobId);
      setJob(response.data);
    } catch (error) {
      console.error('Error fetching job:', error);
      setError('Failed to load job details');
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async () => {
    setError('');
    setSuccess('');
    setApplying(true);

    try {
      await applicationAPI.createApplication({
        job_id: parseInt(jobId),
      });
      setSuccess('Application submitted successfully!');
      setTimeout(() => {
        router.push('/job-seeker/applications');
      }, 2000);
    } catch (err) {
      console.error('Error applying:', err);
      setError(err.response?.data?.detail || 'Failed to submit application');
      setApplying(false);
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading job details...</div>;
  }

  if (error && !job) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.container}>
      <button onClick={() => router.back()} className={styles.backBtn}>
        ← Back to Jobs
      </button>

      <div className={styles.jobCard}>
        <h1 className={styles.title}>{job.job_title}</h1>
        <p className={styles.location}>📍 {job.location}</p>

        <div className={styles.section}>
          <h2>Job Description</h2>
          <p className={styles.description}>{job.description}</p>
        </div>

        {error && <div className={styles.errorBox}>{error}</div>}
        {success && <div className={styles.successBox}>{success}</div>}

        <div className={styles.actions}>
          <button
            onClick={handleApply}
            disabled={applying || success}
            className={styles.applyBtn}
          >
            {applying ? 'Submitting...' : success ? 'Applied ✓' : 'Apply Now'}
          </button>
        </div>
      </div>
    </div>
  );
}
