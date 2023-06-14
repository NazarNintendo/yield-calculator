from datetime import datetime

from instruments.bond import CouponBond, DiscountBond
from plots.compound import plot_compound_interest

ua_war_bonds = [
    DiscountBond(
        isin="227003",
        maturity_date=datetime(2023, 12, 28),
        price=977.58
    ),
    DiscountBond(
        isin="227409",
        maturity_date=datetime(2024, 3, 21),
        price=967.60
    ),
    CouponBond(
        isin="227656",
        maturity_date=datetime(2025, 1, 15),
        price=1081.26,
        coupon_rate=0.195,
    )
]

for bond in ua_war_bonds:
    print(bond.summary)

principals = [25_000] * 3
annual_rates = [bond.annual_rate for bond in ua_war_bonds]

plot_compound_interest(
    principals=principals,
    annual_rates=annual_rates,
    years=5
)
