import sqlite3
import logging
from typing import List

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_table_info(conn: sqlite3.Connection, table: str) -> List[tuple]:
    """Get detailed information about table columns"""
    cursor = conn.execute(f"PRAGMA table_info({table})")
    return cursor.fetchall()

def run_migration(db_path: str = "quotes.db"):
    logger.info(f"Running migration on database: {db_path}")
    
    with open("migration.sql", "r") as f:
        migration_sql = f.read()
    
    try:
        with sqlite3.connect(db_path) as conn:
            # Show current schema
            logger.info("Current table schema:")
            for col in get_table_info(conn, "quotepost"):
                logger.info(f"Column: {col}")
            
            # Execute each statement separately for better error reporting
            for statement in migration_sql.split(';'):
                if statement.strip():
                    logger.debug(f"Executing: {statement.strip()}")
                    try:
                        conn.execute(statement)
                    except sqlite3.Error as e:
                        logger.error(f"Failed to execute: {statement.strip()}")
                        logger.error(f"Error: {e}")
                        raise
            
            conn.commit()
            
            # Verify the changes
            logger.info("Updated table schema:")
            for col in get_table_info(conn, "quotepost"):
                logger.info(f"Column: {col}")
            
            logger.info("Migration completed successfully")
            
    except sqlite3.Error as e:
        logger.error(f"Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migration() 