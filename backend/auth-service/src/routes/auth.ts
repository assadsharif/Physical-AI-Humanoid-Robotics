import { Router, Request, Response } from 'express';
import { auth } from '../auth.js';
import { toNodeHandler } from 'better-auth/node';
import logger from '../utils/logger.js';

const router = Router();

// Mount better-auth handler - this needs to handle all paths under /api/auth/
// It will automatically route to the appropriate better-auth endpoints
const handler = toNodeHandler(auth);

// Use the handler for all routes
router.all('*', async (req: Request, res: Response) => {
  logger.debug(`Auth endpoint: ${req.method} ${req.path}`);
  return handler(req, res);
});

export default router;
