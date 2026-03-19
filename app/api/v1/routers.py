from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.user import CRUDUser
from app.schemas.user import CreateUser, AuthKeyUser, FirstLoginResponce, FirstLoginChangePassword
from app.core.config import config
from app.auth import AuthService
from fastapi.responses import HTMLResponse
import os



router = APIRouter()


crud_user = CRUDUser()


@router.get("/", response_class=HTMLResponse, tags=["Фронтенд"])
def serve_frontend():
    """
    Этот эндпоинт просто читает файл index.html и отдает его в браузер
    """
    # Укажи правильный путь к файлу index.html, если он лежит в другой папке
    file_path = "app/api/v1/index.html" 

    if not os.path.exists(file_path):
        return "<h1>Файл index.html не найден!</h1>"

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


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
            #"password":user.hashed_password
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

@router.post("/first_login", response_model=FirstLoginResponce)
def first_login(data:FirstLoginChangePassword, db:Session=Depends(get_db)):
    user = crud_user.get_by_email(db, data.email)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Такой пользователь уже есть")
    
    #if not AuthService.verify_password(data.password, user.hashed_password):
        #raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail = "Неверный емайл или пароль")
    
    if not user.must_change_password:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Пароль уже был изменен")
    
    user.hashed_password = AuthService.get_password_hash(data.new_password)
    user.must_change_password = False
    db.commit()
    return FirstLoginResponce(
        message = "Пароль успешно изменен",
        success = True,
    )



    





    

        