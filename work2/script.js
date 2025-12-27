/**
 * 風雷神風スロットゲーム
 */

const SYMBOL_WIDTH = 150;
const SYMBOL_HEIGHT = 150;
const REEL_COUNT = 5;
const ROW_COUNT = 3;

// Feature Constants
const FEATURE_RAIJIN = 'RAIJIN';
const FEATURE_FUJIN = 'FUJIN';

// Symbols definitions
const SYMBOLS = [
    // ID 0 (WILD) Removed
    { id: 1, name: 'FUJIN', value: 1000 },
    { id: 2, name: 'RAIJIN', value: 1000 },
    { id: 3, name: 'OIRAN', value: 500 },
    { id: 4, name: 'FAN', value: 200 },
    { id: 5, name: 'DRUM', value: 150 },
    { id: 6, name: 'A', value: 50 },
    { id: 7, name: 'K', value: 40 },
    { id: 8, name: 'Q', value: 30 },
    { id: 9, name: 'J', value: 20 },
    { id: 10, name: '10', value: 10 },
    { id: 11, name: 'BONUS', value: 0 },
    { id: 12, name: 'FUJIN_WILD', value: 0 }, // New
    { id: 13, name: 'RAIJIN_WILD', value: 0 }, // New
    { id: 14, name: 'DARUMA', value: 200 }     // New Daruma (Same as Fan)
];

const SYMBOL_WEIGHTS_LUCKY = [
    { id: 1, weight: 550 }, { id: 2, weight: 550 }, { id: 3, weight: 200 },
    { id: 4, weight: 1000 }, { id: 5, weight: 1000 }, { id: 6, weight: 1200 },
    { id: 7, weight: 1200 }, { id: 8, weight: 1200 }, { id: 9, weight: 1200 },
    { id: 10, weight: 1200 }, { id: 11, weight: 300 }, { id: 14, weight: 1000 }
];

const SYMBOL_WEIGHTS_NORMAL = [
    { id: 1, weight: 500 }, { id: 2, weight: 500 }, { id: 3, weight: 180 },
    { id: 4, weight: 950 }, { id: 5, weight: 950 }, { id: 6, weight: 1250 },
    { id: 7, weight: 1250 }, { id: 8, weight: 1250 }, { id: 9, weight: 1250 },
    { id: 10, weight: 1250 }, { id: 11, weight: 300 }, { id: 14, weight: 950 }
];

const SYMBOL_WEIGHTS_TIGHT = [
    { id: 1, weight: 450 }, { id: 2, weight: 450 }, { id: 3, weight: 150 },
    { id: 4, weight: 900 }, { id: 5, weight: 900 }, { id: 6, weight: 1300 },
    { id: 7, weight: 1300 }, { id: 8, weight: 1300 }, { id: 9, weight: 1300 },
    { id: 10, weight: 1300 }, { id: 11, weight: 300 }, { id: 14, weight: 900 }
];

const MODE_CONFIG = {
    0: { // DEBUG MODE
        name: 'DEBUG (Mode 0)',
        noticeProb: 1.0, // Keep 100% for verification convenience
        raijinProbs: [ // Synchronized with Normal
            { id: 9, p: 35.0 }, { id: 8, p: 30.0 }, { id: 7, p: 15.4 }, { id: 6, p: 10.0 },
            { id: 4, p: 2.5 }, { id: 14, p: 2.5 }, { id: 5, p: 2.0 }, { id: 2, p: 1.5 }, { id: 1, p: 1.0 }, { id: 3, p: 0.1 }
        ],
        weights: SYMBOL_WEIGHTS_NORMAL
    },
    1: { // Lucky (RTP < 80%)
        name: 'LUCKY',
        noticeProb: 0.06,
        raijinProbs: [
            { id: 9, p: 27.3 }, { id: 8, p: 23.0 }, { id: 7, p: 20.0 }, { id: 6, p: 13.0 },
            { id: 4, p: 4.0 }, { id: 14, p: 4.0 }, { id: 5, p: 3.5 }, { id: 2, p: 3.0 }, { id: 1, p: 2.0 }, { id: 3, p: 0.2 }
        ],
        weights: SYMBOL_WEIGHTS_LUCKY
    },
    2: { // Normal (80% <= RTP <= 115%)
        name: 'NORMAL',
        noticeProb: 0.06,
        raijinProbs: [
            { id: 9, p: 35.0 }, { id: 8, p: 30.0 }, { id: 7, p: 15.4 }, { id: 6, p: 10.0 },
            { id: 4, p: 2.5 }, { id: 14, p: 2.5 }, { id: 5, p: 2.0 }, { id: 2, p: 1.5 }, { id: 1, p: 1.0 }, { id: 3, p: 0.1 }
        ],
        weights: SYMBOL_WEIGHTS_NORMAL
    },
    3: { // Tight (RTP > 115%)
        name: 'TIGHT',
        noticeProb: 0.06,
        raijinProbs: [
            { id: 9, p: 35.0 }, { id: 8, p: 30.0 }, { id: 7, p: 15.5 }, { id: 6, p: 15.0 },
            { id: 4, p: 2.0 }, { id: 14, p: 2.0 }, { id: 5, p: 0.4 }, { id: 2, p: 0.1 }, { id: 1, p: 0.0 }, { id: 3, p: 0.0 }
        ],
        weights: SYMBOL_WEIGHTS_TIGHT
    }
};

const PAYLINES = [
    [{ c: 0, r: 1 }, { c: 1, r: 1 }, { c: 2, r: 1 }, { c: 3, r: 1 }, { c: 4, r: 1 }],
    [{ c: 0, r: 0 }, { c: 1, r: 0 }, { c: 2, r: 0 }, { c: 3, r: 0 }, { c: 4, r: 0 }],
    [{ c: 0, r: 2 }, { c: 1, r: 2 }, { c: 2, r: 2 }, { c: 3, r: 2 }, { c: 4, r: 2 }],
    [{ c: 0, r: 0 }, { c: 1, r: 1 }, { c: 2, r: 2 }, { c: 3, r: 1 }, { c: 4, r: 0 }],
    [{ c: 0, r: 2 }, { c: 1, r: 1 }, { c: 2, r: 0 }, { c: 3, r: 1 }, { c: 4, r: 2 }],
    [{ c: 0, r: 0 }, { c: 1, r: 0 }, { c: 2, r: 1 }, { c: 3, r: 2 }, { c: 4, r: 2 }],
    [{ c: 0, r: 2 }, { c: 1, r: 2 }, { c: 2, r: 1 }, { c: 3, r: 0 }, { c: 4, r: 0 }],
    [{ c: 0, r: 1 }, { c: 1, r: 2 }, { c: 2, r: 2 }, { c: 3, r: 2 }, { c: 4, r: 1 }],
    [{ c: 0, r: 1 }, { c: 1, r: 0 }, { c: 2, r: 0 }, { c: 3, r: 0 }, { c: 4, r: 1 }],
    [{ c: 0, r: 0 }, { c: 0, r: 1 }, { c: 0, r: 2 }],
    [{ c: 1, r: 0 }, { c: 1, r: 1 }, { c: 1, r: 2 }],
    [{ c: 2, r: 0 }, { c: 2, r: 1 }, { c: 2, r: 2 }],
    [{ c: 3, r: 0 }, { c: 3, r: 1 }, { c: 3, r: 2 }],
    [{ c: 4, r: 0 }, { c: 4, r: 1 }, { c: 4, r: 2 }]
];

class Game {
    constructor() {
        this.canvas = document.getElementById('slot-screen');
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;

        this.credit = 5000;
        this.bet = 0;
        this.maxBet = 90;
        this.isPlaying = false;
        this.winningLines = [];

        this.totalIn = 0;
        this.totalOut = 0;
        this.rtp = 0;
        this.lastAddedWinIndex = -1;
        this.pendingGodFeature = null; // null, 'RAIJIN', 'FUJIN', 'FREEGAME'

        // Free Game State
        this.inFreeGame = false;
        this.freeSpinsLeft = 0;
        this.freeGameTotalWin = 0;
        this.freeGameRound = 1; // Track continuation rounds (1-4+)
        this.normalSpinWin = 0; // Store normal spin payout before Free Game starts

        this.bgm = document.getElementById('bgm');
        this.bgmFreeGame = document.getElementById('bgm-freegame');
        this.seStop = document.getElementById('se-stop');
        this.seWin = document.getElementById('se-win');
        this.seThunder = document.getElementById('se-thunder');
        this.seUpgrade = document.getElementById('se-upgrade');
        this.seWind = document.getElementById('se-wind');
        this.seRaijinCutin = document.getElementById('se-raijin-cutin');
        this.seFujinCutin = document.getElementById('se-fujin-cutin');
        this.currentMode = 2; // Default to Normal (Mode 2)

        // Rolling RTP tracking (last 100 spins)
        this.historyIn = [];
        this.historyOut = [];
        this.spinCount = 0; // Total spin counter
        this.bonusEffects = []; // { c, r, type: 'light', startTime, life: 500 }
        this.sushiSymbolCount = 0;

        this.reels = [];
        this.assets = {
            symbols: new Image(),
            bg: new Image(),
            fujinWild: new Image(),
            raijinWild: new Image(),
            fujinWildTall: new Image(),
            raijinWildTall: new Image()
        };

        let loaded = 0;
        const totalAssets = 6; // Increased to 6
        const onLoad = () => {
            loaded++;
            if (loaded === totalAssets) {
                this.init();
            }
        };

        this.assets.symbols.src = "assets/symbols.png";
        this.assets.symbols.onload = onLoad;
        this.assets.symbols.onerror = (e) => console.error("Symbol image load failed", e);

        this.assets.bg.src = "assets/bg.png";
        this.assets.bg.onload = onLoad;

        this.assets.fujinWild.src = "assets/fujin_wild.png";
        this.assets.fujinWild.onload = onLoad;

        this.assets.raijinWild.src = "assets/raijin_wild.png";
        this.assets.raijinWild.onload = onLoad;

        this.assets.fujinWildTall.src = "assets/fujin_wild_tall.png";
        this.assets.fujinWildTall.onload = onLoad;

        this.assets.raijinWildTall.src = "assets/raijin_wild_tall.png";
        this.assets.raijinWildTall.onload = onLoad;
    }

