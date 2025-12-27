import random
import copy
import matplotlib.pyplot as plt

# --- Constants & Config ---
SPINS = 100000
BET = 90
STD_BET_PER_LINE = 10
INTERVAL = 1000

# Names needed for logic
SYMBOLS = [] # Not used in sim logic directly as we use IDs

# --- Mode Configurations (Notice 8% Fixed) ---
MODE_CONFIG = {
    1: { # Lucky
        'notice_prob': 0.15,
        'raijin_probs': [
           {'id': 9, 'p': 25.0}, {'id': 8, 'p': 25.0}, {'id': 7, 'p': 20.0}, {'id': 6, 'p': 20.0},
           {'id': 4, 'p': 4.0}, {'id': 5, 'p': 2.5}, {'id': 2, 'p': 2.0}, {'id': 1, 'p': 1.0}, {'id': 3, 'p': 0.5}
        ],
        'weights': [
            {'id': 1, 'weight': 500}, {'id': 2, 'weight': 500}, {'id': 3, 'weight': 200},
            {'id': 4, 'weight': 900}, {'id': 5, 'weight': 900}, {'id': 6, 'weight': 1200},
            {'id': 7, 'weight': 1200}, {'id': 8, 'weight': 1200}, {'id': 9, 'weight': 1200},
            {'id': 10, 'weight': 1200}, {'id': 11, 'weight': 400}
        ]
    },
    2: { # Normal
        'notice_prob': 0.08, # 8.0%
        'raijin_probs': [
           {'id': 9, 'p': 40.0}, {'id': 8, 'p': 30.0}, {'id': 7, 'p': 16.0}, {'id': 6, 'p': 9.2},
           {'id': 4, 'p': 2.0}, {'id': 5, 'p': 1.25}, {'id': 2, 'p': 1.0}, {'id': 1, 'p': 0.5}, {'id': 3, 'p': 0.05}
        ],
        'weights': [
            {'id': 1, 'weight': 450}, {'id': 2, 'weight': 450}, {'id': 3, 'weight': 180},
            {'id': 4, 'weight': 850}, {'id': 5, 'weight': 850}, {'id': 6, 'weight': 1250},
            {'id': 7, 'weight': 1250}, {'id': 8, 'weight': 1250}, {'id': 9, 'weight': 1250},
            {'id': 10, 'weight': 1250}, {'id': 11, 'weight': 400}
        ]
    },
    3: { # Tight
        'notice_prob': 0.01,
        'raijin_probs': [
           {'id': 9, 'p': 29.1}, {'id': 8, 'p': 26.3}, {'id': 7, 'p': 21.3}, {'id': 6, 'p': 21.3},
           {'id': 4, 'p': 1.0}, {'id': 5, 'p': 0.6}, {'id': 2, 'p': 0.3}, {'id': 1, 'p': 0.1}, {'id': 3, 'p': 0.0}
        ],
        'weights': [
            {'id': 1, 'weight': 400}, {'id': 2, 'weight': 400}, {'id': 3, 'weight': 150},
            {'id': 4, 'weight': 800}, {'id': 5, 'weight': 800}, {'id': 6, 'weight': 1300},
            {'id': 7, 'weight': 1300}, {'id': 8, 'weight': 1300}, {'id': 9, 'weight': 1300},
            {'id': 10, 'weight': 1300}, {'id': 11, 'weight': 400}
        ]
    }
}

PAYLINES = [
    [{'c': 0, 'r': 1}, {'c': 1, 'r': 1}, {'c': 2, 'r': 1}, {'c': 3, 'r': 1}, {'c': 4, 'r': 1}],
    [{'c': 0, 'r': 0}, {'c': 1, 'r': 0}, {'c': 2, 'r': 0}, {'c': 3, 'r': 0}, {'c': 4, 'r': 0}],
    [{'c': 0, 'r': 2}, {'c': 1, 'r': 2}, {'c': 2, 'r': 2}, {'c': 3, 'r': 2}, {'c': 4, 'r': 2}],
    [{'c': 0, 'r': 0}, {'c': 1, 'r': 1}, {'c': 2, 'r': 2}, {'c': 3, 'r': 1}, {'c': 4, 'r': 0}],
    [{'c': 0, 'r': 2}, {'c': 1, 'r': 1}, {'c': 2, 'r': 0}, {'c': 3, 'r': 1}, {'c': 4, 'r': 2}],
    [{'c': 0, 'r': 0}, {'c': 1, 'r': 0}, {'c': 2, 'r': 1}, {'c': 3, 'r': 2}, {'c': 4, 'r': 2}],
    [{'c': 0, 'r': 2}, {'c': 1, 'r': 2}, {'c': 2, 'r': 1}, {'c': 3, 'r': 0}, {'c': 4, 'r': 0}],
    [{'c': 0, 'r': 1}, {'c': 1, 'r': 2}, {'c': 2, 'r': 2}, {'c': 3, 'r': 2}, {'c': 4, 'r': 1}],
    [{'c': 0, 'r': 1}, {'c': 1, 'r': 0}, {'c': 2, 'r': 0}, {'c': 3, 'r': 0}, {'c': 4, 'r': 1}],
    [{'c': 0, 'r': 0}, {'c': 0, 'r': 1}, {'c': 0, 'r': 2}],
    [{'c': 1, 'r': 0}, {'c': 1, 'r': 1}, {'c': 1, 'r': 2}],
    [{'c': 2, 'r': 0}, {'c': 2, 'r': 1}, {'c': 2, 'r': 2}],
    [{'c': 3, 'r': 0}, {'c': 3, 'r': 1}, {'c': 3, 'r': 2}],
    [{'c': 4, 'r': 0}, {'c': 4, 'r': 1}, {'c': 4, 'r': 2}]
]

