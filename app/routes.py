from flask import Blueprint, request, jsonify
from app import db
from app.models import User
import bcrypt
from sqlalchemy import select # 👈 Add this modern select token here

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register_user():
    """
    Captures incoming user registrations, hashes passwords using bcrypt, 
    and provisions clean user rows into the PostgreSQL database.
    """
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password parameters"}), 400

    # 🔒 Modern Security Barrier: Query the database matching the exact user record
    stmt = select(User).where(User.email == email)
    existing_user = db.session.execute(stmt).scalar()
    
    if existing_user:
        return jsonify({"error": "An account with this email address already exists"}), 400

    # 🛡️ Process raw text through the bcrypt hashing machine
    salt = bcrypt.gensalt(rounds=12)
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    try:
        new_user = User(email=email, hashed_password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully into Jarboe Digital vault",
            "user_id": new_user.id,
            "email": new_user.email
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database provisioning failure: {str(e)}"}), 500