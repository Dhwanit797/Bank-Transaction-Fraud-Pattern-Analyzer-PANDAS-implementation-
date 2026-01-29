🏦 Bank Transaction Fraud Pattern Analyzer
Description

A data analysis project built using Python and Pandas to simulate bank transactions and detect potential fraud patterns using rule-based analytics and a weighted risk scoring system.

Features

Synthetic bank transaction dataset generation

High-amount debit anomaly detection

Rapid-fire (high-frequency) transaction analysis

Location-based anomaly detection

Risky merchant usage analysis (gambling, crypto, luxury)

Balance drain behavior detection

Multi-signal fraud risk scoring engine

CSV-based fraud reports generation

Tech Stack

Python

Pandas

NumPy

How to Run

Place transactions.csv in the project directory

Run the analysis script:

python fraud_analysis.py


Generated reports will be saved as CSV files

Output Files

high_amount_alerts.csv

rapid_transactions_accounts.csv

location_mismatch_accounts.csv

risky_merchant_account.csv

balance_drain_cases.csv

fraud_risk_report.csv

Project Structure
├── transactions.csv
├── fraud_analysis.py
├── high_amount_alerts.csv
├── rapid_transactions_accounts.csv
├── location_mismatch_accounts.csv
├── risky_merchant_account.csv
├── balance_drain_cases.csv
├── fraud_risk_report.csv

Author

Dhwanit

Future Scope

Machine learning–based fraud classification

Real-time transaction stream analysis

Dynamic risk scoring using historical behavior

Dashboard visualization (Power BI / Tableau / Streamlit)
