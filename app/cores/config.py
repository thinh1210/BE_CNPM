from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

ADMIN_SECRET_KEY="adminsuperkeyusedtocreateadminaccountcapcap"
# Cấu hình database
DB_USER = "root"  # Thay bằng username của bạn
DB_PASSWORD = "12102004"  # Thay bằng password của bạn
DB_HOST = "localhost"  # Hoặc địa chỉ IP của server MySQL
DB_PORT = 3306  # Cổng mặc định của MySQL
DB_NAME = "test_db"  # Thay bằng tên database của bạn
# Tạo URL kết nối MySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SECRET_KEY: str = "your-secret-key"
API_V1_STR: str = "/api/v1"

ADMIN_KEY: str ="something"