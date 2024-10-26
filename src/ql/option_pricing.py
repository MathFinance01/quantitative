import QuantLib as ql
import collections
from ql.descriptors import PositiveNumber, Number, FutureDate

option_tuple = collections.namedtuple('Option', ['price', 'delta', 'gamma', 'rho', 'vega', 'theta'])

class OptionPricer:

    def __init__(self, option_style='European'):
        self.option_style = option_style
        self.start_date = ql.Date.todaysDate()
        self.stock_price = PositiveNumber()
        self.strike_price = PositiveNumber()
        self.interest_rate = Number()
        self.volatility = PositiveNumber()
        self.maturity_date = FutureDate()

    def binomial_engine(self, bsm_process, steps):
        binomial_engine = ql.BinomialVanillaEngine(bsm_process, 'crr', steps)
        return binomial_engine

    def analytical_european_engine(self, process):
        return ql.AnalyticEuropeanEngine(process)
    def option_price_and_greeks(self, stock_price, strike_price, volatility, interest_rate, maturity_date, option_type):
        ql.Settings.instance().evaluationDate = self.start_date

        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        if self.option_style == 'European':
            exercise = ql.EuropeanExercise(maturity_date)
            option = ql.EuropeanOption(payoff, exercise)
        elif self.option_style == 'American':
            exercise = ql.AmericanExercise(self.start_date, maturity_date)
            option = ql.VanillaOption(payoff, exercise)


        u = ql.SimpleQuote(stock_price)
        r = ql.SimpleQuote(interest_rate)
        sigma = ql.SimpleQuote(volatility)

        rate_curve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(r), ql.Actual360())
        volatility = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(sigma), ql.Actual360())
        process = ql.BlackScholesProcess(ql.QuoteHandle(u), ql.YieldTermStructureHandle(rate_curve),
                                      ql.BlackVolTermStructureHandle(volatility))

        engine = self.analytical_european_engine(process)
        if self.option_style == 'European':
            engine = self.analytical_european_engine(process)
        elif self.option_style == 'American':
            engine = self.binomial_engine(process, 1000)

        option.setPricingEngine(engine)

        price = option.NPV()
        delta = option.delta()
        gamma = option.gamma()
        rho = 0#option.rho()
        vega = 0#option.vega()
        theta = 0#option.theta()

        return option_tuple(price, delta, gamma, rho, vega, theta)
