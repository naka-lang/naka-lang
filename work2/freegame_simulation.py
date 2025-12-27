"""
フリーゲーム実装後のスロットマシン完全シミュレーション
100,000回転でRTP、ボーナス発生率、配当分布を分析
"""

import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUIなしで動作

# 定数定義
BET_AMOUNT = 9  # 1回転あたりのベット額
SIMULATIONS = 100_000

# モード設定（Mode 2: Normal）
NOTICE_PROB = 0.08  # 予告発生率 8%

# シンボルペイアウトテーブル
PAYOUTS = {
    3: {5: 2500, 4: 1000, 3: 100, 2: 10},  # Oiran
    1: {5: 250, 4: 150, 3: 50, 2: 5},      # Fujin
    2: {5: 150, 4: 100, 3: 30, 2: 3},      # Raijin
    5: {5: 100, 4: 50, 3: 20, 2: 2},       # Drum
    4: {5: 75, 4: 30, 3: 10},              # Fan
    6: {5: 50, 4: 20, 3: 5},               # A
    7: {5: 50, 4: 20, 3: 5},               # K
    8: {5: 25, 4: 10, 3: 5},               # Q
    9: {5: 25, 4: 10, 3: 5},               # J
    10: {5: 25, 4: 10, 3: 5}               # 10
}

# 統計カウンター
total_in = 0
total_out = 0
freegame_count = 0
fujin_count = 0
raijin_count = 0
bonus_count = 0
credit_history = []
current_credit = 0

def simulate_notice():
    """予告発生と結果を判定"""
    if random.random() >= NOTICE_PROB:
        return None
    
    # 予告タイプ振り分け: Fujin 40%, Raijin 40%, FreeGame 20%
    r = random.random() * 100
    if r < 40:
        notice_type = 'FUJIN'
    elif r < 80:
        notice_type = 'RAIJIN'
    else:
        notice_type = 'FREEGAME'
    
    # 成功判定
    if notice_type == 'FREEGAME':
        # 100% 確定、内部分岐
        split = random.random() * 100
        if split < 34:
            return 'FREEGAME'
        elif split < 67:
            return 'FUJIN'
        else:
            return 'RAIJIN'
    else:
        # 30% 成功率
        if random.random() < 0.30:
            return notice_type
    return None

def simulate_normal_spin():
    """通常スピンの配当を簡易計算（平均値ベース）"""
    # 簡易的にベースRTPを50%と仮定（ボーナスなし時）
    if random.random() < 0.15:  # 15%の確率で当たり
        # 平均配当を3倍と設定
        return BET_AMOUNT * random.uniform(1, 10)
    return 0

def simulate_fujin_bonus():
    """風神ボーナス（1ライン確定当選）"""
    # 平均配当: ベットの10-30倍
    return BET_AMOUNT * random.uniform(10, 30)

def simulate_raijin_bonus():
    """雷神ボーナス（シンボルアップグレード）"""
    # 平均配当: ベットの15-50倍
    return BET_AMOUNT * random.uniform(15, 50)

def simulate_freegame():
    """フリーゲームシミュレーション（5回スピン、継続あり）"""
    total_win = 0
    round_num = 1
    
    while round_num <= 4:  # 最大4ラウンド
        # 5回スピン
        for _ in range(5):
            # 左右両端ワイルド固定なので、通常より高配当
            if random.random() < 0.6:  # 60%の確率で当たり
                total_win += BET_AMOUNT * random.uniform(3, 20)
        
        # 継続判定
        if round_num == 1:
            continue_chance = 0.50
        elif round_num == 2:
            continue_chance = 0.30
        elif round_num == 3:
            continue_chance = 0.10
        else:
            break
        
        if random.random() < continue_chance:
            round_num += 1
        else:
            break
    
    return total_win

def simulate_bonus_game():
    """寿司ボーナスゲーム"""
    # 平均配当: ベットの5-20倍
    return BET_AMOUNT * random.uniform(5, 20)

# メインシミュレーション
print(f"シミュレーション開始: {SIMULATIONS:,}回転")
print(f"ベット額: {BET_AMOUNT} per spin")
print("-" * 50)

for i in range(SIMULATIONS):
    total_in += BET_AMOUNT
    spin_win = 0
    
    # 予告判定
    feature = simulate_notice()
    
    # 通常スピン配当
    normal_win = simulate_normal_spin()
    
    # ボーナスゲーム判定（3%の確率）
    if random.random() < 0.03:
        bonus_count += 1
        spin_win += simulate_bonus_game()
    
    # フィーチャー実行
    if feature == 'FREEGAME':
        freegame_count += 1
        spin_win += normal_win + simulate_freegame()
    elif feature == 'FUJIN':
        fujin_count += 1
        spin_win += normal_win + simulate_fujin_bonus()
    elif feature == 'RAIJIN':
        raijin_count += 1
        spin_win += normal_win + simulate_raijin_bonus()
    else:
        spin_win += normal_win
    
    total_out += spin_win
    current_credit += (spin_win - BET_AMOUNT)
    
    # 100回転ごとにクレジット記録
    if (i + 1) % 100 == 0:
        credit_history.append(current_credit)
    
    # 進捗表示
    if (i + 1) % 10000 == 0:
        print(f"進捗: {i+1:,} / {SIMULATIONS:,} 回転")

# 結果計算
rtp = (total_out / total_in) * 100 if total_in > 0 else 0

print("\n" + "=" * 50)
print("シミュレーション結果")
print("=" * 50)
print(f"総回転数: {SIMULATIONS:,}")
print(f"総ベット額: {total_in:,}")
print(f"総払い出し: {total_out:,.0f}")
print(f"純損益: {total_out - total_in:,.0f}")
print(f"\n★ RTP: {rtp:.2f}%")
print("\n" + "-" * 50)
print("ボーナス発生回数:")
print(f"  フリーゲーム: {freegame_count:,} ({freegame_count/SIMULATIONS*100:.3f}%)")
print(f"  風神ボーナス: {fujin_count:,} ({fujin_count/SIMULATIONS*100:.3f}%)")
print(f"  雷神ボーナス: {raijin_count:,} ({raijin_count/SIMULATIONS*100:.3f}%)")
print(f"  寿司ボーナス: {bonus_count:,} ({bonus_count/SIMULATIONS*100:.3f}%)")
print(f"  合計: {freegame_count + fujin_count + raijin_count:,}")

# グラフ作成
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# グラフ1: クレジット推移
ax1.plot(range(0, len(credit_history) * 100, 100), credit_history, linewidth=1, color='blue', alpha=0.7)
ax1.axhline(y=0, color='red', linestyle='--', linewidth=1)
ax1.set_xlabel('Spins', fontsize=12)
ax1.set_ylabel('Credit', fontsize=12)
ax1.set_title(f'Credit History (100,000 spins, RTP: {rtp:.2f}%)', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# グラフ2: ボーナス発生率
labels = ['FreGame\n{:.3f}%'.format(freegame_count/SIMULATIONS*100),
          'Fujin\n{:.3f}%'.format(fujin_count/SIMULATIONS*100),
          'Raijin\n{:.3f}%'.format(raijin_count/SIMULATIONS*100),
          'Sushi\n{:.3f}%'.format(bonus_count/SIMULATIONS*100)]
sizes = [freegame_count, fujin_count, raijin_count, bonus_count]
colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']
explode = (0.1, 0, 0, 0)

ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax2.set_title('Bonus Distribution', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/nakaneshunsuke/Desktop/antigarvity/work2/simulation_result.png', dpi=150, bbox_inches='tight')
print(f"\nグラフ保存: simulation_result.png")
print("=" * 50)
