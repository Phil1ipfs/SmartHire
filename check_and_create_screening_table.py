"""
Check if screening table exists and create it if needed.
"""
from app import app, db
from sqlalchemy import text, inspect
import sqlite3
import os

def check_and_create_screening():
    """Check if screening table exists, create it if not."""
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        
        if 'sqlite' in db_uri.lower() or os.path.exists('instance/smarthire.db'):
            db_path = 'instance/smarthire.db'
            
            if not os.path.exists(db_path):
                print(f"Error: Database file not found at {db_path}")
                return False
            
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check if table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='screening'")
                table_exists = cursor.fetchone() is not None
                
                if not table_exists:
                    print("Creating screening table...")
                    # Create the screening table with all columns
                    cursor.execute("""
                        CREATE TABLE screening (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            resume_id INTEGER NOT NULL,
                            job_id INTEGER,
                            employer_id INTEGER,
                            applicant_name VARCHAR(150),
                            applicant_email VARCHAR(150),
                            applicant_phone VARCHAR(50),
                            job_description_text TEXT NOT NULL,
                            matched_skills TEXT,
                            match_score REAL,
                            resume_text_summary TEXT,
                            screened_at DATETIME,
                            FOREIGN KEY(resume_id) REFERENCES resume(id),
                            FOREIGN KEY(job_id) REFERENCES Job(id),
                            FOREIGN KEY(employer_id) REFERENCES employer(id)
                        )
                    """)
                    conn.commit()
                    print("Successfully created screening table with employer_id column!")
                else:
                    # Table exists, check if employer_id column exists
                    cursor.execute("PRAGMA table_info(screening)")
                    columns = [row[1] for row in cursor.fetchall()]
                    
                    if 'employer_id' not in columns:
                        print("Adding employer_id column to existing screening table...")
                        cursor.execute("ALTER TABLE screening ADD COLUMN employer_id INTEGER")
                        conn.commit()
                        print("Successfully added employer_id column!")
                    else:
                        print("screening table already has employer_id column.")
                
                conn.close()
                return True
                
            except sqlite3.Error as e:
                print(f"SQLite error: {e}")
                return False
            except Exception as e:
                print(f"Error: {e}")
                return False
        else:
            # For non-SQLite databases, use SQLAlchemy
            try:
                # Try to create all tables (this will only create missing ones)
                db.create_all()
                print("Tables created/updated using SQLAlchemy.")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False

if __name__ == "__main__":
    print("=" * 60)
    print("Checking and creating screening table")
    print("=" * 60)
    check_and_create_screening()

