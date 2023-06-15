from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from datetime import date
from math import ceil

DAYS_IN_YEAR = 365.0
DEFAULT_FACE_VALUE = 1_000.0
DEFAULT_COUPON_FREQUENCY = 2


@dataclass
class AbstractBond(ABC):
    """
    Abstract class for instruments.

    Attributes:
        isin (str): International Securities Identification Number.
        face_value (float): The amount of money that the holder of a bond will
                            get back at the bond's maturity date.
        maturity_date (date): The date when the bond expires.
        price (float): The price of the bond.
        days_to_maturity (int): The number of days to maturity.
        years_to_maturity (float): The fractional value of years to maturity.
    """
    isin: str
    maturity_date: date
    price: float
    face_value: float = field(default=DEFAULT_FACE_VALUE, kw_only=True)

    def __post_init__(self) -> None:
        """
        Calculate the number of days and years to maturity.
        :return: None
        :raises: ValueError if the bond has already expired.
        """
        self.days_to_maturity = (self.maturity_date - date.today()).days

        if self.days_to_maturity < 1:
            raise ValueError("Bond has already expired.")

        self.years_to_maturity = self.days_to_maturity / DAYS_IN_YEAR

    @abstractmethod
    def get_return(self) -> float:
        """
        Calculate the total return of the bond.
        :return: The return of the bond.
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @property
    def interest(self) -> float:
        """
        Calculate the interest of the bond.
        :return: The interest.
        """
        return self.get_return() - self.price

    @property
    def roi(self) -> float:
        """
        Calculate the return on investment (ROI) of the bond.
        :return: The ROI.
        """
        return self.interest / self.price

    @property
    def annual_rate(self) -> float:
        """
        Calculate the annual rate of the bond.
        :return: The annual rate.
        """
        return self.roi / self.years_to_maturity

    @property
    def summary(self) -> str:
        """
        Get the summary of the bond.
        :return: The summary.
        """
        return f"ISIN: {self.isin}\n" \
               f"Face value: {self.face_value:.2f}\n" \
               f"Maturity date: {self.maturity_date}\n" \
               "───────────────────────────────────\n" \
               f"Price: {self.price:.2f}\n" \
               f"Days to maturity: {self.days_to_maturity}\n" \
               f"Years to maturity: {self.years_to_maturity:.2f}\n" \
               "───────────────────────────────────\n" \
               f"Total return: {self.get_return():.2f}\n" \
               f"Interest: {self.interest:.2f}\n" \
               f"ROI: {self.roi * 100:.2f}%\n" \
               f"Annual rate: {self.annual_rate * 100:.2f}%\n" \
               "───────────────────────────────────\n"


@dataclass
class DiscountBond(AbstractBond):
    """
    Class for discount instruments.
    """

    def get_return(self) -> float:
        """
        Get the total return of the bond which is equal to its face value
        for discount bonds.
        :return: The return of the bond.
        """
        return self.face_value


@dataclass
class CouponBond(AbstractBond):
    """
    Class for coupon instruments.

    Attributes:
        coupon_rate (float): The annual coupon rate.
        frequency (int): The number of coupon payouts per year.
    """
    coupon_rate: float
    frequency: int = DEFAULT_COUPON_FREQUENCY

    def __post_init__(self) -> None:
        """
        Calculate the frequency-adjusted coupon rate. Calculate the number of
        payouts before the maturity date.
        :return: None.
        """
        super().__post_init__()
        self.coupon_rate /= self.frequency
        self.payouts_num = ceil(self.years_to_maturity * self.frequency)

    def get_return(self) -> float:
        """
        Get the total return of the bond which is the sum of all coupon payouts
        before the maturity date and the face value for coupon bonds.
        :return:
        """
        coupon_payout = self.face_value * self.coupon_rate
        return self.face_value + self.payouts_num * coupon_payout
