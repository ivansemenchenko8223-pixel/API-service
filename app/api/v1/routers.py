from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.user import CRUDUser
from app.schemas.user import CreateUser, AuthKeyUser
from app.core.config import config



router = APIRouter()


crud_user = CRUDUser()


@router.post("/auth_with_key", status_code=status.HTTP_200_OK)
def auth_with_key(user_data:AuthKeyUser, db:Session=Depends(get_db)):
    user = crud_user.get_by_email(db, user_data.email)
    if user is None:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Такого пользователя нет")
    
    if config.SECRET_KEY not in user_data.key:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Такого ключа нет")
    
    return {"message":"Успешная аутентификация",
            "id": user.id,
            "email": user.email,
            "job_title":user.job_title,
            "full_name": user.full_name,
            "password":user.hashed_password
            }


@router.post("/create_user", status_code=status.HTTP_200_OK)
def create_user(data:CreateUser, db:Session=Depends(get_db)):
    user = crud_user.get_by_email(db, data.user_data.email)
    if user:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Такой пользователь уже есть")
    
    if data.admin_key != config.ADMIN_KEY:
         return HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Неверный ADMIN_KEY")
        
    user =  crud_user.create_user(db, data)
    return {"message":"Пользователь создан"}


    





    

        