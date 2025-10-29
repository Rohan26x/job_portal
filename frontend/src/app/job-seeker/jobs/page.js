'use client';

import { useState, useEffect } from 'react';
import { jobAPI } from '@/lib/api';
import styles from './Jobs.module.css';
import Link from 'next/link';

export default function JobSeekerJobsPage() {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [locationFilter, setLocationFilter] = useState('');

  useEffect(() => {
    fetchJobs();
  }, []);

  useEffect(() => {
    filterJobs();
  }, [searchTerm, locationFilter, jobs]);

  const fetchJobs = async () => {
    try {
      const response = await jobAPI.getAllJobs();
      setJobs(response.data);
      setFilteredJobs(response.data);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterJobs = () => {
    let filtered = jobs;

    if (searchTerm) {
      filtered = filtered.filter(job =>
        job.job_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (locationFilter) {
      filtered = filtered.filter(job =>
        job.location.toLowerCase().includes(locationFilter.toLowerCase())
      );
    }

    setFilteredJobs(filtered);
  };

  if (loading) {
    return <div className={styles.loading}>Loading jobs...</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Browse Jobs</h1>

      <div className={styles.filters}>
        <input
          type="text"
          placeholder="Search by title or description..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className={styles.searchInput}
        />
        <input
          type="text"
          placeholder="Filter by location..."
          value={locationFilter}
          onChange={(e) => setLocationFilter(e.target.value)}
          className={styles.searchInput}
        />
      </div>

      {filteredJobs.length === 0 ? (
        <div className={styles.emptyState}>
          <p>No jobs found matching your criteria</p>
        </div>
      ) : (
        <div className={styles.jobsList}>
          {filteredJobs.map((job) => (
            <div key={job.job_id} className={styles.jobCard}>
              <h2>{job.job_title}</h2>
              <p className={styles.location}>📍 {job.location}</p>
              <p className={styles.description}>
                {job.description.substring(0, 200)}...
              </p>
              <Link
                href={`/job-seeker/jobs/${job.job_id}`}
                className={styles.viewBtn}
              >
                View Details & Apply
              </Link>
            </div>
          ))}
        </div>
      )}

      <div className={styles.resultsCount}>
        Showing {filteredJobs.length} of {jobs.length} jobs
      </div>
    </div>
  );
}
