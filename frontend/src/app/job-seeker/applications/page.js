'use client';

import { useState, useEffect } from 'react';
import { applicationAPI } from '@/lib/api';
import styles from './Applications.module.css';
import Link from 'next/link';

export default function MyApplicationsPage() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await applicationAPI.getMyApplications();
      setApplications(response.data);
    } catch (error) {
      console.error('Error fetching applications:', error);
    } finally {
      setLoading(false);
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

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Applications</h1>

      {applications.length === 0 ? (
        <div className={styles.emptyState}>
          <p>You haven't applied to any jobs yet</p>
          <Link href="/job-seeker/jobs" className="btn btn-primary">
            Browse Jobs
          </Link>
        </div>
      ) : (
        <div className={styles.applicationsList}>
          {applications.map((app) => (
            <div key={app.application_id} className={styles.appCard}>
              <div className={styles.appHeader}>
                <div>
                  <h2>{app.job?.job_title || 'Job Title'}</h2>
                  <p className={styles.location}>
                    📍 {app.job?.location || 'Location'}
                  </p>
                </div>
                {getStatusBadge(app.status)}
              </div>
              <p className={styles.date}>
                Applied on: {new Date(app.applied_at).toLocaleDateString()}
              </p>
              <div className={styles.actions}>
                <Link
                  href={`/job-seeker/jobs/${app.job_id}`}
                  className={styles.viewBtn}
                >
                  View Job
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
