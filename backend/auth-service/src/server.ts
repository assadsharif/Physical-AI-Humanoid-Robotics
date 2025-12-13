import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import { auth } from './auth.js';
import { toNodeHandler } from 'better-auth/node';
import { errorHandler } from './middleware/errorHandler.js';
import logger from './utils/logger.js';

// Initialize Express app
const app = express();

// Parse environment variables
const PORT = process.env.PORT || 3001;
const NODE_ENV = process.env.NODE_ENV || 'development';
const CORS_ORIGINS = (process.env.CORS_ORIGINS || 'http://localhost:3000,http://localhost:5000')
  .split(',')
  .map((origin) => origin.trim());

// Middleware: Body parser
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ limit: '10kb', extended: true }));

// Middleware: CORS - Must be before auth routes
const corsOptions = {
  origin: CORS_ORIGINS,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
};
app.use(cors(corsOptions));

// Middleware: Request logging
app.use((req: Request, res: Response, next: NextFunction) => {
  logger.debug(`${req.method} ${req.path}`);
  next();
});

// Middleware: Rate limiting
const signupLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 3, // 3 signup attempts per hour per IP
  message: 'Too many signup attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: false,
});

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 login attempts per 15 minutes per IP
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: false,
});

// Apply rate limiting to specific endpoints
app.use('/api/auth/sign-up', signupLimiter);
app.use('/api/auth/sign-in', loginLimiter);

// Mount better-auth handler - MUST be before custom routes
const authHandler = toNodeHandler(auth);
app.use('/api/auth', authHandler);

// Health check endpoint
app.get('/api/health', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'healthy',
    database: 'connected',
    timestamp: new Date().toISOString(),
  });
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
  res.status(200).json({
    name: 'Better-Auth Service',
    version: '1.0.0',
    status: 'running',
    endpoints: {
      auth: '/api/auth',
      health: '/api/health',
      docs: 'https://www.better-auth.com/docs',
    },
  });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({
    code: 'NOT_FOUND',
    message: `Endpoint not found: ${req.method} ${req.path}`,
  });
});

// Error handling middleware (must be last)
app.use(errorHandler);

// Server startup
const server = app.listen(PORT, () => {
  logger.info(`Auth service listening on port ${PORT}`);
  logger.info(`Environment: ${NODE_ENV}`);
  logger.info(`CORS origins: ${CORS_ORIGINS.join(', ')}`);
  logger.info('Ready to accept requests');
});

// Graceful shutdown
const gracefulShutdown = () => {
  logger.info('Shutting down gracefully...');
  server.close(() => {
    logger.info('Server closed');
    process.exit(0);
  });

  // Force shutdown after 10 seconds
  setTimeout(() => {
    logger.error('Forced shutdown due to timeout');
    process.exit(1);
  }, 10000);
};

process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

// Unhandled rejection handler
process.on('unhandledRejection', (reason: any, promise: Promise<any>) => {
  logger.error('Unhandled Rejection', {
    reason: reason instanceof Error ? reason.message : String(reason),
    promise: String(promise),
  });
});

// Uncaught exception handler
process.on('uncaughtException', (error: Error) => {
  logger.error('Uncaught Exception', {
    message: error.message,
    stack: error.stack,
  });
  process.exit(1);
});

export default app;
