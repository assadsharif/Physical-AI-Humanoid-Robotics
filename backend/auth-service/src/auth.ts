import { betterAuth } from 'better-auth';
import { Pool } from 'pg';
import logger from './utils/logger.js';

// Validate required environment variables
const requiredEnvVars = ['DATABASE_URL'];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    logger.error(`Missing required environment variable: ${envVar}`);
    process.exit(1);
  }
}

// Create PostgreSQL connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL!,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Test database connection
pool.on('error', (err: Error) => {
  logger.error('Unexpected error on idle client', { error: err.message });
});

// Initialize better-auth with Postgres adapter
export const auth = betterAuth({
  database: pool,

  // Email and password authentication
  emailAndPassword: {
    enabled: true,
  },

  // Session configuration (24 hours)
  session: {
    expiresIn: 86400, // 24 hours in seconds
    updateAge: 3600, // Update session every hour
  },

  // Trusted origins for CORS
  trustedOrigins: (process.env.CORS_ORIGINS || 'http://localhost:3000')
    .split(',')
    .map((origin) => origin.trim()),

  // Enable experimental joins for better performance
  experimental: {
    joins: true,
  },
});

export type Auth = typeof auth;

logger.info('Better-Auth initialized successfully with PostgreSQL adapter');
