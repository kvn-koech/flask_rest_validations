from app import app
from models import db, User
from faker import Faker
import random

def seed_database():
    fake = Faker()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        User.query.delete()
        
        # Generate fake users
        users = []
        existing_emails = set()
        
        print("🎭 Generating fake users...")
        
        for i in range(50):  # Generate 50 fake users
            # Generate unique email
            while True:
                email = fake.unique.email()
                if email not in existing_emails:
                    existing_emails.add(email)
                    break
            
            user = User(
                name=fake.name(),
                email=email,
                age=random.randint(18, 80)  # Realistic age range
            )
            users.append(user)
            
            # Print progress for larger datasets
            if (i + 1) % 10 == 0:
                print(f"✅ Generated {i + 1} users...")
        
        # Add all users to database
        db.session.add_all(users)
        db.session.commit()
        
        print(f"🎉 Successfully seeded {len(users)} fake users!")
        
        # Display sample of created users
        print("\n📋 Sample of created users:")
        print("-" * 60)
        sample_users = User.query.limit(5).all()
        for user in sample_users:
            print(f"👤 {user.name} | 📧 {user.email} | 🎂 {user.age} years old")
        
        # Show some statistics
        total_users = User.query.count()
        avg_age = db.session.query(db.func.avg(User.age)).scalar()
        youngest = db.session.query(db.func.min(User.age)).scalar()
        oldest = db.session.query(db.func.max(User.age)).scalar()
        
        print("\n📊 Database Statistics:")
        print(f"   Total users: {total_users}")
        print(f"   Average age: {avg_age:.1f} years")
        print(f"   Youngest: {youngest} years")
        print(f"   Oldest: {oldest} years")

def add_specific_test_users():
    """Add specific test users for manual testing"""
    fake = Faker()
    
    with app.app_context():
        test_users = [
            {"name": "Admin User", "email": "admin@test.com", "age": 35},
            {"name": "Test Manager", "email": "manager@test.com", "age": 42},
            {"name": "Demo Account", "email": "demo@test.com", "age": 28}
        ]
        
        for user_data in test_users:
            # Check if user already exists
            if not User.query.filter_by(email=user_data['email']).first():
                user = User(**user_data)
                db.session.add(user)
                print(f"✅ Added test user: {user_data['name']}")
        
        db.session.commit()

if __name__ == "__main__":
    seed_database()
    add_specific_test_users()