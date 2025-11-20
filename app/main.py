from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Cấu hình PostgreSQL RDS
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "fastapi-cicd")

# Tạo connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine
engine = create_engine(DATABASE_URL)

def check_db_connection():
    """Kiểm tra kết nối đến database"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, "Kết nối Database thành công!"
    except OperationalError as e:
        return False, f"Kết nối Database thất bại: {str(e)}"
    except Exception as e:
        return False, f"Lỗi: {str(e)}"

@app.get("/")
def read_root():
    return {"message": "Hello World from CI/CD!"}

@app.get("/health")
def health_check():
    """Kiểm tra trạng thái ứng dụng và kết nối database"""
    is_connected, message = check_db_connection()
    
    if is_connected:
        return {
            "status": "healthy",
            "message": message,
            "database": "connected"
        }
    else:
        return {
            "status": "unhealthy",
            "message": message,
            "database": "disconnected"
        }

@app.get("/db-status")
def db_status():
    """Endpoint riêng để kiểm tra kết nối database"""
    is_connected, message = check_db_connection()
    return {
        "connected": is_connected,
        "message": message,
        "database_url": f"postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    }