PAYOUTS = {
    3: {5: 2500, 4: 1000, 3: 100, 2: 10, 'v3': 10}, 
    1: {5: 250, 4: 150, 3: 50, 2: 5, 'v3': 5},
    2: {5: 150, 4: 100, 3: 30, 2: 3, 'v3': 4},
    5: {5: 100, 4: 50, 3: 20, 2: 2, 'v3': 3},
    4: {5: 75, 4: 30, 3: 10, 'v3': 2},
    6: {5: 50, 4: 20, 3: 5, 'v3': 1},
    7: {5: 50, 4: 20, 3: 5, 'v3': 1},
    8: {5: 25, 4: 10, 3: 5, 'v3': 1},
    9: {5: 25, 4: 10, 3: 5, 'v3': 1},
    10: {5: 25, 4: 10, 3: 5, 'v3': 1}
}

# --- Core Simulation Functions ---

def get_random_symbol(current_mode, raijin_mode=False):
    if raijin_mode and random.random() < 0.7:
        low_ids = [8, 9, 10]
        return random.choice(low_ids)
    
    config = MODE_CONFIG[current_mode]
    weights = config['weights']
    total_weight = sum(w['weight'] for w in weights)
    r = random.randint(0, total_weight - 1)
    acc = 0
    for w in weights:
        acc += w['weight']
        if r < acc:
            return w['id']
    return 10

def calculate_initial_grid(current_mode, pending_feature):
    grid = []
    for c in range(5):
        col = []
        for r in range(3):
            is_raijin = (pending_feature == 'RAIJIN')
            sym_id = get_random_symbol(current_mode, raijin_mode=is_raijin)
            col.append(sym_id)
        grid.append(col)
    return grid

def check_line_wins(grid):
    total_win = 0
    for line_idx, line in enumerate(PAYLINES):
        line_symbols = [grid[pos['c']][pos['r']] for pos in line]
        first_id = line_symbols[0]
        count_a = 0
        for s in line_symbols:
            if s == first_id: count_a += 1
            else: break
        mult_a = 0
        if first_id in PAYOUTS:
            table = PAYOUTS[first_id]
            if line_idx >= 9:
                if count_a == 3 and 'v3' in table: mult_a = table['v3']
            else:
                if count_a in table: mult_a = table[count_a]
        count_b = 0
        target_id = -1
        for s in line_symbols:
            if s != 3:
                target_id = s
                break
        mult_b = 0
        if target_id != -1:
            for s in line_symbols:
                if s == 3 or s == target_id: count_b += 1
                else: break
            if target_id in PAYOUTS:
                table = PAYOUTS[target_id]
                if line_idx >= 9:
                    if count_b == 3 and 'v3' in table: mult_b = table['v3']
                else:
                    if count_b in table: mult_b = table[count_b]
        best_mult = max(mult_a, mult_b)
        if best_mult > 0:
            current_line_bet = BET if line_idx >= 9 else STD_BET_PER_LINE
            total_win += best_mult * current_line_bet
    return total_win

def simulate_sushi_bonus():
    total_bonus_win = 0
    mults = [[0.5, 0.75, 1.0], [0.8, 1.2, 1.6], [1.0, 1.5, 2.0], [2.0, 3.0, 4.0], [5.0, 10.0, 15.0]]
    qualified_req = [2, 2, 1, 1, 0]
    for i in range(5):
        r_win = sum([int(BET * m) for m in random.choices(mults[i], k=3)])
        total_bonus_win += r_win
        if i == 4: break
        qualified_indices = random.sample(range(9), qualified_req[i])
        picked_indices = random.sample(range(9), 3)
        hits = len(set(qualified_indices) & set(picked_indices))
        if hits == 0: return total_bonus_win
    return total_bonus_win

