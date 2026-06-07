from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from basic import User
from db import get_db, UserDB

from fastapi import Form

router = APIRouter()

@router.post("/register")
def register(name: str = Form(...), age: str = Form(...), db: Session = Depends(get_db)):
    new_user = UserDB(
        username=name,
        age=age,
        password="1234"
    )
    
    db.add(new_user)
    db.commit()

    return {"message": "회원가입 완료"}

@router.get("/login")
def login(name: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(
        (UserDB.username == name) & (UserDB.password == password)
    ).first()

    if not db_user:
        return {"message": "사용자 정보가 올바르지 않음"}
    
    return {"message": "로그인 성공"}

@router.get("/modify") 
def modify_password(name: str, newpassword: str, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(
        UserDB.username == name
    ).first()

    if not db_user:
        return {"message": "사용자 정보가 올바르지 않음"}
    
    db_user.password = newpassword
    db.commit()
    
    return {"message": f"{newpassword}로 비밀번호 수정 완료"}