#!/usr/bin/env python3
"""
Database connection and setup test
"""
import os
from database import SessionLocal, CareerSession, CareerAnswer, create_tables

def test_database_connection():
    """Test database connection"""
    try:
        print("🔍 Testing database connection...")
        db = SessionLocal()
        
        # Test basic query
        sessions = db.query(CareerSession).count()
        print(f"✅ Database connected! Found {sessions} sessions")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_create_tables():
    """Test table creation"""
    try:
        print("🏗️ Creating database tables...")
        create_tables()
        print("✅ Tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def test_database_operations():
    """Test basic database operations"""
    try:
        print("🧪 Testing database operations...")
        db = SessionLocal()
        
        # Test session creation
        from uuid import uuid4
        session_id = str(uuid4())
        
        new_session = CareerSession(
            id=session_id,
            completed=0,
            current_question=0,
            realistic_score=0,
            investigative_score=0,
            artistic_score=0,
            social_score=0,
            enterprising_score=0,
            conventional_score=0
        )
        
        db.add(new_session)
        db.commit()
        
        # Test retrieval
        retrieved = db.query(CareerSession).filter(CareerSession.id == session_id).first()
        if retrieved:
            print(f"✅ Database operations successful! Session: {session_id}")
            
            # Cleanup
            db.delete(retrieved)
            db.commit()
        else:
            print("❌ Failed to retrieve test session")
            
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database operations failed: {e}")
        return False

if __name__ == "__main__":
    print("🗄️ Database Integration Test")
    print("=" * 50)
    
    # Check environment variables
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL environment variable not set")
        print("Please run: export $(grep -v '^#' .env | xargs)")
        exit(1)
    
    print(f"Database URL: {db_url[:50]}...")
    
    # Run tests
    if test_database_connection():
        if test_create_tables():
            if test_database_operations():
                print("\n✅ All database tests passed!")
            else:
                print("\n❌ Database operations test failed")
        else:
            print("\n❌ Table creation test failed")
    else:
        print("\n❌ Database connection test failed")
