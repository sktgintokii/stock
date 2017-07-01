import os
import pandas as pd
import mathplotlab.pyplot as plt

def symbol_to_path(symbol, base_dir='data'):
    return os.path.join(base_dir, '{}.csv'.format(str(symbol)))

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


def plot_selected(df, columns, start_date, end_date):
    df[start_date:end_date][columns].plot()
    plt.show()

def plot_data(df, title='Stock Price'):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()

def test_run():
    dates = pd.date_range('2010-01-01', '2010-12-31')
    symbols = ['GOOG', 'AAPL', 'GLD', 'IBM']

    df = get_data(symbols, dates)
    plot_selected(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')

if __name__ == "__main__":
    test_run()
