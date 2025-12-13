import { Router, Request, Response } from 'express';
import { auth } from '../auth.js';
import logger from '../utils/logger.js';

const router = Router();

// Handle sign-up endpoint
router.post('/sign-up', async (req: Request, res: Response) => {
  try {
    logger.debug('Sign-up request received', { email: req.body.email });

    const { email, password, name } = req.body;

    // Validate input
    if (!email || !password || !name) {
      return res.status(400).json({
        error: 'Missing required fields: email, password, name',
      });
    }

    if (password.length < 8) {
      return res.status(400).json({
        error: 'Password must be at least 8 characters',
      });
    }

    // Call better-auth to create user - using correct API format
    const data = await auth.api.signUpEmail({
      body: {
        email: email.trim(),
        password,
        name: name.trim(),
      },
    });

    // Check if token exists (successful signup)
    if (data.token) {
      logger.info('User signed up successfully', { email });
      return res.status(200).json({
        user: data.user,
        session: {
          token: data.token,
        },
      });
    } else if (data.user) {
      // User created but no token (might need email verification)
      logger.info('User signed up but needs verification', { email });
      return res.status(200).json({
        user: data.user,
        session: data.token ? { token: data.token } : null,
      });
    } else {
      logger.warn('Sign-up failed', { email });
      return res.status(400).json({
        error: 'Failed to create account',
      });
    }
  } catch (error) {
    logger.error('Sign-up error', {
      error: error instanceof Error ? error.message : String(error),
    });
    return res.status(500).json({
      error: 'Internal server error during sign-up',
    });
  }
});

// Handle sign-in endpoint
router.post('/sign-in', async (req: Request, res: Response) => {
  try {
    logger.debug('Sign-in request received', { email: req.body.email });

    const { email, password } = req.body;

    // Validate input
    if (!email || !password) {
      return res.status(400).json({
        error: 'Missing required fields: email, password',
      });
    }

    // Call better-auth to sign in - using correct API format
    const data = await auth.api.signInEmail({
      body: {
        email: email.trim(),
        password,
      },
    });

    // Check if token exists (successful signin)
    if (data.token) {
      logger.info('User signed in successfully', { email });
      return res.status(200).json({
        user: data.user,
        session: {
          token: data.token,
        },
      });
    } else {
      logger.warn('Sign-in failed', { email });
      return res.status(401).json({
        error: 'Invalid credentials',
      });
    }
  } catch (error) {
    logger.error('Sign-in error', {
      error: error instanceof Error ? error.message : String(error),
    });
    return res.status(500).json({
      error: 'Invalid credentials',
    });
  }
});

// Handle sign-out endpoint
router.post('/sign-out', async (req: Request, res: Response) => {
  try {
    logger.debug('Sign-out request received');

    // Just return success for now
    return res.status(200).json({
      ok: true,
      message: 'Signed out successfully',
    });
  } catch (error) {
    logger.error('Sign-out error', {
      error: error instanceof Error ? error.message : String(error),
    });
    return res.status(500).json({
      error: 'Internal server error during sign-out',
    });
  }
});

// Handle session endpoint
router.get('/session', async (req: Request, res: Response) => {
  try {
    logger.debug('Session request received');

    // Return null session for now (user not authenticated)
    return res.status(200).json(null);
  } catch (error) {
    logger.error('Session error', {
      error: error instanceof Error ? error.message : String(error),
    });
    return res.status(500).json({
      error: 'Internal server error',
    });
  }
});

export default router;
