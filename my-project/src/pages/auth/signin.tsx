import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import styles from './auth.module.css';

export default function SignIn(): ReactNode {
  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div className={clsx('container', styles.authContainer)}>
        <div className={styles.authCard}>
          <h1>Sign In</h1>
          <p className={styles.subtitle}>Welcome back! Sign in to your account to access personalized content.</p>

          <form className={styles.authForm}>
            <div className={styles.formGroup}>
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                placeholder="your@email.com"
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                placeholder="••••••••"
                required
              />
            </div>

            <button type="submit" className={clsx('button', styles.submitBtn)}>
              Sign In
            </button>
          </form>

          <div className={styles.authFooter}>
            <p>
              Don't have an account?{' '}
              <a href="/auth/signup" className={styles.link}>
                Sign up here
              </a>
            </p>
          </div>

          <div className={styles.comingSoon}>
            <p>
              <strong>Note:</strong> Authentication is currently under development.
              The auth service will be integrated in the next phase.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