    init() {
        const reelWidth = SYMBOL_WIDTH;
        const totalReelWidth = reelWidth * REEL_COUNT;
        const startX = (this.width - totalReelWidth) / 2;
        const mainHeight = ROW_COUNT * SYMBOL_HEIGHT;
        const startY = (this.height - mainHeight) / 2;

        for (let i = 0; i < REEL_COUNT; i++) {
            this.reels.push(new Reel(i, startX + i * reelWidth, startY, reelWidth, mainHeight));
        }

        this.eventListeners();
        this.updateUI();
        // Start Main Loop
        this.loop();
    }

    loop() {
        this.update();
        this.draw();
        requestAnimationFrame(() => this.loop());
    }

    update() {
        if (this.isWinAnimating && this.winningLines.length > 0) {
            // 現在のアニメーション対象（同一ラインIdxのグループ）の賞金を一括加算
            if (this.winAnimIndex > this.lastAddedWinIndex) {
                let groupTotal = 0;
                let lastIdxInGroup = this.winAnimIndex;
                const currentLineIdx = this.winningLines[this.winAnimIndex].lineIdx;

                // 現在のグループ（同じlineIdxの連続する要素）をすべて合算
                for (let i = this.winAnimIndex; i < this.winningLines.length; i++) {
                    if (this.winningLines[i].lineIdx === currentLineIdx) {
                        groupTotal += this.winningLines[i].amount;
                        lastIdxInGroup = i;
                    } else {
                        break;
                    }
                }

                this.displayedWin += groupTotal;
                this.lastAddedWinIndex = lastIdxInGroup; // グループの最後まで加算済みとする
                this.updateUI();

                // Play Sound for Symbol Zoom (勝利演出専用の効果音)
                if (this.seWin) {
                    this.seWin.currentTime = 0;
                    this.seWin.play().catch(e => { });
                }
            }

            const now = Date.now();
            const dt = now - this.lastFrameTime;
            this.lastFrameTime = now;

            // 各ラインのアニメーション時間（0.6秒 + 0.3秒の間隔）
            this.winAnimProgress += dt / 600;
            if (this.winAnimProgress >= 1.5) {
                this.winAnimProgress = 0;
                const currentLineIdx = this.winningLines[this.winAnimIndex].lineIdx;
                // Skip all contiguous wins for the SAME lineIdx to progress to next distinct line
                while (this.winAnimIndex < this.winningLines.length &&
                    this.winningLines[this.winAnimIndex].lineIdx === currentLineIdx) {
                    this.winAnimIndex++;
                }

                if (this.winAnimIndex >= this.winningLines.length) {
                    this.stopWinAnimation();
                    this.onWinAnimationComplete();
                }
            }
        }

        // Update Bonus Effects
        const now = Date.now();
        this.bonusEffects = this.bonusEffects.filter(e => now - e.startTime < e.life);
    }

    eventListeners() {
        document.getElementById('btn-spin').addEventListener('click', () => this.spin());
        document.getElementById('btn-bet1').addEventListener('click', () => this.addBet(1));
        document.getElementById('btn-bet-max').addEventListener('click', () => this.addBet(90));
        document.getElementById('btn-auto').addEventListener('click', () => this.toggleAuto());
        document.getElementById('btn-help').addEventListener('click', () => {
            document.getElementById('help-overlay').classList.remove('hidden');
        });
        document.getElementById('btn-help-return').addEventListener('click', () => {
            document.getElementById('help-overlay').classList.add('hidden');
        });
        // document.getElementById('btn-debug').addEventListener('click', () => this.toggleDebugMode());
    }

    addBet(amount) {
        if (this.isPlaying) return;
        let newBet = this.bet + amount;
        if (amount === 90) newBet = this.maxBet;
        if (newBet > this.maxBet) newBet = this.maxBet;
        if (newBet > this.credit) newBet = this.credit;
        this.bet = newBet;
        this.updateUI();
    }

    toggleDebugMode() {
        this.isDebugMode = !this.isDebugMode;
        const btn = document.getElementById('btn-debug');

        // --- Reset Stats & Credit (User Request) ---
        this.credit = 5000;
        this.totalIn = 0;
        this.totalOut = 0;
        this.rtp = 0;

        if (this.isDebugMode) {
            this.currentMode = 0; // Force Mode 0
            btn.classList.add('active');
            console.log("DEBUG MODE ON: Switched to Mode 0 (Stats Reset)");
        } else {
            this.currentMode = 2; // Reset to Normal
            btn.classList.remove('active');
            console.log("DEBUG MODE OFF: Resumed Normal Mode (Stats Reset)");
        }

        this.updateUI();
        // Explicitly update stat displays
        document.getElementById('stat-in').innerText = this.totalIn;
        document.getElementById('stat-out').innerText = this.totalOut;
        document.getElementById('stat-rtp').innerText = this.rtp.toFixed(2) + "%";
    }

    toggleAuto() {
        this.isAutoMode = !this.isAutoMode;
        const btn = document.getElementById('btn-auto');
        if (this.isAutoMode) {
            btn.innerText = "AUTO STOP";
            btn.classList.add('active');
            if (!this.isPlaying && this.credit > 0) {
                console.log("toggleAuto: Starting immediate spin");
                this.spin();
            }
        } else {
            console.log("Auto Stop Requested");
            btn.innerText = "AUTO ON";
            btn.classList.remove('active');
        }
    }

