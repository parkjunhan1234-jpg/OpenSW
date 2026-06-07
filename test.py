from fastapi import FastAPI

from basic import router as basic_router
from auth import router as auth_router
from crawling import router as crawling_router
from llm import router as llm_router

app = FastAPI()
app.include_router(basic_router)
app.include_router(auth_router)
app.include_router(crawling_router)
app.include_router(llm_router)

