import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter

router = APIRouter()

@router.get("/crawling")
def crawling():
    soup = BeautifulSoup(requests.get("http://quotes.toscrape.com/").text, "lxml")

    quotes = []
    for i in soup.find_all("div", {"class": "quote"}):
        quotes.append(i.text.strip())

    return {"quotes": quotes}
