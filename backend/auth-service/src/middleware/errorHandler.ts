import { Request, Response, NextFunction } from 'express';
import logger from '../utils/logger.js';

// Custom error class
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public isOperational: boolean = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

// Express error handler middleware
export const errorHandler = (
  err: Error | AppError,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  // Log error details
  if (err instanceof AppError) {
    logger.error({
      message: err.message,
      code: err.code,
      statusCode: err.statusCode,
      endpoint: req.path,
      method: req.method,
      timestamp: new Date().toISOString(),
    });
  } else {
    logger.error({
      message: err.message,
      stack: err.stack,
      endpoint: req.path,
      method: req.method,
      timestamp: new Date().toISOString(),
    });
  }

  // Handle known errors
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      code: err.code,
      message: err.message,
    });
    return;
  }

  // Handle better-auth specific errors
  if (err.message?.includes('already exists')) {
    res.status(400).json({
      code: 'EMAIL_EXISTS',
      message: 'Email already registered',
    });
    return;
  }

  if (err.message?.includes('password')) {
    res.status(400).json({
      code: 'INVALID_PASSWORD',
      message: 'Password does not meet requirements (min 8 chars, must include uppercase, lowercase, number, special char)',
    });
    return;
  }

  if (err.message?.includes('invalid') || err.message?.includes('credentials')) {
    // Generic message to prevent email enumeration
    res.status(401).json({
      code: 'INVALID_CREDENTIALS',
      message: 'Invalid email or password',
    });
    return;
  }

  // Database connection errors
  if (err.message?.includes('connect') || err.message?.includes('ECONNREFUSED')) {
    res.status(503).json({
      code: 'DATABASE_ERROR',
      message: 'Service temporarily unavailable',
    });
    return;
  }

  // Default error response
  const statusCode = (err as any).statusCode || 500;
  const isDevelopment = process.env.NODE_ENV === 'development';

  res.status(statusCode).json({
    code: 'INTERNAL_SERVER_ERROR',
    message: isDevelopment ? err.message : 'An unexpected error occurred',
    ...(isDevelopment && { stack: err.stack }),
  });
};

// Async error wrapper for route handlers
export const asyncHandler = (
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};
