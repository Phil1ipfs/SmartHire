"""
SQLite migration script to add employer_id column to screening table.
"""
from app import app, db
from sqlalchemy import text, inspect
import sqlite3
import os

def migrate_screening():
    """Add employer_id column to screening table in SQLite database."""
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
                cursor.execute("PRAGMA table_info(screening)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'employer_id' in columns:
                    print("Column employer_id already exists in screening table. No changes needed.")
                    conn.close()
                    return True
                
                # Add the column
                cursor.execute("ALTER TABLE screening ADD COLUMN employer_id INTEGER")
                conn.commit()
                conn.close()
                
                print("Successfully added employer_id column to screening table!")
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
                columns = [col['name'] for col in inspector.get_columns('screening')]
                
                if 'employer_id' in columns:
                    print("Column employer_id already exists in screening table. No changes needed.")
                    return True
                
                # Add the column using SQLAlchemy
                db.session.execute(text("ALTER TABLE screening ADD COLUMN employer_id INTEGER"))
                db.session.commit()
                print("Successfully added employer_id column to screening table!")
                return True
                
            except Exception as e:
                db.session.rollback()
                if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                    print("Column employer_id already exists in screening table. No changes needed.")
                    return True
                else:
                    print(f"Error: {e}")
                    return False

if __name__ == "__main__":
    print("=" * 60)
    print("SQLite Migration: Adding employer_id column to screening table")
    print("=" * 60)
    migrate_screening()

