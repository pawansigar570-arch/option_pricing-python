import numpy as np
class MonteCarloOptionPricing:

    def __init__(
        self,
        spot_price,
        strike_price,
        risk_free_rate,
        volatility,
        time_to_maturity
    ):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.time_to_maturity = time_to_maturity

    def calculate_call_price(self, simulations=100000):

        z = np.random.standard_normal(simulations)

        stock_price_at_expiry = (
            self.spot_price
            * np.exp(
                (
                    self.risk_free_rate
                    - 0.5 * self.volatility ** 2
                )
                * self.time_to_maturity
                + self.volatility
                * np.sqrt(self.time_to_maturity)
                * z
            )
        )

        payoffs = np.maximum(
            stock_price_at_expiry - self.strike_price,
            0
        )

        call_price = (
            np.exp(
                -self.risk_free_rate
                * self.time_to_maturity
            )
            * np.mean(payoffs)
        )

        return call_price
    def calculate_put_price(self, simulations=100000):
        

        z = np.random.standard_normal(simulations)

        stock_price_at_expiry = (
            self.spot_price
            * np.exp(
                (
                    self.risk_free_rate
                    - 0.5 * self.volatility ** 2
                )
                * self.time_to_maturity
                +
                self.volatility
                * np.sqrt(self.time_to_maturity)
                * z
            )
        )
        payoffs = np.maximum(
            self.strike_price - stock_price_at_expiry,
            0
        )
        put_price = (
            np.exp(
                -self.risk_free_rate
                * self.time_to_maturity
            )
            * np.mean(payoffs)
        )

        return put_price