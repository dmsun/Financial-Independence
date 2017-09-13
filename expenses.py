#! usr/bin/env python3

#	import modules from main
import os
import math
import decimal
import datetime as dt
import calendar
import six

#	import other modules
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#	import local functions
import monthly_analysis as mon
import quarterly_analysis as qtr
import yearly_analysis as ytd
import net_worth as networth

#	some initial setup - abbreviating the Decimal command, changing the style of matplotlib, assigning the current working directory variable and filepath variable
D = decimal.Decimal
matplotlib.style.use('ggplot')
cwd = os.getcwd()
cwd = "C:\\users\\ssamdj\\Google Drive\\python\\Expenses"
filepath = "{}\\data\\Expenses.csv".format(cwd)


#	These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

#	Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

# 	read in CSV and create a dataframe, assigned to df. Change currency format into float as is parsed as string due to commas.
#	dayfirst assumes that dates are in the form of DD/MM
df = pd.read_csv(filepath, parse_dates = [1,2], infer_datetime_format = True, dayfirst= True)
df['Cost'] = (df['Cost'].str.replace(r'[^-+\d.]', '').astype(float))

#	print the metadata definitions
with open("{}\\docs\\Metadata Definitions.txt".format(cwd), "w+") as file:
	file.write("The following is a list of the data types read in from the Expenses file. \n")
	file.write(pd.Series.to_string(df.dtypes))
	file.write("\n")

#	create a working dataframe df_work, add quarter column
df_work = df[['ID', 'Date','Cost', 'Category']].dropna()
#df_work.rename(columns = {'Date' : 'Date'}) #why?
df_work.loc[:,'Month'] = df_work.loc[:, 'Date'].dt.month
df_work.loc[:,'Quarter'] = df_work.loc[:, 'Date'].dt.quarter
df_work.loc[:,'Year'] = df_work.loc[:, 'Date'].dt.year
#   the below code remaps the Quarters of the year, to Quarters of Australia's financial year
for row in range(len(df_work['Date'])):
    if df_work.loc[row,'Quarter'] == 2:
        df_work.loc[row,'Quarter'] = 4
    else:
        df_work.loc[row,'Quarter'] = (df_work.loc[row,'Quarter'] + 2) % 4
    if df_work.loc[row, 'Month'] < 7:
        df_work.loc[row ,'FY'] = 'JUL' + str((df_work.loc[row, 'Date'].to_pydatetime()).year - 1) + '-' + 'JUN' + str((df_work.loc[row, 'Date'].to_pydatetime()).year)
    else:
        df_work.loc[row ,'FY'] = 'JUL' + str((df_work.loc[row, 'Date'].to_pydatetime()).year) + '-' + 'JUN' + str((df_work.loc[row, 'Date'].to_pydatetime()).year + 1)

#	begin the monthly reporting
mon.mon(df_work, cwd, tableau20)
#	begin the Quarterly reporting
qtr.qtr(df_work, cwd, tableau20)
#	begin the YTD reporting
ytd.ytd(df_work, cwd, tableau20)
#   begin the Networth reporting
networth.networth(cwd, tableau20)
