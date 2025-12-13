import type {ReactNode} from 'react';
import {useState} from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import styles from './auth.module.css';

export default function SignIn(): ReactNode {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Use environment variable or default to localhost for development
      const authServiceUrl = process.env.REACT_APP_AUTH_SERVICE_URL || 'http://localhost:3001';

      const response = await fetch(`${authServiceUrl}/api/auth/sign-in`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          email: email.trim(),
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Sign in failed');
      }

      const data = await response.json();

      // Store JWT token in localStorage
      if (data.session?.token) {
        localStorage.setItem('authToken', data.session.token);
      }

      // Store user info
      if (data.user) {
        localStorage.setItem('user', JSON.stringify(data.user));
      }

      // Redirect to home
      window.location.href = '/';
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div className={clsx('container', styles.authContainer)}>
        <div className={styles.authCard}>
          <h1>Sign In</h1>
          <p className={styles.subtitle}>Welcome back! Sign in to your account to access personalized content.</p>

          {error && <div className={styles.errorMessage}>{error}</div>}

          <form className={styles.authForm} onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className={clsx('button', styles.submitBtn)}
              disabled={loading}
            >
              {loading ? 'Signing In...' : 'Sign In'}
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
        </div>
      </div>
    </Layout>
  );
}
