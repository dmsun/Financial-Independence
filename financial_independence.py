#! usr/bin/env python3

#	import modules from main
import os
from decimal import Decimal as D
import datetime as dt

#	import other modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
#   import utils package
import utils


def fin_ind(age=dt.date.today().year - 1990,
                           gross_income=D(87000),
                           curr_investments=D(20000),
                           super_bal=D(30000),
                           expenses=D(48000),  # actual spend in FY 2016-2017 was $44 856.51
                           super_rate=D(11.5),
                           co_contrib=D(3),
                           growth_rate=D(0.08),
                           inflation_rate=D(0.03)):
    # age = input("Enter your current age in years: ")
    """
    This code will take the inputs and graph the finanical horizon given those inputs. The key factors are the average annual expenses and gross income. These determine the savings ratio, which in turn has a significant impact on the age of finanical independence.

    The modelling assumption as is, assumes that the networth will not decrease in order to earn your income. Instead, the asset growth, after inflation and taxes, will have to provide the required income to match the annual expenses.
    """
    retirement_age = 65
    safety_factor = D(1)

    withdraw_rate = utils.withdraw_rate(growth_rate, inflation_rate, safety_factor)
    principal_required = utils.principal(expenses, withdraw_rate)
    annual_super = utils.annual_super_contribution(gross_income, super_rate, co_contrib)
    taxable_income = utils.calc_taxable_income(gross_income, super_rate, co_contrib)
    tax = utils.calc_tax(taxable_income)
    net_income = taxable_income - tax
    savings = net_income - expenses
    savings_ratio = D(round((net_income - expenses) / net_income, 2))

    print("Annual savings amount is: $", savings)
    print("The savings ratio is:", savings_ratio)
    # define the total length of the arrays
    L = 70
    indexVec = np.linspace(0, L - age, num=L - age + 1)
    ageVec = np.linspace(age, L, num=L - age + 1)
    expensesVec = np.linspace(float(expenses), float(expenses), num=L - age + 1)
    incomeVec = np.zeros(L - age + 1)

    # define index at retirement age
    index_retire = retirement_age - age
    end = L - age + 1

    # the compound function calculates the savings in today's money across the array.
    # growth_rate is gross, and does not include taxes, due to CGT, fees or inflation.
    # Capital Gains are only realised for taxation purposes only when the assets are sold.
    savingsVec = utils.compound_array(curr_investments, growth_rate, 12 * indexVec, savings / 12, inflation_rate)
    superVec = utils.compound_array(super_bal, growth_rate, 12 * indexVec, annual_super / 12, inflation_rate)
    principalVec = utils.compound_array(principal_required, inflation_rate, 12 * indexVec, 0, inflation_rate)
    networthVec = savingsVec + superVec

    # super is added to the income stream after retirement age
    # TODO: Complete a better implementation of post - retirement usage.
    incomeVec[0:index_retire] = float(withdraw_rate) * savingsVec[0:index_retire]
    incomeVec[index_retire:end] = float(withdraw_rate) * networthVec[index_retire:end]

    index_fi = np.nonzero(incomeVec >= expenses)[0][0]
    return ageVec, networthVec, superVec, savingsVec, principalVec, incomeVec, expensesVec, index_fi

