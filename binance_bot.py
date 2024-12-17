from binance.client import Client
from binance.websockets import BinanceSocketManager
import asyncio
import pandas as pd
import numpy as np
import logging

class BinanceBot:
    logging.basicConfig(filename='binance_trading_bot.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, api_key, api_secret, symbol='BTCUSDT'):
        self.client = Client(api_key, api_secret)
        self.bm = BinanceSocketManager(self.client)
        self.symbol = symbol
        self.data = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        self.conn_key = None

    async def start_socket(self):
        def process_message(msg):
            ts = pd.to_datetime(msg['E'], unit='ms')
            if not self.data.empty and ts == self.data.index[-1]:
                self.data.iloc[-1] = [msg['k']['o'], msg['k']['h'], msg['k']['l'], msg['k']['c'], msg['k']['v']]
            else:
                self.data = self.data.append(pd.Series({
                    'Open': msg['k']['o'],
                    'High': msg['k']['h'],
                    'Low': msg['k']['l'],
                    'Close': msg['k']['c'],
                    'Volume': msg['k']['v']
                }, name=ts))

        self.conn_key = self.bm.start_kline_socket(self.symbol, process_message, interval='1m')
        self.bm.start()

    async def stop_socket(self):
        self.bm.stop_socket(self.conn_key)
        self.bm.close()

    def advanced_strategy(df):
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['SMA200'] = df['Close'].rolling(window=200).mean()
        df['ATR'] = df['High'].rolling(window=14).max() - df['Low'].rolling(window=14).min()
        df['Signal'] = np.where(df['SMA50'] > df['SMA200'], 1, -1)
        df['Position'] = df['Signal'].diff()

        # Risk Management: Position Sizing based on ATR
        df['Position_Size'] = df['Close'] / (df['ATR'] * 10)  # Assuming 10 ATR for risk per trade
        return df

    def place_order(self, side, quantity):
        try:
            order = self.client.order_market(
                symbol=self.symbol,
                side=side,
                quantity=quantity
            )
            logging.info(f"Placed {side} order for {quantity} {self.symbol}")
            return order
        except Exception as e:
            logging.error(f"Error placing order: {e}")

    async def run(self):
        try:
            await self.start_socket()
            while True:
                if not self.data.empty:
                    signals = self.advanced_strategy(self.data)
                    latest_signal = signals.iloc[-1]

                    if latest_signal['Position'] > 0:  # Buy signal
                        quantity = latest_signal['Position_Size']
                        self.place_order('BUY', quantity)
                    elif latest_signal['Position'] < 0:  # Sell signal
                        # Here, you'd need to know how many to sell based on current position,
                        # but for simplicity, assume selling all:
                        quantity = signals['Position_Size'].iloc[-2] if len(signals) > 1 else latest_signal[
                            'Position_Size']
                        self.place_order('SELL', quantity)

                await asyncio.sleep(60)  # Check every minute
        except Exception as e:
            logging.error(f"Bot error: {e}")
        finally:
            await self.stop_socket()