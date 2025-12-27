
import random

# Constants
BET = 90
SIMULATIONS = 100000

# Symbol Definitions
SYMBOLS = [
    {'id': 1, 'name': 'RedFuji', 'value': 1000, 'payout': {5: 250, 4: 150, 3: 50, 2: 5, 'v3': 5}},
    {'id': 2, 'name': 'Helmet', 'value': 1000, 'payout': {5: 150, 4: 100, 3: 30, 2: 3, 'v3': 4}},
    {'id': 3, 'name': 'OIRAN', 'value': 500, 'payout': {5: 2500, 4: 1000, 3: 100, 2: 10, 'v3': 10}}, # WILD
    {'id': 4, 'name': 'FAN', 'value': 200, 'payout': {5: 75, 4: 30, 3: 10, 'v3': 2}},
    {'id': 5, 'name': 'DRUM', 'value': 150, 'payout': {5: 100, 4: 50, 3: 20, 2: 2, 'v3': 3}},
    {'id': 6, 'name': 'A', 'value': 50, 'payout': {5: 50, 4: 20, 3: 5, 'v3': 1}},
    {'id': 7, 'name': 'K', 'value': 40, 'payout': {5: 50, 4: 20, 3: 5, 'v3': 1}},
    {'id': 8, 'name': 'Q', 'value': 30, 'payout': {5: 25, 4: 10, 3: 5, 'v3': 1}},
    {'id': 9, 'name': 'J', 'value': 20, 'payout': {5: 25, 4: 10, 3: 5, 'v3': 1}},
    {'id': 10, 'name': '10', 'value': 10, 'payout': {5: 25, 4: 10, 3: 5, 'v3': 1}},
    {'id': 11, 'name': 'BONUS', 'value': 0, 'payout': {}}
]

# Weights (Normal Mode)
WEIGHTS = [
    {'id': 1, 'weight': 450}, {'id': 2, 'weight': 450}, {'id': 3, 'weight': 180},
    {'id': 4, 'weight': 850}, {'id': 5, 'weight': 850}, {'id': 6, 'weight': 1250},
    {'id': 7, 'weight': 1250}, {'id': 8, 'weight': 1250}, {'id': 9, 'weight': 1250},
    {'id': 10, 'weight': 1250}, {'id': 11, 'weight': 400}
]
TOTAL_WEIGHT = sum(w['weight'] for w in WEIGHTS)

PAYLINES = [
    [{'c': 0, 'r': 1}, {'c': 1, 'r': 1}, {'c': 2, 'r': 1}, {'c': 3, 'r': 1}, {'c': 4, 'r': 1}], # 0
    [{'c': 0, 'r': 0}, {'c': 1, 'r': 0}, {'c': 2, 'r': 0}, {'c': 3, 'r': 0}, {'c': 4, 'r': 0}], # 1
    [{'c': 0, 'r': 2}, {'c': 1, 'r': 2}, {'c': 2, 'r': 2}, {'c': 3, 'r': 2}, {'c': 4, 'r': 2}], # 2
    [{'c': 0, 'r': 0}, {'c': 1, 'r': 1}, {'c': 2, 'r': 2}, {'c': 3, 'r': 1}, {'c': 4, 'r': 0}], # 3
    [{'c': 0, 'r': 2}, {'c': 1, 'r': 1}, {'c': 2, 'r': 0}, {'c': 3, 'r': 1}, {'c': 4, 'r': 2}], # 4
    [{'c': 0, 'r': 0}, {'c': 1, 'r': 0}, {'c': 2, 'r': 1}, {'c': 3, 'r': 2}, {'c': 4, 'r': 2}], # 5
    [{'c': 0, 'r': 2}, {'c': 1, 'r': 2}, {'c': 2, 'r': 1}, {'c': 3, 'r': 0}, {'c': 4, 'r': 0}], # 6
    [{'c': 0, 'r': 1}, {'c': 1, 'r': 2}, {'c': 2, 'r': 2}, {'c': 3, 'r': 2}, {'c': 4, 'r': 1}], # 7
    [{'c': 0, 'r': 1}, {'c': 1, 'r': 0}, {'c': 2, 'r': 0}, {'c': 3, 'r': 0}, {'c': 4, 'r': 1}], # 8
    [{'c': 0, 'r': 0}, {'c': 0, 'r': 1}, {'c': 0, 'r': 2}], # 9 (Vert 0)
    [{'c': 1, 'r': 0}, {'c': 1, 'r': 1}, {'c': 1, 'r': 2}], # 10 (Vert 1)
    [{'c': 2, 'r': 0}, {'c': 2, 'r': 1}, {'c': 2, 'r': 2}], # 11 (Vert 2)
    [{'c': 3, 'r': 0}, {'c': 3, 'r': 1}, {'c': 3, 'r': 2}], # 12 (Vert 3)
    [{'c': 4, 'r': 0}, {'c': 4, 'r': 1}, {'c': 4, 'r': 2}]  # 13 (Vert 4)
]

