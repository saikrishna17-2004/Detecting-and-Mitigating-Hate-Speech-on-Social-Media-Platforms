"""
Test MongoDB Atlas connection
Usage: python test_mongodb_connection.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test if MongoDB connection works"""
    try:
        from pymongo import MongoClient
        
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            print("❌ DATABASE_URL not set in .env file")
            return False
        
        if not database_url.startswith('mongodb+srv://'):
            print("⚠️  DATABASE_URL is not MongoDB Atlas format")
            print(f"Current: {database_url}")
            return False
        
        print("🔌 Attempting to connect to MongoDB Atlas...")
        print(f"Connection string: {database_url.split('@')[0]}@...")
        
        # Connect to MongoDB
        client = MongoClient(database_url, serverSelectionTimeoutMS=5000)
        
        # Test connection
        server_info = client.server_info()
        
        print("✅ Successfully connected to MongoDB Atlas!")
        print(f"   Server version: {server_info.get('version')}")
        
        # List databases
        databases = client.list_database_names()
        print(f"   Available databases: {', '.join(databases)}")
        
        # Get database
        db = client.get_database()
        print(f"   Current database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"   Collections: {', '.join(collections) if collections else 'No collections yet'}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\n📋 Troubleshooting:")
        print("   1. Verify DATABASE_URL in .env file is correct")
        print("   2. Replace <db_password> with your actual MongoDB password")
        print("   3. Check MongoDB Atlas IP whitelist (0.0.0.0/0)")
        print("   4. Ensure cluster is running")
        return False

if __name__ == '__main__':
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
