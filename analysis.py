import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from pathlib import Path

# --- Save folder (always the same folder as analysis.py) ---
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)


def compute_metrics(data: pd.DataFrame, price_col: str, risk_free_rate: float = 0.02) -> dict:
    prices = data[price_col]
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
    return x.iloc[:, 0] if isinstance(x, pd.DataFrame) else x


def save_current_fig(filename: str) -> None:
    """Save the current matplotlib figure into /images."""
    out_path = IMAGES_DIR / filename
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"Saved: {out_path.resolve()}")


def main() -> None:
    ticker = "AAPL"
    start_date = "2020-01-01"
    risk_free_rate = 0.02

    # --- Download stock data ---
    data = yf.download(ticker, start=start_date)
    if data.empty:
        raise ValueError("No data downloaded. Check your internet connection or ticker.")

    if "Adj Close" in data.columns:
        price_col = "Adj Close"
    elif "Close" in data.columns:
        price_col = "Close"
    else:
        raise ValueError("No price column found (expected 'Adj Close' or 'Close').")

    stock_prices = _to_series(data[price_col])

    # --- Compute metrics ---
    metrics = compute_metrics(data, price_col=price_col, risk_free_rate=risk_free_rate)

    print(f"Ticker: {ticker}")
    print(f"Annual Return: {metrics['annual_return']:.2%}")
    print(f"Annual Volatility: {metrics['annual_volatility']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Value at Risk (95%): {metrics['var_95']:.2%}")

    # --- Plot A: AAPL vs SPY (Normalised) ---
    benchmark = yf.download("SPY", start=start_date)
    if not benchmark.empty:
        if "Adj Close" in benchmark.columns:
            bench_price_col = "Adj Close"
        elif "Close" in benchmark.columns:
            bench_price_col = "Close"
        else:
            bench_price_col = None

        if bench_price_col:
            bench_prices = _to_series(benchmark[bench_price_col])

            plt.figure()
            (stock_prices / stock_prices.iloc[0]).plot(label=ticker)
            (bench_prices / bench_prices.iloc[0]).plot(label="SPY")
            plt.title(f"{ticker} vs SPY (Normalised Prices)")
            plt.xlabel("Date")
            plt.ylabel("Normalised Price")
            plt.legend()
            save_current_fig("aapl_vs_spy.png")
            plt.show()
            plt.close()

    # --- Plot B: Price history ---
    plt.figure()
    stock_prices.plot()
    plt.title(f"{ticker} Price History ({price_col})")
    plt.xlabel("Date")
    plt.ylabel("Price")
    save_current_fig("price_history.png")
    plt.show()
    plt.close()

    # --- Plot C: Daily returns distribution ---
    plt.figure()
    metrics["returns"].hist(bins=50)
    plt.title(f"{ticker} Daily Return Distribution")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    save_current_fig("returns_distribution.png")
    plt.show()
    plt.close()

    # --- Plot D: Monte Carlo simulation ---
    simulated_prices = monte_carlo_paths(
        last_price=float(stock_prices.iloc[-1]),
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
    save_current_fig("monte_carlo_paths.png")
    plt.show()
    plt.close()

    print("\nAll images saved to:", IMAGES_DIR.resolve())


if __name__ == "__main__":
    main()