    spin() {
        console.log("spin() called. isPlaying:", this.isPlaying, "bet:", this.bet, "credit:", this.credit, "Auto:", this.isAutoMode);
        if (this.isPlaying || this.bet === 0) {
            console.log("spin() aborted. isPlaying:", this.isPlaying, "bet:", this.bet);
            return;
        }
        this.inFreeGame = false;
        this.credit -= this.bet;
        this.totalIn += this.bet;
        this.displayedWin = 0;
        this.isPlaying = true;
        this.winningLines = [];
        this.pendingGodFeature = null;

        if (this.totalIn > 0) {
            this.rtp = (this.totalOut / this.totalIn) * 100;
        }

        // --- RTP Mode Switching Logic (Rolling 100-spin) ---
        // Mode 1 (Lucky): Rolling RTP < 80%
        // Mode 2 (Normal): 80% <= Rolling RTP <= 115%
        // Mode 3 (Tight): Rolling RTP > 115%

        if (!this.isDebugMode && this.historyIn.length > 0) {
            const recentIn = this.historyIn.reduce((a, b) => a + b, 0);
            const recentOut = this.historyOut.reduce((a, b) => a + b, 0);
            const rollingRTP = recentIn > 0 ? (recentOut / recentIn) * 100 : 100;

            if (rollingRTP < 80.0) {
                this.currentMode = 1;
            } else if (rollingRTP > 115.0) {
                this.currentMode = 3;
            } else {
                this.currentMode = 2;
            }
        }

        // Increment spin counter
        this.spinCount++;

        // Calculate rolling RTP for display
        const rollingRTP = this.historyIn.length > 0
            ? (this.historyOut.reduce((a, b) => a + b, 0) / this.historyIn.reduce((a, b) => a + b, 0)) * 100
            : 100;

        console.log(`Spin: ${this.spinCount} | Cumulative RTP: ${this.rtp.toFixed(2)}% | Rolling RTP (${this.historyIn.length}G): ${rollingRTP.toFixed(2)}% | Mode: ${MODE_CONFIG[this.currentMode].name}`);

        document.getElementById('message-content').innerText = "";
        document.getElementById('message-overlay').classList.add('hidden');
        document.getElementById('bonus-overlay').classList.add('hidden');
        document.getElementById('notice-overlay').classList.add('hidden');
        document.getElementById('notice-lightning').classList.add('hidden');
        document.getElementById('notice-tornado').classList.add('hidden');
        this.updateUI();

        if (this.bgm) {
            this.bgm.play().catch(e => console.log("Audio play failed", e));
        }

        // Logic: God Feature Notice
        const modeConfig = MODE_CONFIG[this.currentMode];
        const isNotice = Math.random() < modeConfig.noticeProb;
        let noticeType = null;

        if (isNotice) {
            // Same distribution for all modes
            // Fujin: 40%, Raijin: 40%, FreeGame: 20%
            const r = Math.random() * 100;
            if (r < 40) noticeType = FEATURE_FUJIN;
            else if (r < 80) noticeType = FEATURE_RAIJIN;
            else noticeType = 'FREEGAME';

            // Success Logic - Same for all modes
            if (noticeType === 'FREEGAME') {
                // FreeGame notice: 100% success, but splits into 3 outcomes
                const split = Math.random() * 100;
                if (split < 34) {
                    this.pendingGodFeature = 'FREEGAME';  // 34%
                } else if (split < 67) {
                    this.pendingGodFeature = FEATURE_FUJIN;  // 33%
                } else {
                    this.pendingGodFeature = FEATURE_RAIJIN; // 33%
                }
            } else {
                // Fujin/Raijin notice: 30% success rate in all modes
                if (Math.random() < 0.30) {
                    this.pendingGodFeature = noticeType;
                }
            }
        }

        const startReels = () => {
            this.reels.forEach(reel => reel.startSpin());

            let resultGrid = [];

            for (let i = 0; i < REEL_COUNT; i++) {
                const reelSymbols = [];
                for (let r = 0; r < ROW_COUNT; r++) {
                    const sym = this.getRandomSymbol();
                    reelSymbols.push(sym);
                }
                resultGrid.push(reelSymbols);
            }

            let stopDelay = 400;
            this.reels.forEach((reel, index) => {
                setTimeout(() => {
                    reel.stopSpin(resultGrid[index]);

                    if (this.seStop) {
                        this.seStop.currentTime = 0;
                        this.seStop.play().catch(e => { });
                    }

                    if (index === REEL_COUNT - 1) {
                        setTimeout(() => {
                            if (this.bgm) this.bgm.pause();
                            this.checkWin(resultGrid);
                        }, 500);
                    }
                }, 800 + (index * stopDelay));
            });
        };

        if (noticeType) {
            // Show Notice Effect
            const overlay = document.getElementById('notice-overlay');
            const lightning = document.getElementById('notice-lightning');
            const tornado = document.getElementById('notice-tornado');

            overlay.classList.remove('hidden');
            lightning.classList.add('hidden');
            tornado.classList.add('hidden');

            if (noticeType === FEATURE_RAIJIN) {
                lightning.classList.remove('hidden');
                if (this.seThunder) { this.seThunder.currentTime = 0; this.seThunder.play().catch(e => { }); }
            } else if (noticeType === FEATURE_FUJIN) {
                tornado.classList.remove('hidden');
                if (this.seWind) { this.seWind.currentTime = 0; this.seWind.play().catch(e => { }); }
                setTimeout(() => { if (this.seWind) { this.seWind.pause(); } }, 1500);
            } else if (noticeType === 'FREEGAME') {
                // Simultaneous Effect
                lightning.classList.remove('hidden');
                tornado.classList.remove('hidden');
                // Play BOTH sounds
                if (this.seThunder) { this.seThunder.currentTime = 0; this.seThunder.play().catch(e => { }); }
                if (this.seWind) { this.seWind.currentTime = 0; this.seWind.play().catch(e => { }); }
                setTimeout(() => { if (this.seWind) { this.seWind.pause(); } }, 2500);
            }

            // Animation Reset
            [lightning, tornado].forEach(el => {
                el.style.animation = 'none';
                el.offsetHeight;
                el.style.animation = null;
            });

            // Wait for anim then start logic
            const waitTime = (noticeType === 'FREEGAME') ? 2500 : 1800;
            setTimeout(() => {
                document.getElementById('notice-overlay').classList.add('hidden');
                // CRITICAL CHANGE: Always start normal reels
                // Free Game will start later from callback after normal spin completes
                startReels();
            }, waitTime);

        } else {
            startReels();
        }
    }



    startFreeGame() {
        console.log("STARTING FREE GAME");
        this.inFreeGame = true;
        this.freeSpinsLeft = 5;
        this.freeGameTotalWin = 0;
        this.freeGameRound = 1; // Initialize to Round 1
        this.pendingGodFeature = null; // Bugfix: Clear pending flag so checkWin doesn't re-trigger

        // Switch BGM to Free Game BGM
        if (this.bgm) {
            this.bgm.pause();
        }
        if (this.bgmFreeGame) {
            this.bgmFreeGame.currentTime = 0;
            this.bgmFreeGame.play().catch(e => { console.log('Free Game BGM play failed', e); });
        }

        // Show Free Game UI
        document.getElementById('free-game-counter').classList.remove('hidden');
        this.updateUI(); // Ensure initial state

        // Force update Reel 0 and Reel 4 visuals to Empty/Wild immediately
        // so old symbols don't show underneath.
        // Reel 0 = Raijin (13) [Left], Reel 4 = Fujin (12) [Right]
        const reel0Syms = [SYMBOLS.find(s => s.id === 13), SYMBOLS.find(s => s.id === 13), SYMBOLS.find(s => s.id === 13)];
        const reel4Syms = [SYMBOLS.find(s => s.id === 12), SYMBOLS.find(s => s.id === 12), SYMBOLS.find(s => s.id === 12)];

        // Ensure symbols are found
        if (!reel0Syms[0]) console.error("Symbol 12 not found!");
        if (!reel4Syms[0]) console.error("Symbol 13 not found!");

        this.reels[0].stopSpin(reel0Syms);
        this.reels[4].stopSpin(reel4Syms);

        // Start first spin
        setTimeout(() => this.spinFreeGame(), 1000);
    }

    spinFreeGame() {
        if (this.freeSpinsLeft <= 0) {
            // Check for continuation based on current round
            let continueChance = 0;
            if (this.freeGameRound === 1) continueChance = 0.40; // 40%
            else if (this.freeGameRound === 2) continueChance = 0.20; // 20%
            else if (this.freeGameRound === 3) continueChance = 0.10; // 10%
            // Round 4+: 0% (no continuation)

            if (continueChance > 0 && Math.random() < continueChance) {
                // CONTINUE! Add 5 more spins
                this.freeSpinsLeft = 5;
                this.freeGameRound++;
                console.log(`FREE GAME CONTINUE! Round ${this.freeGameRound} started`);

                // Play thunder sound effect
                if (this.seThunder) {
                    this.seThunder.currentTime = 0;
                    this.seThunder.play().catch(e => { });
                }

                // Spin counter will automatically update below
                // Continue spinning (fall through to normal spin logic)
            } else {
                // End Free Game
                this.endFreeGame();
                return;
            }
        }

        this.freeSpinsLeft--;
        document.getElementById('free-spins-num').innerText = this.freeSpinsLeft;
        this.updateUI();

        // Start Reels - Only middle 3 reels (1, 2, 3). Reels 0 and 4 are fixed wilds.
        for (let i = 1; i <= 3; i++) {
            this.reels[i].startSpin();
        }

        setTimeout(() => this.stopFreeGameReels(), 1000); // Faster spin
    }

    stopFreeGameReels() {
        // Grid Generation: Col 0 and 4 are FORCE FILLED with OIRAN (ID 3 - Wild)
        // Grid Generation:
        // Col 0 -> Fujin Wild (12), Col 4 -> Raijin Wild (13)
        const grid = [];
        for (let i = 0; i < REEL_COUNT; i++) {
            const col = [];
            for (let j = 0; j < ROW_COUNT; j++) {
                if (i === 0) {
                    col.push(SYMBOLS.find(s => s.id === 13)); // Left: Raijin
                } else if (i === 4) {
                    col.push(SYMBOLS.find(s => s.id === 12)); // Right: Fujin
                } else {
                    col.push(this.getRandomSymbol());
                }
            }
            grid.push(col);
        }

        // Stop Visuals - Sequential, only middle 3 reels (1, 2, 3)
        // Reels 0 and 4 stay fixed as wilds throughout Free Game
        let stopDelay = 400;
        let stoppedCount = 0;

        for (let i = 1; i <= 3; i++) {
            setTimeout(() => {
                this.reels[i].stopSpin(grid[i]);

                // Play stop sound only for middle reels
                if (this.seStop) {
                    this.seStop.currentTime = 0;
                    this.seStop.play().catch(e => { });
                }

                stoppedCount++;
                // After last middle reel stops (reel 3), calculate win
                if (stoppedCount === 3) {
                    setTimeout(() => this.processFreeGameWin(grid), 300);
                }
            }, (i - 1) * stopDelay); // Offset by (i-1) so reel 1 = 0ms, reel 2 = 400ms, reel 3 = 800ms
        }
    }

