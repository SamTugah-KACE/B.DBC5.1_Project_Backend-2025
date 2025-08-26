from sqlalchemy.orm import Session
from .session import SessionLocal, Base, engine
from . import models
from core.security import get_password_hash

def seed():
    """Insert initial demo data."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # Create demo users
        alice = models.User(
            username="alice",
            email="alice@example.com",
            full_name="Alice Wonderland",
            hashed_password=get_password_hash("secret123"),
            is_active=True,
        )
        bob = models.User(
            username="bob",
            email="bob@example.com",
            full_name="Bob Builder",
            hashed_password=get_password_hash("secret123"),
            is_active=True,
        )
        db.add_all([alice, bob])
        db.commit()

        # Add demo students
        s1 = models.Student(
            first_name="John",
            last_name="Doe",
            index_number="STU-001",
            program="Computer Science",
            level=200,
            owner_id=alice.id,
        )
        s2 = models.Student(
            first_name="Jane",
            last_name="Smith",
            index_number="STU-002",
            program="Mathematics",
            level=100,
            owner_id=alice.id,
        )
        s3 = models.Student(
            first_name="Sam",
            last_name="Taylor",
            index_number="STU-003",
            program="Physics",
            level=300,
            owner_id=bob.id,
        )
        db.add_all([s1, s2, s3])
        db.commit()
        print("Database seeded successfully.")
    finally:
        db.close()

def seed_if_needed():
    """Idempotent seeding: only seed if no users exist."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        exists = db.query(models.User.id).limit(1).first()
        if exists:
            print("Seed skipped: data already present.")
            return
        print("Seeding initial data...")
        seed()
    finally:
        db.close()

if __name__ == "__main__":
    seed_if_needed()
