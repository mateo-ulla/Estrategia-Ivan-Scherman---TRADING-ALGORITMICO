import numpy as np

class SMAStrategy:

    def __init__(
        self,
        data,
        initial_cash=100000,
        risk_per_trade=0.01,
        vol_multiplier=1.0
    ):
        self.data = data.copy()
        self.cash = initial_cash
        self.initial_cash = initial_cash
        self.risk_per_trade = risk_per_trade
        self.vol_multiplier = vol_multiplier

        self.position = 0
        self.entry_price = None
        self.sl_price = None

        self.operations = []
        self.equity_curve = []

        # Indicadores
        self.data['SMA200'] = self.data['close'].rolling(200).mean()
        self.data['SMA5'] = self.data['close'].rolling(5).mean()
        self.data['Volatility'] = (
            self.data['close']
            .pct_change()
            .rolling(14)
            .std()
        )

    def run(self):

        for i in range(200, len(self.data) - 1):

            row = self.data.iloc[i]
            next_row = self.data.iloc[i + 1]
            date = self.data.index[i]

            # ================= ENTRADA =================
            if self.position == 0 and row['close'] > row['SMA200']:

                c1 = self.data.iloc[i - 1]
                c2 = self.data.iloc[i - 2]
                c3 = self.data.iloc[i - 3]

                red_candles = (
                    c1['close'] < c1['open'] and
                    c2['close'] < c2['open'] and
                    c3['close'] < c3['open']
                )

                lower_closes = (
                    c1['close'] < c2['close'] < c3['close']
                )

                no_gaps = (
                    abs(c2['open'] - c3['close']) / c3['close'] < 0.001 and
                    abs(c1['open'] - c2['close']) / c2['close'] < 0.001
                )

                if red_candles and lower_closes and no_gaps:

                    volatility = row['Volatility']
                    if np.isnan(volatility):
                        continue

                    entry_price = next_row['open']
                    sl_price = entry_price - (
                        entry_price * volatility * self.vol_multiplier
                    )

                    risk_amount = self.cash * self.risk_per_trade
                    size = risk_amount / (entry_price - sl_price)

                    self.position = size
                    self.entry_price = entry_price
                    self.sl_price = sl_price
                    self.cash -= size * entry_price

                    self.operations.append({
                        'entry_date': next_row.name,
                        'entry_price': entry_price,
                        'exit_date': None,
                        'exit_price': None,
                        'pnl': None
                    })

            # ================= SALIDA =================
            elif self.position > 0:

                exit_price = None

                if row['close'] <= self.sl_price:
                    exit_price = self.sl_price

                elif row['close'] > row['SMA5']:
                    exit_price = next_row['open']

                if exit_price is not None:
                    pnl = self.position * (exit_price - self.entry_price)
                    self.cash += self.position * exit_price

                    self.operations[-1]['exit_date'] = next_row.name
                    self.operations[-1]['exit_price'] = exit_price
                    self.operations[-1]['pnl'] = pnl

                    self.position = 0
                    self.entry_price = None
                    self.sl_price = None

            equity = self.cash + (
                self.position * row['close'] if self.position > 0 else 0
            )
            self.equity_curve.append((date, equity))

        return self.cash, self.operations, self.equity_curve