    processFreeGameWin(grid) {
        // Calculate Win
        const winAmount = this.checkWin(grid, true);

        if (winAmount > 0) {
            this.freeGameTotalWin += winAmount;
            this.displayedWin = this.freeGameTotalWin;
            this.updateUI();

            if (this.seWin) {
                this.seWin.currentTime = 0;
                this.seWin.play().catch(e => { });
            }
        }

        // Wait for Animation (Polling) - CRITICAL FIX
        const waitForAnim = () => {
            if (this.isWinAnimating) {
                console.log("FreeGame: Waiting for animation, isWinAnimating=true");
                requestAnimationFrame(waitForAnim);
            } else {
                console.log("FreeGame: Animation complete, proceeding to next spin");
                // Extra safety delay after animation completes
                setTimeout(() => {
                    this.stopWinAnimation(); // Ensure clean state
                    this.spinFreeGame();
                }, 500);
            }
        };

        if (winAmount > 0) {
            console.log(`FreeGame: Win detected (${winAmount}), starting polling`);
            waitForAnim();
        } else {
            console.log("FreeGame: No win, next spin after short delay");
            setTimeout(() => this.spinFreeGame(), 800);
        }
    }

    endFreeGame() {
        // this.inFreeGame = false; // MOVED to spin() start to keep visuals visible after game ends
        document.getElementById('free-game-counter').classList.add('hidden');

        // Combine normal spin payout + Free Game payout
        const combinedWin = this.normalSpinWin + this.freeGameTotalWin;
        console.log(`End FG: Normal=${this.normalSpinWin}, FG=${this.freeGameTotalWin}, Combined=${combinedWin}`);

        // Payout to Credit
        this.credit += combinedWin;
        this.totalOut += combinedWin;

        // Reset for next time
        this.normalSpinWin = 0;

        // Message (Use overlay instead of blocking alert)
        document.getElementById('message-content').innerHTML = `FREE GAME FINISHED!<br><span style='font-size:1.5rem'>Total Win: ${combinedWin}</span>`;
        document.getElementById('message-overlay').classList.remove('hidden');

        // Clear message after delay or on click
        setTimeout(() => {
            document.getElementById('message-overlay').classList.add('hidden');
        }, 3000);
        document.getElementById('message-overlay').onclick = () => {
            document.getElementById('message-overlay').classList.add('hidden');
            document.getElementById('message-overlay').onclick = null;
        };

        // Restore normal BGM
        if (this.bgmFreeGame) {
            this.bgmFreeGame.pause();
        }
        if (this.bgm) {
            this.bgm.play().catch(e => { console.log('Normal BGM play failed', e); });
        }

        // CRITICAL: Reset all state flags to allow normal spin
        this.isPlaying = false;
        this.displayedWin = 0;
        this.winningLines = [];
        this.isWinAnimating = false;
        this.winCallback = null;
        this.pendingGodFeature = null;

        this.updateUI();

        // AUTO MODE: Continue spinning after message clears if auto is enabled
        if (this.isAutoMode && this.credit > 0) {
            console.log("endFreeGame: Auto mode enabled, scheduling next spin");
            setTimeout(() => {
                if (this.isAutoMode && this.credit > 0 && !this.isPlaying) {
                    this.spin();
                }
            }, 3500); // After message auto-closes (3000ms) + small delay
        }
    }

    getRandomSymbol() {
        const modeConfig = MODE_CONFIG[this.currentMode];
        const weights = modeConfig.weights;
        const totalWeight = weights.reduce((acc, item) => acc + item.weight, 0);
        let rand = Math.floor(Math.random() * totalWeight);

        for (let i = 0; i < weights.length; i++) {
            if (rand < weights[i].weight) {
                return SYMBOLS.find(s => s.id === weights[i].id);
            }
            rand -= weights[i].weight;
        }
        return SYMBOLS[10];
    }

    calculateLineMultiplier(lineSymbols, lineIdx) {
        const PAYOUTS = {
            3: { 5: 2500, 4: 1000, 3: 100, 2: 10, v3: 10 },
            1: { 5: 250, 4: 150, 3: 50, 2: 5, v3: 5 },
            2: { 5: 150, 4: 100, 3: 30, 2: 3, v3: 4 },
            5: { 5: 100, 4: 50, 3: 20, 2: 2, v3: 3 },
            4: { 5: 75, 4: 30, 3: 10, v3: 2 },
            6: { 5: 50, 4: 20, 3: 5, v3: 1 },
            7: { 5: 50, 4: 20, 3: 5, v3: 1 },
            8: { 5: 25, 4: 10, 3: 5, v3: 1 },
            9: { 5: 25, 4: 10, 3: 5, v3: 1 },
            10: { 5: 25, 4: 10, 3: 5, v3: 1 },
            14: { 5: 75, 4: 30, 3: 10, v3: 2 }
        };

        // Logic A: Natural Win
        let countA = 0;
        const firstId = lineSymbols[0].id;
        for (let i = 0; i < lineSymbols.length; i++) {
            if (lineSymbols[i].id === firstId) countA++;
            else break;
        }

        let multiplierA = 0;
        const tableA = PAYOUTS[firstId];
        if (lineIdx >= 9) {
            if (countA === 3 && tableA && tableA.v3 !== undefined) {
                multiplierA = tableA.v3;
            }
        } else {
            if (tableA && tableA[countA]) multiplierA = tableA[countA];
        }

        // Logic B: Wild Win
        let countB = 0;
        let targetId = -1;

        for (let s of lineSymbols) {
            if (s.id !== 3 && s.id !== 12 && s.id !== 13) {
                targetId = s.id;
                break;
            }
        }

        let multiplierB = 0;
        if (targetId !== -1) {
            for (let i = 0; i < lineSymbols.length; i++) {
                const id = lineSymbols[i].id;
                if (id === targetId || id === 3 || id === 12 || id === 13) countB++;
                else break;
            }

            const tableB = PAYOUTS[targetId];
            if (lineIdx >= 9) {
                if (countB === 3 && tableB && tableB.v3 !== undefined) {
                    multiplierB = tableB.v3;
                }
            } else {
                if (tableB && tableB[countB]) multiplierB = tableB[countB];
            }
        }

        const bestMultiplier = Math.max(multiplierA, multiplierB);
        const bestCount = multiplierA >= multiplierB ? countA : countB;

        return { multiplier: bestMultiplier, count: bestCount };
    }

    checkWin(grid, isFreeGame = false) {
        let totalWin = 0;
        this.winningLines = [];

        const stdBetPerLine = Math.max(1, Math.floor(this.bet / 9));

        PAYLINES.forEach((line, lineIdx) => {
            // Free Game Rule: Vertical Lines on Reel 0 (Idx 9) and Reel 4 (Idx 13) are INVALID
            if (isFreeGame) {
                if (lineIdx === 9 || lineIdx === 13) return;
            }

            const lineSymbols = line.map(pos => grid[pos.c][pos.r]);

            // Calculate Left-to-Right
            const resultLR = this.calculateLineMultiplier(lineSymbols, lineIdx);

            // Calculate Right-to-Left (Horizontal/Diagonal only)
            let resultRL = { multiplier: 0, count: 0 };
            if (lineIdx < 9) {
                // STRICT: Skip R-L if L-R is already a 5-match
                if (resultLR.count < 5) {
                    const reversedSymbols = [...lineSymbols].reverse();
                    resultRL = this.calculateLineMultiplier(reversedSymbols, lineIdx);
                }
            }

            // Calculate wins
            let currentLineBet = (lineIdx >= 9) ? this.bet : stdBetPerLine;
            if (this.bet === 0) currentLineBet = 0;

            // Add L-R win
            if (resultLR.multiplier > 0) {
                const lineWin = resultLR.multiplier * currentLineBet;
                totalWin += lineWin;
                this.winningLines.push({ lineIdx, count: resultLR.count, amount: lineWin, isReversed: false });
            }

            // Add R-L win
            if (resultRL.multiplier > 0) {
                const lineWin = resultRL.multiplier * currentLineBet;
                totalWin += lineWin;
                this.winningLines.push({ lineIdx, count: resultRL.count, amount: lineWin, isReversed: true });
            }
        });

        // SORT Winning Lines: Group by lineIdx, then by amount
        this.winningLines.sort((a, b) => {
            if (a.lineIdx !== b.lineIdx) return a.lineIdx - b.lineIdx;
            return a.amount - b.amount;
        });

        let bonusCount = 0;
        grid.flat().forEach(s => { if (s.id === 11) bonusCount++; });
        this.sushiSymbolCount = bonusCount; // Capture for Payout Bonus


        // Removed random God trigger (Math.random < 0.03) as per new requirement

        const lockedFeatureType = this.pendingGodFeature;
        const nextStep = lockedFeatureType ? () => {
            // Use locally captured type, as this.pendingGodFeature will be null by now
            this.triggerGodFeature(grid, lockedFeatureType);
        } : null;

        // Clear pending flag immediately (but keep reference in nextStep callback)
        if (this.pendingGodFeature) this.pendingGodFeature = null;

        if (bonusCount >= 3) {
            // Pass nextStep callback to bonus game so God Feature triggers after
            setTimeout(() => this.triggerBonus(nextStep), 1000);
        } else {
            // If Free Game, we handle flow in stopFreeGameReels, BUT we want animation.
            // processWin triggers animation AND finishRound.
            // We want animation but NOT finishRound (credit add).

            if (isFreeGame) {
                // Manually trigger animation logic without the full processWin callback chain
                if (totalWin > 0) {
                    this.displayedWin = totalWin; // Update display context for this spin
                    this.updateUI();
                    this.startWinAnimation();
                    // finishRound is SKIPPED here. Logic handled in waitForAnimationEnd in stopFreeGameReels.
                }
            } else {
                // CRITICAL: If Free Game is pending, save normal spin payout
                if (lockedFeatureType === 'FREEGAME') {
                    this.normalSpinWin = totalWin;
                    console.log(`Normal spin before FG: ${totalWin} saved`);
                }
                this.processWin(totalWin, nextStep);
            }
        }

        return totalWin; // MUST return for Free Game accumulator
    }

