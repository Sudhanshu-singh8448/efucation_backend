#!/usr/bin/env python3
"""
Neon PostgreSQL Setup Helper
"""

import os

def main():
    print("🔧 Neon PostgreSQL Setup Helper")
    print("=" * 40)
    print()

    print("📋 To get your Neon connection string:")
    print("1. Go to https://console.neon.tech/")
    print("2. Select your project")
    print("3. Go to 'Connection Details' tab")
    print("4. Copy the 'Connection string' (it should look like this):")
    print("   postgresql://username:password@hostname/database?sslmode=require")
    print()

    connection_string = input("🔗 Paste your full Neon connection string: ").strip()

    if connection_string:
        # Update the database.py file
        with open('database.py', 'r') as f:
            content = f.read()

        # Replace the DATABASE_URL line
        old_line = 'DATABASE_URL = "postgresql://neondb_owner:YOUR_PASSWORD@ep-solitary-smoke-a1lvn1qt.us-east-2.aws.neon.tech/neondb?sslmode=require"'
        new_line = f'DATABASE_URL = "{connection_string}"'

        updated_content = content.replace(old_line, new_line)

        with open('database.py', 'w') as f:
            f.write(updated_content)

        print("✅ Database configuration updated!")
        print()
        print("🧪 Testing database connection...")

        # Test the connection
        try:
            from database import engine, create_tables
            create_tables()
            print("✅ Database tables created successfully!")
            print("🎉 Your Neon PostgreSQL database is ready!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("Please check your connection string and try again.")
    else:
        print("❌ No connection string provided.")
        print("Please run this script again with your Neon connection string.")

if __name__ == "__main__":
    main()
