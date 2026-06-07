from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/minus")
def minus(a: int, b: int):
    return {"result": a - b}

from pydantic import BaseModel

class Item(BaseModel):
    name : str
    price : int
   
@app.post("/item")
def create_item(item: Item):
    return {
        "name": item.name,
        "price": item.price
    }

class User(BaseModel):
    name : str
    age : int

@app.post("/user")
def create_user(user: User):
    return {
        "message": f"{user.name} 등록 완료",
        "age": user.age
    }

#SQLite 기초 설정, test.db를 생성함.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 회원 테이블(users)을 생성함.
from sqlalchemy import Column, Integer, String

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

    
#생성한 test.db 사용 준비
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#사용자의 /register 명령에 따라 DB 저장
@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):

    new_user = UserDB(
        username=user.name,
        password="1234",
    )

    db.add(new_user)
    db.commit()

    return {"message": "회원가입 완료"}

#사용자의 /login 요청에 따라 DB 조회 및 응답
@app.get("/login")
def login(name: str, password: str, db: Session = Depends(get_db)):

    db_user = db.query(UserDB).filter((UserDB.username == name) & (UserDB.password == password)).first()

    if not db_user:
        return {"message": "사용자 정보가 올바르지 않음"}
    
    return {"message": "로그인 성공"}

@app.get("/modify") #url 주소로 적절한 명령을 작성
def login(name: str, newpassword: str, db: Session = Depends(get_db)): #url 주소로 적절한 명령을 작성

    db_user = db.query(UserDB).filter(UserDB.username == name).first()

    if not db_user:
        return {"message": "사용자 정보가 올바르지 않음"}
    
    db_user.password = newpassword
    db.commit()
    return {"message": f"{newpassword}로 비밀번호 수정 완료"}