    triggerGodFeature(currentGrid, type) {
        // Handle Free Game - no god overlay, just start directly
        if (type === 'FREEGAME') {
            console.log("triggerGodFeature: Starting Free Game");
            this.startFreeGame();
            return;
        }

        // type is FEATURE_RAIJIN or FEATURE_FUJIN
        const overlay = document.getElementById('god-overlay');
        const img = document.getElementById('god-img');

        overlay.classList.remove('hidden');
        if (type === FEATURE_RAIJIN) {
            img.src = "assets/raijin_god.png";
            if (this.seRaijinCutin) {
                this.seRaijinCutin.currentTime = 0;
                this.seRaijinCutin.play().catch(e => { });
            }
        } else if (type === FEATURE_FUJIN) {
            img.src = "assets/fujin_god.png";
            if (this.seFujinCutin) {
                this.seFujinCutin.currentTime = 0;
                this.seFujinCutin.play().catch(e => { });
            }
        } else {
            // Unknown type - do not show overlay or trigger logic
            overlay.classList.add('hidden');
            return;
        }

        // Trigger reflow for animation
        img.style.animation = 'none';
        img.offsetHeight;
        img.style.animation = null;

        // Wait for descent animation (e.g., 2s), then effect
        setTimeout(() => {
            overlay.classList.add('hidden');

            if (type === FEATURE_RAIJIN) {
                // Raijin Logic: Symbol Upgrade
                this.performSymbolUpgrade(currentGrid, () => {
                    this.pendingGodFeature = null;
                    this.checkWin(currentGrid);
                });
            } else {
                // Fujin Logic: Single Line Win (Sequential)
                const lineIdx = Math.floor(Math.random() * 9); // Horizontal 0-8 (9-13 vertical excluded)
                const lineDef = PAYLINES[lineIdx];

                // Weighted Selection for Win Symbol (IDs 1-10)
                // Oiran(3): 0.5%, Red Fuji(1): 1.5%, Helmet(2): 3%
                // Drum(5): 5%, Fan(4): 10%
                // A(6)-10(10): 16% each (Total 80%)
                const fujinWeights = [
                    { id: 3, p: 0.5 },
                    { id: 1, p: 1.5 },
                    { id: 2, p: 3.0 },
                    { id: 5, p: 5.0 },
                    { id: 4, p: 10.0 },
                    { id: 14, p: 10.0 },
                    { id: 6, p: 16.0 },
                    { id: 7, p: 16.0 },
                    { id: 8, p: 16.0 },
                    { id: 9, p: 16.0 },
                    { id: 10, p: 16.0 }
                ];

                const rVal = Math.random() * 100;
                let acc = 0;
                let winSymId = 10;
                for (let w of fujinWeights) {
                    acc += w.p;
                    if (rVal < acc) {
                        winSymId = w.id;
                        break;
                    }
                }
                const winSym = SYMBOLS.find(s => s.id === winSymId);

                let step = 0;
                const processNext = () => {
                    if (step < lineDef.length) {
                        const pos = lineDef[step];
                        currentGrid[pos.c][pos.r] = winSym;
                        this.reels[pos.c].stopSpin(currentGrid[pos.c]);

                        // Tornado Effect
                        this.bonusEffects.push({ c: pos.c, r: pos.r, type: 'tornado', startTime: Date.now(), life: 600 });

                        // Stop Cutin SE at first change
                        if (step === 0) {
                            if (this.seFujinCutin) { this.seFujinCutin.pause(); this.seFujinCutin.currentTime = 0; }
                        }

                        // Play Sound (Same as Raijin Upgrade)
                        if (this.seUpgrade) {
                            this.seUpgrade.currentTime = 0;
                            this.seUpgrade.play().catch(e => { });
                        }

                        step++;
                        setTimeout(processNext, 300); // Fast speed (300ms)
                    } else {
                        // Finished
                        setTimeout(() => {
                            this.pendingGodFeature = null; // Clear flag
                            this.checkWin(currentGrid); // Re-check
                        }, 500);
                    }
                };
                processNext();
            }
        }, 2000);
    }

    performSymbolUpgrade(grid, callback) {
        // Define Upgrade Path (Order of IDs)
        const pathIds = [10, 9, 8, 7, 6, 4, 14, 5, 2, 1, 3];
        // 10->J->Q->K->A->Fan->Daruma->Drum->Helmet->RedFuji->Oiran
        // 10->J->Q->K->A->Fan->Drum->Helmet->RedFuji->Oiran

        // Define Final Destination Probabilities
        // Use Mode Config
        const modeConfig = MODE_CONFIG[this.currentMode];
        const probabilities = modeConfig.raijinProbs;

        // 1. Determine Final Destination
        const r = Math.random() * 100;
        let cumulative = 0;
        let finalId = 9; // Default fallback (J)

        for (let p of probabilities) {
            cumulative += p.p; // config uses 'p' NOT 'percent'
            if (r < cumulative) {
                finalId = p.id;
                break;
            }
        }

        // 2. Build Execution Steps
        // Find index of finalId in pathIds
        const maxIndex = pathIds.indexOf(finalId);
        // Start from index 0 (ID 10) up to maxIndex
        // The loop will go from i=0 to maxIndex-1, converting pathIds[i] to pathIds[i+1]

        const steps = [];
        for (let i = 0; i < maxIndex; i++) {
            steps.push({
                target: pathIds[i],
                next: pathIds[i + 1],
                delay: 1500 // Adjust delay curve if needed
            });
        }

        const upgradeStep = (targetId, nextId, delay) => {
            return new Promise((resolve) => {
                setTimeout(() => {
                    let changed = false;
                    for (let c = 0; c < REEL_COUNT; c++) {
                        for (let r = 0; r < ROW_COUNT; r++) {
                            if (grid[c][r].id === targetId) {
                                grid[c][r] = SYMBOLS.find(s => s.id === nextId);
                                changed = true;
                                // Lightning Effect
                                this.bonusEffects.push({ c, r, type: 'lightning', startTime: Date.now(), life: 600 });
                            }
                        }
                    }
                    if (changed) {
                        // Stop Cutin SE at the moment of transformation
                        if (this.seRaijinCutin) { this.seRaijinCutin.pause(); this.seRaijinCutin.currentTime = 0; }

                        this.reels.forEach((reel, c) => reel.stopSpin(grid[c]));
                        // Play Upgrade Sound
                        if (this.seUpgrade) {
                            this.seUpgrade.currentTime = 0;
                            this.seUpgrade.play().catch(e => { });
                        }
                    }
                    resolve(changed);
                }, delay);
            });
        };

        (async () => {
            // Execute the determined path
            for (let step of steps) {
                await upgradeStep(step.target, step.next, step.delay);
            }
            setTimeout(callback, 1000);
        })();
    }

    processWin(winAmount, callback) {
        console.log("processWin called. Amount:", winAmount, "Callback present:", !!callback);
        this.winCallback = callback;

        if (winAmount > 0) {
            // Do NOT reset displayedWin here, to allow accumulation from Round 1 + Round 2
            // this.displayedWin = 0; 
            this.updateUI();

            // Start Win Animation
            this.startWinAnimation();

            // Skip animation handler
            this.canvas.onclick = () => {
                if (this.isWinAnimating) {
                    this.skipWinAnimation();
                }
            };
        } else {
            if (this.winCallback) {
                const cb = this.winCallback;
                this.winCallback = null;
                cb();
            } else {
                this.finishRound();
            }
        }
    }

    startWinAnimation() {
        this.isWinAnimating = true;
        this.winAnimIndex = 0;
        this.winAnimProgress = 0;
        this.lastFrameTime = Date.now();
        this.lastAddedWinIndex = -1;
    }

    stopWinAnimation() {
        this.isWinAnimating = false;
        this.canvas.onclick = null;
    }

    skipWinAnimation() {
        this.stopWinAnimation();
        // Calculate remaining win and add
        // We only add what has NOT been added yet
        const remaining = this.winningLines.slice(this.lastAddedWinIndex + 1).reduce((acc, l) => acc + l.amount, 0);
        this.displayedWin += remaining;
        this.updateUI();
        this.onWinAnimationComplete();
    }

