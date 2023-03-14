import sys

sys.path.append(".")

from db.connection_manager import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)
