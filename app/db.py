import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:your_password@localhost:5432/science_manager")

def get_db_connection():
    # Kết nối đến CSDL Postgres
    conn = psycopg2.connect(DB_URL)
    return conn
