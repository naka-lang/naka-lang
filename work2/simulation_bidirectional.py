"""
script.js完全準拠シミュレーション（Full Implementation）
全配当計算ロジック、ペイライン、Fujin/Raijin/寿司ボーナスを完全実装
"""

import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# 定数定義
BET_AMOUNT = 90
SIMULATIONS = 1_000_000

# モード設定
MODE_CONFIG = {
    1: {'name': 'Lucky', 'notice_prob': 0.06},
    2: {'name': 'Normal', 'notice_prob': 0.06},
    3: {'name': 'Tight', 'notice_prob': 0.06}
}

# シンボルウェイト
SYMBOL_WEIGHTS = {
    1: {1: 550, 2: 550, 3: 200, 4: 1000, 5: 1000, 6: 1200, 7: 1200, 8: 1200, 9: 1200, 10: 1200, 11: 300, 14: 1000},
    2: {1: 500, 2: 500, 3: 180, 4: 950, 5: 950, 6: 1250, 7: 1250, 8: 1250, 9: 1250, 10: 1250, 11: 300, 14: 950},
    3: {1: 450, 2: 450, 3: 150, 4: 900, 5: 900, 6: 1300, 7: 1300, 8: 1300, 9: 1300, 10: 1300, 11: 300, 14: 900}
};

# 配当テーブル（script.js PAYOUTS準拠）
PAYOUTS = {
    3: {5: 2500, 4: 1000, 3: 100, 2: 10, 'v3': 10},  # Oiran (Wild)
    1: {5: 250, 4: 150, 3: 50, 2: 5, 'v3': 5},       # Fujin
    2: {5: 150, 4: 100, 3: 30, 2: 3, 'v3': 4},       # Raijin
    5: {5: 100, 4: 50, 3: 20, 2: 2, 'v3': 3},        # Drum
    4: {5: 75, 4: 30, 3: 10, 'v3': 2},               # Fan
    14: {5: 75, 4: 30, 3: 10, 'v3': 2},              # Daruma (Same as Fan)
    6: {5: 50, 4: 20, 3: 5, 'v3': 1},                # A
    7: {5: 50, 4: 20, 3: 5, 'v3': 1},                # K
    8: {5: 25, 4: 10, 3: 5, 'v3': 1},                # Q
    9: {5: 25, 4: 10, 3: 5, 'v3': 1},                # J
    10: {5: 25, 4: 10, 3: 5, 'v3': 1}                # 10
}

# ペイライン定義（14本）
PAYLINES = [
    [(0,1), (1,1), (2,1), (3,1), (4,1)],  # 0: 中段横
    [(0,0), (1,0), (2,0), (3,0), (4,0)],  # 1: 上段横
    [(0,2), (1,2), (2,2), (3,2), (4,2)],  # 2: 下段横
    [(0,0), (1,1), (2,2), (3,1), (4,0)],  # 3: V字
    [(0,2), (1,1), (2,0), (3,1), (4,2)],  # 4: 逆V字
    [(0,0), (1,0), (2,1), (3,2), (4,2)],  # 5: 小V字
    [(0,2), (1,2), (2,1), (3,0), (4,0)],  # 6: 小逆V
    [(0,1), (1,2), (2,2), (3,2), (4,1)],  # 7: U字
    [(0,1), (1,0), (2,0), (3,0), (4,1)],  # 8: 逆U字
    [(0,0), (0,1), (0,2)],                # 9: 縦 reel 0
    [(1,0), (1,1), (1,2)],                # 10: 縦 reel 1
    [(2,0), (2,1), (2,2)],                # 11: 縦 reel 2
    [(3,0), (3,1), (3,2)],                # 12: 縦 reel 3
    [(4,0), (4,1), (4,2)]                 # 13: 縦 reel 4
]

# Fujinシンボル選択ウェイト
FUJIN_WEIGHTS = [
    (3, 0.5), (1, 1.5), (2, 3.0), (5, 5.0), (4, 10.0), (14, 10.0),
    (6, 16.0), (7, 16.0), (8, 16.0), (9, 16.0), (10, 16.0)
]

# Raijinターゲット確率（Normal Mode）
RAIJIN_PROBS = [
    (9, 35.0), (8, 30.0), (7, 15.4), (6, 10.0),
    (4, 2.5), (14, 2.5), (5, 2.0), (2, 1.5), (1, 1.0), (3, 0.1)
]

