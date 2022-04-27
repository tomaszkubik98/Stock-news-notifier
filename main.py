STOCK = "TSLA"
COMPANY_NAME = "Tesla"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

NEWS_API_KEY = "key1"
ALPHA_API_KEY = "key2"
alpha_params = {
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY
}
import requests
import datetime as dt
import smtplib
import math


today = str(dt.date.today())
yesterday = str(dt.date.today() - dt.timedelta(days=1))
day_before = str(dt.date.today() - dt.timedelta(days=2))

response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY",params=alpha_params)
response.raise_for_status()
stock_data = response.json()
yesterdays_close_price = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])
day_before_close_price = float(stock_data["Time Series (Daily)"][day_before]["4. close"])

def price_change():
     if day_before_close_price*0.95 > yesterdays_close_price or day_before_close_price*1.05 < yesterdays_close_price:
        news_parameters = {
            "q": COMPANY_NAME,
            "from": today,
            "sortBy": "popularity",
            "apikey": NEWS_API_KEY,
        }
        news_response = requests.get("https://newsapi.org/v2/everything",params=news_parameters)
        articles = news_response.json()["articles"][:4]
        list_of_articles = [[{"title":articles[num]["title"],"brief":articles[num]["description"]}] for num in range(0,3)]

        for num in range(0,2):
            with smtplib.SMTP("smtp.office365.com") as connection:
                connection.starttls()
                connection.login(user="my_email",password="password")
                connection.sendmail(
                    from_addr="my_email",
                    to_addrs="user_email",
                    msg=f"Subject:{price_direction()},{list_of_articles[num][0]['title']}\n\n{list_of_articles[num][0]['brief']}"
                )

def price_direction():
    if yesterdays_close_price>day_before_close_price:
        return f"{math.ceil((yesterdays_close_price/day_before_close_price-1)*100)}"
    else:
        return f"{math.ceil((yesterdays_close_price/day_before_close_price-1)*-100)}"

price_change()

