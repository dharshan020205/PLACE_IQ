import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine, Base
from backend.models import User
from backend.auth import get_password_hash

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def seed_admin():
    db = SessionLocal()
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        hashed_password = get_password_hash("admin123")
        admin_user = User(username="admin", hashed_password=hashed_password)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Admin user created! (username: admin, password: admin123)")
    else:
        print("Admin user already exists.")
    db.close()

if __name__ == "__main__":
    seed_admin()
