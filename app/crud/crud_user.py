from sqlmodel import Session, select
from sqlmodel import func
from math import ceil
from typing import List, Tuple
from app.model import User
from app.schemas.user import UserIn, Register_In
from app.schemas.metadata import Metadata
from app.cores.security import get_password_hash, verify_password
import requests
import base64
import json
import os
from bs4 import BeautifulSoup
from fastapi import HTTPException

def get_information(user, passs):
    login_data = {
        'username': user,
        'password': passs,
        '_eventId': 'submit',
        'submit': 'Login',
    }

    def decode_jwt_payload(jwt):
        # Tách phần payload của JWT
        payload = jwt.split(".")[1]
        
        # Chuyển Base64-URL thành Base64 chuẩn
        payload += "=" * (-len(payload) % 4)  # Thêm padding nếu cần
        decoded_bytes = base64.urlsafe_b64decode(payload)  # Giải mã Base64
        
        # Chuyển bytes thành chuỗi JSON
        decoded_str = decoded_bytes.decode("utf-8")
        
        # Parse JSON thành dictionary
        return json.loads(decoded_str)

    os.system('cls')  # Clear the console

    with requests.Session() as S:
        S.cookies.clear()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 Edg/126.0.0.0'
        }

        # Login to MyBK
        login_url = 'https://sso.hcmut.edu.vn/cas/login?service=https%3A%2F%2Fmybk.hcmut.edu.vn%2Fapp%2Flogin%2Fcas'
        home_url = 'https://mybk.hcmut.edu.vn/app/'
        r = S.get(login_url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        login_data['lt'] = soup.find('input', attrs={'name': 'lt'})['value']
        login_data['execution'] = soup.find('input', attrs={'name': 'execution'})['value']
        r = S.post(login_url, data=login_data)

        if r.url == home_url:
            uni_records_url = 'https://mybk.hcmut.edu.vn/app/he-thong-quan-ly/sinh-vien/ket-qua-hoc-tap'
            response_records = S.get(uni_records_url)
            soup1 = BeautifulSoup(response_records.content, 'html5lib')
            token = soup1.find('input', attrs={'id': 'hid_Token'})['value']

            json_data = decode_jwt_payload(token)

            profiles = json_data['profiles']
            person_ID = json.loads(profiles)['personId']

            url_mark = f"https://mybk.hcmut.edu.vn/api/sinh-vien/xem-ket-qua-hoc-tap/v2?mssv={person_ID}&null"
            url_full_info = f"https://mybk.hcmut.edu.vn/api/v1/student/detail-info-by-code/{person_ID}?null"

            if response_records.status_code == 200:
                headers = {
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }

                response_info = S.get(url_full_info, headers=headers)
                full_info = response_info.json()

                response_info = S.get(url_mark, headers=headers)
                mark = response_info.json()
                data = full_info['data']
                code = data['code']
                lastName = data['lastName']
                firstName = data['firstName']
                orgEmail = data['orgEmail']

                # Kết quả trả về
                info = {
                    'code': code,
                    'lastName': lastName,
                    'firstName': firstName,
                    'orgEmail': orgEmail
}
                return {"status": "success", "full_info": info}
        return {"status": "failed"}

def get_user_by_username(session: Session, username: str) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user



def create_user(session: Session, user_create: UserIn) -> User:
    
    result = get_information(user_create.username, user_create.password)
    if result["status"] == "failed":
        return None
    data= result["full_info"]

    db_user = User(
        username=user_create.username,
        password=get_password_hash(user_create.password),
        MSSV=data['code'],
        lastname=data['lastName'],
        firstname=data['firstName'],
        email=data['orgEmail'],
        isUser=True,
        isAdmin=False,
        isActive=True
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def register_user(session: Session, user_create: Register_In, isAdmin: bool =False ) -> User:
    db_user = User(
        username=user_create.username,
        password=get_password_hash(user_create.password),
        MSSV=None,
        lastname=user_create.lastname,
        firstname=user_create.firstname,
        email=user_create.email,
        isUser=True,
        isAdmin=isAdmin,
        isActive=True
    )
    print(db_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def change_user_pasword(session: Session, username: str, password: str) -> User:
    db_user = get_user_by_username(session, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.password = get_password_hash(password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def change_user_info(session: Session, username: str, user_create: Register_In) -> User:
    db_user = get_user_by_username(session, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.lastname = user_create.lastname
    db_user.firstname = user_create.firstname
    db_user.email = user_create.email
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def change_user_status(session: Session, username: str, isActive: bool) -> List[User]:
    db_user = get_user_by_username(session, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.isActive = isActive
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_all_user(session: Session, metadata:Metadata ) -> Tuple[List[User], Metadata]: 
    if (metadata.total ==0):
        metadata.total = session.exec(select(func.count(User.id))).first()
        metadata.total_page = ceil(metadata.total / metadata.perpage)
        offset = (metadata.page - 1) * metadata.perpage
    
    #get users from database
    users =session.exec(
        select(User).offset(offset).limit(metadata.perpage)
        ).all()
    
    return users, metadata