# problem statment#1
 
# 🤖 ML Meets Blockchain: DeFi Wallet Behavior Scoring

In the decentralized finance (DeFi) space, there is no centralized credit agency to evaluate a wallet’s reliability. This project bridges the gap between **blockchain transparency** and **machine learning intelligence** by analyzing wallet-level activity and assigning each a credit score from 0 to 1000. The dataset used includes on-chain transactions from the Aave V2 protocol.

---

## 🌐 Use Case

Today, decentralized lending protocols often treat all wallets equally. But with behavioral analysis, we can distinguish:
- 💡 Responsible users (who repay loans)
- ⚠️ Risky or bot-like wallets (who default or get liquidated)

This system gives a data-driven view of wallet quality that can power:
- Risk modeling
- Lending decisions
- On-chain reputation systems

---

## 🧠 How It Works

We extract wallet-level features from the raw transaction data (JSON format) and use simple rule-based logic to compute scores. Features include:
- ✅ Number of deposits, borrows, repays
- ✅ Total amount involved in each
- ✅ Unique tokens interacted with
- ❌ Liquidation history (penalized)

The final output is a single score per wallet based on behavioral signals.

---

## 🗂 Directory Structure

```
.
├── main.py                  # Runs the full pipeline
├── user-wallet-transactions.json  # Sample transaction data (100K records)
├── wallet_credit_scores.csv # Output: Wallets with score (0–1000)
└── README.md
```

---

## 💻 How to Run

### 1. Prerequisites
- Python 3.8+
- Install required libraries:
```bash
pip install pandas numpy
```

### 2. Run
```bash
python main.py
```

### 3. Output
You’ll get a CSV file: `wallet_credit_scores.csv` with each wallet's behavior score.

---

## 📌 Example Score Table

| Wallet Address          | Score |
|-------------------------|-------|
| 0xabc123...             | 700   |
| 0xdef456...             | 910   |

---

## 🔬 Future Directions

- Train a supervised ML model (if labels are available)
- Add visual dashboards with score distributions
- Integrate into DeFi lending dashboards
- Extend to multi-chain behavior tracking

---

## 🧰 Built With

### Blockchain
- **Aave V2** – For historical DeFi transaction data
- **Ethereum wallets** – Each user is identified via wallet address

### Machine Learning
- **Scikit-Learn** – Potential for model-based scoring
- **NumPy + Pandas** – Data manipulation and aggregation

---

## 📃 License

Distributed under the MIT License – feel free to use or extend.

