#!/usr/bin/env python
"""
MongoDB Atlas Connection Tester for VS Code Integration
Tests connectivity and displays database structure
"""

import os
import sys
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

def test_connection():
    """Test MongoDB Atlas connection"""
    
    # Load connection string from .env
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in .env")
        print("Add this line to .env:")
        print("DATABASE_URL=mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority")
        return False
    
    print(f"🔍 Testing MongoDB Atlas Connection...")
    print(f"📍 Connection String: {database_url[:80]}...")
    print()
    
    try:
        # Create client with timeout
        client = MongoClient(database_url, serverSelectionTimeoutMS=5000, connectTimeoutMS=10000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        print()
        
        # Get database
        db = client.get_default_database()
        print(f"📦 Database: {db.name}")
        print()
        
        # List collections
        collections = db.list_collection_names()
        print(f"📊 Collections ({len(collections)}):")
        for col in collections:
            count = db[col].count_documents({})
            print(f"  • {col}: {count} documents")
        print()
        
        # Check indexes
        print("🔑 Indexes:")
        for col in ['users', 'posts', 'violations', 'counters']:
            if col in collections:
                indexes = db[col].list_indexes()
                print(f"  {col}:")
                for idx in indexes:
                    print(f"    - {idx['name']}")
        print()
        
        # Sample data
        print("📋 Sample Data:")
        
        # Users
        user_count = db.users.count_documents({})
        print(f"  Users: {user_count} total")
        if user_count > 0:
            sample_user = db.users.find_one()
            print(f"    Sample: {sample_user.get('username', 'N/A')} ({sample_user.get('email', 'N/A')})")
        
        # Posts
        post_count = db.posts.count_documents({})
        print(f"  Posts: {post_count} total")
        
        # Violations
        violation_count = db.violations.count_documents({})
        print(f"  Violations: {violation_count} total")
        
        print()
        print("✨ Ready to use in VS Code MongoDB extension!")
        print()
        print("Next steps:")
        print("  1. Open MongoDB extension (left sidebar)")
        print("  2. Click 'Add Connection'")
        print("  3. Paste connection string:")
        print(f"     {database_url}")
        print("  4. Browse your collections in the sidebar")
        
        client.close()
        return True
        
    except ServerSelectionTimeoutError:
        print("❌ Connection Timeout!")
        print()
        print("This means MongoDB cluster is either:")
        print("  1. PAUSED - Go to https://cloud.mongodb.com")
        print("     → Database → Cluster0 → Click Resume")
        print("  2. IP NOT WHITELISTED - Go to Security → Network Access")
        print("     → Add 0.0.0.0/0 (Allow Access from Anywhere)")
        print()
        print("Wait 1-2 minutes for changes to apply, then try again.")
        return False
        
    except OperationFailure as e:
        print(f"❌ Authentication Error: {e}")
        print()
        print("Check your credentials in DATABASE_URL:")
        print("  - Username: SAIKRISHNA")
        print("  - Password: YadavNakkala")
        print("  - Database: hate_speech_db")
        return False
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print()
        print("Troubleshooting:")
        print("  • Verify .env DATABASE_URL is correct")
        print("  • Check internet connection")
        print("  • Ensure MongoDB cluster is running")
        print("  • Try again in 1-2 minutes")
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
