"""
MongoDB Database Configuration and Connection
"""
import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self._connect()

    def _connect(self):
        """Connect to MongoDB Atlas"""
        try:
            mongodb_url = os.getenv('MONGODB_URI')
            database_name = os.getenv('DATABASE_NAME', 'education_platform')
            
            if not mongodb_url:
                raise ValueError("MONGODB_URI environment variable is not set")
            
            self.client = MongoClient(mongodb_url)
            self.db = self.client[database_name]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"✅ Connected to MongoDB database: {database_name}")
            
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise

    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection from the database"""
        if self.db is None:
            raise RuntimeError("Database not connected")
        return self.db[collection_name]

    def health_check(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            # Ping the database
            self.client.admin.command('ping')
            
            # Get database stats
            stats = self.db.command("dbStats")
            
            return {
                "status": "healthy",
                "database": self.db.name,
                "collections": len(self.db.list_collection_names()),
                "dataSize": stats.get("dataSize", 0),
                "storageSize": stats.get("storageSize", 0),
                "indexes": stats.get("indexes", 0),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Global MongoDB instance (initialize later)
mongodb = None

# Collection names
COLLECTIONS = {
    'career_sessions': 'career_sessions',
    'career_answers': 'career_answers',
    'colleges': 'colleges',
    'courses': 'courses',
    'news_articles': 'news_articles',
    'scholarships': 'scholarships',
    'users': 'users'
}

def get_db() -> Database:
    """Get database instance"""
    if mongodb is None:
        init_database()
    return mongodb.db

def get_collection(name: str) -> Collection:
    """Get collection by name"""
    if mongodb is None:
        init_database()
    return mongodb.get_collection(name)

def init_database():
    """Initialize the database connection"""
    global mongodb
    if mongodb is None:
        mongodb = MongoDB()
    return mongodb

def get_database():
    """Get database instance (alternative name)"""
    if mongodb is None:
        init_database()
    return mongodb.db

def close_database():
    """Close database connection"""
    global mongodb
    if mongodb and mongodb.client:
        mongodb.client.close()
        logger.info("Database connection closed")
