from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserData(BaseModel):
    email:EmailStr
    job_title:str
    full_name:str
    password:str

class CreateUser(BaseModel):
    admin_key:str
    user_data:UserData

class AuthKeyUser(BaseModel):
    email:EmailStr
    key:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    job_title:str
    full_name:str
    hashed_password:str
    created_at: datetime

class ChangePassword(BaseModel):
    ...

class FirstLoginResponce(BaseModel):
    message:str
    success:bool

class FirstLoginChangePassword(BaseModel):
    email:EmailStr
    password:str
    new_password:str

    

