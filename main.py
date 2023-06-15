from data.clean import bond_data
from instruments.bond import CouponBond
from plots.compound import plot_compound_interest

df_bonds = bond_data()
ua_war_bonds = [CouponBond(**bond) for bond in df_bonds.to_dict('records')]

for bond in ua_war_bonds:
    print(bond.summary)

principals = [1_000] * len(ua_war_bonds)
annual_rates = [bond.annual_rate for bond in ua_war_bonds]
years = 2

plot_compound_interest(
    principals=principals,
    annual_rates=annual_rates,
    years=years
)
