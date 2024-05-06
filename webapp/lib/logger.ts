// logger.ts
import winston from "winston";

let LoggingWinston;
if (typeof window === "undefined") {
  LoggingWinston = require("@google-cloud/logging-winston").LoggingWinston;
}

const logger = winston.createLogger({
  level: "info",
  format: winston.format.simple(),
  transports: [
    new winston.transports.Console(), // Transport pour la console en mode local
    LoggingWinston
      ? new LoggingWinston({
          logName: "augmented-chatbot-webapp",
        })
      : null, // Transport pour Google Cloud Logging en production
  ].filter(Boolean), // Supprimez les éléments null du tableau
});

export default logger;
