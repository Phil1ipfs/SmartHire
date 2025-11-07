#!/usr/bin/env python
"""
Check users in database
"""
from app import app, db, User

with app.app_context():
    users = User.query.all()
    print("=" * 60)
    print("Users in Database:")
    print("=" * 60)
    if users:
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}")
            print(f"  Password (first 20 chars): {str(user.password)[:20]}...")
            print(f"  Password is hashed: {str(user.password).startswith('scrypt:') or str(user.password).startswith('pbkdf2:')}")
            print("-" * 60)
    else:
        print("No users found in database!")
    print(f"\nTotal users: {len(users)}")


