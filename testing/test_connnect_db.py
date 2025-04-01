from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Cấu hình database
DB_USER = "root"  # Thay bằng username của bạn
DB_PASSWORD = "12102004"  # Thay bằng password của bạn
DB_HOST = "localhost"  # Hoặc địa chỉ IP của server MySQL
DB_PORT = 3306  # Cổng mặc định của MySQL
DB_NAME = "name_table"  # Thay bằng tên database của bạn
# Tạo URL kết nối MySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine kết nối
engine = create_engine(DATABASE_URL, echo=True)

# Tạo session
SessionLocal = sessionmaker(bind=engine)

def test_connection():
    try:
        db = SessionLocal()
        conn = db.connection()
        print("✅ Kết nối MySQL thành công!")
        conn.close()
    except Exception as e:
        print("❌ Lỗi kết nối MySQL:", e)

if __name__ == "__main__":
    test_connection()
