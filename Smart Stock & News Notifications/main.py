import requests
from twilio.rest import Client

# Twilio Configuration
VIRTUAL_TWILIO_NUMBER = "your_virtual_twilio_number"
VERIFIED_NUMBER = "your_verified_phone_number"

# Stock and News API Configuration
STOCK_NAME = "TSLA"  # Tesla Stock
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR_ALPHAVANTAGE_API_KEY"
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"
TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"

# Fetch Stock Data
stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK_NAME,
    "interval": "60min",
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json().get("Time Series (60min)", {})

# Convert dictionary to list and fetch latest two data points
data_list = list(data.values())
if len(data_list) < 2:
    print("Not enough stock data available. Try again later.")
    exit()

latest_data = data_list[0]
previous_data = data_list[1]

# Get closing prices
latest_closing_price = float(latest_data["4. close"])
previous_closing_price = float(previous_data["4. close"])

# Calculate percentage change
difference = latest_closing_price - previous_closing_price
diff_percent = round((difference / previous_closing_price) * 100, 2)
print(f"Stock Change Detected: {diff_percent}%")

# Fetch news if significant stock change is detected
if abs(diff_percent) > 0.3:
    # Fetch News Articles
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
        "sortBy": "popularity",
        "language": "en",
        "pageSize": 3,  # Get top 3 news articles
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()

    # ✅ Check if 'articles' key exists
    if "articles" not in news_data:
        print("News API Response:", news_data)  # Debugging
        exit()

    # Extract and format news articles
    articles = news_data["articles"][:3]
    formatted_articles = [
        f"{STOCK_NAME}: {'🔺' if difference > 0 else '🔻'}{diff_percent}%\n"
        f"Headline: {article['title']}\nBrief: {article['description']}"
        for article in articles
    ]
    print(formatted_articles)

    # Send SMS via Twilio
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )

else:
    print(f"No significant stock change detected ({diff_percent}%). No news fetched.")
