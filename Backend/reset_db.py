from sqlalchemy import text
from sqlalchemy.orm import Session
from database import engine, Base
from models import User, University, UserShortlist

print("⚠️  FORCE RESETTING DATABASE...")

# 1. DROP TABLES (The Nuclear Option)
with engine.connect() as connection:
    trans = connection.begin()
    sql_commands = [
        "DROP TABLE IF EXISTS tasks CASCADE;",
        "DROP TABLE IF EXISTS user_shortlist CASCADE;",
        "DROP TABLE IF EXISTS universities CASCADE;",
        "DROP TABLE IF EXISTS users CASCADE;"
    ]
    for command in sql_commands:
        print(f"🔥 Executing: {command}")
        connection.execute(text(command))
    trans.commit()

print("✅ Old tables destroyed.")

# 2. CREATE TABLES
print("🏗️  Creating new tables...")
Base.metadata.create_all(bind=engine)

# 3. SEED DATA (Add Universities back!)
print("🌱 Seeding database with Universities...")
with Session(engine) as session:
    mit = University(name="MIT", location="Cambridge, MA", ranking=1)
    stanford = University(name="Stanford", location="Stanford, CA", ranking=2)
    toronto = University(name="University of Toronto", location="Toronto, Canada", ranking=25)
    tum = University(name="Technical University of Munich", location="Munich, Germany", ranking=30)
    
    session.add_all([mit, stanford, toronto, tum])
    session.commit()

print("✅ Database reset & SEEDED successfully!")