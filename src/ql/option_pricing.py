import QuantLib as ql
import collections
from ql.descriptors import PositiveNumber, Number, FutureDate

option_tuple = collections.namedtuple('Option', ['price', 'delta', 'gamma', 'rho', 'vega', 'theta'])

class OptionPricer:

    def __init__(self, option_style='european'):
        self.option_style = option_style
        self.start_date = ql.Date.todaysDate()
        self.stock_price = PositiveNumber()
        self.strike_price = PositiveNumber()
        self.interest_rate = Number()
        self.volatility = PositiveNumber()
        self.maturity_date = FutureDate()

    def option_price_and_greeks(self, stock_price, strike_price, volatility, interest_rate, maturity_date, option_type):

        ql.Settings.instance().evaluationDate = self.start_date
        option = ql.EuropeanOption(ql.PlainVanillaPayoff(option_type, strike_price), ql.EuropeanExercise(maturity_date))

        u = ql.SimpleQuote(stock_price)
        r = ql.SimpleQuote(interest_rate)
        sigma = ql.SimpleQuote(volatility)

        rate_curve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(r), ql.Actual360())
        volatility = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(sigma), ql.Actual360())
        process = ql.BlackScholesProcess(ql.QuoteHandle(u), ql.YieldTermStructureHandle(rate_curve),
                                      ql.BlackVolTermStructureHandle(volatility))
        engine = ql.AnalyticEuropeanEngine(process)
        option.setPricingEngine(engine)

        price = option.NPV()
        delta = option.delta()
        gamma = option.gamma()
        rho = option.rho()
        vega = option.vega()
        theta = option.theta()

        return option_tuple(price, delta, gamma, rho, vega, theta)
