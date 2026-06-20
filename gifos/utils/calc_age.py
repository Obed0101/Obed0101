from datetime import date

from gifos.utils.schemas.user_age import UserAge

"""This module contains a utility function for calculating a person's age."""


def calc_age(day: int, month: int, year: int) -> UserAge:
    """Calculate the age of a person given their birth date.

    :param day: The day of the month the person was born (1-31).
    :type day: int
    :param month: The month the person was born (1-12).
    :type month: int
    :param year: The year the person was born.
    :type year: int
    :return: An object containing the person's age in years, months, and days.
    :rtype: UserAge
    """
    birth_date = date(year, month, day)
    today = date.today()

    years = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        years -= 1

    month_anchor_year = birth_date.year + years
    months = today.month - birth_date.month
    if today.day < birth_date.day:
        months -= 1
    if months < 0:
        months += 12

    anchor_month = birth_date.month + months
    anchor_year = month_anchor_year
    if anchor_month > 12:
        anchor_month -= 12
        anchor_year += 1

    try:
        anchor_date = date(anchor_year, anchor_month, birth_date.day)
    except ValueError:
        next_month = anchor_month + 1
        next_year = anchor_year
        if next_month > 12:
            next_month = 1
            next_year += 1
        anchor_date = date(next_year, next_month, 1) - date.resolution

    days = (today - anchor_date).days
    return UserAge(years, months, days)
