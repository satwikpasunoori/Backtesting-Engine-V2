🚀 Professional Backtesting Engine (FastAPI + Docker)

A production-ready quantitative backtesting engine built with FastAPI, Docker, and risk-based capital management.

This engine allows traders to:

Upload OHLC data (CSV / XLSX)

Apply rule-based strategy logic

Execute realistic R-based risk management

Generate full trade logs

Evaluate strategy robustness using Monte Carlo simulations

Designed for systematic traders building automated trading systems.

🧠 Core Architecture
1️⃣ Strategy Layer

Implements signal generation + stop logic.
(Current example: Break above previous high → Long)
Source: 

strategy

2️⃣ Backtest Execution Engine

Handles:

Fixed % capital risk per trade

Position sizing based on stop distance

RR-based targets

Realistic SL/TP evaluation

Trade recording

R-multiple tracking

Source: 

engine

3️⃣ Metrics Engine

Automatically calculates:

Total trades

Win rate

Expectancy (R)

Profit Factor

Max losing streak

4️⃣ Monte Carlo Simulation

1000 randomized trade sequences

Median final R

95th percentile worst drawdown

95th percentile losing streak

This helps evaluate psychological & sequence risk.

5️⃣ API Interface

Built with FastAPI.

Upload dataset

Input RR

Input Capital

Input Risk %

Get JSON performance report

Download full trade logs

Source: 

main

🐳 Docker Deployment

Fully containerized.

Docker config:

Service definition → 

docker-compose

Dependencies → 

requirements

Run:
docker-compose up --build

Then open:

http://localhost:8000
⚙️ Risk Model

Position size =

risk_amount / stop_distance

Where:

risk_amount = capital × risk_percent

1R = full predefined risk

This makes it compatible with:

Stocks

Index futures

Crypto

Options (with adjusted delta logic externally)

📊 Output Example
{
  "Strategy_Result": {
    "trades": 319,
    "win_rate": 41.69,
    "expectancy_R": 0.252,
    "profit_factor": 1.43,
    "max_losing_streak": 9
  },
  "Monte_Carlo": {
    "median_final_R": 80.39,
    "worst_dd_95p": 20.0,
    "worst_losing_streak_95p": 13
  }
}
🔥 Why This Matters

Backtests alone are not enough.

This engine measures:

Capital-adjusted risk

Sequence risk

Psychological stress zones

Drawdown probability

It bridges the gap between:

Backtest → Probability → Real Execution
