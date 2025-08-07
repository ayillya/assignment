from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os

from momentum import get_price_momentum
from news import get_news_headlines
from llm import get_pulse_from_llm

load_dotenv()

app = FastAPI()

@app.get("/api/v1/market-pulse")
async def market_pulse(ticker: str = Query(..., description="Stock ticker symbol")):
    alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")
    news_key = os.getenv("NEWS_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    momentum = get_price_momentum(ticker, alpha_key)
    news = get_news_headlines(ticker, news_key)
    pulse, explanation = get_pulse_from_llm(ticker, momentum, news, gemini_key)

    return {
        "ticker": ticker.upper(),
        "momentum": momentum,
        "news": news,
        "pulse": pulse,
        "llm_explanation": explanation
    }
