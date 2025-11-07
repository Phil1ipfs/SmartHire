"""
MySQL migration script to add resume_text_summary column to screening table.
"""
from app import app, db
from sqlalchemy import text, inspect

def migrate_screening_resume_text_summary():
    """Add resume_text_summary column to screening table in MySQL database."""
    with app.app_context():
        try:
            # Check if column already exists
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('screening')]
            
            if 'resume_text_summary' in columns:
                print("Column resume_text_summary already exists in screening table. No changes needed.")
                return True
            
            # Add the column using SQLAlchemy with proper MySQL syntax
            # TEXT type for MySQL, nullable as per model definition
            db.session.execute(text("ALTER TABLE screening ADD COLUMN resume_text_summary TEXT NULL"))
            
            db.session.commit()
            print("Successfully added resume_text_summary column to screening table!")
            return True
            
        except Exception as e:
            db.session.rollback()
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower() or "1050" in str(e):
                print("Column resume_text_summary already exists in screening table. No changes needed.")
                return True
            else:
                print(f"Error: {e}")
                return False

if __name__ == "__main__":
    print("=" * 60)
    print("MySQL Migration: Adding resume_text_summary column to screening table")
    print("=" * 60)
    migrate_screening_resume_text_summary()

