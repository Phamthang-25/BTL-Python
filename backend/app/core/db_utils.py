from sqlalchemy import text, inspect
from app.database import engine

def ensure_schema_consistency():
    """Senior-level schema check and auto-migration for missing columns."""
    print("Checking database schema consistency...")
    inspector = inspect(engine)
    
    # Check 'reviews' table
    columns = [c['name'] for c in inspector.get_columns('reviews')]
    
    with engine.begin() as conn:
        # Ensure criteria_scores exists
        if 'criteria_scores' not in columns:
            print("Adding missing column 'criteria_scores' to 'reviews' table...")
            conn.execute(text("ALTER TABLE reviews ADD COLUMN criteria_scores JSONB DEFAULT NULL"))
        
        # Ensure reviewed_at exists (just in case)
        if 'reviewed_at' not in columns:
            print("Adding missing column 'reviewed_at' to 'reviews' table...")
            conn.execute(text("ALTER TABLE reviews ADD COLUMN reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT NULL"))

    print("Schema consistency check completed.")