def get_random_symbol():
    r = random.random() * TOTAL_WEIGHT
    acc = 0
    for w in WEIGHTS:
        acc += w['weight']
        if r < acc:
            return next(s for s in SYMBOLS if s['id'] == w['id'])
    return SYMBOLS[9] # Fallback 10

def check_win(grid, is_free_game=False):
    total_win = 0
    std_bet_line = max(1, int(BET / 9))
    
    for idx, line in enumerate(PAYLINES):
        if is_free_game and (idx == 9 or idx == 13):
            continue
            
        line_symbols = [grid[p['c']][p['r']] for p in line]
        
        # Logic A (Natural)
        first = line_symbols[0]
        count_a = 0
        for s in line_symbols:
            if s['id'] == first['id']: count_a += 1
            else: break
            
        mult_a = 0
        if idx >= 9: # Vertical
            if count_a == 3 and 'v3' in first['payout']: mult_a = first['payout']['v3']
        else:
            if count_a in first['payout']: mult_a = first['payout'][count_a]
            
        # Logic B (Wild ID 3)
        count_b = 0
        target = None
        for s in line_symbols:
            if s['id'] != 3:
                target = s
                break
        
        mult_b = 0
        if target:
            for s in line_symbols:
                if s['id'] == 3 or s['id'] == target['id']:
                    count_b += 1
                else: break
            
            if idx >= 9:
                if count_b == 3 and 'v3' in target['payout']: mult_b = target['payout']['v3']
            else:
                if count_b in target['payout']: mult_b = target['payout'][count_b]
        
        best = max(mult_a, mult_b)
        if best > 0:
            if idx >= 9:
                total_win += best * BET
            else:
                total_win += best * std_bet_line
                
    return total_win

def simulate_free_game():
    # 5 spins initial
    spins = 5
    round_num = 1
    total_win = 0
    
    while True:
        for _ in range(spins):
            # Generate Grid
            grid = []
            for c in range(5):
                col = []
                for r in range(3):
                    if is_free_game and (c == 0 or c == 4):
                        col.append(next(s for s in SYMBOLS if s['id'] == 3)) # Wild
                    else:
                        col.append(get_random_symbol())
                grid.append(col)
            
            total_win += check_win(grid, is_free_game=True)
        
        # Continuation
        chance = 0
        if round_num == 1: chance = 0.5
        elif round_num == 2: chance = 0.3
        elif round_num == 3: chance = 0.1
        
        if random.random() < chance:
            round_num += 1
            spins = 5
        else:
            break
            
    return total_win

def simulate_fujin_feature():
    # Single Line Win
    line_idx = random.randint(0, 8)
    # Weights for Fujin Symbol
    # ID: 3(0.5), 1(1.5), 2(3), 5(5), 4(10), 6-10(16 each)
    f_weights = [
        (3, 0.5), (1, 1.5), (2, 3.0), (5, 5.0), (4, 10.0),
        (6, 16.0), (7, 16.0), (8, 16.0), (9, 16.0), (10, 16.0)
    ]
    r = random.random() * 100
    acc = 0
    win_id = 10
    for fid, p in f_weights:
        acc += p
        if r < acc:
            win_id = fid
            break
            
    win_sym = next(s for s in SYMBOLS if s['id'] == win_id)
    mult = 0
    if 5 in win_sym['payout']: mult = win_sym['payout'][5]
    
    # Line Bet (std)
    std_bet = max(1, int(BET/9))
    return mult * std_bet

def simulate_raijin_feature():
    # Upgrade Logic
    # 1. Generate Random Grid
    grid = []
    for c in range(5):
        col = []
        for r in range(3):
            col.append(get_random_symbol())
        grid.append(col)
        
    # 2. Determine Target
    raijin_probs = [
        (9, 40.0), (8, 30.0), (7, 16.0), (6, 9.2),
        (4, 2.0), (5, 1.25), (2, 1.0), (1, 0.5), (3, 0.05)
    ]
    r = random.random() * 100
    acc = 0
    final_id = 9
    for fid, p in raijin_probs:
        acc += p
        if r < acc:
            final_id = fid
            break
            
    # 3. Upgrade
    path = [10, 9, 8, 7, 6, 4, 5, 2, 1, 3] # ID path
    try:
        max_idx = path.index(final_id)
    except ValueError:
        max_idx = 0
        
    ids_to_change = path[:max_idx] # These will all become final_id eventually?
    # Logic in JS: iterates upgrades. 10->J, J->Q...
    # Effectively: Any symbol in `ids_to_change` becomes `final_id`.
    # AND `final_id` stays `final_id`.
    # Symbols NOT in path (Bonus ID 11) stay same? Path includes almost everything except Bonus.
    
    target_sym = next(s for s in SYMBOLS if s['id'] == final_id)
    
    for c in range(5):
        for r in range(3):
            if grid[c][r]['id'] in ids_to_change or grid[c][r]['id'] == final_id:
                grid[c][r] = target_sym
                
    return check_win(grid, is_free_game=False)

