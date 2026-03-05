from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.user import CreateUser, UserResponse
from app.auth import AuthService


auth_service = AuthService()


class CRUDUser:
    def get_by_email(self, db:Session, email:str):
        return db.query(User).filter(email==User.email).first()

    
    def create_user(self, db:Session, user_data:CreateUser):
        user_obj = User(
            email = user_data.user_data.email,
            job_title = user_data.user_data.job_title,
            full_name = user_data.user_data.full_name,
            hashed_password = user_data.user_data.password,
            must_change_password = True 
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

        
