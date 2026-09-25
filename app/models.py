import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy Database Schema mapping user profiles and security matrices.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # Stores securely processed bcrypt text blocks (Never store plain text passwords!)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False) # 💳 Identifies Stripe paid tier profiles
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Establishes a cascading relational link down to the individual todo lists
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")


class Todo(Base):
    """
    SQLAlchemy Database Schema mapping contextual tasks and AI parsing payloads.
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True) # Holds the raw text input loops
    is_completed = Column(Boolean, default=False)
    
    # --- AI Contextual Metadata Layers ---
    category = Column(String, default="General") # AI parses context (e.g., "DBA", "Finance")
    priority = Column(String, default="Medium") # AI assigns weights (e.g., "High", "Low")
    due_date = Column(DateTime, nullable=True) # AI extracts deadline parameters
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 🔒 Security Barrier: Foreign Key mapping the task directly back to its single author user
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="todos")