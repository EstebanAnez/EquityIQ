import yfinance as yf
import requests
import os
import streamlit as st
from langchain.tools import tool

@tool
def get_stock_snapshot(ticker: str):
    """
    Use this tool when the user asks for company-level stock information
    such as current price, market cap, valuation, profitability, or business details.
    Input should be a stock ticker like MSFT, AAPL, or NVDA.
    """
    print("The agent is using get_stock_snapshot tool")
    print(ticker)

    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "symbol" not in info:
            return f"Could not retrieve stock information for ticker {ticker}."

        snapshot = {
            "company_name": info.get("longName"),
            "ticker": info.get("symbol"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "trailing_pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "price_to_book": info.get("priceToBook"),
            "profit_margin": info.get("profitMargins"),
            "return_on_equity": info.get("returnOnEquity"),
            "revenue_growth": info.get("revenueGrowth"),
            "beta": info.get("beta"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        }

        return str(snapshot)

    except Exception as e:
        return f"Error retrieving stock snapshot for {ticker}: {str(e)}"


@tool
def get_price_performance(ticker: str):
    """
    Use this tool when the user asks about recent stock performance,
    price trend, returns, volatility, or recent trading behavior.
    Input should be a stock ticker like MSFT, AAPL, or NVDA.
    """
    print("The agent is using get_price_performance tool")
    print(ticker)

    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo")

        if hist.empty:
            return f"Could not retrieve price history for ticker {ticker}."

        start_price = float(hist["Close"].iloc[0])
        end_price = float(hist["Close"].iloc[-1])
        high_price = float(hist["High"].max())
        low_price = float(hist["Low"].min())
        avg_volume = float(hist["Volume"].mean())

        return_pct = ((end_price - start_price) / start_price) * 100

        performance = {
            "ticker": ticker,
            "period": "3 months",
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "return_pct": round(return_pct, 2),
            "high_price": round(high_price, 2),
            "low_price": round(low_price, 2),
            "average_volume": round(avg_volume, 2),
        }

        return str(performance)

    except Exception as e:
        return f"Error retrieving price performance for {ticker}: {str(e)}"


@tool
def get_news_sentiment(ticker: str):
    """
    Use this tool when the user asks about recent news, headlines, or sentiment.
    Returns recent headlines and a simple sentiment classification.
    Input should be a stock ticker like MSFT, AAPL, or NVDA.
    """
    print("The agent is using get_news_sentiment tool")
    print(ticker)

    positive_words = [
        "beat", "growth", "strong", "surge", "gain", "up",
        "bullish", "record", "expand", "positive", "profit", "upgrade"
    ]

    negative_words = [
        "miss", "weak", "drop", "fall", "down",
        "bearish", "risk", "concern", "loss", "cut", "downgrade", "decline"
    ]

    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        news_items = stock.news

        if not news_items:
            return f"No recent news found for ticker {ticker}."

        headlines = []
        total_score = 0

        for item in news_items[:5]:
            title = item.get("title", "")
            lower_title = title.lower()

            score = 0

            for word in positive_words:
                if word in lower_title:
                    score += 1

            for word in negative_words:
                if word in lower_title:
                    score -= 1

            headlines.append({
                "headline": title,
                "score": score
            })

            total_score += score

        # Determine overall sentiment
        if total_score > 1:
            sentiment = "Positive"
        elif total_score < -1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        result = {
            "ticker": ticker,
            "sentiment": sentiment,
            "headlines": headlines
        }

        return str(result)

    except Exception as e:
        return f"Error retrieving news sentiment for {ticker}: {str(e)}"


@tool
def interpret_financial_ratios(ticker: str):
    """
    Use this tool when the user asks for valuation interpretation, ratio analysis,
    financial strength, profitability quality, growth quality, or risk interpretation.

    This tool retrieves key financial ratios for a stock ticker and converts them into
    analyst-style signals. It should be used after or alongside the stock snapshot tool
    when the user asks for a full company analysis, valuation view, risk view, or
    investment-style interpretation.

    Input should be a stock ticker like MSFT, AAPL, or NVDA.
    """
    print("The agent is using interpret_financial_ratios tool")
    print(ticker)

    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "symbol" not in info:
            return f"Could not retrieve financial ratios for ticker {ticker}."

        trailing_pe = info.get("trailingPE")
        forward_pe = info.get("forwardPE")
        price_to_book = info.get("priceToBook")
        profit_margin = info.get("profitMargins")
        return_on_equity = info.get("returnOnEquity")
        revenue_growth = info.get("revenueGrowth")
        beta = info.get("beta")

        interpretation = {
            "ticker": ticker,
            "valuation_signal": "",
            "profitability_signal": "",
            "growth_signal": "",
            "risk_signal": "",
            "summary": ""
        }

        # Valuation interpretation
        if trailing_pe is None:
            interpretation["valuation_signal"] = "Trailing P/E is unavailable, so valuation is harder to judge from earnings."
        elif trailing_pe < 15:
            interpretation["valuation_signal"] = f"Trailing P/E of {round(trailing_pe, 2)} suggests a relatively low earnings multiple."
        elif trailing_pe <= 30:
            interpretation["valuation_signal"] = f"Trailing P/E of {round(trailing_pe, 2)} suggests a moderate valuation."
        else:
            interpretation["valuation_signal"] = f"Trailing P/E of {round(trailing_pe, 2)} suggests a premium valuation that requires strong future growth."

        # Forward valuation interpretation
        if forward_pe is not None:
            if trailing_pe is not None and forward_pe < trailing_pe:
                interpretation["valuation_signal"] += f" Forward P/E of {round(forward_pe, 2)} is below trailing P/E, which may suggest expected earnings growth."
            else:
                interpretation["valuation_signal"] += f" Forward P/E is {round(forward_pe, 2)}."

        # Profitability interpretation
        if profit_margin is None and return_on_equity is None:
            interpretation["profitability_signal"] = "Profit margin and ROE are unavailable."
        else:
            profitability_points = []

            if profit_margin is not None:
                margin_pct = profit_margin * 100
                if margin_pct < 5:
                    profitability_points.append(f"Profit margin of {round(margin_pct, 2)}% is relatively thin.")
                elif margin_pct <= 20:
                    profitability_points.append(f"Profit margin of {round(margin_pct, 2)}% is solid.")
                else:
                    profitability_points.append(f"Profit margin of {round(margin_pct, 2)}% is very strong.")

            if return_on_equity is not None:
                roe_pct = return_on_equity * 100
                if roe_pct < 10:
                    profitability_points.append(f"ROE of {round(roe_pct, 2)}% is modest.")
                elif roe_pct <= 25:
                    profitability_points.append(f"ROE of {round(roe_pct, 2)}% is strong.")
                else:
                    profitability_points.append(f"ROE of {round(roe_pct, 2)}% is very high, suggesting strong returns on equity.")

            interpretation["profitability_signal"] = " ".join(profitability_points)

        # Growth interpretation
        if revenue_growth is None:
            interpretation["growth_signal"] = "Revenue growth is unavailable."
        else:
            growth_pct = revenue_growth * 100

            if growth_pct < 0:
                interpretation["growth_signal"] = f"Revenue growth of {round(growth_pct, 2)}% indicates recent contraction."
            elif growth_pct < 5:
                interpretation["growth_signal"] = f"Revenue growth of {round(growth_pct, 2)}% is low."
            elif growth_pct <= 15:
                interpretation["growth_signal"] = f"Revenue growth of {round(growth_pct, 2)}% is healthy."
            else:
                interpretation["growth_signal"] = f"Revenue growth of {round(growth_pct, 2)}% is strong."

        # Risk interpretation
        if beta is None:
            interpretation["risk_signal"] = "Beta is unavailable, so market sensitivity is harder to assess."
        elif beta < 0.8:
            interpretation["risk_signal"] = f"Beta of {round(beta, 2)} suggests below-market volatility."
        elif beta <= 1.2:
            interpretation["risk_signal"] = f"Beta of {round(beta, 2)} suggests market-like volatility."
        else:
            interpretation["risk_signal"] = f"Beta of {round(beta, 2)} suggests above-market volatility."

        # Summary interpretation
        interpretation["summary"] = (
            "Use these signals to explain whether the stock looks expensive or inexpensive, "
            "whether profitability supports the valuation, whether growth justifies the multiple, "
            "and whether risk is elevated."
        )

        return str(interpretation)

    except Exception as e:
        return f"Error interpreting financial ratios for {ticker}: {str(e)}"
@tool
def get_news_headlines(ticker: str):
    """
    Use this tool when the user asks for real-world news, recent developments,
    or latest headlines about a company.

    This tool retrieves recent news articles using NewsAPI.

    Input should be a stock ticker like MSFT, AAPL, or NVDA.
    """
    print("The agent is using get_news_headlines tool")
    print(ticker)

    try:
        ticker = ticker.upper()


        api_key = st.secrets["NEWS_API_KEY"]

        url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&pageSize=5&apiKey={api_key}"

        response = requests.get(url)
        data = response.json()

        if data["status"] != "ok":
            return "Error retrieving news."

        articles = data.get("articles", [])

        if not articles:
            return f"No recent news found for ticker {ticker}."

        headlines = []

        for article in articles[:5]:
            headlines.append(article["title"])

        return str({
            "ticker": ticker,
            "headlines": headlines
        })

    except Exception as e:
        return f"Error retrieving news headlines for {ticker}: {str(e)}"