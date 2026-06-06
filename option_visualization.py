import datetime
import matplotlib.pyplot as plt

from european_option_pricing import EuropeanOptionPricing

strike_prices = [200, 250, 300, 350, 390, 400]
option_prices = []

for strike in strike_prices:

    option = EuropeanOptionPricing(
        ticker="TSLA",
        expiry_date=datetime.datetime(2028, 1, 1),
        strike=strike,
        dividend=0
    )

    call_price, put_price = option.calculate_option_prices()
    option_prices.append(call_price)

plt.plot(strike_prices, option_prices)
plt.title("Option Price vs Strike Price")
plt.xlabel("Strike Price")
plt.ylabel("Option Price")
plt.grid(True)
plt.show()