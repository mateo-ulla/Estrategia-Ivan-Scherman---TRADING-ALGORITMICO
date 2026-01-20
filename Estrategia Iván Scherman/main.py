import pandas as pd
import matplotlib.pyplot as plt

from data_loader import load_sp500_data
from strategy import SMAStrategy

def main():

    print("Cargando datos...")
    data = load_sp500_data(start="1990-01-01")

    print("Ejecutando backtest...")
    strategy = SMAStrategy(
        data=data,
        initial_cash=100000,
        risk_per_trade=0.01,
        vol_multiplier=1.0
    )

    final_cash, operations, equity_curve = strategy.run()

    trades = pd.DataFrame(operations)
    equity_df = pd.DataFrame(
        equity_curve,
        columns=['date', 'equity']
    ).set_index('date')

    # ================= RESULTADOS =================
    total_return = (final_cash / strategy.initial_cash - 1) * 100
    winrate = (trades['pnl'] > 0).mean() * 100
    max_dd = (
        equity_df['equity'] /
        equity_df['equity'].cummax() - 1
    ).min() * 100

    print("\n===== RESULTADOS DEL BACKTEST =====")
    print(f"Capital inicial: ${strategy.initial_cash:,.2f}")
    print(f"Capital final:   ${final_cash:,.2f}")
    print(f"Rentabilidad:    {total_return:.2f}%")
    print(f"Cantidad trades: {len(trades)}")
    print(f"Winrate:         {winrate:.2f}%")
    print(f"Max Drawdown:    {max_dd:.2f}%")

    # ================= GRAFICO =================
    plt.figure(figsize=(12, 6))
    plt.plot(equity_df.index, equity_df['equity'])
    plt.title("Equity Curve - Estrategia SMA (Iván Scherman)")
    plt.xlabel("Fecha")
    plt.ylabel("Capital")
    plt.yscale("log")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
