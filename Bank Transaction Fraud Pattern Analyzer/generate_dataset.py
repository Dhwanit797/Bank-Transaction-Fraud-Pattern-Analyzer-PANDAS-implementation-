import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -------------------- CONFIG --------------------
np.random.seed(42)

NUM_TRANSACTIONS = 12000
NUM_ACCOUNTS = 400

# -------------------- IDS --------------------
transaction_ids = np.arange(1, NUM_TRANSACTIONS + 1)
account_ids = np.random.randint(
    100001,
    100001 + NUM_ACCOUNTS,
    size=NUM_TRANSACTIONS
)

# -------------------- DATES --------------------
end_date = datetime.now()
start_date = end_date - timedelta(days=270)

transaction_dates = pd.to_datetime(
    np.random.randint(
        int(start_date.timestamp()),
        int(end_date.timestamp()),
        size=NUM_TRANSACTIONS
    ),
    unit="s"
)

# -------------------- TRANSACTION TYPE --------------------
transaction_types = np.random.choice(
    ["debit", "credit"],
    size=NUM_TRANSACTIONS,
    p=[0.7, 0.3]
)

# -------------------- AMOUNTS --------------------
amounts = np.round(
    np.random.exponential(scale=2000, size=NUM_TRANSACTIONS),
    2
)
amounts = np.clip(amounts, 50, None)

# -------------------- INTERNATIONAL FLAG --------------------
is_international = np.random.choice(
    [0, 1],
    size=NUM_TRANSACTIONS,
    p=[0.92, 0.08]
)

# International transactions are higher value
amounts[is_international == 1] *= np.random.uniform(1.5, 3.0)
amounts = np.round(amounts, 2)

# -------------------- MERCHANT CATEGORY --------------------
merchant_categories = np.random.choice(
    ["groceries", "fuel", "electronics", "gambling", "crypto", "travel", "luxury"],
    size=NUM_TRANSACTIONS,
    p=[0.30, 0.20, 0.15, 0.05, 0.05, 0.15, 0.10]
)

# -------------------- LOCATION & CHANNEL --------------------
locations = np.random.choice(
    ["Ahmedabad", "Mumbai", "Delhi", "Bangalore", "Pune"],
    size=NUM_TRANSACTIONS
)

channels = np.random.choice(
    ["ATM", "Online", "POS"],
    size=NUM_TRANSACTIONS,
    p=[0.25, 0.45, 0.30]
)

# -------------------- BUILD DATAFRAME --------------------
df = pd.DataFrame({
    "transaction_id": transaction_ids,
    "account_id": account_ids,
    "transaction_date": transaction_dates,
    "transaction_type": transaction_types,
    "amount": amounts,
    "merchant_category": merchant_categories,
    "location": locations,
    "channel": channels,
    "is_international": is_international
})

# -------------------- SORT (CRITICAL) --------------------
df = df.sort_values(["account_id", "transaction_date"]).reset_index(drop=True)

# -------------------- BALANCE GENERATION --------------------
starting_balance = {
    acc: np.random.randint(20000, 100000)
    for acc in df["account_id"].unique()
}

balances = []
current_balance = {}

for _, row in df.iterrows():
    acc = row["account_id"]

    if acc not in current_balance:
        current_balance[acc] = starting_balance[acc]

    if row["transaction_type"] == "debit":
        # Simulate failed debit if insufficient balance
        if current_balance[acc] >= row["amount"]:
            current_balance[acc] -= row["amount"]
    else:
        current_balance[acc] += row["amount"]

    balances.append(round(current_balance[acc], 2))

df["balance_after"] = balances

# -------------------- EXPORT --------------------
df.to_csv("transactions.csv", index=False)
