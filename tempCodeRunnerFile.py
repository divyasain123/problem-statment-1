def compute_score(row):
    score = 500  # Start from a base score

    # Reward responsible repayment
    if row['borrow_amount'] > 0:
        repay_ratio = row['repay_amount'] / row['borrow_amount']
        score += min(repay_ratio, 1) * 300  # cap reward at 300 pts
    else:
        repay_ratio = 0

    # Reward consistent deposits
    score += min(row['deposit_count'], 10) * 10  # up to 100 pts

    # Reward asset diversity
    score += min(row['unique_assets'], 5) * 10  # up to 50 pts

    # Penalize liquidations
    score -= min(row['liquidation_count'], 5) * 30  # up to -150 pts

    return np.clip(score, 0, 1000)  # Clamp between 0 and 1000

# Compute score per wallet
df['score'] = df.apply(compute_score, axis=1)

# View top 5 scored wallets
print("\nTop 5 wallets with scores:")
print(df[['wallet', 'score']].sort_values(by='score', ascending=False).head())

# Save final scored data
df.to_csv("wallet_credit_scores.csv", index=False)
