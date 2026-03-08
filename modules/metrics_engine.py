import pandas as pd


def compute_metrics(df):

    if df.empty:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "loss_rate": 0,
            "gross_profit": 0,
            "gross_loss": 0,
            "profit_factor": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "best_trade": 0,
            "worst_trade": 0,
            "total_profit": 0
        }

    total_trades = len(df)

    wins = df[df["net_profit"] > 0]
    losses = df[df["net_profit"] < 0]

    win_rate = (len(wins) / total_trades) * 100 if total_trades else 0
    loss_rate = (len(losses) / total_trades) * 100 if total_trades else 0

    gross_profit = wins["net_profit"].sum()
    gross_loss = abs(losses["net_profit"].sum())

    profit_factor = gross_profit / gross_loss if gross_loss != 0 else 0

    avg_win = wins["net_profit"].mean() if not wins.empty else 0
    avg_loss = losses["net_profit"].mean() if not losses.empty else 0

    best_trade = df["net_profit"].max()
    worst_trade = df["net_profit"].min()

    total_profit = df["net_profit"].sum()

    return {

        "total_trades": total_trades,
        "win_rate": round(win_rate,2),
        "loss_rate": round(loss_rate,2),

        "gross_profit": round(gross_profit,2),
        "gross_loss": round(gross_loss,2),

        "profit_factor": round(profit_factor,2),

        "avg_win": round(avg_win,2),
        "avg_loss": round(avg_loss,2),

        "best_trade": round(best_trade,2),
        "worst_trade": round(worst_trade,2),

        "total_profit": round(total_profit,2)

    }
