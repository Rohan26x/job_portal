'use client';

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import styles from './Header.module.css';

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          Job Portal
        </Link>

        <nav className={styles.nav}>
          {user ? (
            <>
              <span className={styles.userInfo}>
                {user.email}
              </span>
              <button onClick={logout} className={styles.logoutBtn}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/auth/login" className={styles.navLink}>
                Login
              </Link>
              <Link href="/auth/register" className={styles.navLink}>
                Sign Up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
