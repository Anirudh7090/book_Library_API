from db import engine, Base
import models  # Import models to register them with Base

# Create all tables in the database
Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
