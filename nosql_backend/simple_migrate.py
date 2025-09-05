#!/usr/bin/env python3
"""
Simple Data Migration Script
Manually migrates data to MongoDB to avoid import issues
"""

import os
import pandas as pd
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_data():
    """Simple data migration"""
    print("🚀 Starting Simple Data Migration")
    print("=" * 50)

    # Add current directory to path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    try:
        # Import database functions
        from database import init_database, get_collection, COLLECTIONS

        # Initialize database
        print("📡 Initializing database connection...")
        init_database()
        print("✅ Database connected")

        # Migrate colleges
        print("\n📦 Migrating Colleges...")
        csv_path = os.path.join('data', 'college_list.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            colleges = df.to_dict('records')

            collection = get_collection(COLLECTIONS['colleges'])
            if len(colleges) > 0:
                collection.insert_many(colleges)
                print(f"✅ Migrated {len(colleges)} colleges")
            else:
                print("❌ No college data to migrate")
        else:
            print(f"❌ College CSV not found at {csv_path}")

        # Migrate courses
        print("\n📦 Migrating Courses...")
        csv_path = os.path.join('data', 'courseAndCollegedata.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            courses = df.to_dict('records')

            collection = get_collection(COLLECTIONS['courses'])
            if len(courses) > 0:
                collection.insert_many(courses)
                print(f"✅ Migrated {len(courses)} courses")
            else:
                print("❌ No course data to migrate")
        else:
            print(f"❌ Course CSV not found at {csv_path}")

        # Migrate news
        print("\n📦 Migrating News Articles...")
        csv_path = os.path.join('data', 'news_data.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            articles = df.to_dict('records')

            collection = get_collection(COLLECTIONS['news_articles'])
            if len(articles) > 0:
                collection.insert_many(articles)
                print(f"✅ Migrated {len(articles)} news articles")
            else:
                print("❌ No news data to migrate")
        else:
            print(f"❌ News CSV not found at {csv_path}")

        # Migrate scholarships
        print("\n📦 Migrating Scholarships...")
        json_path = os.path.join('data', 'scholarship.json')
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                scholarships = json.load(f)

            if isinstance(scholarships, dict):
                scholarships = [scholarships]

            collection = get_collection(COLLECTIONS['scholarships'])
            if len(scholarships) > 0:
                collection.insert_many(scholarships)
                print(f"✅ Migrated {len(scholarships)} scholarships")
            else:
                print("❌ No scholarship data to migrate")
        else:
            print(f"❌ Scholarship JSON not found at {json_path}")

        print("\n🎉 Data migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate_data()
