"""
MySQL migration script to add employer_id column to screening table.
"""
from app import app, db
from sqlalchemy import text, inspect

def migrate_screening_mysql():
    """Add employer_id column to screening table in MySQL database."""
    with app.app_context():
        try:
            # Check if column already exists
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('screening')]
            
            if 'employer_id' in columns:
                print("Column employer_id already exists in screening table. No changes needed.")
                return True
            
            # Add the column using SQLAlchemy with proper MySQL syntax
            # First, add the column as nullable
            db.session.execute(text("ALTER TABLE screening ADD COLUMN employer_id INT NULL"))
            
            # Add foreign key constraint if employer table exists
            try:
                db.session.execute(text("""
                    ALTER TABLE screening 
                    ADD CONSTRAINT fk_screening_employer 
                    FOREIGN KEY (employer_id) REFERENCES employer(id)
                """))
            except Exception as fk_error:
                # Foreign key might already exist or table might not exist
                print(f"Note: Could not add foreign key constraint: {fk_error}")
                print("Column added without foreign key constraint.")
            
            db.session.commit()
            print("Successfully added employer_id column to screening table!")
            return True
            
        except Exception as e:
            db.session.rollback()
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower() or "1050" in str(e):
                print("Column employer_id already exists in screening table. No changes needed.")
                return True
            else:
                print(f"Error: {e}")
                return False

if __name__ == "__main__":
    print("=" * 60)
    print("MySQL Migration: Adding employer_id column to screening table")
    print("=" * 60)
    migrate_screening_mysql()

