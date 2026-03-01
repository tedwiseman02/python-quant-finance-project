import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def compute_metrics(data: pd.DataFrame, price_col: str, risk_free_rate: float = 0.02) -> dict:
    """Compute annualised return, volatility, Sharpe ratio, and 95% daily VaR."""
    prices = data[price_col]

    # If prices is a DataFrame (can happen with multi-index), take first column
    if isinstance(prices, pd.DataFrame):
        prices = prices.iloc[:, 0]

    returns = prices.pct_change().dropna()

    annual_return = float(returns.mean() * 252)
    annual_volatility = float(returns.std() * np.sqrt(252))
    sharpe_ratio = float((annual_return - risk_free_rate) / annual_volatility)
    var_95 = float(np.percentile(returns, 5))

    return {
        "returns": returns,
        "annual_return": annual_return,
        "annual_volatility": annual_volatility,
        "sharpe_ratio": sharpe_ratio,
        "var_95": var_95,
    }


def monte_carlo_paths(
    last_price: float,
    annual_return: float,
    annual_volatility: float,
    days: int = 252,
    simulations: int = 1000,
) -> np.ndarray:
    """Simple Monte Carlo simulation of future prices using normal daily returns."""
    mu_daily = annual_return / 252
    sigma_daily = annual_volatility / np.sqrt(252)

    simulated_prices = np.zeros((days, simulations))

    for i in range(simulations):
        price = last_price
        for t in range(days):
            shock = np.random.normal(mu_daily, sigma_daily)
            price = price * (1 + shock)
            simulated_prices[t, i] = price

    return simulated_prices


def _to_series(x) -> pd.Series:
    """If x is a DataFrame, take first column; else return as-is."""
    return x.iloc[:, 0] if isinstance(x, pd.DataFrame) else x


def main() -> None:
    ticker = "AAPL"
    start_date = "2020-01-01"
    risk_free_rate = 0.02

    # --- Download stock data ---
    data = yf.download(ticker, start=start_date)
    if data.empty:
        raise ValueError("No data downloaded for ticker. Check your internet connection or try again.")

    # Choose a price column safely
    if "Adj Close" in data.columns:
        price_col = "Adj Close"
    elif "Close" in data.columns:
        price_col = "Close"
    else:
        raise ValueError("No price column found (expected 'Adj Close' or 'Close').")

    # --- Compute metrics ---
    metrics = compute_metrics(data, price_col=price_col, risk_free_rate=risk_free_rate)

    print(f"Ticker: {ticker}")
    print(f"Annual Return: {metrics['annual_return']:.2%}")
    print(f"Annual Volatility: {metrics['annual_volatility']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Value at Risk (95%): {metrics['var_95']:.2%}")

    # --- Benchmark comparison (SPY) ---
    benchmark = yf.download("SPY", start=start_date)

    if benchmark.empty:
        print("\nBenchmark: SPY (download failed or empty). Skipping benchmark comparison.")
    else:
        # Pick benchmark price column
        if "Adj Close" in benchmark.columns:
            bench_price_col = "Adj Close"
        elif "Close" in benchmark.columns:
            bench_price_col = "Close"
        else:
            bench_price_col = None

        if bench_price_col is None:
            print("\nBenchmark: SPY (no price column found). Skipping benchmark comparison.")
        else:
            bench_prices = _to_series(benchmark[bench_price_col])
            bench_returns = bench_prices.pct_change().dropna()

            bench_annual_return = float(bench_returns.mean() * 252)
            bench_annual_volatility = float(bench_returns.std() * np.sqrt(252))

            print("\nBenchmark: SPY")
            print(f"SPY Annual Return: {bench_annual_return:.2%}")
            print(f"SPY Annual Volatility: {bench_annual_volatility:.2%}")

            # Plot: Normalised price comparison
            plt.figure()
            stock_prices = _to_series(data[price_col])
            (stock_prices / stock_prices.iloc[0]).plot(label=ticker)
            (bench_prices / bench_prices.iloc[0]).plot(label="SPY")
            plt.title(f"{ticker} vs SPY (Normalised Prices)")
            plt.xlabel("Date")
            plt.ylabel("Normalised Price")
            plt.legend()
            plt.show()

    # --- Plot 1: Price history ---
    plt.figure()
    stock_prices = _to_series(data[price_col])
    stock_prices.plot(title=f"{ticker} {price_col} Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

    # --- Plot 2: Returns distribution ---
    plt.figure()
    metrics["returns"].hist(bins=50)
    plt.title(f"{ticker} Daily Return Distribution")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.show()

    # --- Plot 3: Monte Carlo simulation ---
    last_price = float(stock_prices.iloc[-1])
    simulated_prices = monte_carlo_paths(
        last_price=last_price,
        annual_return=metrics["annual_return"],
        annual_volatility=metrics["annual_volatility"],
        days=252,
        simulations=1000,
    )

    plt.figure()
    plt.plot(simulated_prices, linewidth=0.7)
    plt.title(f"{ticker} Monte Carlo Simulation (1 Year, 1000 paths)")
    plt.xlabel("Trading Days")
    plt.ylabel("Simulated Price")
    plt.show()


if __name__ == "__main__":
    main()