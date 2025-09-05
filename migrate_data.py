"""
Data Migration Script for NoSQL Backend
Migrates data from CSV/JSON files to MongoDB collections
"""

import os
import sys
import pandas as pd
import json
import logging
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_collection, COLLECTIONS, init_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_college_data():
    """Migrate college data from CSV to MongoDB"""
    try:
        logger.info("Starting college data migration...")
        
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'college_list.csv')
        if not os.path.exists(csv_path):
            logger.warning(f"College CSV not found at {csv_path}")
            return False
        
        # Import here to avoid module-level initialization issues
        from database import get_collection, COLLECTIONS
        collection = get_collection(COLLECTIONS['colleges'])
        
        # Check if data already exists
        try:
            count = collection.count_documents({})
            if count > 0:
                logger.info("College data already exists in MongoDB")
                return True
        except Exception as e:
            logger.warning(f"Could not check existing data: {e}")
            # Continue with migration
        
        # Load and migrate data
        df = pd.read_csv(csv_path)
        colleges = df.to_dict('records')
        
        # Add metadata
        for college in colleges:
            college['created_at'] = pd.Timestamp.now()
            college['updated_at'] = pd.Timestamp.now()
        
        if len(colleges) > 0:
            collection.insert_many(colleges)
            logger.info(f"Migrated {len(colleges)} colleges to MongoDB")
            return True
        
    except Exception as e:
        logger.error(f"Error migrating college data: {e}")
        return False

def migrate_course_data():
    """Migrate course data from CSV to MongoDB"""
    try:
        logger.info("Starting course data migration...")
        
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'courseAndCollegedata.csv')
        if not os.path.exists(csv_path):
            logger.warning(f"Course CSV not found at {csv_path}")
            return False
        
        # Import here to avoid module-level initialization issues
        from database import get_collection, COLLECTIONS
        collection = get_collection(COLLECTIONS['courses'])
        
        # Check if data already exists
        try:
            count = collection.count_documents({})
            if count > 0:
                logger.info("Course data already exists in MongoDB")
                return True
        except Exception as e:
            logger.warning(f"Could not check existing data: {e}")
            # Continue with migration
        
        # Load and migrate data
        df = pd.read_csv(csv_path)
        courses = df.to_dict('records')
        
        # Add metadata
        for course in courses:
            course['created_at'] = pd.Timestamp.now()
            course['updated_at'] = pd.Timestamp.now()
        
        if len(courses) > 0:
            collection.insert_many(courses)
            logger.info(f"Migrated {len(courses)} courses to MongoDB")
            return True
        
    except Exception as e:
        logger.error(f"Error migrating course data: {e}")
        return False

def migrate_news_data():
    """Migrate news data from CSV to MongoDB"""
    try:
        logger.info("Starting news data migration...")
        
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'news_data.csv')
        if not os.path.exists(csv_path):
            logger.warning(f"News CSV not found at {csv_path}")
            return False
        
        # Import here to avoid module-level initialization issues
        from database import get_collection, COLLECTIONS
        collection = get_collection(COLLECTIONS['news_articles'])
        
        # Check if data already exists
        try:
            count = collection.count_documents({})
            if count > 0:
                logger.info("News data already exists in MongoDB")
                return True
        except Exception as e:
            logger.warning(f"Could not check existing data: {e}")
            # Continue with migration
        
        # Load and migrate data
        df = pd.read_csv(csv_path)
        articles = df.to_dict('records')
        
        # Add metadata
        for article in articles:
            article['created_at'] = pd.Timestamp.now()
            article['updated_at'] = pd.Timestamp.now()
            article['views'] = 0
            article['likes'] = 0
        
        if len(articles) > 0:
            collection.insert_many(articles)
            logger.info(f"Migrated {len(articles)} news articles to MongoDB")
            return True
        
    except Exception as e:
        logger.error(f"Error migrating news data: {e}")
        return False

