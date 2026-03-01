# Python Quant Finance Project

## Overview
This project performs systematic equity risk analysis using historical market data from Yahoo Finance.

It calculates:

- Annualised return
- Annualised volatility
- Sharpe ratio
- 95% Value at Risk (VaR)
- Monte Carlo price simulation (1-year horizon)
- Benchmark comparison vs SPY

---

## Methodology

Daily returns are computed from adjusted closing prices.

Metrics are annualised assuming:
- 252 trading days per year
- 2% risk-free rate (Sharpe ratio calculation)

Monte Carlo simulations assume normally distributed daily returns using historical mean and volatility.

---

## Tools Used
- Python
- NumPy
- Pandas
- Matplotlib
- yFinance

---

## Author
Ted Wiseman
