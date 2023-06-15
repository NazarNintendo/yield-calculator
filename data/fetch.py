import io
from datetime import datetime, timedelta

import pandas as pd
import requests


def fetch_price() -> pd.DataFrame:
    """
    Fetches price data from the National Bank of Ukraine.
    https://bank.gov.ua/ua/markets/ovdp/fair-value
    :return: pandas.DataFrame
    """
    lookup_date = datetime.now()

    while True:
        month = lookup_date.strftime('%Y%m')
        date = lookup_date.strftime('%Y%m%d')
        url = f'https://bank.gov.ua/files/Fair_value/{month}/{date}_fv.xlsx'
        response = requests.get(url)

        if response.status_code == 404:
            lookup_date = lookup_date - timedelta(days=1)
            continue
        else:
            break

    return pd.read_excel(io.BytesIO(response.content))


def fetch_coupon_rate() -> pd.DataFrame:
    """
    Fetches coupon rate data from the Ministry of Finance of Ukraine.
    https://mof.gov.ua/uk/local_bonds_issued_during_the_war_time-572
    :return: pd.DataFrame
    """
    url = "https://mof.gov.ua/uk/local_bonds_issued_during_the_war_time-572"
    tables = pd.read_html(url)
    return tables[0]
