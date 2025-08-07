import requests

def get_price_momentum(ticker: str, api_key: str):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "outputsize": "compact",
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            raise ValueError(f"Alpha Vantage error: {data.get('Note') or data.get('Error Message')}")

        # Extract and sort the most recent 6 closing prices
        sorted_dates = sorted(time_series.keys(), reverse=True)
        closes = [float(time_series[date]["5. adjusted close"]) for date in sorted_dates[:6]]

        if len(closes) < 6:
            raise ValueError("Not enough data to calculate 5 returns")

        # Calculate 5 daily % returns
        returns = []
        for i in range(1, 6):
            prev = closes[i]
            curr = closes[i - 1]
            ret = ((curr - prev) / prev) * 100
            returns.append(round(ret, 2))

        # Momentum score = average return
        score = round(sum(returns) / len(returns), 2)

        return {
            "returns": returns,
            "score": score
        }

    except Exception as e:
        print("Error in get_price_momentum:", e)
        return {
            "returns": [],
            "score": 0.0
        }
