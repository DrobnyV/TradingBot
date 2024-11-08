import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from datetime import datetime, time

# Set up your API keys here
API_KEY = 'PK8FSYECUOIAANSVPH5N'
API_SECRET = '4xgIfzXakEdo421OeykFgf6qHUKNWw020PxknEvG'
BASE_URL = 'https://paper-api.alpaca.markets'  # Alpaca's demo URL

# Initialize API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Parameters for the strategy
SYMBOL = input("Enter trading symbol (e.g., TSLA): ").upper()  # Trading symbol
SHORT_WINDOW = 21  # Short moving average window
LONG_WINDOW = 100  # Long moving average window
TRADE_QUANTITY = 1  # Number of shares to trade
TRADE_START_TIME = time(15, 0)  # 15:00 (3 PM)
TRADE_END_TIME = time(21, 0)    # 21:00 (9 PM)

# Function to fetch historical price data
def get_historical_data(symbol, start, end, timeframe='15Min'):
    bars = api.get_bars(symbol, timeframe, start=start, end=end).df
    bars = bars.tz_convert(None)  # Remove timezone info for simplicity
    return bars[['close']]

# Trading strategy with time restriction and visualization
def crossover_strategy_with_plot(data):
    data['short_mavg'] = data['close'].rolling(window=SHORT_WINDOW).mean()
    data['long_mavg'] = data['close'].rolling(window=LONG_WINDOW).mean()

    in_position = False
    last_buy_price = None
    total_profit = 0  # To accumulate total profit

    # Track buy and sell points for visualization
    buy_signals = []
    sell_signals = []

    print("=" * 50)
    print(f"Starting backtest for {SYMBOL} using Moving Average Crossover Strategy (15:00 - 21:00)")
    print("=" * 50)

    for i in range(LONG_WINDOW, len(data)):
        short_mavg = data['short_mavg'].iloc[i]
        long_mavg = data['long_mavg'].iloc[i]
        current_price = data['close'].iloc[i]
        current_time = data.index[i]

        # Extract time from current timestamp
        trade_time = current_time.time()

        # Only execute strategy between TRADE_START_TIME and TRADE_END_TIME
        if TRADE_START_TIME <= trade_time <= TRADE_END_TIME:
            if short_mavg > long_mavg and not in_position:
                # Buy signal when short moving average crosses above long moving average
                in_position = True
                last_buy_price = current_price
                buy_signals.append((current_time, current_price))

                print(f"\n[{current_time}] BUY SIGNAL")
                print(f"Buying 1 share at {last_buy_price:.2f}")
                print("-" * 50)

            elif short_mavg < long_mavg and in_position:
                # Sell signal when short moving average crosses below long moving average
                in_position = False
                sell_signals.append((current_time, current_price))
                profit_or_loss = (current_price - last_buy_price) * TRADE_QUANTITY
                total_profit += profit_or_loss  # Accumulate profit or loss
                result = "Profit" if profit_or_loss > 0 else "Loss"
                print(f"[{current_time}] SELL SIGNAL")
                print(f"Selling at {current_price:.2f}, {result}: ${profit_or_loss:.2f}")
                print("-" * 50)

    # Plotting the data and moving averages
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['close'], label='Close Price', color='gray', alpha=0.6)
    plt.plot(data.index, data['short_mavg'], label=f'Short {SHORT_WINDOW}-Period MA', color='blue')
    plt.plot(data.index, data['long_mavg'], label=f'Long {LONG_WINDOW}-Period MA', color='red')

    # Plot buy and sell signals
    buy_times, buy_prices = zip(*buy_signals) if buy_signals else ([], [])
    sell_times, sell_prices = zip(*sell_signals) if sell_signals else ([], [])
    plt.scatter(buy_times, buy_prices, marker='^', color='green', s=100, label='Buy Signal')
    plt.scatter(sell_times, sell_prices, marker='v', color='red', s=100, label='Sell Signal')
    # Display total profit
    print("\nBacktest completed.")
    print("=" * 50)
    print(f"Total Profit from Backtest: ${total_profit:.2f}")
    print("=" * 50)
    input("\nPress Enter to show graph...")
    # Chart formatting
    plt.title(f"{SYMBOL} Price with Moving Averages and Trade Signals")
    plt.xlabel("Time")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid()
    plt.show()



# Run the bot with historical data
def run_backtest():
    # Define historical period (e.g., the last 7 days)
    start_date = '2024-10-01'
    end_date = '2024-11-01'

    try:
        data = get_historical_data(SYMBOL, start=start_date, end=end_date)
        crossover_strategy_with_plot(data)

    except Exception as e:
        print(f"Error fetching historical data: {e}")

# Start the backtest
run_backtest()
