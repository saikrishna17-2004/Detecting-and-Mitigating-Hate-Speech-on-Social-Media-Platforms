"""
Add password_hash column to existing database and update posts table
"""
import sqlite3
import os

db_path = 'instance/hate_speech_detection.db'

if not os.path.exists(db_path):
    print(f"❌ Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check and add password_hash column to users table
    cursor.execute("PRAGMA table_info(users)")
    user_columns = [row[1] for row in cursor.fetchall()]
    
    if 'password_hash' not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)")
        conn.commit()
        print("✅ password_hash column added to users table")
    else:
        print("✅ password_hash column already exists in users table")
    
    # Check and add image_url column to posts table
    cursor.execute("PRAGMA table_info(posts)")
    post_columns = [row[1] for row in cursor.fetchall()]
    
    if 'image_url' not in post_columns:
        cursor.execute("ALTER TABLE posts ADD COLUMN image_url VARCHAR(500)")
        conn.commit()
        print("✅ image_url column added to posts table")
    else:
        print("✅ image_url column already exists in posts table")
    
    # Check and add likes_count column to posts table
    if 'likes_count' not in post_columns:
        cursor.execute("ALTER TABLE posts ADD COLUMN likes_count INTEGER DEFAULT 0")
        conn.commit()
        print("✅ likes_count column added to posts table")
    else:
        print("✅ likes_count column already exists in posts table")
    
    # Verify users table
    cursor.execute("PRAGMA table_info(users)")
    print("\n📋 Users table schema:")
    for row in cursor.fetchall():
        print(f"   {row[1]} ({row[2]})")
    
    # Verify posts table
    cursor.execute("PRAGMA table_info(posts)")
    print("\n📋 Posts table schema:")
    for row in cursor.fetchall():
        print(f"   {row[1]} ({row[2]})")
        
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
