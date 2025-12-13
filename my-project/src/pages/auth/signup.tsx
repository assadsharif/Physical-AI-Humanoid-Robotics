import type {ReactNode} from 'react';
import {useState} from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import styles from './auth.module.css';

export default function SignUp(): ReactNode {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [experience, setExperience] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // Validate password length
    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      const authServiceUrl = 'http://localhost:3001';

      const response = await fetch(`${authServiceUrl}/api/auth/sign-up`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          email: email.trim(),
          password,
          name: name.trim(),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Sign up failed');
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

      // Store experience level if provided
      if (experience) {
        localStorage.setItem('experienceLevel', experience);
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
    <Layout title="Sign Up" description="Create your account">
      <div className={clsx('container', styles.authContainer)}>
        <div className={styles.authCard}>
          <h1>Sign Up</h1>
          <p className={styles.subtitle}>Create an account to personalize your learning experience with adaptive content.</p>

          {error && <div className={styles.errorMessage}>{error}</div>}

          <form className={styles.authForm} onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
              <label htmlFor="name">Full Name</label>
              <input
                type="text"
                id="name"
                name="name"
                placeholder="John Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
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
              <small>Password must be at least 8 characters</small>
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="experience">Software Experience Level (Optional)</label>
              <select
                id="experience"
                name="experience"
                value={experience}
                onChange={(e) => setExperience(e.target.value)}
              >
                <option value="">Select your experience level...</option>
                <option value="beginner">Beginner - New to programming</option>
                <option value="intermediate">Intermediate - Some experience</option>
                <option value="advanced">Advanced - Extensive experience</option>
              </select>
              <small>This helps us personalize content for you</small>
            </div>

            <button
              type="submit"
              className={clsx('button', styles.submitBtn)}
              disabled={loading}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
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
