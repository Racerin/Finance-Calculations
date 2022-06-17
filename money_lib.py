from library import *
import math
from numbers import Number
from dataclasses import dataclass
from collections import deque
from collections.abc import Sequence

from PARAMS import *


def round_money(amount, to_cents=True, deposit=False):
    """ 
    Round money to cents/dollar.
    I fthe money is deposit, bank would not want to pay you more.
    They would pay you less therefore money will be lower (floor).
    Algorithm reference: https://stackoverflow.com/a/41383821
     """
    decimal_factor = 100.0 if to_cents else 1
    if to_cents:
        if deposit:
            math.floor(amount * decimal_factor)/decimal_factor
        else:
            math.ceil(amount * decimal_factor)/decimal_factor

# class InterestCycle(enum.Enum):
class InterestCycle:
    NONE=None
    MONTHLY=1
    BIMONTHLY=2
    QUATERLY=3
    SEMIANNUALLY=6
    ANNUALLY=12
    YEARLY=ANNUALLY

class Banking:
    _initial = dict()

    bank = Number = 0

    __total_withdrawal : Number = 0
    __total_deposits : Number = 0

    _main_bank_ : str = 'bank'
    _screenshots_ = list()

    interest_cycle = InterestCycle.ANNUALLY

    def __init__(self):
        # Save a prerecorded value for variables in Banking
        self.save_initial_values()
    
    def save_initial_values(self):
        # get string values
        names = get_public_attributes(self)
        # Save the values in _initial
        for nm in names:
            val = getattr(self, nm)
            self._initial.update({nm:val})

    def deposit(self, amount:Number, attr:str=None):
        """ 
        Keep account of money deposited into account.
        attr : refers to attribute to be added to or taken from.
         """
        if attr is None:
            attr = self._main_bank_
        prev_val = getattr(self, attr)
        setattr(self, attr, prev_val + amount)
        self.__total_deposits += amount

    def withdraw(self, amount:Number, attr:str='bank'):
        """ 
        Keep account of money withdrawn.
        attr : refers to attribute to be added to or taken from.
         """
        prev_val = getattr(self, attr)
        setattr(self, attr, prev_val - amount)
        self.__total_withdrawal += amount

    def accounts_screenshot(self):
        """ Records all the important account numbers and adds it to a single list of dicts. """
        # Get public attributes of self
        attrs = get_public_attributes(self)
        # Put pairs of attr:value in dict to be stored
        ans = {nm:getattr(self,nm) for nm in attrs}
        self._screenshots_.append(ans)

    def accounts_recall(self, to_recall):
        """ Return values stored in screenshots. """
        if isinstance(to_recall, Sequence):
            # Get the list of strings and use each to get values to be returned
            attrs = [x for x in to_recall if isinstance(x, str)]
            to_return = list()
            for attr in attrs:
                ans = [dic.get(attr, None) for dic in self._screenshots_]
                to_return.append(ans)
            return to_return
        elif isinstance(to_recall, str):
            # Get the values for that attr 'to_recall'
            return [dic.get(to_recall, None) for dic in self._screenshots_]


class InterestRateCalculate:
    pass

@dataclass
class MortgageCalculate(Banking):
    mortgage : Number = 0
    downpayment : Number = 0
    monthly_payment : Number = 0
    interest_rate : float = 0.0
    
    _main_bank_ : str = 'mortgage'
    
    last_mortgage = mortgage
    
    def __post_init__(self):
        super(MortgageCalculate, self).__init__()

    @classmethod
    def example(cls):
        """ Produces a scenario with default values to do calculations with. """
        return cls(mortgage=1e6, downpayment=3e5, monthly_payment=6e3, interest_rate=0.03)

    def pay(self, amount:Number=None):
        """ 
        Pay on mortgage.
        amount : Defaults to 'monthly_payment' if 'None'
         """
        if amount is None:
            amount = self.monthly_payment
        self.mortgage -= amount
        self.withdraw(amount)
        # Bookkeeping

    def accumulate_interest(self, month=None):
        """ 
        Accumulate interest.
        If month is specified, check whether it is a month to pay interest on.
        """
        if month is None or (isinstance(month, int) and (month+1) % self.interest_cycle == 0):
            self.mortgage *= (1 + self.interest_rate)

    def is_mortgage_shrinking(self, m):
        pass

    def is_mortgage_complete(self):
        return self.mortgage <= 0

    def pay_mortgage(self):
        """ Do entire mortgage calculations. """
        # Book keeping
        prev_mortgages = deque((0,), maxlen=self.interest_cycle)

        # Withdraw downpayment 1st
        self.pay(self.downpayment)

        # Iterate for each month
        for month in range(MAX_MONTHS):
            # Accumulate interest if at interest period
            self.accumulate_interest(month)
            # Check to ensure mortgage is going down after the interest period.
            max_of_last_mortgages = max(prev_mortgages)
            if max_of_last_mortgages < self.mortgage and len(prev_mortgages) >= self.interest_cycle:
                raise Exception("You cannot pay off your mortgage. {}|{}".format(max_of_last_mortgages, self))
            # Pay for the month
            self.pay()
            # Check whether mortgage payment is complete
            if self.is_mortgage_complete():
                years_months_str = str_months_to_years_and_months(month)
                print("Congratulations, you payed off your mortgage in {}.".format(years_months_str))
                print(self._screenshots_)
                # for i, m in enumerate(self.accounts_recall('mortgage')):
                #     print("Mortgage {}: {}".format(i, m))
                return

            # Update your last mortgages
            prev_mortgages.append(self.mortgage)
            self.accounts_screenshot()

