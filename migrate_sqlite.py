"""
SQLite migration script to add photo_filename column to applicant table.
This script handles SQLite's limitations with ALTER TABLE.
"""
from app import app, db
from sqlalchemy import text, inspect
import sqlite3
import os

def migrate_sqlite():
    """Add photo_filename column to applicant table in SQLite database."""
    with app.app_context():
        # Get database path
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        
        # Check if using SQLite
        if 'sqlite' in db_uri.lower() or os.path.exists('instance/smarthire.db'):
            db_path = 'instance/smarthire.db'
            
            if not os.path.exists(db_path):
                print(f"Error: Database file not found at {db_path}")
                return False
            
            try:
                # Connect to SQLite database
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check if column already exists
                cursor.execute("PRAGMA table_info(applicant)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'photo_filename' in columns:
                    print("Column photo_filename already exists. No changes needed.")
                    conn.close()
                    return True
                
                # Add the column
                cursor.execute("ALTER TABLE applicant ADD COLUMN photo_filename VARCHAR(255)")
                conn.commit()
                conn.close()
                
                print("Successfully added photo_filename column to applicant table!")
                return True
                
            except sqlite3.Error as e:
                print(f"SQLite error: {e}")
                return False
            except Exception as e:
                print(f"Error: {e}")
                return False
        else:
            # Try using SQLAlchemy for other databases
            try:
                inspector = inspect(db.engine)
                columns = [col['name'] for col in inspector.get_columns('applicant')]
                
                if 'photo_filename' in columns:
                    print("Column photo_filename already exists. No changes needed.")
                    return True
                
                # Add the column using SQLAlchemy
                db.session.execute(text("ALTER TABLE applicant ADD COLUMN photo_filename VARCHAR(255)"))
                db.session.commit()
                print("Successfully added photo_filename column to applicant table!")
                return True
                
            except Exception as e:
                db.session.rollback()
                if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                    print("Column photo_filename already exists. No changes needed.")
                    return True
                else:
                    print(f"Error: {e}")
                    return False

if __name__ == "__main__":
    print("=" * 60)
    print("SQLite Migration: Adding photo_filename column")
    print("=" * 60)
    migrate_sqlite()

