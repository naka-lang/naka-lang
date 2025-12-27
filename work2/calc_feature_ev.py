import random
import statistics

# --- Copied Constants & Config from simulate_rtp.py (Latest) ---
BET = 90
STD_BET_PER_LINE = 10

# Copied from simulate_rtp.py
MODE_CONFIG = {
    2: { # Normal
        'notice_prob': 0.08, 
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

# --- Helper Functions ---

def get_random_symbol(current_mode, raijin_mode=False):
    # Standard logic: if raijin_mode, 70% chance to return low symbol
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
        if r < acc: return w['id']
    return 10

def calculate_initial_grid(current_mode, pending_feature):
    grid = []
    for c in range(5):
        col = []
        for r in range(3):
            # If pending feature is RAIJIN, use bias mode
            is_raijin = (pending_feature == 'RAIJIN')
            sym_id = get_random_symbol(current_mode, raijin_mode=is_raijin)
            col.append(sym_id)
        grid.append(col)
    return grid

def perform_symbol_upgrade(current_mode, grid):
    path_ids = [10, 9, 8, 7, 6, 4, 5, 2, 1, 3] # Upgrade Path
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

    # Execute Upgrade
    for i in range(max_idx):
        target = path_ids[i]
        next_s = path_ids[i+1]
        for c in range(5):
            for r in range(3):
                if grid[c][r] == target:
                    grid[c][r] = next_s
    return grid

def perform_fujin_feature(grid):
    line_idx = random.randint(0, 8)
    line_def = PAYLINES[line_idx]
    
    # Feature Weights (Fixed across modes usually)
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

def check_line_wins(grid):
    total_win = 0
    for line_idx, line in enumerate(PAYLINES):
        line_symbols = [grid[pos['c']][pos['r']] for pos in line]
        
        # Check from Left (Pattern A)
        first_id = line_symbols[0]
        count_a = 0
        for s in line_symbols:
            if s == first_id: count_a += 1
            else: break
        mult_a = 0
        if first_id in PAYOUTS:
            table = PAYOUTS[first_id]
            if line_idx >= 9: # Vertical lines
                if count_a == 3 and 'v3' in table: mult_a = table['v3']
            else:
                if count_a in table: mult_a = table[count_a]
        
        # Check (Pattern B) - Wild/Any? 
        # Actually logic in main script is complex, simplified here as "Any-Oiran-Mix"
        # Standard checks usually suffice.
        # Let's trust the logic copied from simulate_rtp.py regarding check_line_wins
        
        # Re-verify check_line_wins logic from simulate_rtp.py 
        # It had "count_b" logic for Wilds/Oiran.
        count_b = 0
        target_id = -1
        for s in line_symbols:
            if s != 3: # 3 is OIRAN (Wild)
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

# --- Main Calc ---
TRIALS = 100000

# 1. RAIJIN Expected Value
raijin_wins = []
for _ in range(TRIALS):
    # Step 1: Initial Grid with Raijin Bias
    grid = calculate_initial_grid(current_mode=2, pending_feature='RAIJIN')
    # Step 2: Upgrade
    grid = perform_symbol_upgrade(current_mode=2, grid=grid)
    # Step 3: Win
    win = check_line_wins(grid)
    raijin_wins.append(win)

raijin_ev = statistics.mean(raijin_wins)

# 2. FUJIN Expected Value
fujin_wins = []
for _ in range(TRIALS):
    # Step 1: Initial Grid with NO Bias (Fujin just overwrites lines)
    grid = calculate_initial_grid(current_mode=2, pending_feature='FUJIN')
    # Step 2: Feature
    grid = perform_fujin_feature(grid)
    # Step 3: Win
    win = check_line_wins(grid)
    fujin_wins.append(win)

fujin_ev = statistics.mean(fujin_wins)

print(f"Raijin Bonus EV: {raijin_ev:.2f} Coins")
print(f"Fujin Bonus EV: {fujin_ev:.2f} Coins")
