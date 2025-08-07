import requests

def get_news_headlines(ticker: str, api_key: str):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "sortBy": "publishedAt",
        "pageSize": 5,
        "language": "en",
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "articles" not in data:
            raise ValueError(f"NewsAPI error: {data.get('message')}")

        articles = data["articles"][:5]
        return [{
            "title": a["title"],
            "description": a["description"],
            "url": a["url"]
        } for a in articles]

    except Exception as e:
        print("Error in get_news_headlines:", e)
        return []
