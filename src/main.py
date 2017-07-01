import os
import pandas as pd
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir='data'):
    dir = os.path.dirname(__file__)

    return os.path.join(dir, base_dir, '{}.csv'.format(str(symbol)))

def fill_missing_values(df):
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

def get_data(symbols, dates):
    df = pd.DataFrame(index=dates)

    # Add SPY if not exist
    if 'SPY' not in symbols:
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp=pd.read_csv(symbol_to_path(symbol), index_col='Date',
            parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})

        df = df.join(df_temp)

        # Drop dates SPY didn't trade
        if symbol == 'SPY':
            df = df.dropna(subset=['SPY'])

    return df

def normalize_data(df):
    return df / df.ix[0,:]

def plot_selected(df, columns, start_date, end_date):
    df[start_date:end_date][columns].plot()
    plt.show()

def plot_data(df, title='Stock Price'):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()

def test_run():
    symbols = ['GOOG', 'AAPL', 'GLD', 'IBM']
    start_date = '2010-01-01'
    end_date = '2010-12-31'

    dates = pd.date_range(start_date, end_date)
    df = normalize_data(get_data(symbols, dates))
    fill_missing_values(df)
    plot_data(df)

if __name__ == "__main__":
    test_run()
