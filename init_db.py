# init_db.py - Native Database Initializer Matrix
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from app import db
from app.models import User, Todo

load_dotenv()

# Build a clean local connection string (pointing to your Mac host interface loopback)
LOCAL_DB_URL = "postgresql+psycopg2://postgres:admin@127.0.0.1:5432/todo_db"

print("🔄 Connecting natively to todo_db to force table generation...")
engine = create_engine(LOCAL_DB_URL)

# Force the metadata engine to drop your plural schemas onto the disk layer!
User.metadata.create_all(bind=engine)
print("🚀 Success! Plural database tables 'users' and 'todos' have been forced onto todo_db!")