    onWinAnimationComplete() {
        // CRITICAL: Skip this logic entirely if we're in Free Game
        // Free Game handles its own flow via waitForAnim polling
        if (this.inFreeGame) {
            console.log("onWinAnimationComplete: Skipped (inFreeGame)");
            return;
        }

        if (this.winCallback) {
            const cb = this.winCallback;
            this.winCallback = null;
            // Short delay before triggering next feature?
            setTimeout(cb, 500);
        } else {
            this.finishRound();
        }
    }

    finishRound() {
        console.log("finishRound called");
        // Wait a moment to show final win, then transfer
        setTimeout(() => {
            if (this.displayedWin > 0) {
                this.credit += this.displayedWin;
                this.totalOut += this.displayedWin;
                // Keep displayedWin visible until next spin
                this.updateUI();
            }

            // Update rolling RTP history (AFTER displayedWin is finalized)
            this.historyIn.push(90);
            this.historyOut.push(this.displayedWin);
            if (this.historyIn.length > 100) {
                this.historyIn.shift();
                this.historyOut.shift();
            }

            this.isPlaying = false;
            this.updateUI();

            if (this.credit <= 0) {
                document.getElementById('message-content').innerHTML = "GAME OVER<br><span style='font-size:1rem'>Click to Reset</span>";
                document.getElementById('message-overlay').classList.remove('hidden');
                document.getElementById('message-overlay').onclick = () => {
                    this.resetGame();
                };
            }

            // AUTO PLAY TRIGGER
            if (this.isAutoMode && this.credit > 0) {
                console.log("finishRound: Auto Triggering next spin");
                setTimeout(() => this.spin(), 500);
            } else if (this.isAutoMode && this.credit <= 0) {
                // Stop Auto if no credit
                this.toggleAuto();
            }

        }, 1200);
    }

    resetGame() {
        this.credit = 5000;
        this.bet = 0;
        document.getElementById('message-overlay').classList.add('hidden');
        document.getElementById('message-overlay').onclick = null;
        this.updateUI();
    }

    triggerBonus(godFeatureCallback = null) {
        document.getElementById('bonus-overlay').classList.remove('hidden');
        document.getElementById('bonus-result').innerText = '';

        // Init Bonus State
        this.sushiRound = 1;
        this.bonusTotalWin = 0;
        this.bonusGodFeatureCallback = godFeatureCallback; // Store for later execution

        // Ensure BGM is playing (User report: it stops)
        if (this.bgm) {
            this.bgm.play().catch(e => { console.log('BGM play failed', e); });
        }

        this.startSushiRound();
    }

    startSushiRound() {
        const container = document.getElementById('sushi-container');
        container.innerHTML = '';
        document.querySelector('#bonus-overlay h2').innerText = `寿司ボーナス - Round ${this.sushiRound}`;
        document.querySelector('#bonus-overlay p').innerText = `あと3枚 選んでください`;

        this.sushiRoundPicks = 0;
        this.sushiPickedIndices = [];
        this.sushiQualifiedIndices = [];

        // Determine Qualified Plates (Hits)
        let qualifiedCount = 0;
        if (this.sushiRound === 1) qualifiedCount = 3;
        else if (this.sushiRound === 2) qualifiedCount = 2;
        else if (this.sushiRound === 3 || this.sushiRound === 4) qualifiedCount = 1;
        else qualifiedCount = 0; // Round 5 (Final)

        // Randomize sushi types for plates
        const sushiTypes = ['maguro', 'salmon', 'ebi', 'tamago', 'hamachi', 'ika', 'anago', 'ikura', 'uni'];
        const currentTypes = [...sushiTypes].sort(() => Math.random() - 0.5);

        // Randomly select indices for Qualified
        const indices = [0, 1, 2, 3, 4, 5, 6, 7, 8];
        for (let i = 0; i < qualifiedCount; i++) {
            const r = Math.floor(Math.random() * indices.length);
            this.sushiQualifiedIndices.push(indices.splice(r, 1)[0]);
        }

        // Create Plates
        for (let i = 0; i < 9; i++) {
            const plate = document.createElement('div');
            plate.className = 'sushi-plate';
            plate.dataset.index = i;
            plate.onclick = () => this.onSushiPick(i, plate);

            // Add Sushi Visuals (2 pieces)
            const type = currentTypes[i];
            const wrapper = document.createElement('div');
            wrapper.className = `sushi-item-wrapper ${type}`;
            for (let p = 1; p <= 2; p++) {
                const piece = document.createElement('div');
                piece.className = `sushi-piece p${p}`;
                if (type === 'ikura' || type === 'uni') {
                    piece.innerHTML = `<div class="gunkan-nori"><div class="gunkan-top"></div></div>`;
                } else {
                    piece.innerHTML = `<div class="topping"></div><div class="rice"></div>`;
                }
                wrapper.appendChild(piece);
            }
            plate.appendChild(wrapper);
            container.appendChild(plate);
        }

        // AUTO PLAY - Start Picking
        if (this.isAutoMode) {
            setTimeout(() => this.autoPickSushi(), 1000);
        }
    }

    autoPickSushi() {
        if (!this.isAutoMode) return;
        // Find unpicked plates
        const plates = document.getElementsByClassName('sushi-plate');
        const availablepoint = [];
        for (let i = 0; i < plates.length; i++) {
            // Check if not opened
            if (!plates[i].classList.contains('opened')) {
                availablepoint.push(i);
            }
        }

        if (availablepoint.length > 0 && this.sushiRoundPicks < 3) {
            const r = Math.floor(Math.random() * availablepoint.length);
            const pickedIndex = availablepoint[r];
            this.onSushiPick(pickedIndex, plates[pickedIndex]);
        }
    }

    onSushiPick(index, element) {
        if (element.classList.contains('opened') || this.sushiRoundPicks >= 3) return;

        element.classList.add('opened');
        this.sushiRoundPicks++;
        this.sushiPickedIndices.push(index);

        // Update Instruction text
        const remaining = 3 - this.sushiRoundPicks;
        if (remaining > 0) {
            document.querySelector('#bonus-overlay p').innerText = `あと${remaining}枚 選んでください`;
        } else {
            document.querySelector('#bonus-overlay p').innerText = `判定中...`;
        }

        // PRIZE LOGIC (Scale with Bet)
        // Expected Value target: ~8x Bet
        let multipliers = [];
        if (this.sushiRound === 1) multipliers = [0.5, 0.75, 1.0];
        else if (this.sushiRound === 2) multipliers = [0.8, 1.2, 1.6];
        else if (this.sushiRound === 3) multipliers = [1.0, 1.5, 2.0];
        else if (this.sushiRound === 4) multipliers = [2.0, 3.0, 4.0];
        else multipliers = [5.0, 10.0, 15.0]; // Round 5

        const mult = multipliers[Math.floor(Math.random() * multipliers.length)];

        // Apply Symbol Count Bonus: (Count - 3) * 30%
        const countBonus = 1 + Math.max(0, (this.sushiSymbolCount - 3) * 0.3);
        const val = Math.floor(this.bet * mult * countBonus);

        let content = document.createElement('div');
        content.className = 'sushi-content';
        content.innerText = val;
        this.bonusTotalWin += val;

        element.appendChild(content);

        document.getElementById('bonus-result').innerText = `Total: ${this.bonusTotalWin}`;

        // Check End of Round
        if (this.sushiRoundPicks >= 3) {
            setTimeout(() => this.resolveSushiRound(), 1000);
        } else {
            // Continue Auto Picking
            if (this.isAutoMode) {
                setTimeout(() => this.autoPickSushi(), 800);
            }
        }
    }

    resolveSushiRound() {
        const plates = document.getElementsByClassName('sushi-plate');

        // Reveal Qualified Plates
        let passed = false;

        // Round 5 is Final, automtically "Pass" (or rather, Finish Successfully)
        if (this.sushiRound === 5) {
            // Just Finish
            passed = true;
        } else {
            // Check matches
            let hitCount = 0;
            for (let idx of this.sushiQualifiedIndices) {
                const p = plates[idx];
                p.classList.add('reveal-qualified'); // Visual style needed
                // If user picked this index
                if (this.sushiPickedIndices.includes(idx)) {
                    hitCount++;
                    p.style.border = "5px solid #ffeb3b"; // Highlight hit
                }

                // Show "Qualified" Tag on ALL qualified plates
                let tag = document.createElement('div');
                tag.className = 'qualified-tag';
                tag.innerText = "合格";
                p.appendChild(tag);
            }

            // (Removed redundant second loop as all qualified plates are handled above)

            passed = (hitCount > 0);

            passed = (hitCount > 0);
        }

        setTimeout(() => {
            if (passed) {
                if (this.sushiRound < 5) {
                    document.querySelector('#bonus-overlay p').innerText = "合格！ 次のラウンドへ";
                    setTimeout(() => {
                        this.sushiRound++;
                        this.startSushiRound();
                    }, 2000);
                } else {
                    // Round 5 Finish
                    document.querySelector('#bonus-overlay p').innerText = "完全制覇！ おめでとう！";
                    document.getElementById('bonus-result').innerText = `FINAL WIN: ${this.bonusTotalWin}`;
                    setTimeout(() => this.endBonus(), 3000);
                }
            } else {
                // Failed
                document.querySelector('#bonus-overlay p').innerText = "残念... 不合格";
                document.getElementById('bonus-result').innerText = `WIN: ${this.bonusTotalWin}`;
                setTimeout(() => this.endBonus(), 3000);
            }
        }, 1000);
    }