def perform_symbol_upgrade(current_mode, grid):
    path_ids = [10, 9, 8, 7, 6, 4, 5, 2, 1, 3]
    config = MODE_CONFIG[current_mode]
    probs = config['raijin_probs']
    r = random.uniform(0, 100)
    acc = 0
    final_id = 9
    for p in probs:
        acc += p['p']
        if r < acc:
            final_id = p['id']
            break
    try: max_idx = path_ids.index(final_id)
    except ValueError: max_idx = 0
    for i in range(max_idx):
        target = path_ids[i]
        next_s = path_ids[i+1]
        for c in range(5):
            for r in range(3):
                if grid[c][r] == target: grid[c][r] = next_s
    return grid

def perform_fujin_feature(grid):
    line_idx = random.randint(0, 8)
    line_def = PAYLINES[line_idx]
    weights = [
        {'id': 3, 'p': 0.5}, {'id': 1, 'p': 1.5}, {'id': 2, 'p': 3.0},
        {'id': 5, 'p': 5.0}, {'id': 4, 'p': 10.0}, {'id': 6, 'p': 16.0},
        {'id': 7, 'p': 16.0}, {'id': 8, 'p': 16.0}, {'id': 9, 'p': 16.0},
        {'id': 10, 'p': 16.0}
    ]
    r_val = random.uniform(0, 100)
    acc = 0
    win_sym = 10
    for w in weights:
        acc += w['p']
        if r_val < acc:
            win_sym = w['id']
            break
    for pos in line_def:
        grid[pos['c']][pos['r']] = win_sym
    return grid

# --- Simulation Runner ---
def run_simulation(low_thr, high_thr, label):
    total_in = 0
    total_out = 0
    current_mode = 2
    credit = 50000
    
    x_axis = []
    y_max = []
    y_min = []
    
    interval_max = -float('inf')
    interval_min = float('inf')
    
    for i in range(SPINS):
        # Mode Switching
        rtp = 0
        if total_in > 0: rtp = (total_out / total_in) * 100
        
        if rtp < low_thr: current_mode = 1
        elif rtp > high_thr: current_mode = 3
        else: current_mode = 2
        
        credit -= BET
        total_in += BET
        spin_out = 0
        
        config = MODE_CONFIG[current_mode]
        pending_god_feature = None
        is_notice = random.random() < config['notice_prob']
        if is_notice:
            notice_type = 'RAIJIN' if random.random() < 0.5 else 'FUJIN'
            if random.random() < 0.30:
                pending_god_feature = notice_type
                
        grid = calculate_initial_grid(current_mode, pending_god_feature)
        spin_out += check_line_wins(grid)
        
        bonus_count = sum(col.count(11) for col in grid)
        if bonus_count >= 3:
            spin_out += simulate_sushi_bonus()
        else:
            if pending_god_feature:
                if pending_god_feature == 'RAIJIN': grid = perform_symbol_upgrade(current_mode, grid)
                else: grid = perform_fujin_feature(grid)
                spin_out += check_line_wins(grid)

        total_out += spin_out
        credit += spin_out
        
        if credit > interval_max: interval_max = credit
        if credit < interval_min: interval_min = credit
        
        if (i + 1) % INTERVAL == 0:
            x_axis.append(i + 1)
            y_max.append(interval_max)
            y_min.append(interval_min)
            interval_max = -float('inf')
            interval_min = float('inf')
            
    final_rtp = (total_out / total_in) * 100
    return x_axis, y_max, y_min, final_rtp

# --- Execute ---
# Scenario 1: Loose (80-120)
x1, y1_max, y1_min, rtp1 = run_simulation(80.0, 120.0, "Range 80-120")
print(f"Scenario 1 (80-120) RTP: {rtp1:.2f}%")

# Scenario 2: Strict (90-100)
x2, y2_max, y2_min, rtp2 = run_simulation(90.0, 100.0, "Range 90-100")
print(f"Scenario 2 (90-100) RTP: {rtp2:.2f}%")

# Plotting Comparison
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Plot 1
ax1.plot(x1, y1_max, label='Max (Limit)', color='green', alpha=0.7)
ax1.plot(x1, y1_min, label='Min (Limit)', color='red', alpha=0.7)
ax1.fill_between(x1, y1_min, y1_max, color='gray', alpha=0.1)
ax1.set_title(f'Scenario A: Range 80% - 120% (RTP: {rtp1:.2f}%)')
ax1.set_ylabel('Medals')
ax1.grid(True)
ax1.legend()

# Plot 2
ax2.plot(x2, y2_max, label='Max (Limit)', color='blue', alpha=0.7)
ax2.plot(x2, y2_min, label='Min (Limit)', color='orange', alpha=0.7)
ax2.fill_between(x2, y2_min, y2_max, color='gray', alpha=0.1)
ax2.set_title(f'Scenario B: Range 90% - 100% (RTP: {rtp2:.2f}%)')
ax2.set_xlabel('Total Spins')
ax2.set_ylabel('Medals')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig('medal_comparison.png')
print("Comparison graph saved to medal_comparison.png")
