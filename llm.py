import requests

def get_pulse_from_llm(ticker, momentum, news, api_key):
    # Build news string separately to avoid backslash issue
    news_lines = ""
    for item in news:
        title = item.get("title", "")
        description = item.get("description", "")
        news_lines += f"- {title}: {description}\n"

    # Build prompt using proper formatting
    prompt = (
        f"You are a stock analyst assistant.\n\n"
        f"Stock: {ticker.upper()}\n"
        f"Momentum Score: {momentum['score']}\n"
        f"Last 5-day Returns: {momentum['returns']}\n\n"
        f"Recent News Headlines:\n"
        f"{news_lines}\n"
        "Based on the momentum and news context, is the stock looking bullish, bearish, or neutral for tomorrow?\n"
        "Give a short explanation in 1–2 sentences referencing the data."
    )

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        full_url = f"{url}?key={api_key}"
        res = requests.post(full_url, headers=headers, json=payload)
        res.raise_for_status()

        reply = res.json()
        text = reply["candidates"][0]["content"]["parts"][0]["text"]

        # Extract pulse
        pulse = "neutral"
        if "bullish" in text.lower():
            pulse = "bullish"
        elif "bearish" in text.lower():
            pulse = "bearish"

        return pulse, text

    except Exception as e:
        print("Error in get_pulse_from_llm:", e)
        return "neutral", "LLM explanation could not be generated due to an error."
