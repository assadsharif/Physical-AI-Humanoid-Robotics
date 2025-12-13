import winston from 'winston';

// Create logger instance with JSON format for structured logging
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'auth-service' },
  transports: [
    // Console output
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.printf(
          ({ level, message, timestamp, service, ...meta }) => {
            const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : '';
            return `${timestamp} [${service}] ${level}: ${message} ${metaStr}`;
          }
        )
      ),
    }),
    // Error log file (if needed in future)
    // new winston.transports.File({ filename: 'error.log', level: 'error' }),
    // Combined log file (if needed in future)
    // new winston.transports.File({ filename: 'combined.log' }),
  ],
});

export default logger;
