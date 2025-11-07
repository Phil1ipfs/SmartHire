#!/usr/bin/env python
"""
Create test users for SmartHire
"""
from app import app, db, User, Applicant, Employer, generate_password_hash

with app.app_context():
    try:
        # Create Admin user
        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin)
            print("[OK] Created admin user (username: admin, password: admin123)")
        else:
            print("[SKIP] Admin user already exists")

        # Create Test Applicant
        applicant_user = User.query.filter_by(username="applicant1").first()
        if not applicant_user:
            applicant_user = User(
                username="applicant1",
                password=generate_password_hash("applicant123"),
                role="applicant"
            )
            db.session.add(applicant_user)
            db.session.flush()
            
            applicant_profile = Applicant(
                user_id=applicant_user.id,
                fullname="Test Applicant",
                email="applicant1@test.com",
                skills="Python, Flask, SQL",
                experience=2
            )
            db.session.add(applicant_profile)
            print("[OK] Created applicant user (username: applicant1, password: applicant123)")
        else:
            print("[SKIP] Applicant user already exists")

        # Create Test Employer
        employer_user = User.query.filter_by(username="employer1").first()
        if not employer_user:
            employer_user = User(
                username="employer1",
                password=generate_password_hash("employer123"),
                role="employer"
            )
            db.session.add(employer_user)
            db.session.flush()
            
            employer_profile = Employer(
                user_id=employer_user.id,
                fullname="Test Employer",
                email="employer1@test.com",
                company="Test Company Inc."
            )
            db.session.add(employer_profile)
            print("[OK] Created employer user (username: employer1, password: employer123)")
        else:
            print("[SKIP] Employer user already exists")

        db.session.commit()
        print("\n" + "=" * 60)
        print("Test Users Created Successfully!")
        print("=" * 60)
        print("\nLogin Credentials:")
        print("  Admin:     username=admin, password=admin123")
        print("  Applicant: username=applicant1, password=applicant123")
        print("  Employer:  username=employer1, password=employer123")
        print("\nYou can now login at http://localhost:5000")
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed to create users: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)

