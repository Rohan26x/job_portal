'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import Header from '@/components/common/Header';
import styles from './JobSeekerLayout.module.css';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function JobSeekerLayout({ children }) {
  const pathname = usePathname();

  const navItems = [
    { href: '/job-seeker/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/job-seeker/search', label: 'AI Job Search', icon: '🔍' },
    { href: '/job-seeker/jobs', label: 'Browse Jobs', icon: '💼' },
    { href: '/job-seeker/applications', label: 'My Applications', icon: '📝' },
    { href: '/job-seeker/resume', label: 'My Resume', icon: '📄' },
    { href: '/job-seeker/profile', label: 'Profile', icon: '👤' },
  ];

  return (
    <ProtectedRoute requiredRole="job_seeker">
      <Header />
      <div className={styles.layout}>
        <aside className={styles.sidebar}>
          <h2 className={styles.sidebarTitle}>Job Seeker Portal</h2>
          <nav className={styles.nav}>
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`${styles.navItem} ${pathname === item.href ? styles.active : ''}`}
              >
                <span className={styles.icon}>{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>
        <main className={styles.main}>
          {children}
        </main>
      </div>
    </ProtectedRoute>
  );
}
