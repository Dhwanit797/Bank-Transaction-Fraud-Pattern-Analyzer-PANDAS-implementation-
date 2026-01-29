import pandas as pd
import numpy as np

# ================== Load & Prepare ==================

df = pd.read_csv("data/transactions.csv")

df["transaction_date"] = pd.to_datetime(df["transaction_date"])
df = df.sort_values(["account_id", "transaction_date"])

# ================== Pattern 1: High Amount Debit ==================

df["account_avg_amount"] = (
    df.groupby("account_id")["amount"].transform("mean")
)

df["deviation_ratio"] = df["amount"] / df["account_avg_amount"]

df["is_high_amount"] = (
    (df["transaction_type"] == "debit") &
    (df["deviation_ratio"] > 3)
)

high_amount_alerts = (
    df[df["is_high_amount"]]
    .sort_values("deviation_ratio", ascending=False)
    [[
        "transaction_id",
        "account_id",
        "transaction_date",
        "amount",
        "account_avg_amount",
        "deviation_ratio",
        "merchant_category",
        "location",
        "channel",
        "is_international"
    ]]
)

high_amount_alerts.to_csv("high_amount_alerts.csv", index=False)

# ================== Pattern 2: Rapid-Fire Transactions ==================

df["transaction_day"] = df["transaction_date"].dt.date

daily_transaction_count = (
    df.groupby(["account_id", "transaction_day"])
    .size()
    .reset_index(name="transaction_count")
)

rapid_fire_accounts = (
    daily_transaction_count[daily_transaction_count["transaction_count"] >= 3]
    .sort_values("transaction_count", ascending=False)
)

rapid_fire_accounts.to_csv("rapid_transactions_accounts.csv", index=False)

# ================== Pattern 3: Location Anomaly ==================

df["prev_location"] = df.groupby("account_id")["location"].shift(1)
df["prev_transaction_time"] = df.groupby("account_id")["transaction_date"].shift(1)

df["time_diff_hours"] = (
    (df["transaction_date"] - df["prev_transaction_time"])
    .dt.total_seconds() / 3600
)

df["is_location_anomaly"] = (
    df["prev_location"].notna() &
    (df["location"] != df["prev_location"]) &
    (df["time_diff_hours"] <= 24)
)

location_anomalies = (
    df[df["is_location_anomaly"]]
    .sort_values("time_diff_hours")
    [[
        "transaction_id",
        "account_id",
        "transaction_date",
        "prev_transaction_time",
        "location",
        "prev_location",
        "time_diff_hours",
        "amount",
        "channel",
        "is_international"
    ]]
)

location_anomalies.to_csv("location_mismatch_accounts.csv", index=False)

# ================== Pattern 4: Risky Merchant Abuse ==================

risky_categories = ["gambling", "crypto", "luxury"]

df["is_risky_merchant"] = df["merchant_category"].isin(risky_categories)

merchant_risk_summary = (
    df.groupby("account_id")
    .agg(
        total_transactions=("transaction_id", "count"),
        risky_transactions=("is_risky_merchant", "sum")
    )
    .reset_index()
)

merchant_risk_summary["risky_transaction_ratio"] = (
    merchant_risk_summary["risky_transactions"] /
    merchant_risk_summary["total_transactions"]
)

risky_merchant_accounts = (
    merchant_risk_summary[merchant_risk_summary["risky_transaction_ratio"] >= 0.40]
    .sort_values("risky_transaction_ratio", ascending=False)
)

risky_merchant_accounts.to_csv("risky_merchant_account.csv", index=False)

# ================== Pattern 5: Balance Drain ==================

df["prev_balance"] = df.groupby("account_id")["balance_after"].shift(1)

df["balance_drop_ratio"] = np.where(
    df["prev_balance"] > 0,
    (df["prev_balance"] - df["balance_after"]) / df["prev_balance"],
    0
)

df["is_balance_drain"] = (
    (df["transaction_type"] == "debit") &
    (df["balance_drop_ratio"] >= 0.60)
)

balance_drain_cases = (
    df[df["is_balance_drain"]]
    .sort_values("balance_drop_ratio", ascending=False)
    [[
        "transaction_id",
        "account_id",
        "transaction_date",
        "prev_balance",
        "balance_after",
        "balance_drop_ratio",
        "amount",
        "channel",
        "location",
        "is_international"
    ]]
)

balance_drain_cases.to_csv("balance_drain_cases.csv", index=False)

# ================== Risk Scoring Engine ==================

df["risk_score"] = 0

df.loc[df["is_high_amount"], "risk_score"] += 2
df.loc[df["is_location_anomaly"], "risk_score"] += 2
df.loc[df["is_risky_merchant"], "risk_score"] += 1
df.loc[df["is_balance_drain"], "risk_score"] += 3

df = df.merge(
    daily_transaction_count,
    on=["account_id", "transaction_day"],
    how="left"
)

df["is_rapid_fire"] = df["transaction_count"] >= 3
df.loc[df["is_rapid_fire"], "risk_score"] += 1

df["is_fraud_suspected"] = df["risk_score"] >= 4

# ================== Final Fraud Report ==================

fraud_cases = (
    df[df["is_fraud_suspected"]]
    .sort_values("risk_score", ascending=False)
    [[
        "transaction_id",
        "account_id",
        "transaction_date",
        "amount",
        "risk_score",
        "merchant_category",
        "location",
        "channel",
        "is_international"
    ]]
)

fraud_cases.to_csv("fraud_risk_report.csv", index=False)