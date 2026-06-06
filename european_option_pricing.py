# coding=utf-8
import datetime
import logging

import numpy as np
from monte_carlo_pricing import MonteCarloOptionPricing
from implied_volatility import implied_volatility_call
import scipy.stats as stats

from base_option_pricing import OptionPricingBase

logging.basicConfig(format='%(level_name)s: %(message)s', level=logging.DEBUG)


class EuropeanOptionPricing(OptionPricingBase):
    """
    This class uses the classic Black-Scholes method to calculate prices for European Call and Put options

    I have made an attempt to include dividends in the calcultion of these options. However, still need to perform
    some testing.
    """

    def __init__(self, ticker, expiry_date, strike, dividend=0.0):
        super(EuropeanOptionPricing, self).__init__(ticker, expiry_date, strike, dividend=dividend)
        logging.info("European Option Pricing. Initializing variables")

        # Get/Calculate all the required underlying parameters, ex. Volatility, Risk-free rate, etc.
        self.initialize_variables()
        self.log_parameters()

    def _calculate_d1(self):
        """ Famous d1 variable from Black-Scholes model calculated as shown in:

                https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
        :return: <float>
        """
        d1 = (np.log(self.spot_price / self.strike_price) +
              (self.risk_free_rate - self.dividend + 0.5 * self.volatility ** 2) * self.time_to_maturity) / \
             (self.volatility * np.sqrt(self.time_to_maturity))
        logging.debug("Calculated value for d1 = %f" % d1)
        return d1

    def _calculate_d2(self):
        """ Famous d2 variable from Black-Scholes model calculated as shown in:

                https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
        :return: <float>
        """
        d2 = (np.log(self.spot_price / self.strike_price) +
              (self.risk_free_rate - self.dividend - 0.5 * self.volatility ** 2) * self.time_to_maturity) / \
             (self.volatility * np.sqrt(self.time_to_maturity))
        logging.debug("Calculated value for d2 = %f" % d2)
        return d2
    def calculate_greeks(self):
        d1 = self._calculate_d1()
        d2 = self._calculate_d2()

        delta = stats.norm.cdf(d1)

        gamma = stats.norm.pdf(d1) / (
            self.spot_price *
            self.volatility *
            np.sqrt(self.time_to_maturity)
        )

        vega = (
            self.spot_price *
            stats.norm.pdf(d1) *
            np.sqrt(self.time_to_maturity)
        )

        theta = (
            -(self.spot_price * stats.norm.pdf(d1) * self.volatility)
            / (2 * np.sqrt(self.time_to_maturity))
            - self.risk_free_rate * self.strike_price
            * np.exp(-self.risk_free_rate * self.time_to_maturity)
            * stats.norm.cdf(d2)
        )

        rho = (
            self.strike_price *
            self.time_to_maturity *
            np.exp(-self.risk_free_rate * self.time_to_maturity)
            * stats.norm.cdf(d2)
        )

        return {
            "Delta": delta,
            "Gamma": gamma,
            "Vega": vega,
            "Theta": theta,
            "Rho": rho
        }

    def calculate_option_prices(self):
        """ Calculate Call and Put option prices based on the below equations from Black-Scholes.
        If dividend is not zero, then it is subtracted from the risk free rate in the below calculations.

            CallOptionPrice =SpotPrice*N(d1) − Strike*exp(−r(T−t))*N(d2))
            PutOptionPrice  = Strike*exp(−r(T−t)) *N(−d2) − SpotPrice*N(−d1)
        :return: <float>, <float> Calculated price of Call & Put options
        """
        d1 = self._calculate_d1()
        d2 = self._calculate_d2()
        call = ((self.spot_price * np.exp(-1 * self.dividend * self.time_to_maturity)) * stats.norm.cdf(d1, 0.0, 1.0) -
                (self.strike_price * np.exp(-1 * self.risk_free_rate * self.time_to_maturity) *
                 stats.norm.cdf(d2, 0.0, 1.0)))
        logging.info("##### Calculated value for European Call Option is %f " % call)
        put = (self.strike_price * np.exp(-1 * self.risk_free_rate * self.time_to_maturity) *
               stats.norm.cdf(-1 * d2, 0.0, 1.0) - (
                       self.spot_price * np.exp(-1 * self.dividend * self.time_to_maturity)) *
               stats.norm.cdf(-1 * d1, 0.0, 1.0))
        logging.info("##### Calculated value for European Put Option is %f " % put)
        return call, put
    def monte_carlo_price(self, simulations=100000):
        mc = MonteCarloOptionPricing(
            spot_price=self.spot_price,
            strike_price=self.strike_price,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            time_to_maturity=self.time_to_maturity
        )

        return mc.calculate_call_price(simulations)
    def monte_carlo_put_price(self, simulations=100000):
        mc = MonteCarloOptionPricing(
            spot_price=self.spot_price,
            strike_price=self.strike_price,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            time_to_maturity=self.time_to_maturity
        )

        return mc.calculate_put_price(simulations)

if __name__ == '__main__':
    pricer = EuropeanOptionPricing(
        'TSLA',
        datetime.datetime(2026, 12, 31),
        300
    )

    call_price, put_price = pricer.calculate_option_prices()
    mc_price = pricer.monte_carlo_price()
    mc_put_price = pricer.monte_carlo_put_price()
    print("Monte Carlo Put Price =", mc_put_price)

    print("Monte Carlo Call Price =", mc_price)
    parity = pricer.is_call_put_parity_maintained(call_price, put_price)
    print("Parity = %s" % parity)
    greeks = pricer.calculate_greeks()

    print("Delta =", greeks["Delta"])
    print("Gamma =", greeks["Gamma"])
    print("Vega =", greeks["Vega"])
    print("Theta =", greeks["Theta"])
    print("Rho =", greeks["Rho"])
    market_price = call_price

iv = implied_volatility_call(
    market_price,
    pricer.spot_price,
    pricer.strike_price,
    pricer.time_to_maturity,
    pricer.risk_free_rate
)

print("Implied Volatility =", iv)
