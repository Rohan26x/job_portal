'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import Header from '@/components/common/Header';
import styles from './RecruiterLayout.module.css';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function RecruiterLayout({ children }) {
  const pathname = usePathname();

  const navItems = [
    { href: '/recruiter/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/recruiter/post-job', label: 'Post Job', icon: '➕' },
    { href: '/recruiter/jobs', label: 'My Jobs', icon: '💼' },
    { href: '/recruiter/applications', label: 'Applications', icon: '📝' },
    { href: '/recruiter/profile', label: 'Profile', icon: '👤' },
  ];

  return (
    <ProtectedRoute requiredRole="recruiter">
      <Header />
      <div className={styles.layout}>
        <aside className={styles.sidebar}>
          <h2 className={styles.sidebarTitle}>Recruiter Portal</h2>
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
