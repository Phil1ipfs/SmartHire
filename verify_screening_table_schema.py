"""
Comprehensive script to verify and add all missing columns to the screening table.
This ensures the database schema matches the SQLAlchemy model definition.
"""
from app import app, db
from sqlalchemy import text, inspect

def verify_and_fix_screening_schema():
    """Verify all Screening model columns exist in the database and add missing ones."""
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            existing_columns = {col['name']: col for col in inspector.get_columns('screening')}
            
            # Expected columns from the Screening model
            expected_columns = {
                'id': {'type': 'INTEGER', 'primary_key': True, 'nullable': False},
                'resume_id': {'type': 'INTEGER', 'nullable': False},
                'job_id': {'type': 'INTEGER', 'nullable': True},
                'employer_id': {'type': 'INTEGER', 'nullable': True},
                'applicant_name': {'type': 'VARCHAR(150)', 'nullable': True},
                'applicant_email': {'type': 'VARCHAR(150)', 'nullable': True},
                'applicant_phone': {'type': 'VARCHAR(50)', 'nullable': True},
                'job_description_text': {'type': 'TEXT', 'nullable': False},
                'matched_skills': {'type': 'TEXT', 'nullable': True},
                'match_score': {'type': 'FLOAT', 'nullable': True},
                'resume_text_summary': {'type': 'TEXT', 'nullable': True},
                'screened_at': {'type': 'DATETIME', 'nullable': True}
            }
            
            missing_columns = []
            for col_name, col_def in expected_columns.items():
                if col_name not in existing_columns:
                    missing_columns.append((col_name, col_def))
            
            if not missing_columns:
                print("[OK] All columns exist in the screening table. Schema is up to date!")
                return True
            
            print(f"Found {len(missing_columns)} missing column(s). Adding them now...")
            
            for col_name, col_def in missing_columns:
                # Skip primary key column (should already exist)
                if col_def.get('primary_key'):
                    print(f"[WARNING] Primary key column '{col_name}' is missing. This is unusual.")
                    continue
                
                # Build ALTER TABLE statement
                nullable = "NULL" if col_def.get('nullable', True) else "NOT NULL"
                col_type = col_def['type']
                
                try:
                    alter_sql = f"ALTER TABLE screening ADD COLUMN {col_name} {col_type} {nullable}"
                    db.session.execute(text(alter_sql))
                    print(f"[OK] Added column: {col_name} ({col_type})")
                except Exception as e:
                    if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                        print(f"[OK] Column {col_name} already exists (race condition)")
                    else:
                        print(f"[ERROR] Error adding column {col_name}: {e}")
                        db.session.rollback()
                        return False
            
            db.session.commit()
            print("\n[OK] Successfully updated screening table schema!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Error: {e}")
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("Screening Table Schema Verification")
    print("=" * 60)
    verify_and_fix_screening_schema()

