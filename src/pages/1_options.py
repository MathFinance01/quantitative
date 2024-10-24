import streamlit as st
import QuantLib as ql
from ql.option_pricing import OptionPricer
from ql.plotting import *
import matplotlib.pyplot as plt

optionStyle = st.selectbox(
    "Choose Style",
    ("American", "European", "Bermudan"),
)

# st.write("You selected:", optionStyle)

option_type_input = st.selectbox(
    "Choose Type",
    ("Call", "Put"),
)


option_type = ql.Option.Call if option_type_input == "Call" else ql.Option.Put

stock_price = st.number_input("Enter the current price of the Stock", value=100.0)

volatility = st.number_input("Enter the Volatility of the Stock", value=0.2)

strike_price = st.number_input("Enter the Strike Price", value=101.0)

rate = st.number_input("Enter the interest rate", value=0.03)

maturity = st.select_slider(
    "Select the number of weeks",
    options=["1", "2", "3", "4"],
    value="3"
)

today = ql.Date.todaysDate()

maturity_date = ql.TARGET().advance(today, ql.Period(int(maturity), ql.Weeks), ql.Following, False)
calendar = ql.TARGET()
op = OptionPricer()
prices_and_greeks = op.option_price_and_greeks(stock_price, strike_price, volatility, rate, maturity_date, option_type)

stock_price_generator = list(generate_continuous_inputs(stock_price))
strike_price_generator = list(generate_continuous_inputs(strike_price))
volatility_generator = list(generate_continuous_inputs(volatility))
interest_rate_generator = list(generate_continuous_inputs(rate))
date_generator = list(generate_dates(today, maturity_date))

price_plot_data = [[next_stock_price, op.option_price_and_greeks(next_stock_price, strike_price, volatility, rate,
                                                               maturity_date, option_type).price]
                   for next_stock_price in stock_price_generator]

delta_plot_data = [[next_stock_price, op.option_price_and_greeks(next_stock_price, strike_price, volatility, rate,
                                                               maturity_date, option_type).delta]
                   for next_stock_price in stock_price_generator]
gamma_plot_data = [[next_stock_price, op.option_price_and_greeks(next_stock_price, strike_price, volatility, rate,
                                                               maturity_date, option_type).gamma]
                   for next_stock_price in stock_price_generator]
vega_plot_data = [[next_volatility, op.option_price_and_greeks(stock_price, strike_price, next_volatility, rate,
                                                               maturity_date, option_type).vega]
                  for next_volatility in volatility_generator]
rho_plot_data = [(next_interest_rate, op.option_price_and_greeks(stock_price, strike_price, volatility, next_interest_rate,
                                                              maturity_date, option_type).rho)
                 for next_interest_rate in interest_rate_generator]
theta_plot_data = [(calendar.businessDaysBetween(ql.Date.todaysDate(), next_maturity_date), op.option_price_and_greeks(stock_price, strike_price, volatility, rate,
                                                              next_maturity_date, option_type).theta)
                   for next_maturity_date in date_generator]

fig, axs = plt.subplots(3, 2, squeeze=False)
fig.set_figheight(15)
fig.set_figwidth(15)

plot_xy(price_plot_data, axs[0][0], f'Price of a {option_type_input} option', x_axis='Stock Price', y_axis='Price')
plot_xy(delta_plot_data, axs[0][1], f'Delta of a {option_type_input} option', x_axis='Stock Price', y_axis='Delta')
plot_xy(gamma_plot_data, axs[1][0], f'Gamma of a {option_type_input} option', x_axis='Stock Price', y_axis='Gamma')
plot_xy(vega_plot_data, axs[1][1], f'Vega of a {option_type_input} option', x_axis='Stock Price', y_axis='Vega')
plot_xy(rho_plot_data, axs[2][0], f'Rho of a {option_type_input} option', x_axis='Stock Price', y_axis='Rho')
plot_xy(theta_plot_data, axs[2][1], f'Theta of a {option_type_input} option', x_axis='Stock Price', y_axis='Theta')

st.pyplot(fig)




