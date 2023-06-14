# yield-calculator

---

## Description
A simple yield calculator for bonds and other fixed income instruments.

## Usage: instruments/bond.py
```python
from datetime import datetime

from instruments.bond import DiscountBond, CouponBond

ua_war_bonds = [
    DiscountBond(
        isin="227003",
        maturity_date=datetime(2023, 12, 28),
        price=977.58
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
```

## Usage: plots/compound.py

```python
from datetime import datetime

from instruments.bond import DiscountBond, CouponBond
from plots.compound import plot_compound_interest

ua_war_bonds = [
    DiscountBond(
        isin="227003",
        maturity_date=datetime(2023, 12, 28),
        price=977.58
    ),
    CouponBond(
        isin="227656",
        maturity_date=datetime(2025, 1, 15),
        price=1081.26,
        coupon_rate=0.195,
    )
]

principals = [500_000] * len(ua_war_bonds)
annual_rates = [bond.annual_rate for bond in ua_war_bonds]
years = 15

plot_compound_interest(
    principals=principals,
    annual_rates=annual_rates,
    years=years
)
```