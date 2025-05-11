import { getDB } from "./db.js"

/**
 * Utility functions module.
 * Exports a function for graceful shutdown of the application.
 * @param {string} signal - The signal received (e.g., SIGINT, SIGTERM).
 */
export const gracefulShutdown = async (signal, err = null) => {
  if (err)
    console.err(`Uncaught exception, gracefully shutting down: ${err.message}`);
  else
    console.log(`\nReceived ${signal}. Cleaning up...`);
  try {
    const db = await getDB();
    await db.end()
    console.log("Database connection closed.");
    process.exit(signal === "uncaughtException" ? 1 : 0);
  } catch (err) {
    console.error("Error during cleanup:", err);
    process.exit(1);
  }
}; 
