
import numpy as np

def run_backtest_real(df, signals_df, rr=2,
                      capital=1000000, risk_percent=1):

    R_results = []
    trades = []
    in_position = False

    risk_amount = capital * (risk_percent / 100)

    for i in range(1, len(df)):

        signal = signals_df["signal"].iloc[i]
        stop_price = signals_df["stop_price"].iloc[i]

        if not in_position and signal == 1:

            entry_price = df["close"].iloc[i]
            entry_time = df.iloc[i].get("datetime", df.index[i])

            stop_distance = entry_price - stop_price
            if stop_distance <= 0:
                continue

            position_size = risk_amount / stop_distance
            target_price = entry_price + stop_distance * rr

            in_position = True
            continue

        if in_position:

            high = df["high"].iloc[i]
            low = df["low"].iloc[i]
            exit_time = df.iloc[i].get("datetime", df.index[i])

            if low <= stop_price:
                exit_price = stop_price
                pnl = -risk_amount
                R = -1
                reason = "SL"

            elif high >= target_price:
                exit_price = target_price
                pnl = risk_amount * rr
                R = rr
                reason = "TP"

            else:
                continue

            trades.append({
                "entry_time": entry_time,
                "exit_time": exit_time,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "stop_price": stop_price,
                "target_price": target_price,
                "position_size": position_size,
                "pnl": pnl,
                "R": R,
                "exit_reason": reason
            })

            R_results.append(R)
            in_position = False

    return np.array(R_results), trades


def basic_metrics(R):

    if len(R) == 0:
        return {}

    wins = R[R > 0]
    losses = R[R < 0]

    win_rate = len(wins) / len(R) * 100
    expectancy = R.mean()
    pf = wins.sum() / abs(losses.sum()) if len(losses) > 0 else 0

    streak = 0
    max_streak = 0
    for r in R:
        if r < 0:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0

    return {
        "trades": int(len(R)),
        "win_rate": round(win_rate, 2),
        "expectancy_R": round(expectancy, 3),
        "profit_factor": round(pf, 2),
        "max_losing_streak": int(max_streak)
    }


def monte_carlo(R):

    if len(R) == 0:
        return {}

    sims = 1000
    final = []
    drawdowns = []
    losing_streaks = []

    for _ in range(sims):
        shuffled = np.random.permutation(R)
        equity = np.cumsum(shuffled)
        final.append(equity[-1])

        peak = np.maximum.accumulate(equity)
        drawdowns.append(np.max(peak - equity))

        streak = 0
        max_streak = 0
        for r in shuffled:
            if r < 0:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        losing_streaks.append(max_streak)

    return {
        "median_final_R": float(np.median(final)),
        "worst_dd_95p": float(np.percentile(drawdowns, 95)),
        "worst_losing_streak_95p": float(np.percentile(losing_streaks, 95))
    }
