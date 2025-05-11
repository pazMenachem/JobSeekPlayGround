import pg from 'pg';
import dotenv from 'dotenv'

dotenv.config()

const db = new pg.Client({
    user: process.env.PG_USER,
    host: process.env.PG_HOST,
    database: process.env.PG_DATABASE,
    password: process.env.PG_PASSWORD,
    port: process.env.PG_PORT
});

/**
 * Establishes and returns a connection to the PostgreSQL database.
 * Ensures a single connection instance is used throughout the application.
 * 
 * @returns {Promise<pg.Client>} - A promise that resolves to the connected database client.
 * @throws {Error} - Throws an error if the connection fails.
 */
export const getDB = async () => {
    if (!db._connected) {
        try {
            await db.connect();
            db._connected = true;
        } 
        catch (err) {
            console.log(`Error connecting to Database: ${err.message}`);
            throw err;
        }
    }
    return db;
};