# 寿司ボーナス倍率（ラウンド別）
SUSHI_MULTIPLIERS = {
    1: [0.5, 0.75, 1.0],
    2: [0.8, 1.2, 1.6],
    3: [1.0, 1.5, 2.0],
    4: [2.0, 3.0, 4.0],
    5: [5.0, 10.0, 15.0]
}

# 統計
total_in = 0
total_out = 0
freegame_count = 0
fujin_count = 0
raijin_count = 0
bonus_count = 0
# 各ボーナスの累計獲得枚数
freegame_total_win = 0
fujin_total_win = 0
raijin_total_win = 0
sushi_total_win = 0
# 通常ゲーム統計
base_game_total_win = 0
base_game_spin_count = 0
credit_history = []
current_credit = 0
mode_usage = {1: 0, 2: 0, 3: 0}
current_mode = 2

# 直近100回転の履歴バッファ
history_in = []
history_out = []

def update_history(in_amount, out_amount):
    history_in.append(in_amount)
    history_out.append(out_amount)
    if len(history_in) > 100:
        history_in.pop(0)
        history_out.pop(0)

def get_current_mode():
    if not history_in:
        return 2
    
    recent_in = sum(history_in)
    recent_out = sum(history_out)
    
    if recent_in == 0:
        return 2
        
    rtp = (recent_out / recent_in) * 100
    if rtp < 80:
        return 1
    elif rtp <= 115:
        return 2
    else:
        return 3

def get_random_symbol(mode):
    weights = SYMBOL_WEIGHTS[mode]
    total_weight = sum(weights.values())
    r = random.random() * total_weight
    cumulative = 0
    for symbol_id in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14]:
        cumulative += weights[symbol_id]
        if r < cumulative:
            return symbol_id
    return 10

def generate_grid(mode, is_free_game=False):
    grid = []
    for col in range(5):
        column = []
        for row in range(3):
            if is_free_game and col == 0:
                column.append(13)  # Raijin Wild (Left)
            elif is_free_game and col == 4:
                column.append(12)  # Fujin Wild (Right)
            else:
                column.append(get_random_symbol(mode))
        grid.append(column)
    return grid

def check_win(grid, is_free_game=False):
    """完全配当計算（script.js checkWin準拠）"""
def calculate_line_mult(line_symbols, line_idx):
    # Logic A: Natural Win
    first_id = line_symbols[0]
    count_a = 0
    for sym_id in line_symbols:
        if sym_id == first_id:
            count_a += 1
        else:
            break
    
    mult_a = 0
    if line_idx >= 9:  # 縦ライン
        if count_a == 3 and first_id in PAYOUTS and 'v3' in PAYOUTS[first_id]:
            mult_a = PAYOUTS[first_id]['v3']
    else:  # 横/斜めライン
        if first_id in PAYOUTS and count_a in PAYOUTS[first_id]:
            mult_a = PAYOUTS[first_id][count_a]
    
    # Logic B: Wild Win (ID 3 = Wild, 12 = Fujin, 13 = Raijin)
    target_id = None
    for sym_id in line_symbols:
        if sym_id != 3 and sym_id != 12 and sym_id != 13:
            target_id = sym_id
            break
    
    mult_b = 0
    count_b = 0
    if target_id is not None:
        for sym_id in line_symbols:
            if sym_id == 3 or sym_id == 12 or sym_id == 13 or sym_id == target_id:
                count_b += 1
            else:
                break
        
        if line_idx >= 9:  # 縦ライン
            if count_b == 3 and target_id in PAYOUTS and 'v3' in PAYOUTS[target_id]:
                mult_b = PAYOUTS[target_id]['v3']
        else:
            if target_id in PAYOUTS and count_b in PAYOUTS[target_id]:
                mult_b = PAYOUTS[target_id][count_b]
    
    # Return best multiplier and its associated count
    if mult_a >= mult_b:
        return mult_a, count_a
    else:
        return mult_b, count_b