    endBonus() {
        this.displayedWin = this.bonusTotalWin;
        document.getElementById('bonus-overlay').classList.add('hidden');

        // Stop BGM (User Request)
        if (this.bgm) {
            this.bgm.pause();
            this.bgm.currentTime = 0;
        }

        // Check if God Feature callback exists (from pending notice before bonus)
        if (this.bonusGodFeatureCallback) {
            const callback = this.bonusGodFeatureCallback;
            this.bonusGodFeatureCallback = null; // Clear

            // Process bonus win first, then trigger God Feature
            this.processWin(0, callback); // Pass callback as nextStep
        } else {
            this.processWin(0);
        }
    }

    updateUI() {
        document.getElementById('credit-display').innerText = this.credit;
        document.getElementById('bet-display').innerText = this.bet;
        document.getElementById('win-display').innerText = this.displayedWin;
        document.getElementById('stat-in').innerText = this.totalIn;
        document.getElementById('stat-out').innerText = this.totalOut;
        const rtp = this.totalIn > 0 ? ((this.totalOut / this.totalIn) * 100).toFixed(1) : 0;
        document.getElementById('stat-rtp').innerText = rtp + "%";
        document.getElementById('btn-spin').disabled = this.isPlaying || this.bet === 0;
        document.getElementById('btn-bet1').disabled = this.isPlaying;
        document.getElementById('btn-bet-max').disabled = this.isPlaying;
    }

    draw() {
        this.ctx.clearRect(0, 0, this.width, this.height);

        // --- DRAW BACKGROUND ---
        if (this.assets.bg.complete) {
            this.ctx.drawImage(this.assets.bg, 0, 0, this.width, this.height);
        }

        this.reels.forEach(reel => reel.draw(this.ctx, this.assets, this.inFreeGame));

        // --- FULL REEL WILD OVERLAY (FREE GAME) ---
        if (this.inFreeGame) {
            const reelWidth = SYMBOL_WIDTH;
            const startX = (this.width - (reelWidth * REEL_COUNT)) / 2;
            const mainHeight = ROW_COUNT * SYMBOL_HEIGHT;
            const startY = (this.height - mainHeight) / 2;

            // Reel 0 (Left): Raijin (Red).
            if (this.assets.raijinWildTall && this.assets.raijinWildTall.complete) {
                this.ctx.drawImage(this.assets.raijinWildTall, startX, startY, reelWidth, mainHeight);
            }

            // Reel 4 (Right): Fujin (Green).
            if (this.assets.fujinWildTall && this.assets.fujinWildTall.complete) {
                this.ctx.drawImage(this.assets.fujinWildTall, startX + 4 * reelWidth, startY, reelWidth, mainHeight);
            }
        }

        // --- BONUS EFFECTS (LIGHTNING / TORNADO) ---
        const bonusNow = Date.now();
        const bReelWidth = SYMBOL_WIDTH;
        const bStartX = (this.width - (bReelWidth * REEL_COUNT)) / 2;
        const bStartY = (this.height - (ROW_COUNT * SYMBOL_HEIGHT)) / 2;

        this.bonusEffects.forEach(e => {
            const x = bStartX + (e.c * bReelWidth);
            const y = bStartY + (e.r * SYMBOL_HEIGHT);
            const progress = (bonusNow - e.startTime) / e.life;
            const alpha = 1 - progress;

            this.ctx.save();
            // --- CLIP TO CELL BOUNDS ---
            this.ctx.beginPath();
            this.ctx.rect(x, y, bReelWidth, SYMBOL_HEIGHT);
            this.ctx.clip();

            this.ctx.globalAlpha = alpha;

            if (e.type === 'lightning') {
                // Intense Lightning Effect
                this.ctx.strokeStyle = '#fff';
                this.ctx.lineWidth = 3 + Math.random() * 5;
                this.ctx.shadowBlur = 20;
                this.ctx.shadowColor = '#0ff';

                const centerX = x + bReelWidth / 2;
                this.ctx.beginPath();
                this.ctx.moveTo(centerX + (Math.random() - 0.5) * 50, y - 100);
                this.ctx.lineTo(centerX + (Math.random() - 0.5) * 30, y + SYMBOL_HEIGHT * 0.3);
                this.ctx.lineTo(centerX + (Math.random() - 0.5) * 60, y + SYMBOL_HEIGHT * 0.6);
                this.ctx.lineTo(centerX + (Math.random() - 0.5) * 20, y + SYMBOL_HEIGHT + 50);
                this.ctx.stroke();

                // Bright Flash at the center
                this.ctx.fillStyle = '#fff';
                this.ctx.globalAlpha = alpha * 0.5;
                this.ctx.beginPath();
                this.ctx.arc(centerX, y + SYMBOL_HEIGHT / 2, SYMBOL_WIDTH * 0.4, 0, Math.PI * 2);
                this.ctx.fill();
            } else if (e.type === 'tornado') {
                // Powerful Tornado Effect
                this.ctx.strokeStyle = '#fff';
                this.ctx.lineWidth = 2;
                this.ctx.shadowBlur = 15;
                this.ctx.shadowColor = '#fff';

                const centerX = x + bReelWidth / 2;
                const bottomY = y + SYMBOL_HEIGHT;

                // Increase spiral density and thickness
                for (let i = 0; i < 25; i++) {
                    const h = (i / 25) * SYMBOL_HEIGHT * 1.5;
                    const r = (SYMBOL_WIDTH * 0.7) * (i / 25) * (1.2 + Math.sin(bonusNow / 30 + i));
                    const spiralY = bottomY - h;

                    this.ctx.beginPath();
                    this.ctx.lineWidth = 3; // Thicker lines
                    this.ctx.ellipse(centerX, spiralY, r, r / 4, Math.sin(bonusNow / 60 + i), 0, Math.PI * 2);
                    this.ctx.stroke();
                }

                // More and larger wind particles
                this.ctx.fillStyle = '#fff';
                for (let p = 0; p < 15; p++) {
                    const px = centerX + (Math.random() - 0.5) * SYMBOL_WIDTH * 1.2;
                    const py = y + (Math.random() - 0.2) * SYMBOL_HEIGHT * 1.2;
                    this.ctx.fillRect(px, py, 4, 4); // Larger particles
                }

                // Add thicker vertical wind streaks
                this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)'; // Higher opacity
                for (let s = 0; s < 8; s++) {
                    const sx = centerX + (Math.random() - 0.5) * SYMBOL_WIDTH;
                    this.ctx.beginPath();
                    this.ctx.lineWidth = 4; // Thicker streaks
                    this.ctx.moveTo(sx, y + SYMBOL_HEIGHT);
                    this.ctx.lineTo(sx + (Math.random() - 0.5) * 20, y - 20);
                    this.ctx.stroke();
                }
            }
            this.ctx.restore();
        });

