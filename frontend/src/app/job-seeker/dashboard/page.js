'use client';

import { useState, useEffect } from 'react';
import { jobAPI, applicationAPI } from '@/lib/api';
import styles from './Dashboard.module.css';
import Link from 'next/link';

export default function JobSeekerDashboard() {
  const [stats, setStats] = useState({
    totalApplications: 0,
    pendingApplications: 0,
    acceptedApplications: 0,
  });
  const [recentJobs, setRecentJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [applicationsResponse, jobsResponse] = await Promise.all([
        applicationAPI.getMyApplications(),
        jobAPI.getAllJobs(0, 5)
      ]);

      const apps = applicationsResponse.data;
      setStats({
        totalApplications: apps.length,
        pendingApplications: apps.filter(app => app.status === 'pending').length,
        acceptedApplications: apps.filter(app => app.status === 'accepted').length,
      });

      setRecentJobs(jobsResponse.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading dashboard...</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Job Seeker Dashboard</h1>

      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <div className={styles.statIcon}>📝</div>
          <div className={styles.statContent}>
            <h3>{stats.totalApplications}</h3>
            <p>Total Applications</p>
          </div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statIcon}>⏳</div>
          <div className={styles.statContent}>
            <h3>{stats.pendingApplications}</h3>
            <p>Pending</p>
          </div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statIcon}>✅</div>
          <div className={styles.statContent}>
            <h3>{stats.acceptedApplications}</h3>
            <p>Accepted</p>
          </div>
        </div>
      </div>

      <div className={styles.section}>
        <div className={styles.sectionHeader}>
          <h2>Latest Job Opportunities</h2>
          <Link href="/job-seeker/jobs" className={styles.viewAllLink}>
            View All
          </Link>
        </div>

        <div className={styles.jobsList}>
          {recentJobs.map((job) => (
            <div key={job.job_id} className={styles.jobCard}>
              <h3>{job.job_title}</h3>
              <p className={styles.location}>📍 {job.location}</p>
              <p className={styles.description}>
                {job.description.substring(0, 100)}...
              </p>
              <Link
                href={`/job-seeker/jobs/${job.job_id}`}
                className={styles.viewBtn}
              >
                View Details
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