def migrate_scholarship_data():
    """Migrate scholarship data from JSON to MongoDB"""
    try:
        logger.info("Starting scholarship data migration...")
        
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'scholarship.json')
        if not os.path.exists(json_path):
            logger.warning(f"Scholarship JSON not found at {json_path}")
            return False
        
        # Import here to avoid module-level initialization issues
        from database import get_collection, COLLECTIONS
        collection = get_collection(COLLECTIONS['scholarships'])
        
        # Check if data already exists
        try:
            count = collection.count_documents({})
            if count > 0:
                logger.info("Scholarship data already exists in MongoDB")
                return True
        except Exception as e:
            logger.warning(f"Could not check existing data: {e}")
            # Continue with migration
        
        # Load and migrate data
        with open(json_path, 'r') as f:
            scholarships = json.load(f)
        
        # Ensure it's a list
        if isinstance(scholarships, dict):
            scholarships = [scholarships]
        
        # Add metadata
        for scholarship in scholarships:
            scholarship['created_at'] = pd.Timestamp.now()
            scholarship['updated_at'] = pd.Timestamp.now()
            scholarship['views'] = 0
            scholarship['applications'] = 0
        
        if len(scholarships) > 0:
            collection.insert_many(scholarships)
            logger.info(f"Migrated {len(scholarships)} scholarships to MongoDB")
            return True
        
    except Exception as e:
        logger.error(f"Error migrating scholarship data: {e}")
        return False

def create_indexes():
    """Create database indexes for better performance"""
    try:
        logger.info("Creating database indexes...")
        
        # Import here to avoid module-level initialization issues
        from database import get_collection, COLLECTIONS
        
        # College indexes
        colleges = get_collection(COLLECTIONS['colleges'])
        colleges.create_index("college_name")
        colleges.create_index("state")
        colleges.create_index("course_type")
        
        # Course indexes
        courses = get_collection(COLLECTIONS['courses'])
        courses.create_index("course_name")
        courses.create_index("college_name")
        courses.create_index("state")
        
        # News indexes
        news = get_collection(COLLECTIONS['news_articles'])
        news.create_index("RIASEC_Type")
        news.create_index("Category")
        news.create_index("Title")
        
        # Scholarship indexes
        scholarships = get_collection(COLLECTIONS['scholarships'])
        scholarships.create_index("field")
        scholarships.create_index("location")
        
        # Career session indexes
        sessions = get_collection(COLLECTIONS['career_sessions'])
        sessions.create_index("session_id")
        sessions.create_index("user_id")
        sessions.create_index("created_at")
        
        logger.info("Database indexes created successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
        return False

def verify_migration():
    """Verify that all data has been migrated successfully"""
    try:
        logger.info("Verifying data migration...")
        
        # Import here to avoid module-level initialization issues
        from database import get_collection, COLLECTIONS
        
        collections_data = {}
        
        for collection_name, collection_key in COLLECTIONS.items():
            collection = get_collection(collection_key)
            try:
                count = collection.count_documents({})
                collections_data[collection_name] = count
                logger.info(f"{collection_name}: {count} documents")
            except Exception as e:
                logger.error(f"Error counting {collection_name}: {e}")
                collections_data[collection_name] = 0
        
        return collections_data
        
    except Exception as e:
        logger.error(f"Error verifying migration: {e}")
        return None

def main():
    """Main migration function"""
    print("🚀 Starting NoSQL Data Migration")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize database
    init_database()
    
    # Run migrations
    migrations = [
        ("Colleges", migrate_college_data),
        ("Courses", migrate_course_data),
        ("News Articles", migrate_news_data),
        ("Scholarships", migrate_scholarship_data)
    ]
    
    successful_migrations = 0
    
    for name, migration_func in migrations:
        print(f"\n📦 Migrating {name}...")
        if migration_func():
            print(f"✅ {name} migration completed")
            successful_migrations += 1
        else:
            print(f"❌ {name} migration failed")
    
    # Create indexes
    print(f"\n🔍 Creating database indexes...")
    if create_indexes():
        print("✅ Indexes created successfully")
    else:
        print("❌ Index creation failed")
    
    # Verify migration
    print(f"\n🔎 Verifying migration...")
    verification_data = verify_migration()
    
    if verification_data:
        print("✅ Migration verification completed")
        total_documents = sum(verification_data.values())
        print(f"📊 Total documents in database: {total_documents}")
    else:
        print("❌ Migration verification failed")
    
    print("\n" + "=" * 50)
    print(f"🎉 Migration completed: {successful_migrations}/{len(migrations)} successful")
    
    if successful_migrations == len(migrations):
        print("✅ All migrations completed successfully!")
        print("🚀 Your NoSQL backend is ready to use!")
    else:
        print("⚠️  Some migrations failed. Check the logs above.")
    
    print("\n💡 Next steps:")
    print("1. Start the Flask application: python app.py")
    print("2. Test the APIs: python test_api.py")
    print("3. Check the API documentation for endpoint details")

if __name__ == "__main__":
    main()
