#! usr/bin/env python3

from decimal import Decimal as D

import numpy as np
import matplotlib.pyplot as plt
"""This script will compile several useful calculators that will be used in other parts of the financial independence calculator

In the long term, the average annual rate of return of a diversified security portfolio is assumed to be 7%. The safety_rate is a factor used to account for variations of this growth through the short term"""
#	These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

def withdraw_rate(growth_rate = 0.07, inflation_rate = 0.03, safety_factor = 1):
    """ The withdraw rate is the rate at which you can "safely" withdraw upon your investments and expect to have a steady income for the duration of your life. The safety factor determines how conservative the approach is. By default, the SF is 1 which is the most aggressive appraoch. Value must be greater than 0
    """
    """while True:
        try:
            value = int(safety_factor)
        except:
            print("Please enter the safety factor such that 0 < SF <= 1")
            continue
        if 0 < safety_factor <= 1:
            break
        else:
            print("Please enter the safety factor such that 0 < SF <= 1")"""
    return D(safety_factor * (growth_rate - inflation_rate))

def principal(expenses, withdraw_rate):
    """ The principal required is proportional to average annual expenditure
    and inversely proportional to the withdrawal rate.

    Note: this does not include any additional investments you would like to have in the future. It's your current situation as it exists now."""
    principal = D(round(expenses / withdraw_rate,2))
    return principal

def super(gross_income, super_rate = 9.5, co_contribution = 0):
    super = D(round((super_rate + co_contribution) / 100 * gross_income,2))
    return super

def taxable_income(gross_income, super_rate = 9.5, co_contribution = 0):
    taxable_income = D(round((1 - (super_rate + co_contribution) / 100) * gross_income,2))
    return taxable_income

def tax(taxable_income):
    """ Tax Brackets: 2017-2018
    $0 - $18 200            NIL
    $18 201 - $37 000       $0.19 for every $1 over $18 200
    $37 001 - $87 000       $3 572 plus $0.325 for every $1 over $37 000
    $87 001 - $180 000      $19 882 plus $0.37 for every $1 over $87 000
    $180 001 and over       $54 547 plus $0.45 for every $1 over $180 000
    """
    if taxable_income >= 180001:
        tax = D(round(54232 + D(0.45) * (taxable_income - 180000),2))
    elif 87001 <= taxable_income <= 180000:
        tax = D(round(19882 + D(0.37) * (taxable_income - 87000),2))
    elif 37001 <= taxable_income <= 87000:
        tax = D(round(3572 + D(0.325) * (taxable_income - 37000),2))
    elif 18201 <= taxable_income <= 37000:
        tax = D(round(D(0.19) * (taxable_income - 18000),2))
    elif 0 <= taxable_income <= 18200:
        tax = 0
    return tax

def compound(P, r, n, d, i):
    """ The compound interest formula with periodical deposits is adjusted with inflation to always provide todays money.
    """
    FV = (P * (1 + D(r/12)) ** n + d * ((1 + D(r/12)) ** n - 1)/ D(r/12) * (1 + D(r/12))) / (1 + D(i/12)) ** n
    FV = D(round(FV,2))
    return FV

def compound_array(P, r, n, d, i):
    """ The compound interest formula with periodical deposits is adjusted with inflation to always provide todays money.

    This function takes arrays for n - number of years/compound periods, uses the Decimal data type to ensure numerical precision.

    This code could be vectorised
    """

    FV = np.zeros(len(n))
    for k in range(len(n)):
        t = D(n[k])
        FV[k] = (P * (1 + r/12) ** t + d * ((1 + r/12) ** t - 1)/ (r/12) * (1 + r/12)) / (1 + i/12) ** t
    FV = np.around(FV,2)
    return FV

def stampduty(house_price):
    """Value of property    Rate of duty
    $0 - $14 000            $1.25 for every $100
    $14 001 - $30 000       $175 plus $1.50 for every $100
    $30 001 - $80 000       $415 plus $1.75 for every $100
    $80 001 - $300 000      $1 290 plus $3.50 for every $100
    $300 001 - $1 000 000   $8 990 plus $4.50 for every $100
    $1 000 001 - $3 000 000 $40 490 plus $5.50 for every $100
    > $3m	                $150 490 plus $7.00 for every $100
    """
    if 0 <= house_price <= 14000:
        stampduty = 1.25 * house_price / 100
    elif 14001 <= house_price <= 30000:
        stampduty = 175 + 1.5 * (house_price - 14000) / 100
    elif 30001 <= house_price <= 80000:
        stampduty = 415 + 1.75 * (house_price - 30000)/ 100
    elif 80001 <= house_price <= 300000:
        stampduty = 1290 + 3.50 * (house_price - 80000) / 100
    elif 300001 <= house_price <= 1000000:
        stampduty = 8990 + 4.50 * (house_price - 300000)/ 100
    elif 1000001 <= house_price <= 3000000:
        stampduty = 40490 + 5.50 * (house_price - 1000000) / 100
    elif house_price > 3000000:
        stampduty = 150490 + 7.00 * (house_price - 3000000) / 100
    return stampduty


def plot_fi(ageVec, networthVec,superVec, savingsVec, principalVec, incomeVec, expensesVec, index_fi):
    fig, ax1 = plt.subplots()
    networth = ax1.plot(ageVec, networthVec, 'b', label = 'Networth')
    super = ax1.plot(ageVec, superVec, 'c', label = 'Super')
    savings = ax1.plot(ageVec, savingsVec, 'g', label = 'Savings')
    principal = ax1.plot(ageVec, principalVec, 'k--', label = 'Principal Required')
    ax1.set_ylabel('Prinicipal Required in $', color='k')
    plt.legend(loc=2)

    # create a separate axis on the same graph, plot income v age, expenses vs age. Expenses is a horizontal line. Label this axis as Retirement income
    ax2 = ax1.twinx()
    retirement_income = ax2.plot(ageVec, incomeVec, 'm', label = 'Retirement Income')
    annual_expenses = ax2.plot(ageVec, expensesVec, 'r--', label = 'Annual Expenses')
    ax2.set_ylabel('Retirement Income in $', color='k')

    # plots vertical line at the age of finanical independence which is parsed into the function. This is dependent of calculations prior to calling the function
    plt.axvline(x=ageVec[index_fi], label = "Finanical Indepdence")
    plt.legend(loc=4)

    plt.show()