def check_win(grid, is_free_game=False):
    """双方向配当計算（Bidirectional Payout, 5-match exclusion）"""
    total_win = 0
    std_bet_per_line = max(1, int(BET_AMOUNT / 9))
    
    for line_idx, line in enumerate(PAYLINES):
        # フリーゲーム時: reel 0, 4の縦ラインは無効
        if is_free_game and (line_idx == 9 or line_idx == 13):
            continue
        
        line_symbols = [grid[pos[0]][pos[1]] for pos in line]
        
        # 1. Left-to-Right (Normal)
        mult_lr, count_lr = calculate_line_mult(line_symbols, line_idx)
        
        # 2. Right-to-Left (Horizontal/Diagonal Only)
        mult_rl = 0
        count_rl = 0
        if line_idx < 9: # Only for horizontal/diagonal lines
             # STRICT: Skip R-L if L-R is already a 5-match
             if count_lr < 5:
                 # Calculate R-L
                 mult_rl, count_rl = calculate_line_mult(list(reversed(line_symbols)), line_idx)
        
        # Calculate Win for LR
        if mult_lr > 0:
            if line_idx >= 9:
                total_win += mult_lr * BET_AMOUNT
            else:
                total_win += mult_lr * std_bet_per_line

        # Calculate Win for RL
        if mult_rl > 0:
            total_win += mult_rl * std_bet_per_line
            
    return total_win

def count_bonus_symbols(grid):
    count = 0
    for col in grid:
        for sym_id in col:
            if sym_id == 11:
                count += 1
    return count

def simulate_notice(mode):
    notice_prob = MODE_CONFIG[mode]['notice_prob']
    if random.random() >= notice_prob:
        return None
    
    r = random.random() * 100
    if r < 40:
        notice_type = 'FUJIN'
    elif r < 80:
        notice_type = 'RAIJIN'
    else:
        notice_type = 'FREEGAME'
    
    if notice_type == 'FREEGAME':
        split = random.random() * 100
        if split < 34:
            return 'FREEGAME'
        elif split < 67:
            return 'FUJIN'
        else:
            return 'RAIJIN'
    else:
        if random.random() < 0.30:
            return notice_type
    return None

def simulate_fujin_bonus(mode):
    """Fujinボーナス（完全実装）"""
    # ライン選択（横0-8）
    line_idx = random.randint(0, 8)
    line = PAYLINES[line_idx]
    
    # シンボル選択（重み付き）
    r = random.random() * 100
    acc = 0
    win_sym_id = 10
    for sym_id, prob in FUJIN_WEIGHTS:
        acc += prob
        if r < acc:
            win_sym_id = sym_id
            break
    
    # グリッド生成＆ライン置き換え
    grid = generate_grid(mode)
    for pos in line:
        grid[pos[0]][pos[1]] = win_sym_id
    
    return check_win(grid)

def simulate_raijin_bonus(mode):
    """Raijinボーナス（script.js完全準拠：段階的アップグレード）"""
    # グリッド生成
    grid = generate_grid(mode)
    
    # ターゲット決定
    r = random.random() * 100
    acc = 0
    target_id = 9
    for sym_id, prob in RAIJIN_PROBS:
        acc += prob
        if r < acc:
            target_id = sym_id
            break
    
    # アップグレードパス
    path = [10, 9, 8, 7, 6, 4, 14, 5, 2, 1, 3]
    # 10→J→Q→K→A→Fan→Daruma→Drum→Helmet→RedFuji→Oiran
    
    try:
        max_idx = path.index(target_id)
    except ValueError:
        max_idx = 0
    
    # script.js準拠：段階的に transform pathIds[i] -> pathIds[i+1]
    # 例: target=A(6)の場合、10→J, J→Q, Q→K, K→A と段階的に変換
    for i in range(max_idx):
        current_id = path[i]
        next_id = path[i + 1]
        
        # グリッド内のcurrent_idをnext_idに変換
        for c in range(5):
            for r in range(3):
                if grid[c][r] == current_id:
                    grid[c][r] = next_id
    
    return check_win(grid)

def simulate_freegame(mode):
    """フリーゲーム（完全実装）"""
    total_win = 0
    round_num = 1
    
    while round_num <= 4:
        # 5スピン
        for _ in range(5):
            grid = generate_grid(mode, is_free_game=True)
            total_win += check_win(grid, is_free_game=True)
        
        # 継続判定
        if round_num == 1:
            continue_chance = 0.40
        elif round_num == 2:
            continue_chance = 0.20
        elif round_num == 3:
            continue_chance = 0.10
        else:
            break
        
        if random.random() < continue_chance:
            round_num += 1
        else:
            break
    
    return total_win

