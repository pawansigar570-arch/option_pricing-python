import scipy.stats as stats
import numpy as np
from scipy.optimize import brentq


def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (
        sigma * np.sqrt(T)
    )

    d2 = d1 - sigma * np.sqrt(T)

    call = (
        S * stats.norm.cdf(d1)
        - K * np.exp(-r * T) * stats.norm.cdf(d2)
    )

    return call


def implied_volatility_call(
    market_price,
    S,
    K,
    T,
    r
):
    f = lambda sigma: (
        black_scholes_call(
            S, K, T, r, sigma
        )
        - market_price
    )

    return brentq(f, 0.0001, 5.0)