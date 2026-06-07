from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

router = APIRouter()

class Item(BaseModel):
    name: str
    price: int

class User(BaseModel):
    name: str
    age: int

@router.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <body>
            <h1>나의 첫 웹 페이지</h1>
            <p>FastAPI가 HTML을 반환했습니다.</p>

            <hr>

            <h2>기능 선택</h2>

            <h2>나만의 질의응답기 with Local LLM</h2>
            <form action="/ask" method="post">
                <p>
                    프롬프트 : <input type="text" name="prompt">
                </p>
                <button type="submit">질문하기</button>
            </form>

            <h2>덧셈</h2>
            <form action="/add" method="get">
                <p>
                    a: <input type="number" name="a" value="10">
                </p>
                <p>
                    b: <input type="number" name="b" value="20">
                </p>
                <button type="submit">덧셈 실행</button>
            </form>

            <h2>뺄셈</h2>
            <form action="/minus" method="get">
                <p>
                    a: <input type="number" name="a" value="30">
                </p>
                <p>
                    b: <input type="number" name="b" value="10">
                </p>
                <button type="submit">뺄셈 실행</button>
            </form>

            <hr>

            <h2>사용자 등록</h2>
            <form action="/register" method="post">
                <p>
                    이름: <input type="text" name="name" value="sdkim">
                </p>
                <p>
                    나이: <input type="text" name="age" value="20">
                </p>
                <button type="submit">사용자 등록</button>
            </form>

            <hr>

            <h2>사용자 로그인</h2>
            <form action="/login" method="get">
                <p>
                    이름: <input type="text" name="name" value="sdkim">
                </p>
                <p>
                    나이: <input type="text" name="password" value="1234">
                </p>
                <button type="submit">사용자 로그인</button>
            </form>

            <hr>

            <h2>사용자 비밀번호 수정</h2>
            <form action="/modify" method="get">
                <p>
                    이름: <input type="text" name="name" value="sdkim">
                </p>
                <p>
                    나이: <input type="text" name="newpassword" value="9876">
                </p>
                <button type="submit">사용자 비밀번호 수정</button>
            </form>

        </body>
    </html>
    """

@router.get("/multi")
def multi(a:int, b:int):
    return {"result": a*b}
   
@router.post("/item")
def create_item(item:Item):
    return {
        "name": item.name,
        "price": item.price
    }

@router.post("/user")
def create_user(user: User):
    return {
        "message": f"{user.name} 등록완료",
        "age": user.age
    }