        // Draw Winning Lines (アニメーション中はシンボル拡大+個別ライン、終了後にライン一括表示)
        if (this.winningLines && this.winningLines.length > 0 && this.isWinAnimating) {
            const reelWidth = SYMBOL_WIDTH;
            const startX = (this.width - (reelWidth * REEL_COUNT)) / 2;
            const mainHeight = ROW_COUNT * SYMBOL_HEIGHT;
            const startY = (this.height - mainHeight) / 2;

            // シンボル拡大エフェクト（現在のラインのシンボルのみ表示）
            this.ctx.save();
            let scale = 1.2;
            // アニメーション全体の1.5の進行度のうち、1.0を超えたら（最後の0.5秒間）サイズを元に戻す
            if (this.winAnimProgress > 1.0) {
                scale = 1.0;
            }

            // 現在アニメーション中のラインのシンボルのみ拡大
            const baseWin = this.winningLines[this.winAnimIndex];
            if (baseWin) {
                const lineGroup = this.winningLines.filter(w => w.lineIdx === baseWin.lineIdx);
                const lineDef = PAYLINES[baseWin.lineIdx];

                let allSymbolsToEnlarge = new Set();
                lineGroup.forEach(win => {
                    const symbols = win.isReversed ? lineDef.slice(-win.count) : lineDef.slice(0, win.count);
                    symbols.forEach(pos => allSymbolsToEnlarge.add(pos));
                });

                allSymbolsToEnlarge.forEach(pos => {


                    const reel = this.reels[pos.c];
                    const sym = reel.viewSymbols[pos.r];
                    if (sym) {
                        const x = startX + (pos.c * reelWidth);
                        const y = startY + (pos.r * SYMBOL_HEIGHT);

                        // Draw centered and scaled
                        const centerX = x + reelWidth / 2;
                        const centerY = y + SYMBOL_HEIGHT / 2;

                        this.ctx.translate(centerX, centerY);
                        this.ctx.scale(scale, scale);
                        this.ctx.translate(-centerX, -centerY);

                        const drawW = 130;
                        const drawH = 130;
                        const dx = x + (SYMBOL_WIDTH - drawW) / 2;
                        const dy = y + (SYMBOL_HEIGHT - drawH) / 2;

                        let img = null;
                        let isSpecial = false;

                        if (sym.id === 12 || sym.id === 13) {
                            // SKIP drawing enlarged Wilds because they are full-reel overlays
                            img = null;
                            isSpecial = false;
                        } else if ((sym.id >= 0 && sym.id <= 11) || sym.id === 14) {
                            img = this.assets.symbols;
                            isSpecial = false;
                        }

                        if (img && img.complete) {
                            if (isSpecial) {
                                this.ctx.drawImage(img, 0, 0, 150, 150, dx, dy, drawW, drawH);
                            } else {
                                this.ctx.drawImage(img, 462, sym.id * 85, 100, 85, dx, dy, drawW, drawH);
                            }
                        }

                        this.ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset transform
                    }
                });
            }
            this.ctx.restore();

            // 現在のラインエフェクト（拡大シンボルの上に描画）
            if (baseWin) {
                this.ctx.save();
                this.ctx.lineWidth = 8;
                this.ctx.lineCap = 'round';
                this.ctx.shadowBlur = 15;
                this.ctx.shadowColor = 'white';

                const lineDef = PAYLINES[baseWin.lineIdx];
                this.ctx.strokeStyle = "gold";
                this.ctx.beginPath();
                this.ctx.lineWidth = 5;
                lineDef.forEach((pos, idx) => {
                    const x = startX + (pos.c * reelWidth) + (reelWidth / 2);
                    const y = startY + (pos.r * SYMBOL_HEIGHT) + (SYMBOL_HEIGHT / 2);
                    if (idx === 0) this.ctx.moveTo(x, y);
                    else this.ctx.lineTo(x, y);
                });
                this.ctx.stroke();
                this.ctx.restore();
            }
        } else if (this.winningLines && this.winningLines.length > 0 && !this.isPlaying) {
            // Static draw if not animating (e.g. skipped)
            this.ctx.save();
            this.ctx.lineWidth = 8;
            this.ctx.lineCap = 'round';
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = 'white';
            const reelWidth = SYMBOL_WIDTH;
            const startX = (this.width - (reelWidth * REEL_COUNT)) / 2;
            const mainHeight = ROW_COUNT * SYMBOL_HEIGHT;
            const startY = (this.height - mainHeight) / 2;

            this.winningLines.forEach(win => {
                const lineDef = PAYLINES[win.lineIdx];
                this.ctx.strokeStyle = "gold";
                this.ctx.beginPath();
                this.ctx.lineWidth = 5;
                lineDef.forEach((pos, idx) => {
                    const x = startX + (pos.c * reelWidth) + (reelWidth / 2);
                    const y = startY + (pos.r * SYMBOL_HEIGHT) + (SYMBOL_HEIGHT / 2);
                    if (idx === 0) this.ctx.moveTo(x, y);
                    else this.ctx.lineTo(x, y);
                });
                this.ctx.stroke();
            });
            this.ctx.restore();
        }

        // Draw Line Bet indicators
        if (this.bet > 0) {
            this.ctx.save();
            this.ctx.fillStyle = 'rgba(255, 215, 0, 0.8)';
            this.ctx.font = 'bold 20px "Sawarabi Mincho"';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.shadowColor = 'black';
            this.ctx.shadowBlur = 4;
            this.ctx.lineWidth = 3;
            this.ctx.strokeStyle = 'black';

            const reelWidth = SYMBOL_WIDTH;
            const startX = (this.width - (reelWidth * REEL_COUNT)) / 2;
            const mainHeight = ROW_COUNT * SYMBOL_HEIGHT;
            const startY = (this.height - mainHeight) / 2;

            const stdBet = Math.max(1, Math.floor(this.bet / 9));
            const vertBet = this.bet;

            // Draw Standard Bet (Sides)
            // Left and Right of rows
            for (let r = 0; r < ROW_COUNT; r++) {
                const y = startY + (r * SYMBOL_HEIGHT) + (SYMBOL_HEIGHT / 2);
                const leftX = startX - 30;
                const rightX = startX + (REEL_COUNT * reelWidth) + 30;

                this.ctx.strokeText(stdBet, leftX, y);
                this.ctx.fillText(stdBet, leftX, y);

                this.ctx.strokeText(stdBet, rightX, y);
                this.ctx.fillText(stdBet, rightX, y);
            }

            // Draw Vertical Bet (Top)
            for (let c = 0; c < REEL_COUNT; c++) {
                const x = startX + (c * reelWidth) + (reelWidth / 2);
                const topY = startY - 30;

                this.ctx.strokeText(vertBet, x, topY);
                this.ctx.fillText(vertBet, x, topY);
            }
            this.ctx.restore();
        }

        // Loop requestAnimation handled by loop()
    }
}

class Reel {
    constructor(id, x, y, width, height) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.isSpinning = false;
        this.speed = 0;
        this.viewSymbols = [SYMBOLS[6], SYMBOLS[7], SYMBOLS[8]];
        this.neighbors = [SYMBOLS[10], SYMBOLS[9]];
        this.offsetY = 0;
    }

    startSpin() {
        this.isSpinning = true;
        this.speed = 30 + Math.random() * 10;
        this.offsetY = 0;
    }

    stopSpin(resultSymbols) {
        this.isSpinning = false;
        this.viewSymbols = resultSymbols;
        const randSym = () => {
            const validIndices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13]; // IDs 1-11 and 14 (Index 13)
            return SYMBOLS[validIndices[Math.floor(Math.random() * validIndices.length)]];
        };
        this.neighbors = [randSym(), randSym()];
        this.offsetY = 0;
    }

    // Updated to accept 'assets' object and 'inFreeGame' flag
    draw(ctx, assets, inFreeGame) {
        ctx.strokeStyle = '#daa520';
        ctx.lineWidth = 4;
        ctx.strokeRect(this.x, this.y, this.width, this.height);
        ctx.fillStyle = 'rgba(0,0,0,0.8)';
        ctx.fillRect(this.x, this.y, this.width, this.height);

        // Suppress symbol drawing for Reel 0 and 4 in Free Game
        if (inFreeGame && (this.id === 0 || this.id === 4)) {
            // Draw nothing inside (just black background), overlay will cover it
            return;
        }

        const clipPad = 10;
        ctx.save();
        ctx.beginPath();
        ctx.rect(this.x, this.y - clipPad, this.width, this.height + clipPad * 2);
        ctx.clip();

        if (this.isSpinning) {
            this.offsetY += this.speed;
            if (this.offsetY >= SYMBOL_HEIGHT) this.offsetY -= SYMBOL_HEIGHT;
            for (let i = -1; i < 4; i++) {
                const validIds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14];
                const randSymId = validIds[Math.floor(Math.random() * validIds.length)];
                this.drawSymbol(ctx, assets, randSymId, this.x, this.y + (i * SYMBOL_HEIGHT) + this.offsetY);
            }
        } else {
            this.drawSymbol(ctx, assets, this.neighbors[0].id, this.x, this.y - SYMBOL_HEIGHT);
            for (let i = 0; i < 3; i++) {
                this.drawSymbol(ctx, assets, this.viewSymbols[i].id, this.x, this.y + i * SYMBOL_HEIGHT);
            }
            this.drawSymbol(ctx, assets, this.neighbors[1].id, this.x, this.y + 3 * SYMBOL_HEIGHT);
        }
        ctx.restore();
    }

    drawSymbol(ctx, assets, symbolId, x, y) {
        // Skip drawing for Fujin Wild (12) and Raijin Wild (13) inside the reel script
        // because they are drawn as full-reel overlays in Game.draw during Free Game.
        if (symbolId === 12 || symbolId === 13) return;

        let img = assets.symbols;
        // Logic for other special symbols if any, currently simple

        if (img && img.complete) {
            const drawW = 130;
            const drawH = 130;
            const dx = x + (SYMBOL_WIDTH - drawW) / 2;
            const dy = y + (SYMBOL_HEIGHT - drawH) / 2;

            if ((symbolId >= 1 && symbolId <= 11) || symbolId === 14) {
                // Existing spritesheet logic (ID 1-11) + Daruma (ID 14)
                ctx.drawImage(img, 462, symbolId * 85, 100, 85, dx, dy, drawW, drawH);
            }
        } else {
            ctx.fillStyle = '#333';
            ctx.fillRect(x, y, SYMBOL_WIDTH, SYMBOL_HEIGHT);
            ctx.fillStyle = '#fff';
            ctx.font = '30px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            let name = "SYM " + symbolId;
            if (symbolId < SYMBOLS.length) name = SYMBOLS[symbolId].name;
            ctx.fillText(name, x + SYMBOL_WIDTH / 2, y + SYMBOL_HEIGHT / 2);
        }
    }
}

window.onload = () => { new Game(); };
