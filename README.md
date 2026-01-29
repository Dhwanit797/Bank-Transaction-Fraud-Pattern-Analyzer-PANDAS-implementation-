# 🏦 Bank Transaction Fraud Pattern Analyzer

## 🔹 Description
This project uses **Python and Pandas** to simulate bank transactions and detect potential fraud patterns.  
It applies **rule-based analytics** and a **weighted risk scoring system** to flag suspicious activity.

---

## 🔹 Features
- Generate and analyze synthetic bank transaction data  
- Detect **high-amount debit anomalies**  
- Identify **rapid-fire transactions** (multiple transactions in a single day)  
- Detect **location-based anomalies** (impossible travel)  
- Track **risky merchant usage** (gambling, crypto, luxury)  
- Detect **balance drain behavior** (sudden large withdrawals)  
- Compute **multi-signal fraud risk score**  
- Generate **CSV reports** for each pattern and overall fraud risk  

---

## 🔹 Tech Stack
- Python  
- Pandas  
- NumPy  

---

## 🔹 How to Run
1. Place `transactions.csv` in the project directory.  
2. Run the analysis script:

```bash
python fraud_analysis.py
````

3. Output CSV reports will be generated in the same directory.

---

## 🔹 Project Structure

```
├── transactions.csv
├── fraud_analysis.py
├── high_amount_alerts.csv
├── rapid_transactions_accounts.csv
├── location_mismatch_accounts.csv
├── risky_merchant_account.csv
├── balance_drain_cases.csv
├── fraud_risk_report.csv
```

---

## 🔹 Output Files

| File Name                         | Description                                         |
| --------------------------------- | --------------------------------------------------- |
| `high_amount_alerts.csv`          | High-amount debit transactions                      |
| `rapid_transactions_accounts.csv` | Accounts with multiple transactions in a single day |
| `location_mismatch_accounts.csv`  | Location anomaly cases                              |
| `risky_merchant_account.csv`      | Accounts with ≥40% risky merchant transactions      |
| `balance_drain_cases.csv`         | Balance drain transactions (≥60% drop)              |
| `fraud_risk_report.csv`           | Consolidated fraud risk scoring report              |

---

## 🔹 Author

**Dhwanit**

---

## 🔹 Future Scope

* Machine learning–based fraud classification
* Real-time transaction stream analysis
* Dynamic risk scoring using historical behavior
* Dashboard visualization using Power BI / Tableau / Streamlit
