import json
import pandas as pd
import numpy as np
from collections import defaultdict

file_path = r"D:\user-wallet-transactions (1).json"



with open(file_path, 'r') as f:
    data = json.load(f)


print(f"Total records loaded: {len(data)}")
print("First record:")
print(data[0])
# Initialize a dictionary to hold wallet-wise statistics
wallet_stats = defaultdict(lambda: {
    'deposit_count': 0,
    
    'borrow_count': 0,
    'repay_count': 0,
    'redeem_count': 0,
    'liquidation_count': 0,
    'total_amount': 0.0,\
    'first_tx': float('inf'),
    'last_tx': 0,
    'assets': set()
})

# Parse and aggregate statistics
for tx in data:
    wallet = tx.get('userWallet')
    action = tx.get('action')
    timestamp = tx.get('timestamp')
    action_data = tx.get('actionData', {})
    amount = float(action_data.get('amount', 0)) / 1e6  # Convert to readable unit
    asset = action_data.get('assetSymbol')

    # Update transaction statistics
    if action == 'deposit':
        wallet_stats[wallet]['deposit_count'] += 1
    elif action == 'borrow':
        wallet_stats[wallet]['borrow_count'] += 1
    elif action == 'repay':
        wallet_stats[wallet]['repay_count'] += 1
    elif action == 'redeemunderlying':
        wallet_stats[wallet]['redeem_count'] += 1
    elif action == 'liquidationcall':
        wallet_stats[wallet]['liquidation_count'] += 1

    wallet_stats[wallet]['total_amount'] += amount
    wallet_stats[wallet]['first_tx'] = min(wallet_stats[wallet]['first_tx'], timestamp)
    wallet_stats[wallet]['last_tx'] = max(wallet_stats[wallet]['last_tx'], timestamp)

    if asset:
        wallet_stats[wallet]['assets'].add(asset)

# Convert sets to counts for easier scoring
for stats in wallet_stats.values():
    stats['unique_assets'] = len(stats['assets'])
    del stats['assets']

# Preview first 3 wallets' stats
preview_stats = dict(list(wallet_stats.items())[:3])
preview_stats


# Convert wallet_stats dictionary into a DataFrame
df = pd.DataFrame.from_dict(wallet_stats, orient='index')

# Reset index to get wallet address as a column
df.reset_index(inplace=True)
df.rename(columns={'index': 'wallet'}, inplace=True)

# Preview the first 5 wallets
print("\nSummary for first 5 wallets:")
print(df.head())

# Save to CSV for review (optional)
df.to_csv("wallet_summary.csv", index=False)

print("\nAvailable columns in DataFrame:")
print(df.columns)

# Function to score each row (wallet)
def compute_score(row):
    score = 500

    if 'borrow_amount' in row and row['borrow_amount'] > 0:
        repay_ratio = row['repay_amount'] / row['borrow_amount']
        score += min(repay_ratio, 1) * 300
    else:
        repay_ratio = 0

    score += min(row.get('deposit_count', 0), 10) * 10
    score += min(row.get('unique_assets', 0), 5) * 10
    score -= min(row.get('liquidation_count', 0), 5) * 30

    return np.clip(score, 0, 1000)


# Compute score per wallet
df['score'] = df.apply(compute_score, axis=1)

# View top 5 scored wallets
print("\nTop 5 wallets with scores:")
print(df[['wallet', 'score']].sort_values(by='score', ascending=False).head())

# Save final scored data
df.to_csv("wallet_credit_scores.csv", index=False)
