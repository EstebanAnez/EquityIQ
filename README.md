<p align="center">
  <img src="Images/EquityIQ_Big.jpeg" alt="EquityIQ" width="420">
</p>

<h1 align="center">EquityIQ</h1>

<p align="center">
  An AI equity research assistant that answers questions about public companies with live market data, news and analyst style reasoning.
</p>

<p align="center">
  <a href="https://equityiq.streamlit.app"><b>Live demo</b></a>
</p>

---

## What it does

Ask EquityIQ about any listed company in plain English ("Give me a full analysis of NVDA", "How has MSFT traded in the last 3 months?", "What's the latest news on AAPL?") and it answers like a junior equity research analyst:

- Pulls **live fundamentals and prices** instead of guessing numbers
- Interprets **valuation, profitability, growth and risk ratios** into clear signals
- Reads **recent headlines** and gives an overall sentiment
- Structures answers like a research note, using a library of real equity research reports as a style and reasoning guide (RAG)

## How it works

```
User question
     │
     ▼
Streamlit chat UI ──► LangChain agent (GPT-4o mini)
                          │
          ┌───────────────┼──────────────────────────┐
          ▼               ▼                          ▼
   Market data tools   News tools              RAG retrieval
   (yfinance)          (yfinance + NewsAPI)    (FAISS + OpenAI embeddings)
```

The agent decides which tools to call for each question:

| Tool | What it returns |
|---|---|
| `get_stock_snapshot` | Price, market cap, valuation multiples, growth, margins, beta, business summary |
| `get_price_performance` | 3 month return, high, low and average volume |
| `interpret_financial_ratios` | Ratio based signals for valuation, profitability, growth and risk |
| `get_news_sentiment` | Recent headlines with an overall sentiment label |
| `get_news_headlines` | Latest real world headlines through NewsAPI |

Retrieved research documents shape the structure of the answer (thesis, bull and bear case, valuation context), while every company specific number comes from the live tools. The system prompt tells the agent never to invent figures.

## Tech stack

Python · LangChain / LangGraph agents · OpenAI API · FAISS · yfinance · NewsAPI · Streamlit · Streamlit Community Cloud

## Run it locally

```bash
git clone https://github.com/EstebanAnez/EquityIQ.git
cd EquityIQ
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` (already in `.gitignore`):

```toml
OPENAI_API_KEY = "your-openai-key"
NEWS_API_KEY = "your-newsapi-key"
```

Then start the app:

```bash
streamlit run app.py
```

The FAISS index ships with the repo. To rebuild it from your own documents, put them in a `rag_files/` folder and run `python build_faiss_index.py`.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit chat interface |
| `EquityIQ_step_5.py` | Agent setup, system prompt and RAG retrieval |
| `EquityIQ_tools.py` | The five research tools |
| `build_faiss_index.py` | Builds the vector index from research documents |
| `faiss_index/` | Prebuilt vector index |

## Disclaimer

EquityIQ is an educational project. Its output is not investment advice.

---

Built by [Esteban Añez](https://www.linkedin.com/in/esteban-anez) · MBA/MSBA, University of Kansas
