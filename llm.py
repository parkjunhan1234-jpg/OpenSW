from fastapi import APIRouter, Form
import requests

from fastapi.responses import HTMLResponse
import html

router = APIRouter()

@router.post("/ask", response_class=HTMLResponse)
def ask_lim(prompt : str = Form(...)):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen2.5-coder:0.5b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)

    if response.status_code != 200:
        return {
            "message": "LLM 서버 호출 실패",
            "status_code": response.status_code
        }
    
    result = response.json()

    answer = result["response"]
    organized_prompt = html.escape(prompt)
    organized_answer = html.escape(answer)

    return f"""
    <html>
        <body>
            <h1>로컬 LLM 답변</h1>

            <h2>질문</h2>
            <p>{organized_prompt}</p>

            <h2>답변</h2>
            <p>{organized_answer}</p>
        <body>
    </html>
    """