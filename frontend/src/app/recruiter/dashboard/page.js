'use client';

import { useState, useEffect } from 'react';
import { jobAPI, applicationAPI } from '@/lib/api';
import styles from './Dashboard.module.css';
import Link from 'next/link';

export default function RecruiterDashboard() {
  const [stats, setStats] = useState({
    totalJobs: 0,
    totalApplications: 0,
    pendingApplications: 0,
  });
  const [recentJobs, setRecentJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const jobsResponse = await jobAPI.getMyJobs();
      const jobs = jobsResponse.data;

      setRecentJobs(jobs.slice(0, 5));

      let totalApps = 0;
      let pendingApps = 0;

      for (const job of jobs) {
        try {
          const appsResponse = await applicationAPI.getApplicationsForJob(job.job_id);
          const apps = appsResponse.data;
          totalApps += apps.length;
          pendingApps += apps.filter(app => app.status === 'pending').length;
        } catch (error) {
          console.error('Error fetching applications:', error);
        }
      }

      setStats({
        totalJobs: jobs.length,
        totalApplications: totalApps,
        pendingApplications: pendingApps,
      });
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
      <h1 className={styles.title}>Recruiter Dashboard</h1>

      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <div className={styles.statIcon}>💼</div>
          <div className={styles.statContent}>
            <h3>{stats.totalJobs}</h3>
            <p>Total Jobs Posted</p>
          </div>
        </div>

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
            <p>Pending Reviews</p>
          </div>
        </div>
      </div>

      <div className={styles.section}>
        <div className={styles.sectionHeader}>
          <h2>Recent Job Postings</h2>
          <Link href="/recruiter/jobs" className={styles.viewAllLink}>
            View All
          </Link>
        </div>

        {recentJobs.length === 0 ? (
          <div className={styles.emptyState}>
            <p>No jobs posted yet</p>
            <Link href="/recruiter/post-job" className="btn btn-primary">
              Post Your First Job
            </Link>
          </div>
        ) : (
          <div className={styles.jobsList}>
            {recentJobs.map((job) => (
              <div key={job.job_id} className={styles.jobCard}>
                <h3>{job.job_title}</h3>
                <p className={styles.location}>📍 {job.location}</p>
                <p className={styles.description}>
                  {job.description.substring(0, 100)}...
                </p>
                <Link
                  href={`/recruiter/jobs/${job.job_id}`}
                  className={styles.viewBtn}
                >
                  View Details
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
