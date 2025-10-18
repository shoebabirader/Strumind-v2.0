"""
Database Setup Script
Run this to initialize the database
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import init_db, engine
from app.core.config import settings
import sqlite3

def check_database():
    """Check database status"""
    print("\n" + "="*60)
    print("DATABASE CONFIGURATION CHECK")
    print("="*60)
    
    print(f"\n📊 Database URL: {settings.DATABASE_URL}")
    
    if settings.DATABASE_URL.startswith('sqlite'):
        db_file = settings.DATABASE_URL.replace('sqlite:///', '')
        print(f"📁 Database Type: SQLite")
        print(f"📍 Database File: {db_file}")
        
        if os.path.exists(db_file):
            print(f"✅ Database file exists")
            
            # Check tables
            # SECURITY FIX: Use context manager to ensure connection is closed
            try:
                with sqlite3.connect(db_file) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                
                if tables:
                    print(f"✅ Tables found: {len(tables)}")
                    for table in tables:
                        print(f"   - {table[0]}")
                else:
                    print(f"⚠️  No tables found")
            except Exception as e:
                print(f"❌ Error checking tables: {e}")
        else:
            print(f"⚠️  Database file does not exist yet")
    else:
        print(f"📁 Database Type: PostgreSQL")
        print(f"⚠️  Make sure PostgreSQL is running")
    
    print("\n" + "="*60)

def setup_database():
    """Initialize database"""
    print("\n🚀 Initializing database...")
    
    success = init_db()
    
    if success:
        print("\n✅ DATABASE SETUP COMPLETE!")
        print("\nYou can now:")
        print("  1. Run the backend: python main.py")
        print("  2. Access API docs: http://localhost:8000/docs")
        print("  3. Use project management features")
    else:
        print("\n⚠️  Database setup had issues")
        print("   Core analysis features will still work")
    
    return success

if __name__ == "__main__":
    print("\n" + "🔧 "*30)
    print("STRUMIND DATABASE SETUP")
    print("🔧 "*30)
    
    # Check current status
    check_database()
    
    # Ask user
    print("\n" + "="*60)
    response = input("\nInitialize/Reset database? (y/n): ").lower()
    
    if response == 'y':
        setup_database()
        print("\n" + "="*60)
        check_database()
    else:
        print("\n❌ Setup cancelled")
    
    print("\n" + "="*60)
