import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import styles from './auth.module.css';

export default function SignUp(): ReactNode {
  return (
    <Layout title="Sign Up" description="Create your account">
      <div className={clsx('container', styles.authContainer)}>
        <div className={styles.authCard}>
          <h1>Sign Up</h1>
          <p className={styles.subtitle}>Create an account to personalize your learning experience with adaptive content.</p>

          <form className={styles.authForm}>
            <div className={styles.formGroup}>
              <label htmlFor="name">Full Name</label>
              <input
                type="text"
                id="name"
                name="name"
                placeholder="John Doe"
                required
              />
            </div>

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
              <small>Password must be at least 8 characters</small>
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                placeholder="••••••••"
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="experience">Software Experience Level (Optional)</label>
              <select id="experience" name="experience">
                <option value="">Select your experience level...</option>
                <option value="beginner">Beginner - New to programming</option>
                <option value="intermediate">Intermediate - Some experience</option>
                <option value="advanced">Advanced - Extensive experience</option>
              </select>
              <small>This helps us personalize content for you</small>
            </div>

            <button type="submit" className={clsx('button', styles.submitBtn)}>
              Create Account
            </button>
          </form>

          <div className={styles.authFooter}>
            <p>
              Already have an account?{' '}
              <a href="/auth/signin" className={styles.link}>
                Sign in here
              </a>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