def simulate_sushi_bonus(bonus_count):
    """寿司ボーナス（5ラウンドシステム完全実装）"""
    total_win = 0
    current_round = 1
    
    # シンボル数による上昇: (シンボル数 - 3) * 30%
    count_bonus = 1.0 + max(0, (bonus_count - 3) * 0.3)
    
    while current_round <= 5:
        # 各ラウンドで3皿選択
        round_win = 0
        for _ in range(3):
            mult = random.choice(SUSHI_MULTIPLIERS[current_round])
            round_win += int(BET_AMOUNT * mult * count_bonus)
        
        total_win += round_win
        
        # 継続判定
        if current_round == 5:
            break  # 最終ラウンド
        
        # 合格条件
        if current_round == 1:
            qualified_count = 3
        elif current_round == 2:
            qualified_count = 2
        elif current_round == 3 or current_round == 4:
            qualified_count = 1
        else:
            qualified_count = 0
        
        # 簡易継続判定（3皿中qualified_count以上当たる確率）
        picks = 3
        total_plates = 9
        hit_prob = qualified_count / total_plates
        
        # 少なくとも1つ当たる確率
        if qualified_count > 0:
            no_hit_prob = 1.0
            for i in range(picks):
                no_hit_prob *= (total_plates - qualified_count - i) / (total_plates - i)
            pass_prob = 1 - no_hit_prob
        else:
            pass_prob = 0
        
        if random.random() < pass_prob:
            current_round += 1
        else:
            break
    
    return total_win

# メインシミュレーション
print(f"完全準拠シミュレーション開始: {SIMULATIONS:,}回転")
print(f"実装: ペイライン判定、配当テーブル、Fujin/Raijin/寿司ボーナス完全版")
print("-" * 60)

for i in range(SIMULATIONS):
    if i > 0:
        current_mode = get_current_mode()
    mode_usage[current_mode] += 1
    
    total_in += BET_AMOUNT
    spin_win = 0
    
    # 予告判定
    feature = simulate_notice(current_mode)
    
    # 通常スピンの配当計算
    normal_grid = generate_grid(current_mode)
    normal_win = check_win(normal_grid)
    
    # 通常ゲーム統計（フィーチャーなしの場合のみ）
    if feature is None:
        base_game_total_win += normal_win
        base_game_spin_count += 1
    
    # BONUSシンボルカウント
    bonus_symbols = count_bonus_symbols(normal_grid)
    if bonus_symbols >= 3:
        bonus_count += 1
        sushi_win = simulate_sushi_bonus(bonus_symbols)
        sushi_total_win += sushi_win
        spin_win += sushi_win
    
    # フィーチャー実行
    if feature == 'FREEGAME':
        freegame_count += 1
        fg_win = simulate_freegame(current_mode)
        freegame_total_win += fg_win
        spin_win += normal_win + fg_win  # FGはnormal_winと合算
    elif feature == 'FUJIN':
        fujin_count += 1
        fujin_win = simulate_fujin_bonus(current_mode)
        fujin_total_win += fujin_win
        spin_win += fujin_win  # Fujinはグリッド書き換えなのでnormal_win加算なし
    elif feature == 'RAIJIN':
        raijin_count += 1
        raijin_win = simulate_raijin_bonus(current_mode)
        raijin_total_win += raijin_win
        spin_win += raijin_win  # Raijinはグリッド書き換えなのでnormal_win加算なし
    else:
        spin_win += normal_win
    
    total_out += spin_win
    current_credit += (spin_win - BET_AMOUNT)

    # 履歴更新 (Rolling RTP用)
    update_history(BET_AMOUNT, spin_win)
    
    if (i + 1) % 100 == 0:
        credit_history.append(current_credit)
    
    if (i + 1) % 10000 == 0:
        rtp = (total_out / total_in) * 100
        print(f"進捗: {i+1:,} / {SIMULATIONS:,} | RTP: {rtp:.2f}% | Mode: {current_mode}")

# 結果
rtp = (total_out / total_in) * 100

print("\n" + "=" * 60)
print("完全準拠シミュレーション結果")
print("=" * 60)
print(f"総回転数: {SIMULATIONS:,}")
print(f"総ベット額: {total_in:,}")
print(f"総払い出し: {int(total_out):,}")
print(f"純損益: {int(total_out - total_in):,}")
print(f"\n★ 最終RTP: {rtp:.2f}%")

print("\n" + "-" * 60)
print("モード使用率:")
for mode_id in [1, 2, 3]:
    count = mode_usage[mode_id]
    pct = (count / SIMULATIONS) * 100
    print(f"  Mode {mode_id} ({MODE_CONFIG[mode_id]['name']:6s}): {count:,} ({pct:.1f}%)")

