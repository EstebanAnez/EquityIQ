"""Tests for EquityIQ's research tools.

yfinance is replaced with a fake ticker, so these run offline and without API keys.
"""
import ast

import pytest

import EquityIQ_tools as tools


class FakeTicker:
    def __init__(self, info):
        self.info = info


@pytest.fixture
def fake_market(monkeypatch):
    """Point yfinance at a fake company with the given fundamentals."""

    def install(**info):
        info.setdefault("symbol", "TEST")
        monkeypatch.setattr(tools.yf, "Ticker", lambda ticker: FakeTicker(info))

    return install


def signals(ticker="test"):
    return ast.literal_eval(tools.interpret_financial_ratios.invoke({"ticker": ticker}))


def test_cheap_profitable_low_risk_company(fake_market):
    fake_market(trailingPE=12, forwardPE=10, profitMargins=0.25, returnOnEquity=0.30,
                revenueGrowth=0.20, beta=0.6)
    s = signals()
    assert s["ticker"] == "TEST"
    assert "relatively low earnings multiple" in s["valuation_signal"]
    assert "expected earnings growth" in s["valuation_signal"]
    assert "very strong" in s["profitability_signal"]
    assert "very high" in s["profitability_signal"]
    assert "is strong" in s["growth_signal"]
    assert "below-market volatility" in s["risk_signal"]


def test_expensive_shrinking_volatile_company(fake_market):
    fake_market(trailingPE=45, forwardPE=50, profitMargins=0.02, returnOnEquity=0.05,
                revenueGrowth=-0.08, beta=1.8)
    s = signals()
    assert "premium valuation" in s["valuation_signal"]
    assert "relatively thin" in s["profitability_signal"]
    assert "modest" in s["profitability_signal"]
    assert "contraction" in s["growth_signal"]
    assert "above-market volatility" in s["risk_signal"]


def test_missing_data_is_reported_not_invented(fake_market):
    fake_market()  # only a symbol, no fundamentals
    s = signals()
    assert "unavailable" in s["valuation_signal"]
    assert "unavailable" in s["profitability_signal"]
    assert "unavailable" in s["growth_signal"]
    assert "unavailable" in s["risk_signal"]


def test_unknown_ticker_is_handled(monkeypatch):
    monkeypatch.setattr(tools.yf, "Ticker", lambda ticker: FakeTicker({}))
    result = tools.get_stock_snapshot.invoke({"ticker": "zzzz"})
    assert result == "Could not retrieve stock information for ticker ZZZZ."


def test_snapshot_returns_key_fields(fake_market):
    fake_market(longName="Test Corp", currentPrice=101.5, marketCap=5_000_000_000)
    snapshot = ast.literal_eval(tools.get_stock_snapshot.invoke({"ticker": "test"}))
    assert snapshot["company_name"] == "Test Corp"
    assert snapshot["current_price"] == 101.5
    assert snapshot["market_cap"] == 5_000_000_000
