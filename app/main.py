from app import create_app
from app import db
# 🚀 FORCE MODELS INTO ROOT CONTEXT TO REVEAL THEM TO METADATA ENGINE BEFORE THE FLUSH!
from app.models import User, Todo 

app = create_app()
