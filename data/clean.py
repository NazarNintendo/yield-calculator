import pandas as pd

from data.fetch import fetch_price, fetch_coupon_rate

PRICE_COLUMN_MAPPING = {
    'ISIN': 'isin',
    'Дата погашення': 'maturity_date',
    'Справедлива вартість одного цінного папера з урахуванням накопиченого '
    'купонного доходу, у валюті номіналу': 'price'
}

COUPON_RATE_COLUMN_MAPPING = {
    'ISIN код військових облігацій': 'isin',
    'Ставка': 'coupon_rate',
}


def clean_price_data() -> pd.DataFrame:
    """
    Clean bond price data. Rename columns according to the mapping and
    filter only future maturity dates.
    :return: pd.DataFrame
    """
    df_price = fetch_price()

    df_price.rename(columns=PRICE_COLUMN_MAPPING, inplace=True)
    df_price = df_price[PRICE_COLUMN_MAPPING.values()]

    # Convert maturity date to date.
    df_price['maturity_date'] = pd.to_datetime(
        df_price['maturity_date']).dt.date

    # Filter only future maturity dates.
    df_price = df_price[
        df_price['maturity_date'] > pd.to_datetime('today').date()]

    return df_price


def clean_coupon_rate_data() -> pd.DataFrame:
    """
    Clean coupon rate data. Rename columns according to the mapping and
    filter only war bonds. Reformat coupon rate to float.
    :return: pd.DataFrame
    """
    df_coupon_rate = fetch_coupon_rate()

    # Add first row as column names.
    new_columns = df_coupon_rate.iloc[0]
    df_coupon_rate = df_coupon_rate[1:]
    df_coupon_rate.columns = new_columns
    df_coupon_rate.reset_index(drop=True, inplace=True)

    df_coupon_rate.rename(columns=COUPON_RATE_COLUMN_MAPPING, inplace=True)
    df_coupon_rate = df_coupon_rate[COUPON_RATE_COLUMN_MAPPING.values()]

    # Filter only war bonds.
    df_coupon_rate = df_coupon_rate[df_coupon_rate['isin'].str.contains('UA')]

    # Remove % sign and replace comma with dot.
    def parse_percent_value(x) -> float:
        return float(x.replace('%', '').replace(',', '.')) / 100

    df_coupon_rate['coupon_rate'] = df_coupon_rate['coupon_rate'].map(
        parse_percent_value
    )

    return df_coupon_rate


def bond_data() -> pd.DataFrame:
    """
    Join price and coupon rate data.
    :return: pd.DataFrame
    """
    df_price = clean_price_data()
    df_coupon_rate = clean_coupon_rate_data()
    return df_price.merge(df_coupon_rate, on='isin')
