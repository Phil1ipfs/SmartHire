#!/usr/bin/env python
"""
Fix any plain text passwords in the database by hashing them
"""
from app import app, db, User, is_hashed, generate_password_hash

with app.app_context():
    users = User.query.all()
    updated_count = 0
    
    print("=" * 60)
    print("Checking and fixing passwords...")
    print("=" * 60)
    
    for user in users:
        if not is_hashed(user.password):
            print(f"[FIXING] User '{user.username}' has plain text password, hashing it...")
            user.password = generate_password_hash(user.password)
            updated_count += 1
        else:
            print(f"[OK] User '{user.username}' already has hashed password")
    
    if updated_count > 0:
        db.session.commit()
        print(f"\n[SUCCESS] Updated {updated_count} user(s) with hashed passwords!")
    else:
        print("\n[OK] All passwords are already hashed. No changes needed.")
    
    print("\n" + "=" * 60)
    import sys
    sys.exit(0)

