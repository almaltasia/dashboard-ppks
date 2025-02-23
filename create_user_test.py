from flask import Flask
from app import create_app
from app.auth.models import db, User

app = create_app()

with app.app_context():
    # Check if test user already exists
    test_user = User.query.filter_by(email='admin@ppks.com').first()
    
    if not test_user:
        # Create a new test user
        test_user = User(
            full_name='Admin PPKS',
            nomor_identitas='123456',
            email='admin@ppks.com',
            roles='super_admin',
            phone='081234567890',
            jurusan='Teknik Elektro',
            prodi='Teknik Listrik',
            is_active=True
        )
        test_user.set_password('password123')
        
        # Add to database
        db.session.add(test_user)
        db.session.commit()
        print("Test user created successfully!")
    else:
        print("Test user already exists!")
        
    # Verify user exists
    print("\nUser details:")
    user = User.query.filter_by(email='admin@ppks.com').first()
    print(f"Email: {user.email}")
    print(f"Role: {user.roles}")
    print(f"Active: {user.is_active}")