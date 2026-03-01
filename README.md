# Python Quant Finance Project

Systematic equity risk analysis and Monte Carlo simulation using Python and historical market data from Yahoo Finance.

---

## Overview

This project performs quantitative risk and return analysis on publicly traded equities using historical price data. It computes key performance metrics and models future price paths via Monte Carlo simulation.

The objective of this project was to demonstrate:

- Application of statistical methods to financial markets  
- Risk-adjusted performance analysis  
- Probabilistic forecasting  
- Structured, reproducible quantitative workflow  

---

## Key Features

### Risk & Performance Metrics
- Annualised Return  
- Annualised Volatility  
- Sharpe Ratio  
- 95% Historical Value-at-Risk (VaR)

### Benchmark Comparison
- Relative performance vs SPY (S&P 500 ETF)
- Normalised price comparison

### Distribution Analysis
- Empirical daily return distribution

### Monte Carlo Simulation
- 1-year forward simulation
- 1,000 simulated price paths
- Parametrised using historical mean and volatility

---

## Quantitative Concepts Applied

- Financial time series analysis  
- Risk-adjusted return measurement  
- Volatility estimation  
- Stochastic simulation  
- Downside risk estimation  

---

## Tech Stack

- Python  
- NumPy  
- Pandas  
- Matplotlib  
- yFinance  

---

## Example Outputs

### Price History
![Price History](images/price_history.png)

### Returns Distribution
![Returns Distribution](images/returns_distribution.png)

### Benchmark Comparison
![Benchmark Comparison](images/aapl_vs_spy.png)

### Monte Carlo Simulation
![Monte Carlo Simulation](images/monte_carlo_paths.png)

---

## How to Run

pip install numpy pandas matplotlib yfinance  
python analysis.py  

---

## Background & Motivation

As a mechanical engineer transitioning into finance, I built this project to apply statistical modelling techniques to capital markets and develop practical intuition around risk, volatility, and probabilistic forecasting.

This project reflects an analytical approach to financial data and demonstrates the ability to implement quantitative models in a structured and reproducible way.

---

## Future Extensions

- CAPM beta estimation  
- Rolling volatility modelling  
- Maximum drawdown analysis  
- Multi-asset portfolio extension  
- Factor exposure analysis  
