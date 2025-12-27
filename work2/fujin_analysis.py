"""
風神ボーナス詳細検証スクリプト
シンボル別の選択確率と配当を分析
"""

import random

BET_AMOUNT = 90

# 風神シンボル選択ウェイト（script.js準拠）
FUJIN_WEIGHTS = [
    (3, 0.5),   # Oiran
    (1, 1.5),   # Fujin
    (2, 3.0),   # Raijin
    (5, 5.0),   # Drum
    (4, 10.0),  # Fan
    (6, 16.0),  # A
    (7, 16.0),  # K
    (8, 16.0),  # Q
    (9, 16.0),  # J
    (10, 16.0)  # 10
]

# 配当テーブル（5-of-a-kind）
PAYOUTS_5 = {
    3: 2500,
    1: 250,
    2: 150,
    5: 100,
    4: 75,
    6: 50,
    7: 50,
    8: 25,
    9: 25,
    10: 25
}

# 理論期待値計算
print("=" * 60)
print("風神ボーナス理論期待値計算")
print("=" * 60)

total_prob = sum(p for _, p in FUJIN_WEIGHTS)
print(f"\n確率合計: {total_prob}%")

expected_value = 0
std_bet_per_line = max(1, int(BET_AMOUNT / 9))

print(f"\nライン当たりベット額: {std_bet_per_line}枚")
print("\nシンボル別詳細:")
print("-" * 60)

for sym_id, prob in FUJIN_WEIGHTS:
    payout_mult = PAYOUTS_5[sym_id]
    payout_coins = payout_mult * std_bet_per_line
    weighted_value = (prob / 100) * payout_coins
    expected_value += weighted_value
    
    sym_names = {
        3: "Oiran", 1: "Fujin", 2: "Raijin", 5: "Drum", 4: "Fan",
        6: "A", 7: "K", 8: "Q", 9: "J", 10: "10"
    }
    
    print(f"{sym_names[sym_id]:6s} (ID:{sym_id:2d}): 確率{prob:5.1f}% | "
          f"倍率{payout_mult:4d}x | 配当{payout_coins:4d}枚 | "
          f"EV貢献+{weighted_value:5.2f}")

print("-" * 60)
print(f"\n理論期待値: {expected_value:.2f}枚 ({expected_value/BET_AMOUNT:.2f}x Bet)")

# 実測シミュレーション
print("\n" + "=" * 60)
print("実測シミュレーション（100,000回）")
print("=" * 60)

SIMS = 100000
total_win = 0
symbol_counts = {sym_id: 0 for sym_id, _ in FUJIN_WEIGHTS}

for _ in range(SIMS):
    r = random.random() * 100
    acc = 0
    win_sym_id = 10
    for sym_id, prob in FUJIN_WEIGHTS:
        acc += prob
        if r < acc:
            win_sym_id = sym_id
            break
    
    symbol_counts[win_sym_id] += 1
    payout = PAYOUTS_5[win_sym_id] * std_bet_per_line
    total_win += payout

avg_win = total_win / SIMS
print(f"\n実測平均獲得枚数: {avg_win:.2f}枚 ({avg_win/BET_AMOUNT:.2f}x Bet)")
print(f"理論値との差異: {avg_win - expected_value:.2f}枚 ({(avg_win - expected_value)/expected_value * 100:.2f}%)")

print("\nシンボル選択分布（実測）:")
for sym_id, count in symbol_counts.items():
    actual_pct = (count / SIMS) * 100
    expected_pct = next(p for s, p in FUJIN_WEIGHTS if s == sym_id)
    sym_names = {
        3: "Oiran", 1: "RedFuji", 2: "Helmet", 5: "Drum", 4: "Fan",
        6: "A", 7: "K", 8: "Q", 9: "J", 10: "10"
    }
    print(f"{sym_names[sym_id]:6s}: {actual_pct:5.2f}% (理論値{expected_pct:5.1f}%, 誤差{actual_pct-expected_pct:+.2f}%)")

print("\n" + "=" * 60)
print("verify_game_mechanics.py との比較")
print("=" * 60)
print(f"理論値: {expected_value:.2f}枚 ({expected_value/BET_AMOUNT:.2f}x Bet)")
print(f"実測値: {avg_win:.2f}枚 ({avg_win/BET_AMOUNT:.2f}x Bet)")
print(f"verify実測値: 603.49枚 (6.71x Bet)")
print(f"\nシミュレーション実測値（前回）: 680.10枚 (7.56x Bet)")
print("=" * 60)
