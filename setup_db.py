"""
Database Setup Script
=====================
This script initializes the database for the Fitness Tracker V4 project.
It creates the required 'neondb' schema and all tables, then seeds
the initial Client (tenant) with the API key from SECRET_KEY.

Usage:
    1. Make sure your .env file has the correct DATABASE_URL
    2. Run: python setup_db.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify DATABASE_URL is set
db_url = os.environ.get('DATABASE_URL')
if not db_url or 'YOUR_DB_PASSWORD' in db_url:
    print("=" * 60)
    print("ERROR: DATABASE_URL is not properly configured!")
    print("Please update your .env file with the correct database URL.")
    print("=" * 60)
    sys.exit(1)

print(f"Connecting to: {db_url[:50]}...")

from app import create_app, db
from app.models import Client

app = create_app()

with app.app_context():
    try:
        # Step 1: Create the 'neondb' schema if it doesn't exist
        print("\n[1/3] Creating 'neondb' schema...")
        db.session.execute(db.text("CREATE SCHEMA IF NOT EXISTS neondb"))
        db.session.commit()
        print("  [OK] Schema 'neondb' created (or already exists)")

        # Step 2: Create all tables defined in models.py
        print("\n[2/3] Creating all tables...")
        db.create_all()
        print("  [OK] All tables created successfully!")
        
        # List created tables
        result = db.session.execute(db.text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'neondb' ORDER BY table_name"
        ))
        tables = [row[0] for row in result]
        print(f"\n  Tables in 'neondb' schema ({len(tables)}):")
        for t in tables:
            print(f"    - {t}")

        # Step 3: Seed the initial Client (tenant) with API key
        print("\n[3/3] Seeding initial Client...")
        api_key = os.environ.get('SECRET_KEY', '2a0d2132-328c-4fb3-a01a-be569ec39c23')
        
        existing_client = Client.query.filter_by(api_key=api_key).first()
        if existing_client:
            print(f"  [OK] Client already exists: '{existing_client.company_name}' (API key: {api_key})")
        else:
            new_client = Client(company_name="Armour Zone")
            # Override the auto-generated API key with the one from SECRET_KEY
            new_client.api_key = api_key
            db.session.add(new_client)
            db.session.commit()
            print(f"  [OK] Client 'Armour Zone' created with API key: {api_key}")

        print("\n" + "=" * 60)
        print("DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print(f"\nYou can now start the server with:")
        print(f"  python run.py")
        print(f"\nThe frontend API key (X-API-Key) is: {api_key}")

    except Exception as e:
        db.session.rollback()
        print(f"\n[ERROR]: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check your DATABASE_URL in .env")
        print("  2. Make sure your Supabase project is active")
        print("  3. Verify the password is correct")
        sys.exit(1)
