import Link from 'next/link';
import styles from './Home.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <span className={styles.highlight}>Job Portal</span>
        </h1>

        <p className={styles.description}>
          AI-powered platform connecting talented job seekers with top recruiters
        </p>

        <div className={styles.features}>
          <div className={styles.feature}>
            <h3>🤖 AI-Powered Matching</h3>
            <p>Smart algorithms match candidates with perfect job opportunities</p>
          </div>

          <div className={styles.feature}>
            <h3>📄 Resume Parser</h3>
            <p>Automatic extraction of skills and experience from resumes</p>
          </div>

          <div className={styles.feature}>
            <h3>🎯 Intelligent Search</h3>
            <p>Natural language job search powered by AI</p>
          </div>
        </div>

        <div className={styles.actions}>
          <Link href="/auth/register" className="btn btn-primary">
            Get Started
          </Link>
          <Link href="/auth/login" className="btn btn-outline">
            Sign In
          </Link>
        </div>
      </main>
    </div>
  );
}
