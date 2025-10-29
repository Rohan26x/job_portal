'use client';

import { useState, useEffect } from 'react';
import { jobAPI, applicationAPI } from '@/lib/api';
import styles from './Applications.module.css';

export default function RecruiterApplicationsPage() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
  }, []);

  useEffect(() => {
    if (selectedJob) {
      fetchApplications(selectedJob);
    }
  }, [selectedJob]);

  const fetchJobs = async () => {
    try {
      const response = await jobAPI.getMyJobs();
      setJobs(response.data);
      if (response.data.length > 0) {
        setSelectedJob(response.data[0].job_id);
      }
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchApplications = async (jobId) => {
    try {
      const response = await applicationAPI.getApplicationsForJob(jobId);
      setApplications(response.data);
    } catch (error) {
      console.error('Error fetching applications:', error);
    }
  };

  const handleStatusUpdate = async (appId, newStatus) => {
    try {
      await applicationAPI.updateStatus(appId, newStatus);
      fetchApplications(selectedJob);
    } catch (error) {
      console.error('Error updating status:', error);
      alert('Failed to update status');
    }
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      pending: styles.statusPending,
      accepted: styles.statusAccepted,
      rejected: styles.statusRejected,
    };

    return (
      <span className={`${styles.statusBadge} ${statusClasses[status]}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  if (loading) {
    return <div className={styles.loading}>Loading applications...</div>;
  }

  if (jobs.length === 0) {
    return (
      <div className={styles.emptyState}>
        <p>You haven't posted any jobs yet</p>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Job Applications</h1>

      <div className={styles.jobSelector}>
        <label htmlFor="job-select">Select Job:</label>
        <select
          id="job-select"
          value={selectedJob || ''}
          onChange={(e) => setSelectedJob(parseInt(e.target.value))}
          className={styles.select}
        >
          {jobs.map((job) => (
            <option key={job.job_id} value={job.job_id}>
              {job.job_title}
            </option>
          ))}
        </select>
      </div>

      {applications.length === 0 ? (
        <div className={styles.emptyState}>
          <p>No applications received for this job yet</p>
        </div>
      ) : (
        <div className={styles.applicationsList}>
          {applications.map((app) => (
            <div key={app.application_id} className={styles.appCard}>
              <div className={styles.appHeader}>
                <div>
                  <h3>
                    {app.job_seeker?.first_name} {app.job_seeker?.last_name}
                  </h3>
                  <p className={styles.date}>
                    Applied: {new Date(app.applied_at).toLocaleDateString()}
                  </p>
                </div>
                {getStatusBadge(app.status)}
              </div>

              <div className={styles.actions}>
                <button
                  onClick={() => handleStatusUpdate(app.application_id, 'accepted')}
                  disabled={app.status === 'accepted'}
                  className={styles.acceptBtn}
                >
                  Accept
                </button>
                <button
                  onClick={() => handleStatusUpdate(app.application_id, 'rejected')}
                  disabled={app.status === 'rejected'}
                  className={styles.rejectBtn}
                >
                  Reject
                </button>
                <button
                  onClick={() => handleStatusUpdate(app.application_id, 'pending')}
                  disabled={app.status === 'pending'}
                  className={styles.pendingBtn}
                >
                  Mark Pending
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
