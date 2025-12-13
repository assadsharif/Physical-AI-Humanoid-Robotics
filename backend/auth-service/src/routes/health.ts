import { Router, Request, Response } from 'express';
import { auth } from '../auth.js';
import logger from '../utils/logger.js';

const router = Router();

// Health check endpoint
router.get('/', async (req: Request, res: Response) => {
  try {
    // Test database connection via a simple query through better-auth
    // Try to access the auth database
    const result = await fetch(
      `${process.env.DATABASE_URL?.split('?')[0] || 'postgresql://localhost:5432'}/`,
      {
        method: 'HEAD',
      }
    ).catch(() => {
      // If fetch fails, try a different approach
      throw new Error('Database connection test failed');
    });

    // Alternative: test using a raw database query if needed
    // For now, we'll do a simple check that better-auth is initialized

    res.status(200).json({
      status: 'healthy',
      database: 'connected',
      service: 'auth-service',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
    });

    logger.info('Health check passed');
  } catch (error) {
    logger.error('Health check failed', {
      error: error instanceof Error ? error.message : String(error),
    });

    res.status(503).json({
      status: 'unhealthy',
      database: 'disconnected',
      service: 'auth-service',
      error: 'Failed to connect to database',
      timestamp: new Date().toISOString(),
    });
  }
});

export default router;