print("\n" + "-" * 60)
print("ボーナス発生回数:")
print(f"  フリーゲーム: {freegame_count} ({freegame_count/SIMULATIONS*100:.3f}%)")
print(f"  風神ボーナス: {fujin_count} ({fujin_count/SIMULATIONS*100:.3f}%)")
print(f"  雷神ボーナス: {raijin_count} ({raijin_count/SIMULATIONS*100:.3f}%)")
print(f"  寿司ボーナス: {bonus_count} ({bonus_count/SIMULATIONS*100:.3f}%)")

print("\n" + "-" * 60)
print("ボーナス平均獲得枚数（完全準拠版シミュレーション）:")
fg_avg = freegame_total_win / freegame_count if freegame_count > 0 else 0
fujin_avg = fujin_total_win / fujin_count if fujin_count > 0 else 0
raijin_avg = raijin_total_win / raijin_count if raijin_count > 0 else 0
sushi_avg = sushi_total_win / bonus_count if bonus_count > 0 else 0

print(f"  フリーゲーム: {fg_avg:.2f}枚 ({fg_avg/BET_AMOUNT:.2f}x Bet)")
print(f"  風神ボーナス: {fujin_avg:.2f}枚 ({fujin_avg/BET_AMOUNT:.2f}x Bet)")
print(f"  雷神ボーナス: {raijin_avg:.2f}枚 ({raijin_avg/BET_AMOUNT:.2f}x Bet)")
print(f"  寿司ボーナス: {sushi_avg:.2f}枚 ({sushi_avg/BET_AMOUNT:.2f}x Bet)")

print("\n" + "-" * 60)
print("通常ゲーム単体RTP:")
base_game_avg = base_game_total_win / base_game_spin_count if base_game_spin_count > 0 else 0
base_game_rtp = (base_game_avg / BET_AMOUNT) * 100
print(f"  平均配当: {base_game_avg:.2f}枚 ({base_game_avg/BET_AMOUNT:.2f}x Bet)")
print(f"  通常ゲームRTP: {base_game_rtp:.2f}%")
print(f"  測定スピン数: {base_game_spin_count:,}回")

print("\n" + "=" * 60)
print("期待値比較（verify_game_mechanics.py 実測値）:")
print("  フリーゲーム: 2054.24枚 (22.82x Bet)")
print("  風神ボーナス: 603.49枚 (6.71x Bet)")
print("  雷神ボーナス: 649.92枚 (7.22x Bet)")
print("  通常ゲーム: 34.25枚 (0.38x Bet = 38% RTP)")
print("※寿司ボーナスは前回測定なし")
print("=" * 60)

# グラフ作成
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

ax1.plot(credit_history, linewidth=0.8)
ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
ax1.set_title('Credit Fluctuation (Full Logic)')
ax1.set_xlabel('Spins (×100)')
ax1.set_ylabel('Credit')
ax1.grid(True, alpha=0.3)

bonus_data = [freegame_count, fujin_count, raijin_count, bonus_count]
bonus_labels = ['Free Game', 'Fujin', 'Raijin', 'Sushi']
colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24']
ax2.bar(bonus_labels, bonus_data, color=colors, alpha=0.7)
ax2.set_title('Bonus Distribution')
ax2.set_ylabel('Count')
ax2.grid(True, alpha=0.3, axis='y')

mode_data = [mode_usage[1], mode_usage[2], mode_usage[3]]
mode_labels = ['Lucky', 'Normal', 'Tight']
ax3.pie(mode_data, labels=mode_labels, autopct='%1.1f%%', startangle=90)
ax3.set_title('Mode Usage')

rtp_history = []
for i in range(len(credit_history)):
    spins = (i + 1) * 100
    bet_total = spins * BET_AMOUNT
    win_total = bet_total + credit_history[i]
    rtp_val = (win_total / bet_total) * 100
    rtp_history.append(rtp_val)

ax4.plot(rtp_history, linewidth=0.8, color='green')
ax4.axhline(y=100, color='r', linestyle='--', alpha=0.5, label='100% RTP')
ax4.set_title('RTP Convergence (Full Logic)')
ax4.set_xlabel('Spins (×100)')
ax4.set_ylabel('RTP (%)')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulation_full_logic.png', dpi=150, bbox_inches='tight')
print("\nグラフ保存: simulation_full_logic.png")
print("=" * 60)
