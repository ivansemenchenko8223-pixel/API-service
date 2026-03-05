from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import datetime
from typing import Dict, List, Optional
from app.core.config import config
from sqlalchemy.orm import Session
import string



pwd_context = CryptContext(schemes=[config.ALGORITHM,"bcrypt"], default = "argon2", deprecated = "auto")
active_session:Dict[str, Dict]= {}


class AuthService:
    @staticmethod
    def get_password_hash(password:str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password:str, hash_password:str):
        return pwd_context.verify(password, hash_password)


    @staticmethod
    def create_session_token(username:str):
        token = secrets.token_urlsafe(32)
        active_session[token] = {"username": username,
                                 "created_at": datetime.datetime.now()}
        return token

    @staticmethod
    def validate_session_token(token:str):
        if token not in active_session:
            return None
        return active_session[token]

    @staticmethod
    def logout(token:str):
        if token in active_session:
            del active_session[token]
            return True
        return False
    
    @staticmethod
    def generate_password():
        alphabet = string.ascii_letters + string.digits + "!@?"
        password = "".join(secrets.choice(alphabet) for _ in range(12))  
        return password

    


security_basic = HTTPBasic()

def get_current_user_basic(credentials: HTTPBasicCredentials = Depends(security_basic)):
    user = AuthService.authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(401,
                            detail = "Неверные учетные данные",
                            headers = {"WWW-Authenticate": "Basic"})
    return user