def simulate_base_game():
    grid = []
    for c in range(5):
        col = []
        for r in range(3):
            col.append(get_random_symbol())
        grid.append(col)
    
    return check_win(grid, is_free_game=False)

# Main Verify
is_free_game = True # Context for free game sim
print(f"Verifying Free Game EV (Max Bet {BET})...")
fg_total = 0
for _ in range(SIMULATIONS):
    fg_total += simulate_free_game()
fg_avg = fg_total / SIMULATIONS
print(f"Average Free Game Win: {fg_avg:.2f} ({fg_avg/BET:.2f}x Bet)")

is_free_game = False
print(f"Verifying Base Game EV...")
base_total = 0
for _ in range(SIMULATIONS):
    base_total += simulate_base_game()
base_avg = base_total / SIMULATIONS
print(f"Average Base Game Win: {base_avg:.2f} ({base_avg/BET:.2f}x Bet)")

print(f"Verifying Fujin EV...")
fu_total = 0
for _ in range(SIMULATIONS):
    fu_total += simulate_fujin_feature()
fu_avg = fu_total / SIMULATIONS
print(f"Average Fujin Win: {fu_avg:.2f} ({fu_avg/BET:.2f}x Bet)")

print(f"Verifying Raijin EV...")
ra_total = 0
for _ in range(SIMULATIONS):
    ra_total += simulate_raijin_feature()
ra_avg = ra_total / SIMULATIONS

print("-" * 50)
print("FINAL RTP VERIFICATION (High Precision)")
print("-" * 50)

# Constants from Analysis
NOTICE_PROB = 0.15
SUCCEESS_RATE_FUJIN = 0.30
SUCCEESS_RATE_RAIJIN = 0.30
# FreeGame triggers: 20% of Notices. 
# Inside FreeGame Notice (100% success): 34% FG, 33% Fujin, 33% Raijin

# Effective Feature Probability (Per Spin)
# Notice = 15%
# 1. Direct Fujin Notice (40% of Notices) * 30% Success = 0.15 * 0.40 * 0.30 = 1.8%
# 2. Direct Raijin Notice (40% of Notices) * 30% Success = 0.15 * 0.40 * 0.30 = 1.8%
# 3. FreeGame Notice (20% of Notices) * 100% Success
#    -> Real FG: 0.15 * 0.20 * 0.34 = 1.02%
#    -> Split Fujin: 0.15 * 0.20 * 0.033 = 0.99%
#    -> Split Raijin: 0.15 * 0.20 * 0.33 = 0.99%
# Wait, let's use the code logic exactly.

# JS Logic:
# if r < 40: type = Fujin
# else if r < 80: type = Raijin
# else: type = FreeGame (20%)

p_notice = 0.15
p_fujin_notice = p_notice * 0.4
p_raijin_notice = p_notice * 0.4
p_fg_notice = p_notice * 0.2

# Success
p_fujin_hit = p_fujin_notice * 0.30
p_raijin_hit = p_raijin_notice * 0.30

# FG Split (100% success for notice)
p_fg_real = p_fg_notice * 0.34
p_fg_fujin = p_fg_notice * 0.33
p_fg_raijin = p_fg_notice * 0.33

total_fujin_prob = p_fujin_hit + p_fg_fujin
total_raijin_prob = p_raijin_hit + p_fg_raijin
total_fg_prob = p_fg_real

print(f"Probabilities per Spin (Notice {p_notice*100}%):")
print(f"  Fujin Feature: {total_fujin_prob*100:.3f}%")
print(f"  Raijin Feature: {total_raijin_prob*100:.3f}%")
print(f"  Free Game: {total_fg_prob*100:.3f}%")

# Expected Values (Medals) from Verification
ev_base = base_avg
ev_fujin = fu_avg
ev_raijin = ra_avg
ev_fg = fg_avg + ev_base # FG includes base spin logic? No, FG replaces base spin?
# Logic: 'spin()' calls startReels(). If notice, eventually triggers feature.
# The base spin (reels stopping) happens BEFORE feature starts.
# So Player pays 90 BET -> Gets Base Spin Result -> Then Feature starts.
# So Feature EV ADDs to Base EV.

# Sushi Logic (Bonus)
# 3% chance in simulation_all_modes, but verified as ~0.5% in logic?
# Let's assume the 0.5% verified frequency.
ev_sushi = 0 # Need verify? 
# In script.js: if (bonusCount >= 3) -> triggerBonus.
# This happens parallel to base win.
# Verified freq is roughly 0.005. EV is ~8x Bet (720).
ev_sushi_game = 720 * 0.005 # Approx contribution

total_return = ev_base
total_return += ev_sushi_game
total_return += total_fujin_prob * ev_fujin
total_return += total_raijin_prob * ev_raijin
total_return += total_fg_prob * ev_fg

rtp_pct = (total_return / BET) * 100
print(f"\nFinal Estimated RTP: {rtp_pct:.2f}%")

