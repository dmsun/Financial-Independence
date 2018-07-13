#! usr/bin/env python3

# import modules from main
import os
import matplotlib.pyplot as plt
# import other modules
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

def net_worth(cwd, tableau20):
    if os.name == 'nt':
        filepath = "{}\\data\\Networth.csv".format(cwd)
        report_dir = "{}\\Reports\\Net Worth.pdf".format(cwd)
    else:
        filepath = "{}/data/Networth.csv".format(cwd)
        report_dir = "{}/reports/Net Worth.pdf".format(cwd)
    columns = ['Number',
               'Month',
               'Net Worth',
               'Growth',
               'Delta',
               'Car',
               'ING Savings',
               'UBank Savings',
               'Savings',
               'Superannuation',
               'Acorns',
               'Stocks',
               'Cryptocurrency',
               'Assets Subtotal',
               'HELP Debt',
               'Car Debt',
               'Personal Debt',
               'Credit Debt',
               'Liabilities Total']
    dtypes = {'Number': np.int32,
              'Month': object,
              'Net Worth': object,
              'Growth': object,
              'Delta': object,
              'Car': object,
              'ING Savings': object,
              'UBank Savings': object,
              'Savings': object,
              'Superannuation': object,
              'Acorns': object,
              'Stocks': object,
              'Cryptocurrency': object,
              'Assets Subtotal': object,
              'HELP Debt': object,
              'Car Debt': object,
              'Personal Debt': object,
              'Credit Debt': object,
              'Liabilities Total': object}
    df_networth = pd.read_csv(filepath,
                              header=0,
                              #names=columns,
                              parse_dates=[1],
                              infer_datetime_format=True,
                              dayfirst=True,
                              dtype=dtypes)
    df_networth.drop(['ING Savings', 'UBank Savings'], axis=1)
    df_networth = df_networth.dropna()
    df_networth = df_networth.sort_values(by=['Number'])
    df_networth = df_networth[df_networth.Number >= 4]
    for (col, colname) in enumerate(columns):
        col_len = len(df_networth[colname])
        try:
            for row in range(col_len):
                if '$' in df_networth.iloc[row, col] or '%' in df_networth.iloc[row, col]:
                    df_networth.loc[:, colname] = (df_networth.loc[:, colname].str.replace(r'[^-+\d.]', '').astype(float))
        except:
            continue
    with PdfPages(report_dir) as pdf:
        fig, ax = plt.subplots()
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Net Worth', color = tableau20[1])
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Assets Subtotal', color = tableau20[3])
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Liabilities Total', color = tableau20[4])
        ax.set_xlabel("Month")
        ax.set_ylabel("Value")
        ax.set_title("Net Worth over time")
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=6)
        ax.xaxis.set_label_position('bottom')
        x = list(df_networth['Month'].get_values())
        y = list(np.zeros(len(df_networth['Net Worth'])))
        ax = plt.plot(x, y, color = 'black')
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

        fig, ax = plt.subplots()
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Acorns', color = tableau20[0])
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Stocks', color = tableau20[1])
        ax.set_xlabel("Month")
        ax.set_ylabel("Value")
        ax.set_title("Net Worth over time")
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=6)
        ax.xaxis.set_label_position('bottom')
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

if __name__ == "__main__":
    if os.name == 'nt':
        filepath = "{}\\data\\Networth.csv".format(cwd)
        report_dir = "{}\\Reports\\Net Worth.pdf".format(cwd)
    else:
        filepath = "{}/data/Networth.csv".format(cwd)
        report_dir = "{}/reports/Net Worth.pdf".format(cwd)
    net_worth(cwd, tableau20)