import { Router, Request, Response, NextFunction } from 'express';
import { auth } from '../auth.js';
import { toNodeHandler } from 'better-auth/node';
import logger from '../utils/logger.js';

const router = Router();

// Mount better-auth handler for all auth endpoints
// This handles: sign-up, sign-in, sign-out, refresh, session, etc.
// The toNodeHandler converts better-auth's Web Standard API to Node.js/Express
router.use(toNodeHandler(auth));

// Log all auth endpoints
router.use((req: Request, res: Response, next: NextFunction) => {
  if (res.statusCode !== 404) {
    logger.debug(`Auth endpoint: ${req.method} ${req.path}`);
  }
  next();
});

export default router;
