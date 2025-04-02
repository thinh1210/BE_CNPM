import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from .config import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    # print(f"Decoding token: {token}")  # In ra token để debug
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)  # In ra payload để debug
        username: str = payload.get("sub")  # Lấy thông tin từ 'sub'
        print(f"Username: {username}")
        if username is None:
            raise jwt.InvalidTokenError("Token không có 'sub'")
        return username
    except jwt.ExpiredSignatureError:
        print("Token đã hết hạn!")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Token không hợp lệ: {e}")
        return None