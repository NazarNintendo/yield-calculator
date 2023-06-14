import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

Y_LABEL_FORMAT = mticker.StrMethodFormatter('{x:,.0f}')


def compound(
        principal: float,
        annual_rate: float,
        years: float
) -> list[float]:
    """
    Calculate the compound interest.
    :param principal: The principal.
    :param annual_rate: The annual rate.
    :param years: The number of years.
    :return: The compound interest.
    """
    compound_interest = [principal]
    for _ in range(years):
        principal += principal * annual_rate
        compound_interest.append(principal)

    return compound_interest


def format_plot(legend: list[str] = None) -> None:
    """
    Format the plot.
    :param legend: The legend.
    :return: None.
    """
    plt.xlabel("Years")
    plt.ylabel("Value")
    plt.title("Compound Interest")
    plt.legend(legend)
    plt.grid(True)
    plt.ticklabel_format(useOffset=False, style='plain')
    y_ticks = plt.gca().get_yticks()
    y_ticks = [y for y in y_ticks if y >= 0]
    plt.gca().set_yticks(y_ticks)
    plt.gca().set_yticklabels([Y_LABEL_FORMAT(y) for y in y_ticks])


def plot_compound_interest(
        principals: list[float],
        annual_rates: list[float],
        years: int = 10
):
    """
    Plot the compound interest for given principals, annual rates and years.
    :param principals: The principals.
    :param annual_rates: The annual rates.
    :param years: The number of years.
    :return: None.
    :raises: ValueError if the number of principals and annual rates
                        are not equal.
    """
    if len(principals) != len(annual_rates):
        raise ValueError(
            "The number of principals and annual rates must be equal.")

    plt.figure(figsize=(12, 8))

    legend = []
    for principal, annual_rate in zip(principals, annual_rates):
        legend.append(f"{principal:.2f} | {annual_rate:.2%}")
        compound_interest = compound(principal, annual_rate, years)
        plt.plot(compound_interest)

    format_plot(legend)
    plt.show()
