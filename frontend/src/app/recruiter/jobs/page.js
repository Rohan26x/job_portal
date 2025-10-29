'use client';

import { useState, useEffect } from 'react';
import { jobAPI } from '@/lib/api';
import styles from './Jobs.module.css';
import Link from 'next/link';

export default function RecruiterJobsPage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await jobAPI.getMyJobs();
      setJobs(response.data);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (jobId) => {
    if (!confirm('Are you sure you want to delete this job?')) {
      return;
    }

    try {
      await jobAPI.deleteJob(jobId);
      setJobs(jobs.filter(job => job.job_id !== jobId));
    } catch (error) {
      console.error('Error deleting job:', error);
      alert('Failed to delete job');
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading jobs...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>My Job Postings</h1>
        <Link href="/recruiter/post-job" className={styles.postBtn}>
          ➕ Post New Job
        </Link>
      </div>

      {jobs.length === 0 ? (
        <div className={styles.emptyState}>
          <p>You haven't posted any jobs yet</p>
          <Link href="/recruiter/post-job" className="btn btn-primary">
            Post Your First Job
          </Link>
        </div>
      ) : (
        <div className={styles.jobsList}>
          {jobs.map((job) => (
            <div key={job.job_id} className={styles.jobCard}>
              <div className={styles.jobHeader}>
                <h2>{job.job_title}</h2>
                <span className={styles.location}>📍 {job.location}</span>
              </div>
              <p className={styles.description}>
                {job.description.substring(0, 150)}...
              </p>
              <div className={styles.actions}>
                <Link
                  href={`/recruiter/jobs/${job.job_id}`}
                  className={styles.viewBtn}
                >
                  View Details
                </Link>
                <Link
                  href={`/recruiter/jobs/${job.job_id}/edit`}
                  className={styles.editBtn}
                >
                  Edit
                </Link>
                <button
                  onClick={() => handleDelete(job.job_id)}
                  className={styles.deleteBtn}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
