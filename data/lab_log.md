# Lab log (research lab; never changes live rules)

## 2026-11-05 - 52-week-high momentum continuation (web idea)
Source: https://quantpedia.com/strategies/52-weeks-high-effect-in-stocks , https://www.r-bloggers.com/2017/05/trading-strategy-52-weeks-high-effect-in-stocks/ (George & Hwang 52-week-high effect; published as monthly cross-sectional, so this is an unverified daily-bar translation).
Rules: long when close > highest close of prior 252 days (variant: within 2%), close > SMA50 > SMA200, SPY > 200d, ATR/price < 6%, 10-day cooldown per symbol, enter at close (+0.05% slip), fixed hold N days, stop k ATR, no other exit. Rank by 63-day return. Same portfolio simulator as the champion (10% x 12 pos, 4/day). Script: lab_52wh.py. 7 variants tried (multiple-comparison discount applies; no year selection was needed since nothing passed).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/0.14/1.39/1.57/1.24/1.45 |
| new high, hold 10, stop 4 | 1042 | 51.2 | 1.14 | 33.3 | 19.8 | 247 / 1.19 | 1.11/0.49/1.12/1.32/1.42/1.03 |
| new high, hold 20 | 623 | 48.6 | 1.18 | 35.8 | 16.6 | 141 / 1.48 | 0.89/0.65/1.25/1.38/1.07/1.43 |
| new high, hold 5 | 1485 | 50.0 | 0.99 | -3.8 | 20.1 | 351 / 0.83 | - |
| new high + vol>1.5x avg, hold 10 | 628 | 54.1 | 1.31 | 53.1 | 14.9 | 148 / 1.08 | 1.83/0.57/1.04/1.77/1.55/1.03 |
| within 2% of high, hold 10 | 1202 | 51.8 | 1.16 | 47.7 | 15.2 | 270 / 1.14 | 1.35/0.87/0.85/1.30/1.42/1.09 |
| new high, hold 10, stop 6 | 1026 | 50.8 | 1.14 | 32.5 | 21.8 | 243 / 1.25 | - |
| new high, exit close<MA10 (hold 20) | 1889 | 49.4 | 0.93 | -9.7 | 12.2 | 428 / 0.89 | - |
| Champion + (vol>1.5x, hold 10) combined | 1175 | 59.6 | 1.34 | 87.5 | 14.0 | 273 / 1.26 | 1.72/0.37/1.26/1.59/1.58/1.16 |

Verdict: NOT a promotion candidate. Breakout continuation is far weaker than mean reversion on win rate (50-54% vs 66%), drawdown 15-20% vs 6%, and fails 2022 and the last 12 months. The volume-confirmed version (PF 1.31) is the only one of interest; it fades in 2023, 2026 and L12 (PF 1.03-1.08), and the combined portfolio's higher return comes with 2x the drawdown (the combined sim shares the same 12 slots, so it is not a clean diversification test). Not added to challenger.py. Possible follow-up: test volume-confirmed breakout only as a separate sleeve with its own slots, and correlation of monthly returns with the champion.

## 2026-11-05 (run 2) - turn-of-month calendar filter on champion entries (web idea)
Source: https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes , https://quantpedia.com/an-examination-of-the-turn-of-the-month-effect/ (published on index returns, not on mean-reversion entries; unverified translation).
Rules: take the champion's own trade list (A+E+F, SPY>200d, hold 7, stop 4 ATR) and keep only entries by calendar position (trading-day index from month start / to month end), then re-run the same portfolio simulator (10% x 12, 4/day). Script: lab_tom.py. 5 variants (multiple-comparison discount applies; no year selection needed since nothing passed).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| TOM window (last 2 + first 3 days) | 193 | 62.2 | 1.60 | 13.6 | 4.8 | 49 / 1.45 | 2.75/.06/.85/3.32/1.82/1.38 |
| NOT TOM window | 600 | 67.2 | 1.39 | 27.4 | 7.7 | 129 / 1.63 | 1.77/.24/1.54/1.30/1.15/1.59 |
| first half of month | 374 | 65.0 | 1.42 | 18.6 | 4.0 | 86 / 1.49 | 2.46/.15/1.28/1.22/2.28/1.42 |
| second half of month | 408 | 67.4 | 1.41 | 18.3 | 4.6 | 93 / 1.58 | 1.52/.13/1.29/1.99/1.05/1.54 |
| last 5 + first 5 days | 373 | 64.6 | 1.31 | 14.8 | 8.1 | 93 / 1.25 | 2.42/.09/1.88/1.59/.86/1.18 |

Verdict: NOT a promotion candidate. TOM entries show a higher PF (1.60) but on only 193 trades, lower win rate, 2023 PF 0.85, and L12 PF below the champion; the year pattern is erratic (2.75 / 3.32 vs 0.85), i.e. noise. Non-TOM entries are as good as the champion, so no calendar filter helps; it only removes trades and return. Not added to challenger.py. Possible follow-up: SPY-dip (3d < -1%) as a priority ranking rather than a hard filter; NR7/inside-day sleeve with its own slots.

## 2026-11-05 (run 3) - stock-selection ranking of same-day champion signals (own idea)
Source: none (own idea; follow-up from the fear-filter round). Rules: take the champion's trade list (A+E+F, SPY>200d, hold 7, stop 4 ATR) and change only WHICH signals fill the 4 daily slots by re-ranking on one feature (63d return minus SPY, ATR%, 20d dollar volume, RSI2, IBS, 3d return), either replacing the rule score or only breaking ties inside a rule tier. Same simulator (10% x 12, 4/day). Script: lab_rank.py. 8 features x 2 modes = 16 variants (heavy multiple-comparison discount).

| Variant (pure rank) | Trades | Win % | PF | Ret % | Max DD % | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| high RS63 vs SPY first | 747 | 66.3 | 1.46 | 43.1 | 6.5 | 1.60 | 1.99/.15/1.22/1.74/1.37/1.47 |
| LOW RS63 first (opposite) | 753 | 66.9 | 1.44 | 42.6 | 6.5 | 1.43 | 1.59/.16/1.39/1.90/1.31/1.37 |
| low ATR% first | 751 | 66.6 | 1.42 | 38.7 | 6.5 | 1.51 | 1.68/.14/1.38/1.70/1.27/1.46 |
| high ATR% first (opposite) | 749 | 65.8 | 1.42 | 40.9 | 6.5 | 1.51 | 1.81/.17/1.20/1.75/1.37/1.37 |
| high dollar volume | 749 | 66.0 | 1.43 | 40.8 | 6.8 | 1.57 | 1.82/.15/1.27/1.79/1.22/1.47 |
| lowest RSI2 | 746 | 66.6 | 1.41 | 38.8 | 6.5 | 1.49 | 1.64/.17/1.31/1.73/1.35/1.37 |
| lowest IBS | 747 | 66.4 | 1.44 | 42.0 | 6.5 | 1.54 | 1.84/.15/1.26/1.79/1.33/1.43 |
| worst 3d return | 744 | 65.7 | 1.44 | 41.7 | 6.5 | 1.58 | 2.00/.17/1.20/1.73/1.32/1.44 |
Tie-break-within-rule-tier versions: PF 1.40-1.42, return 37-39%, i.e. identical to champion.

Verdict: NOT a promotion candidate; selection ranking is not a source of edge. Opposite rankings (high RS vs low RS, high vs low ATR%) both give PF ~1.42-1.46 vs 1.40, so the small gains are reshuffling noise, not signal. Best-looking (high RS) has lower 2023 PF (1.22) and a higher drawdown than champion. The edge sits in the entry rules and regime gate, not in which of the same-day candidates gets chosen. Not added to challenger.py. Possible follow-up (web run next): NR7/inside-day contraction sleeve with its own slots; multi-day-low (N-day low) reversion variants; pairs/relative value.

## 2026-11-05 (run 4) - Connors cumulative RSI(2), N-day-low and NR7 reversion sleeves (web idea)
Source: https://www.prorealcode.com/prorealtime-trading-strategies/rsi-2-strategy-larry-connors/ , https://www.mql5.com/en/articles/17636 (Connors RSI(2)/cumulative RSI; marketed backtests, unverified; daily-bar translation on the cached universe).
Rules: long, close > SMA200, SPY>200d gate, ATR/price < 6%, 3-day cooldown, enter at close, stop 4 ATR, hold 7. Triggers: crsi35 = RSI2(t)+RSI2(t-1) < 35; crsi10 = sum < 10; low10 = 10-day closing low and close 3% below MA5; low5down = 3 down closes + 6-day low + RSI2<20; NR7 = narrowest range of 7 days, close down, IBS<0.3. Same simulator (10% x 12, 4/day), standalone sleeve and combined with champion (shared slots). Script: lab_crsi.py. 6 variants (multiple-comparison discount; nothing passed so no year selection).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| crsi<35, ma5 exit | 2166 | 64.5 | 1.16 | 42.9 | 14.5 | 510 / 1.02 | 1.27/.25/1.23/1.53/1.21/.99 |
| crsi<10, ma5 exit | 883 | 64.4 | 1.23 | 25.4 | 6.8 | 220 / 1.54 | 1.49/.28/1.12/1.40/1.05/1.52 |
| crsi<10, prev-high exit | 897 | 66.2 | 1.35 | 38.6 | 6.0 | 222 / 1.62 | 1.45/.29/1.31/1.32/1.49/1.65 |
|   + champion combined | 1138 | 65.6 | 1.32 | 47.6 | 8.6 | 279 / 1.54 | 1.51/.14/1.23/1.47/1.22/1.59 |
| 10d low & 3% under MA5 | 1025 | 63.1 | 1.26 | 45.0 | 12.9 | 288 / 1.49 | 1.55/.14/1.15/1.43/1.20/1.53 |
| 3 down days + 6d low + RSI2<20 | 1919 | 64.8 | 1.21 | 52.5 | 13.4 | 447 / 1.01 | 1.48/.22/1.25/1.29/1.66/1.03 |
| NR7 + weak close | 1600 | 63.6 | 0.98 | -4.3 | 13.8 | 376 / 0.92 | 1.24/.42/.93/1.05/.98/.92 |

Verdict: NOT a promotion candidate. Best variant (crsi<10 with prior-high exit) is essentially a re-skin of the champion's RSI2 rules: PF 1.35 vs 1.40, lower on 4 of 5 non-2022 years vs champion, and the combined portfolio has higher return (47.6%) but lower PF (1.32) and 8.6% drawdown, i.e. same signals, no real diversification (2022 still fails ~0.14-0.29). Looser triggers (crsi<35, 3-down-days) add trades and drawdown 13-14% with L12 PF ~1.0. NR7 contraction has no edge on the long side (PF 0.98). Conclusion: the short-term reversion edge is already captured by A+E+F; more oversold-variant triggers only add correlated trades. Not added to challenger.py. Follow-ups: sector-relative reversion (buy the weakest stock within a strong sector), overnight-vs-intraday split, gap-fade sleeve.

## 2026-11-05 (run 5) - gap-down fade ("gap down then recover") and overnight-hold sleeves (own idea, gap-fade/overnight topics from the seed list)
Source: none (own idea; follow-up listed in runs 3-4). Rules: long, close > SMA200, SPY>200d gate, ATR/price < 6%, 3-day cooldown, enter at close (+0.05% slip), stop 4 ATR, exit on close > prior high, max hold 7. Trigger "gap-recover": open < prior close by X% and close > open. Overnight variants: buy close, sell next open. Same simulator (10% x 12, 4/day), standalone and combined with champion (shared slots). Script: lab_gap.py. 9 variants tried (multiple-comparison discount; no year selection, all thresholds reported).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| gap<-1% & close>open | 1904 | 68.4 | 1.30 | 89.0 | 12.3 | 497 / 1.38 | 1.28/.58/1.11/1.62/1.28/1.43 |
| gap<-2% & close>open | 790 | 69.0 | 1.41 | 52.7 | 11.5 | 213 / 1.67 | 2.60/.31/.89/1.74/1.48/1.64 |
|   + champion combined | 1317 | 66.7 | 1.40 | 85.7 | 9.7 | 324 / 1.53 | 2.14/.29/1.08/1.64/1.36/1.51 |
| gap<-3% & close>open | 379 | 71.8 | 1.40 | 21.7 | 4.2 | 116 / 1.23 | 1.79/.26/.94/2.01/1.85/1.20 |
|   + champion combined | 1012 | 67.5 | 1.37 | 52.4 | 6.6 | 247 / 1.25 | 1.81/.18/1.20/1.86/1.27/1.27 |
| gap<-2%, recover, IBS>.6 | 670 | 70.0 | 1.18 | 17.4 | 9.4 | 186 / 1.08 | 2.37/.39/.90/1.49/1.42/1.07 |
| gap<-3% & IBS<.3 (no recovery) | 196 | 57.7 | 1.10 | 3.2 | 5.1 | 61 / 1.06 | - |
| gap<-2% & RSI2<15 | 640 | 65.0 | 1.31 | 29.8 | 7.3 | 152 / 1.02 | 2.47/.28/1.41/1.23/1.46/1.08 |
| RSI2<5, prev-high exit (reference) | 1315 | 65.6 | 1.28 | 49.7 | 9.8 | 324 / 1.39 | 1.21/.25/1.21/1.69/1.22/1.39 |
| RSI2<5 overnight only | 1665 | 49.5 | 1.05 | 3.1 | 6.4 | 417 / 0.96 | - |
| RSI2<10 & IBS<.15 overnight only | 1566 | 51.4 | 1.03 | 1.5 | 6.7 | 387 / 1.16 | - |

Verdict: NOT a promotion candidate, but the most interesting complement so far. A stock that gaps down 2%+ and then closes above its open (intraday buyers absorbed the gap) is a different entry condition from RSI2/IBS "close near the low": win rate 69-72%, PF 1.3-1.4 across thresholds -1/-2/-3% (neighbours agree, so not a single lucky threshold), L12 PF 1.23-1.67, and 2022 PF 0.58 at the -1% threshold (better than the champion's 0.14). The combined portfolio (champion + gap<-2%) keeps PF 1.40, raises return 36.8 -> 85.7% and L12 PF 1.50 -> 1.53, but max drawdown rises 6.2 -> 9.7%, Sharpe is flat (1.02 vs 1.05) and 2023 PF falls to 1.08 (sleeve alone 0.89-0.94 in 2023 at every threshold). It does not beat the champion on PF or on all-but-one year, and the extra return is mostly more capital deployed in shared slots. Overnight-only holds have no edge (PF 1.03-1.05): the reversion profit accrues over the multi-day hold, not the first night. Not added to challenger.py. Follow-ups: gap-recover with 2023-style regime check (why does it fail 2023?), a gap sleeve with its own non-shared slots/position sizing, and sector-relative reversion.

## 2026-11-05 (run 6) - volume-conditioned short-term reversal filter on champion entries (web idea)
Source: https://ideas.repec.org/a/bla/jfinan/v61y2006i5p2365-2394.html (Avramov, Chordia, Goyal 2006, liquidity and autocorrelations), https://users.nber.org/~confer/2004/mmsu04/goyal.pdf (search hits only; I did not fetch the papers, so the exact claims are unverified). Literature hypothesis: low-volume declines reverse more than high-volume ones. Daily-bar translation on the cached universe.
Rules: take the champion's own trades (A+E+F, SPY>200d, hold 7, stop 4 ATR) and keep only those whose signal-day volume / 20d avg volume (or 3-day avg volume ratio) falls in a band; re-run the same simulator (10% x 12, 4/day). Script: lab_vol.py. 7 variants (multiple-comparison discount). Filtered lists are fewer trades, so total return falls mechanically.

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| vol ratio < 0.8 | 250 | 65.6 | 1.20 | 5.7 | 3.9 | 59 / 1.51 | 1.43/1.00/.78/1.30/1.14/1.42 |
| vol ratio < 1.0 | 399 | 67.7 | 1.28 | 12.2 | 4.7 | 106 / 1.61 | 1.14/.16/1.13/1.54/.92/1.71 |
| vol ratio >= 1.0 | 477 | 64.4 | 1.50 | 29.2 | 4.8 | 95 / 1.70 | 1.73/.13/1.24/1.96/1.54/1.50 |
| vol ratio >= 1.5 | 201 | 63.2 | 1.30 | 7.8 | 3.5 | 38 / 2.12 | 1.69/.01/1.05/1.25/1.32/1.97 |
| vol ratio >= 2.0 | 62 | 61.3 | 1.51 | 4.8 | 2.0 | 5 / 3.82 | 0.60/0/1.53/1.59/2.97/2.77 |
| 3d avg vol < 1.0x | 449 | 64.6 | 1.26 | 14.0 | 5.7 | 113 / 1.28 | .88/.16/1.30/1.99/1.03/1.24 |
| 3d avg vol >= 1.3x | 151 | 67.5 | 1.78 | 11.6 | 2.1 | 21 / 3.27 | 3.16/.06/1.32/1.91/1.71/2.52 |

Verdict: NOT a promotion candidate; the published low-volume effect does NOT show up (low-volume entries PF 1.20-1.28, worse than champion). Heavier volume is mildly better (>=1.0x: PF 1.50, Sharpe 1.28, lower drawdown) but with 36% fewer trades, lower return (29.2 vs 36.8%), and 2023 PF 1.24 < champion 1.39, so it fails the beat-on-return and year tests. Notable: heavy-volume days (selling capitulation) pair with run 5's gap-recover finding; a volume-ranked tie-break was effectively covered in run 3 (dollar volume = noise). Not added to challenger.py. Follow-ups: sector-relative reversion, gap sleeve with own slots, pairs.

## 2026-11-05 (run 7) - sector-relative reversion: filter/rank champion entries by sector-peer weakness (own idea)
Source: none (own idea; follow-up listed in runs 3-6; related to fear-filter finding that weakness is where the edge is richest). Rules: take the champion's trades (A+E+F, SPY>200d, hold 7, stop 4 ATR). For each signal compute the mean 3-day (and 20-day) return of the other cached stocks in the same sector (market.SECTOR_OF, self excluded, >=2 peers) and the share of peers above SMA50, then filter or re-rank. Same simulator (10% x 12, 4/day). Scripts: lab_sector.py, lab_sector2.py. 16 variants tried (8 + 8 threshold/rank neighbours; discount applies). Year choice: 2021-23 were the early years, 2024-26 confirmation; 2026 never used for picking thresholds (the 0% threshold is the least tuned of the gradient).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| stock-specific drop (3d idio < -3% vs peers) | 281 | 69.0 | 1.66 | 24.7 | 4.1 | 1.40 | 79 / 1.58 | 3.98/0/1.46/1.51/1.50/1.54 |
| sector-wide drop (idio >= -3%) | 557 | 65.4 | 1.34 | 19.8 | 5.8 | 0.86 | 114 / 1.63 | 1.31/.17/1.07/2.02/1.28/1.44 |
| peers 20d > 0 (strong sector) | 464 | 66.8 | 1.55 | 30.8 | 4.2 | 1.26 | 101 / 1.66 | 1.81/.08/1.93/1.65/1.32/1.55 |
| peers 20d <= 0 (weak sector) | 347 | 66.0 | 1.32 | 12.2 | 5.8 | 0.64 | 80 / 1.40 | 1.58/.20/.79/2.14/1.55/1.18 |
| weakest in strong sector (idio<-3 & m20>0) | 207 | 68.1 | 1.52 | 14.3 | 4.1 | 1.03 | 51 / 1.23 | 3.05/0/3.05/1.35/.99/1.37 |
| peers >=50% above SMA50 | 520 | 66.2 | 1.48 | 30.0 | 6.6 | 1.10 | 109 / 1.49 | 1.93/.17/1.58/1.74/1.34/1.35 |
| **peers 3d < 0%** | 623 | 67.1 | 1.63 | 46.4 | 5.3 | 1.37 | 144 / 1.76 | 2.05/.19/1.32/2.02/1.64/1.67 |
| peers 3d < -0.5% | 562 | 66.5 | 1.65 | 43.2 | 5.9 | 1.37 | 132 / 1.80 | 2.03/.17/1.16/2.29/1.65/1.70 |
| peers 3d < -1% | 489 | 67.3 | 1.80 | 44.5 | 5.9 | 1.56 | 123 / 1.90 | 2.71/.20/.92/2.82/1.75/1.74 |
| peers 3d < -1.5% | 405 | 67.4 | 1.77 | 37.3 | 5.8 | 1.40 | 104 / 1.78 | 2.15/.19/1.02/2.87/1.73/1.67 |
| peers 3d < -2% | 322 | 68.3 | 1.71 | 27.2 | 4.8 | 1.33 | 91 / 1.71 | 1.95/.09/1.19/2.67/2.18/1.52 |
| peers 3d < -3% | 192 | 74.0 | 2.59 | 29.3 | 2.6 | 1.87 | 49 / 2.86 | 10.2/.05/1.50/3.64/2.05/2.71 |
| **rank all signals by weakest peers first (no filter)** | 749 | 66.8 | 1.49 | 46.7 | 6.5 | 1.23 | 172 / 1.58 | 1.86/.14/1.42/1.76/1.39/1.49 |
| rank by weak peers within rule tier | 749 | 66.6 | 1.43 | 40.6 | 6.5 | 1.12 | 171 / 1.51 | 1.97/.14/1.43/1.53/1.35/1.46 |

Verdict: PROMOTION CANDIDATE (two forms, both added to challenger.py as "lab:" variants; weekly job now tracks them). The signal is "the stock's own sector fell over the last 3 days": PF rises monotonically with the threshold (1.63 at <0%, 1.65, 1.80, 1.77, 1.71, 2.59 at <-3%), a smooth gradient rather than one lucky cut, with L12 PF 1.71-2.86 and lower drawdown. Strict form "peers 3d < 0%": PF 1.63 vs 1.40, return 46.4% vs 36.8%, L12 PF 1.76 vs 1.50, Sharpe 1.37 vs 1.05, maxDD 5.3% vs 6.2%; beats the champion in 2021, 2024, 2025, 2026 and misses only 2023 (1.32 vs 1.39); 2022 stays bad (0.19), so the SPY>200d gate must stay. Tighter thresholds fail 2023 harder (0.92-1.19), so do not tighten. Soft form "rank by weakest peers first" keeps all trades and beats the champion in every year (PF 1.49, ret 46.7%, L12 1.58) with drawdown flat (6.5%), the safer change. Idiosyncratic vs sector-wide drop does not matter; what matters is that the sector is currently falling (this is the same effect as the SPY-3d-dip finding from the fear-filter round, localized to the sector, and it improved return, unlike the SPY version). Caveats: ~16 variants (but the gradient is monotone, which a pure data-mining artifact usually is not); the universe is today's ~126 survivors, with 4-17 stocks per sector so peer averages are noisy; costs are only 0.05% slippage; no independent out-of-sample beyond 2024-26. Suggested review step for the daily improvement task: consider the soft rank form first (a tie-break/priority change when more than 4 signals compete), then the strict <0% filter; the live bot needs a sector-peer 3d-return computation from its own bars. Live rules were NOT changed.
Follow-ups: apply the same peer-weakness feature to the gap-recover sleeve (run 5, which failed 2023); test the weak-sector effect using the sector ETFs (XL*) instead of peers to check it is not a universe artifact.

## 2026-11-06 (run 8) - sector dip inside a strong sector; sector filter on the gap-recover sleeve (follow-ups of runs 5 and 7; literature on industry-adjusted reversal searched only: https://www.cxoadvisory.com/momentum-investing/short-term-reversal-by-industry , not fetched, unverified)
Rules: champion trades (A+E+F, SPY>200d, hold 7, stop 4 ATR) filtered by sector-peer features from lab_sector.feats; gap sleeve = lab_gap "gap<-2% & close>open". Same simulator (10% x 12, 4/day). Script: lab_sector3.py. 7 variants here, ~23 sector-feature variants cumulative across runs 7-8 (multiple-comparison discount applies; 2026 not used to pick; the new filter is the intersection of two run-7 features that each already worked).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| peers 3d<0 (run 7 ref) | 623 | 67.1 | 1.63 | 46.4 | 5.3 | 1.37 | 144 / 1.76 | 2.05/.19/1.32/2.02/1.64/1.67 |
| **peers 3d<0 & peers 20d>0** | 359 | 68.5 | 1.94 | 36.7 | 3.5 | 1.58 | 81 / 2.18 | 2.23/.16/1.84/2.27/1.87/1.93 |
| peers 3d<0 & >=50% peers>SMA50 | 408 | 67.9 | 1.76 | 33.5 | 5.2 | 1.39 | 87 / 1.73 | 2.79/.24/1.48/2.07/1.85/1.52 |
| gap<-2% recover alone | 790 | 69.0 | 1.41 | 52.7 | 11.5 | 0.78 | 213 / 1.67 | 2.60/.31/.89/1.74/1.48/1.64 |
| gap<-2% recover & peers 3d<0 | 435 | 72.9 | 1.49 | 31.5 | 9.0 | 0.89 | 125 / 1.49 | 4.68/.23/.82/1.93/2.54/1.40 |
| champ strict + gap strict combined | 914 | 68.9 | 1.54 | 70.7 | 10.3 | 1.23 | 228 / 1.58 | 2.66/.17/.98/2.22/1.87/1.49 |
| champ + gap, rank weakest peers, no filter | 1324 | 66.4 | 1.41 | 91.0 | 10.1 | 1.08 | 324 / 1.59 | 2.21/.27/1.01/1.67/1.41/1.55 |

Verdict: "peers 3d<0 & peers 20d>0" (a short dip inside an intact sector uptrend) is the cleanest champion refinement so far: PF 1.94 vs 1.40, Sharpe 1.58, maxDD 3.5% vs 6.2%, L12 PF 2.18, and it beats the champion in every year including 2023 (1.84 vs 1.39); 2022 still fails (0.16), so the SPY>200d gate stays. Caveat: total return is flat (36.7% vs 36.8%) because only 359 trades fill the slots, so it is a quality-over-quantity filter (capital sits idle ~half the time), and it was found by intersecting features after seeing run 7. WATCH-LIST (not a full PROMOTION CANDIDATE since return does not beat the champion); added to challenger.py as a "lab:" variant so the weekly job tracks it. Idle capital could be used by a second sleeve, but the gap sleeve does not fill that role: the gap-recover sleeve fails 2023 (0.82-0.89) even with the peer filter, with drawdown 9-11%; the sector filter does not rescue it. Combined champion+gap runs return 70-91% but at ~10% drawdown and 2023 PF ~1.0, i.e. leverage-like, not an edge. Live rules NOT changed.
Follow-up: the sector-ETF cross-check (to rule out a today's-survivors universe artifact in peer averages); use the strict form as a sizing tier (larger positions when peers 3d<0 & 20d>0) rather than a filter, so idle capital is used.

## 2026-11-06 (run 9) - sector-ETF cross-check of the peer-weakness filter (own idea; follow-up of runs 7-8, rules out a survivor-universe artifact)
Source: none. Rules: champion trades (A+E+F, SPY>200d, hold 7, stop 4 ATR) filtered by the 3d / 20d return of the stock's sector ETF (market.SECTOR_OF; XLK/XLF/XLE/XLV/XLY/XLP/XLI/XLB/XLU/XLC/XLRE/SMH/XBI/ITA bars from the cache) instead of the average of cached peer stocks. Same simulator (10% x 12, 4/day). Script: lab_sector4.py. 7 variants (cumulative ~30 sector-feature variants across runs 7-9; discount applies; no thresholds tuned this run, the 0% cuts are the ones from runs 7-8).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| ETF 3d<0 | 634 | 66.6 | 1.46 | 36.2 | 6.1 | 1.11 | 150 / 1.55 | 1.63/.16/1.43/1.90/1.24/1.50 |
| ETF 3d<0 & ETF 20d>0 | 382 | 69.4 | 1.64 | 27.0 | 3.4 | 1.18 | 83 / 1.72 | 1.61/.08/2.08/2.00/1.44/1.60 |
| peers 3d<0 & 20d>0 (run 8 ref) | 359 | 68.5 | 1.94 | 36.7 | 3.5 | 1.58 | 81 / 2.18 | 2.23/.16/1.84/2.27/1.87/1.93 |
| ETF AND peers (both) | 286 | 69.2 | 1.82 | 24.5 | 3.3 | 1.32 | 70 / 1.94 | 1.41/.16/2.56/1.74/3.14/1.62 |
| ETF 3d<0 but peers 3d>=0 (disagree) | 70 | 65.7 | 0.87 | -1.3 | 3.5 | -0.24 | 19 / 1.11 | thin |
| ETF 3d>=0 (sector up) | 153 | 62.7 | 1.17 | 2.9 | 2.7 | 0.33 | 28 / 1.17 | 2.16/0/.98/1.08/1.31/1.07 |
| ETF 3d>=0 & 20d>0 (control) | 120 | 63.3 | 1.21 | 3.0 | 2.3 | 0.41 | 22 / 1.15 | thin |

Verdict: the sector-dip effect is REAL, not a peer-average artifact: with independent ETF data, entries when the sector is down 3d inside a 20d uptrend have PF 1.64 vs 1.40 (every year but 2021/2022 better than champion, 2023 2.08, L12 1.72, maxDD 3.4%), and the control (sector flat/up) is clearly worse (PF 1.17-1.21, near-zero return). It is weaker than the peer version (PF 1.94) and, like it, return does not beat the champion (27% vs 36.8%, fewer trades), so the ETF form is NOT added to challenger.py; the run-8 watch-list variant stays as is. Entries where the stock's sector is rising are the weak ones: the edge is concentrated in sector pullbacks. Useful for the daily-improvement task: if the sector rule is ever adopted, the live bot can use the sector ETF 3d return (cheaper than peer averages) as a fallback, but the peer form tested better. Live rules NOT changed.
Follow-up: a sector-pullback rank or size tier (priority for sector-dip signals rather than a hard filter) is already covered by run 7's rank form; remaining untested seed ideas: sector momentum rotation (long top ETFs), pairs/relative value, post-earnings drift (needs earnings dates).

## 2026-11-06 (run 10) - monthly sector-momentum rotation sleeve (web idea: Faber 'relative strength' sector rotation)
Source: https://quantpedia.com/strategies/sector-momentum-rotational-system (fetched; claims 13.9% a year, Sharpe 0.54, 1928-2009, costs excluded; treated as an unverified hypothesis). Rules (daily bars, scripts lab_rotation.py, lab_rotation2.py): on the first trading day of each month rank the 14 cached sector ETFs by 12-month return skipping the last month (12-1), buy the top 3 at that close, exit the close 21 trading days later (no stop), 0.05% slippage per side, 10% per position. Sleeve is simulated alone (max 12 pos) and combined with the champion trades (18 slots, 6 new/day, 10% each). 12 variants tried in total (6 + 6 robustness; discount applies; the base 12-1m top-3 rule is the published one and was not tuned).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| **ETF top3 12-1m, no gate (sleeve alone)** | 140 | 57.1 | 1.87 | 26.2 | 4.8 | 1.23 | 25 / 1.73 | 2.62/1.01/1.49/4.20/2.54/1.91 |
| **champion + that sleeve (18 slots)** | 910 | 64.7 | 1.57 | 83.1 | 7.9 | 1.35 | 198 / 1.58 | 1.97/.71/1.40/2.02/1.64/1.51 |
| ETF top3 12-1m, SPY>200d | 106 | 56.6 | 1.68 | 15.4 | 5.9 | 1.09 | 22 / 1.31 | 2.62/.47/.92/4.20/2.29/1.44 |
| ETF top3 6m, SPY>200d | 124 | 54.0 | 1.58 | 14.7 | 5.1 | 0.80 | 24 / 1.53 | 1.16/.19/.82/2.89/3.83/1.86 |
| ETF top3 3m, SPY>200d | 124 | 51.6 | 1.54 | 14.9 | 8.0 | 0.74 | 23 / 1.80 | .98/.18/.49/2.52/6.47/1.77 |
| stocks top10 12-1m, SPY>200d | 351 | 52.1 | 1.61 | 144.7 | 32.6 | 0.89 | 76 / 1.80 | 1.57/.17/1.09/3.77/1.45/2.08 |
| stocks top10 6m, SPY>200d | 385 | 52.5 | 1.51 | 114.2 | 23.6 | 0.80 | 74 / 1.95 | 1.32/.13/.91/2.34/1.79/2.24 |
| robustness: ex SMH | 138 | 52.9 | 1.36 | 10.5 | 5.3 | 0.62 | 25 / 0.82 | 1.49/1.21/1.03/2.06/2.17/.94 |
| robustness: 11 broad SPDR only | 139 | 59.0 | 1.96 | 25.6 | 4.8 | 1.31 | 25 / 2.68 | 1.49/1.17/1.62/3.09/2.51/3.53 |
| robustness: top5 | 235 | 59.1 | 1.99 | 50.5 | 6.4 | 1.33 | 41 / 1.71 | 1.81/1.13/1.73/3.44/3.90/1.91 |
| robustness: top3 hold 10d | 186 | 55.4 | 1.58 | 17.2 | 6.9 | 0.81 | 36 / 1.46 | 14.0/.56/1.59/3.60/1.38/1.78 |
| base split 2021-23 | 66 | 50.0 | 1.35 | 5.6 | 4.8 | 0.65 | - | 2.62/1.01/1.49 |
| base split 2024-26 | 77 | 64.9 | 2.80 | 22.3 | 2.8 | 1.89 | 25 / 1.73 | 5.14/2.54/1.91 |

Monthly-return correlation with the champion: 0.27 (base), 0.13-0.28 for the other ETF forms, 0.14-0.17 for stocks. Stock-level top-10 momentum is not comparable: it is ~100% invested, 24-33% drawdown, 2023 PF about 1.0, so it is leverage, not edge; rejected.
Verdict: usefully COMPLEMENTS the champion, but with caveats, so treat as WATCH-LIST / PROMOTION CANDIDATE for the combined portfolio only (challenger.py flags it by its automatic rule). Pros: low correlation, positive in every year including 2022 (PF 1.01 alone; combined 2022 PF 0.71 vs 0.14 for the champion alone), combined return 83% vs 37%, Sharpe 1.35 vs 1.05, L12 PF 1.58 vs 1.50, combined beats the champion in every non-2022 year; the 12-1m rule works without a gate (the SPY>200d gate hurt: PF 1.68, return 15%). Cons: (1) the edge is mostly 2024-26 (PF 2.80) versus a weak 2021-23 (PF 1.35, return 5.6%), so it fails the early-years-then-confirm pattern in strength even though it was positive early; (2) it leans on SMH (39 of 140 trades) and is fragile to the ETF list: dropping SMH only gives PF 1.36 and L12 0.82, while dropping SMH, XBI and ITA gives PF 1.96, i.e. the sample is noisy (about 47 monthly rebalances, 14 ETFs); (3) combined drawdown rises 6.2 to 7.9% because the combined portfolio uses 18 slots (more capital deployed), so part of the extra return is exposure; (4) 2026 never used for choices. Not for live yet: needs a live-path decision on monthly rebalance orders and ETFs in the universe, which belongs to the daily improvement task. Live rules NOT changed. Added challenger.py variant "lab: champion + sector-ETF rotation sleeve" and tests/test_lab_rotation.py.
Follow-ups: sleeve sizing at fixed 5% per ETF to compare risk-matched; longer ETF history if the bars cache is extended (only 2021+ trades since 12-month lookback); pairs/relative value and post-earnings drift remain untested.

## 2026-11-06 (run 11) - bear-regime sleeves: short-the-rip and strict long reversion when SPY < 200d (own idea; shorts were on the "be skeptical" list)
Source: none. Script lab_bear.py. Idea: the champion is switched off when SPY < 200d, so test what can fill those days. Rules: same entry triggers as sweep.py (rsi2 / ibs), 3-day cooldown, ATR/price < 6%, enter at close (+0.05% slip), exit when close > prior high (or MA5), hold 5-10, stop 3-6 ATR; only on days SPY < 200d. Same portfolio simulator (10% x 12, 4/day). Round 1: 6 variants (4 short, 2 long); round 2: 8 neighbour/robustness variants of the winner. 14 variants in total (discount applies).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF per year |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 (2021-26) |
| short rsi2>95, s50<s200, SPY<200d | 152 | 55.9 | 0.86 | -3.5 | 8.3 | 4 / 0.13 | 2022 1.33, 2023 .22, 2025 .49, 2026 .13 |
| short rsi2>90, below 200d, SPY<200d | 431 | 57.3 | 0.74 | -20.6 | 31.2 | 17 / 0.46 | .96/.22/.64/.46 |
| short ibs>.9, below 200d | 538 | 50.7 | 0.73 | -25.4 | 30.2 | 28 / 0.24 | .84/.15/1.15/.24 |
| short rsi2>95 in bear regime, no trend | 310 | 50.0 | 0.71 | -15.7 | 22.3 | 32 / 0.45 | .85/.27/1.01/.45 |
| long rsi2<5, stock>200d, SPY<200d (BASE) | 250 | 68.8 | 1.67 | 19.3 | 6.8 | 19 / 4.96 | 2022 1.46, 2023 2.18, 2025 1.12, 2026 4.96 |
| **BASE + champion combined (same 12 slots)** | 994 | 66.7 | 1.47 | 63.3 | 7.5 | 188 / 1.63 | 1.82/1.21/1.60/1.57/1.21/1.61 |
| long rsi2<5, stock>50>200, SPY<200d | 98 | 63.3 | 0.92 | -1.2 | 6.9 | 5 / 0.56 | 2022 .73, 2023 4.39 |
| robustness: rsi2<10 | 393 | 69.0 | 1.51 | 23.6 | 7.5 | 30 / 3.85 | 1.43/1.65/1.14/3.85 |
| robustness: hold 5 / hold 10 | 257 / 247 | 66.9 / 69.2 | 1.66 / 1.78 | 19.4 / 21.1 | 5.4 / 5.7 | 19 / 4.8-5.0 | all years > 1.1 except 2025 1.10-1.12 |
| robustness: stop 3 / stop 6 | 255 / 249 | 68.6 / 69.1 | 1.61 / 1.60 | 18.5 / 18.0 | 6.4 / 7.2 | 19 / 6.1, 4.8 | 2025 0.96 / 0.90 |
| robustness: exit MA5 | 244 | 68.9 | 1.54 | 15.7 | 4.5 | 20 / 3.86 | 1.33/2.14/1.15/3.86 |
| robustness: ibs<.1 | 463 | 67.6 | 1.41 | 24.5 | 11.6 | 26 / 3.71 | 1.50/1.81/.73/3.71 |
| split <=2023 / >=2024 | 207 / 43 | 68.6 / 69.8 | 1.60 / 1.94 | 14.0 / 4.7 | 6.8 / 2.8 | - | confirms in later years (thin n=43) |

Verdict:
1) SHORTS REJECTED again: every short form has PF 0.71-0.86 and the larger ones draw down 22-31%. Rips in this universe keep going; the only year above 1 is 2022. Shorts stay unproven.
2) Long reversion in the bear regime, but ONLY in stocks that are still above their own 200d, is a PROMOTION CANDIDATE (as a complement). It fills the champion's idle days: sleeve alone PF 1.67, win 69%, maxDD 6.8%; combined PF 1.47, return 63% vs 37%, Sharpe 1.46 vs 1.05, L12 PF 1.63 vs 1.50, and the champion's worst year 2022 goes from PF 0.14 to 1.21 (the sleeve is positive in 2022, 2023 and 2026, 1.12 in 2025). It holds for all 8 neighbour variants (PF 1.41-1.78), so it is not a single lucky parameter. The challenger.py automatic rule shows "better in 2/5 years" only because the sleeve is idle (tie) in 2021 and 2024, when SPY never fell below its 200d; it never loses a year except 2025 (1.21 vs 1.24). Requiring stock > s50 > s200 kills the effect (PF 0.92), so "above 200d only" is the active ingredient, not a stricter trend.
Caveats (important): (a) only about 5 bear-regime episodes (2022 dominates: 207 of 250 trades in 2022-23), so n is large but independent episodes are few; (b) the 126-stock universe is today's survivors, which flatters "still above its 200d during a bear market" (2022 winners such as LLY, AMGN, COP, CVX, GILD are the top symbols); (c) 2026 (PF 4.96, n=19) was NOT used for selection but looks too good to extrapolate; (d) capital is only deployed in bear regimes, so return comes with the same 12-slot cap, no extra exposure. Live rules NOT changed. Added challenger.py variant "lab: champion + bear-regime long sleeve" and tests/test_lab_bear.py. For the daily-improvement task: the cheapest live change would be to allow the existing rules A/E/F when SPY < 200d only for stocks above their 200d (check also with a delisted-stock universe if one ever exists).
Follow-ups: test the sleeve with a size cap (5% per position in bear regime); a pairs/relative-value study and post-earnings drift remain untested.

## 2026-11-06 (run 12) - market-breadth washout filter on champion entries (web-seeded: breadth-capitulation literature, e.g. https://sentimentrader.com/blog/do-new-lows-suggest-capitulation ; search snippets only, not fetched, unverified)
Script lab_breadth.py. Rule: on the signal day (known at the close, where the bot enters), breadth = share of the 126-stock universe with RSI2 < 10 (or closing at a 5-day low). Keep a champion trade only if breadth is above a threshold. Same simulator (10% x 12, 4/day). 8 variants tried (thresholds 10/20/30% RSI2, 25/40/60% 5d-low, plus the complementary low-breadth sets); discount applies, but every threshold points the same way (monotonic), and the early/late split was done for the headline rule.

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| **RSI2<10 breadth >= 10%** | 605 | 68.6 | 1.79 | 52.3 | 5.6 | 1.75 | 137 / 2.59 | 2.04/.13/1.35/1.93/1.71/2.66 |
| RSI2<10 breadth < 10% (complement) | 195 | 59.0 | 0.76 | -7.1 | 8.8 | -0.62 | 51 / 0.60 | 1.25/.25/1.18/.77/.71/.60 |
| RSI2<10 breadth >= 20% | 348 | 66.1 | 1.75 | 26.0 | 4.5 | 1.41 | 65 / 2.99 | 2.54/.03/1.52/1.73/1.81/3.46 |
| RSI2<10 breadth >= 30% | 176 | 69.3 | 2.22 | 17.1 | 2.3 | 1.75 | 28 / 2.10 | 24.2/.03/2.72/2.21/1.45/2.21 |
| 5d-low breadth >= 25% | 556 | 66.5 | 1.68 | 43.5 | 5.9 | 1.50 | 124 / 2.29 | 2.25/.18/1.41/1.89/1.33/2.25 |
| 5d-low breadth >= 40% | 344 | 67.7 | 1.85 | 27.5 | 4.0 | 1.57 | 70 / 2.31 | 3.75/.13/1.31/2.09/1.64/2.10 |
| 5d-low breadth >= 60% | 103 | 70.9 | 3.46 | 14.4 | 1.6 | 2.16 | 8 / 2.29 | thin |
| 5d-low breadth < 25% (complement) | 255 | 65.1 | 0.98 | -0.9 | 6.4 | -0.05 | 64 / 1.01 | .80/.08/.81/1.17/1.23/1.02 |
| split of RSI2 breadth >=10%: <=2023 / >=2024 | 220 / 385 | 64.1 / 71.2 | 1.37 / 2.07 | 8.3 / 40.7 | 5.6 / 5.5 | - | 137 / 2.59 | confirms in later years |

Verdict: PROMOTION CANDIDATE (filter). Single-stock oversold signals when the rest of the market is NOT oversold (idiosyncratic dips, breadth < 10%) are net losers (PF 0.76, 0.98 by the other measure); all of the champion's edge comes from market-wide washouts. Dropping them lifts PF 1.40 to 1.79, return 36.8 to 52.3%, Sharpe 1.05 to 1.75, L12 PF 1.50 to 2.59, drawdown 6.2 to 5.6%, with 19% fewer trades. Better than the champion in 2021, 2024, 2025, 2026, about equal in 2023 (1.35 vs 1.39) and 2022 (both ~0.13); the effect is monotonic across thresholds and across two breadth measures, and the low-breadth complement loses in 5 of 6 years. Caveats: early-years edge is modest (PF 1.37 in 2021-23 vs 2.07 in 2024-26, so most of the gain is in later years); the survivor-biased universe makes breadth a slightly rosier measure; 2022 still fails (the filter does nothing there, the SPY gate/bear sleeve are the other levers); related to run 6/7 findings (washouts and sector-wide dips beat idiosyncratic dips), so it is partly the same effect, not independent evidence. Live rules NOT changed; added challenger.py variant "lab: only if >=10% of universe RSI2<10" and tests/test_lab_breadth.py. For the daily-improvement task: needs a universe-wide RSI2 count at signal time (the bot already computes RSI2 for the whole universe when scanning). Suggest testing it as a rank/size tier combined with the sector-peer rank.
Follow-ups: breadth vs bear-sleeve combination; sizing tiers (e.g. 12% when breadth >= 20%); pairs/relative value and post-earnings drift still untested.

## 2026-11-06 (run 13) - bear-regime long sleeve on top of the NEW live setup (own idea; follow-up of runs 11-12)
Source: none. Script lab_bear2.py. Rules: live setup = champion A+E+F (SPY>200d, hold 7, stop 4 ATR) + breadth>=10% filter + weakest-sector-peer rank. Sleeve (from run 11): SPY<200d, stock>own 200d, RSI2<5, exit close>prev high, hold 7, stop 4 ATR; tested with and without the breadth filter on the sleeve. Same simulator (10% x 12, 4/day). 6 combined variants (multiple-comparison discount; thresholds 10%/20% were reused from run 12, not tuned here). Data through 2026-10-29.

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| OLD champion | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| NEW LIVE (breadth+rank) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| bear sleeve alone | 251 | 68.5 | 1.52 | 16.0 | 7.2 | 1.28 | 21 / 4.07 | -/1.38/1.71/-/1.12/4.07 |
| sleeve alone, breadth>=10% | 212 | 69.3 | 1.62 | 14.6 | 6.8 | 1.25 | 18 / 8.61 | -/1.33/1.79/-/1.87/8.61 |
| LIVE + sleeve (no breadth on sleeve) | 851 | 68.9 | 1.75 | 84.5 | 7.2 | 1.96 | 155 / 2.78 | 1.89/1.17/1.51/2.19/1.67/2.84 |
| **LIVE + sleeve, breadth>=10%** | 813 | 69.1 | 1.80 | 82.5 | 6.8 | 1.96 | 152 / 2.91 | 1.89/1.11/1.50/2.19/1.92/3.01 |
| LIVE + sleeve, breadth>=20% | 783 | 69.9 | 1.90 | 87.2 | 5.9 | 2.07 | 150 / 2.88 | 1.89/1.43/1.39/2.19/1.96/2.96 |
| split 2021-23: LIVE -> LIVE+sleeve10 | 221 -> 399 | 64.7 -> 66.7 | 1.38 -> 1.39 | 9.0 -> 17.7 | 5.9 -> 6.8 | 0.80 -> 1.02 | - | 2022 .13 -> 1.11 |
| split 2024-26: LIVE -> LIVE+sleeve10 | 383 -> 414 | 71.5 | 2.25 -> 2.33 | 46.5 -> 55.0 | 5.2 -> 5.6 | 2.78 -> 3.27 | 152 / 2.91 | same |

Verdict: usefully COMPLEMENTS the new live setup (WATCH-LIST / PROMOTION CANDIDATE for combined portfolio; added to challenger.py as "lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%)"). The sleeve fills days when the SPY>200d gate is off: return 59.6% -> 82.5%, Sharpe 1.85 -> 1.96, L12 PF 2.65 -> 2.91, 2022 PF 0.13 -> 1.11, and the benefit shows in the early selection period too (2021-23 return 9.0% -> 17.7%, Sharpe 0.80 -> 1.02) as well as the later one, so it passes the walk-forward check. Cost: combined PF 1.88 -> 1.80 (it does not beat live on PF), maxDD 5.9 -> 6.8. Breadth>=20% on the sleeve looks better still (PF 1.90, 2022 1.43) but is the more tuned choice, treat as one-sided evidence. Caveats carry over from run 11: survivor universe flatters "stock still above its 200d in a bear market", only ~2 bear episodes in the data (2022, early 2025), sleeve n in the last 12 months is just 18-21. Note: bear_long raw signal count is 421, 251 survive the portfolio caps. Needs more bear-regime data before live; SPY>200d gate for the main strategy stays.
Follow-ups: risk-matched sleeve size (5%); pairs/relative value and post-earnings drift remain untested.

## 2026-11-06 (run 14) - short max-hold and volatility-targeted sizing on the NEW live setup (web idea)
Source: https://quantpedia.com/testing-an-ai-assisted-research-workflow-for-multi-asset-pullback-strategy-discovery/ (fetched; ETF pullback study 2006-2025 recommending 1-day holds and 10%/21d-vol sizing; its own caveats: parameters chosen in-sample, no costs, inconsistent sweep count; treated as an unverified hypothesis on ETFs, not single stocks). Script lab_hold.py. Rules: live setup (A+E+F, SPY>200d, stop 4 ATR, breadth>=10%, weakest-peer rank), vary max hold 1/2/3/5/10 days (prev-high exit unchanged); sizing post-hoc scaled by 2.5/ATR% (caps 1.5x, 1.0x). Same simulator (10% x 12, 4/day). 7 variants. Data through 2026-10-29.

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE hold 7 (ref) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| hold 1 | 743 | 50.7 | 1.26 | 13.1 | 3.9 | 0.84 | 1.35 | 1.12/.19/1.04/1.63/1.49/1.25 |
| hold 2 | 666 | 56.8 | 1.37 | 23.0 | 4.9 | 0.98 | 1.62 | 1.54/.13/1.20/1.69/1.21/1.59 |
| hold 3 | 646 | 63.6 | 1.71 | 47.2 | 5.8 | 1.57 | 1.88 | 1.66/.12/1.27/2.49/1.66/1.94 |
| hold 5 | 614 | 66.8 | 1.70 | 49.2 | 7.4 | 1.45 | 2.14 | 1.88/.14/1.23/2.15/1.71/2.10 |
| hold 10 | 598 | 70.1 | 1.91 | 60.9 | 6.8 | 1.77 | 2.77 | 2.06/.14/1.46/2.32/1.69/2.84 |
| size 2.5/ATR% cap 1.5x | - | - | - | 40.3 | 6.5 | 1.40 | - | 1.53/.10/1.34/1.72/1.84/2.13 |
| size 2.5/ATR% cap 1.0x | - | - | - | 39.4 | 5.2 | 1.61 | - | 1.66/.12/1.40/1.96/1.85/2.24 |

Verdict: NOT a promotion candidate. The published 1-day hold does not transfer to single stocks here: PF falls monotonically as the hold shortens (hold 1: PF 1.26, win 51%, return 13%). Hold 10 is a tie with hold 7 (PF 1.91 vs 1.88, return 60.9 vs 59.6, higher drawdown 6.8 vs 5.9, worse 2025), consistent with the earlier hold sweep. Vol-targeted sizing lowers return (39-40% vs 59.6%) and Sharpe in both the early and late periods (2021-23 Sharpe 0.80 -> 0.47; 2024-26 2.78 -> 2.29): this mean-reversion edge is richer in higher-volatility names, so scaling them down hurts. The current exit (hold 7, prior-high exit) stays.
Follow-ups: pairs/relative value and post-earnings drift remain untested; sleeve sizing at 5%.

## 2026-11-06 (run 15) - post-earnings-drift PROXY (gap + volume spike) as a sleeve (web idea: PEAD)
Source: https://pl.tradingview.com/scripts/pead , https://doc.stocksharp.com/pt/api-examples/1161_PEAD (open PEAD strategy scripts found by search; snippets only, not fetched, unverified; academic PEAD is on earnings surprise, which we cannot test: no earnings dates offline). Script lab_pead.py.
Rules: "earnings-like day" = open gap vs prior close >= X% AND volume >= 3x 20d avg AND close > open (continuation long), ATR/price < 9%, SPY>200d gate (one variant without), 10-day cooldown, enter at close (+slip), stop 4 ATR, fixed hold N, no other exit. Reversal variant: gap <= -5%, vol >= 3x, close > open, prev-high exit, hold 7. Same simulator (10% x 12, 4/day), standalone and combined with the NEW live setup (breadth>=10% + weakest-peer rank). 6 variants (multiple-comparison discount; nothing passed so no year selection).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (breadth+rank) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| gap-up>=5%, h10 | 101 | 58.4 | 1.34 | 8.6 | 8.0 | 0.52 | 24 / 1.03 | 10.5/0/1.39/2.19/.28/1.56 |
| gap-up>=5%, h20 | 97 | 56.7 | 1.74 | 26.9 | 7.8 | 1.01 | 24 / 1.84 | 8.7/0/1.09/5.09/.30/2.63 |
|   + live combined | 656 | 66.8 | 1.79 | 88.6 | 9.8 | 1.65 | 151 / 2.26 | 2.77/.08/1.26/2.69/1.15/2.43 |
| gap-up>=8%, h20 | 59 | 54.2 | 1.81 | 19.6 | 9.5 | 0.96 | 15 / 1.89 | -/0/2.63/7.28/.10/2.48 |
|   + live combined | 633 | 66.8 | 1.76 | 74.4 | 8.5 | 1.55 | 144 / 2.24 | 2.39/.08/1.65/2.57/1.06/2.33 |
| gap-up>=5%, IBS>.7, h10 | 67 | 67.2 | 1.47 | 9.2 | 7.7 | 0.65 | 17 / 0.61 | -/0/2.39/3.31/.21/.97 |
| gap-up>=5%, h10, no SPY gate | 115 | 56.5 | 1.19 | 5.9 | 8.8 | 0.30 | 24 / 1.03 | 10.5/.48/1.57/2.19/.28/1.56 |
| gap-down<=-5% recover, h7 | 70 | 61.4 | 0.92 | -1.1 | 4.9 | -0.16 | 8 / 2.68 | 1.31/.98/1.70/.59/1.12/1.15 |

Verdict: NOT a promotion candidate. Only ~60-115 signals in 5.8 years (this universe has few big earnings gaps that pass the filters), so every row is a tiny sample (2021 PF 8-10 comes from a handful of trades). Continuation after a volume-confirmed gap-up has a lower win rate (54-58%) than the live reversion (69%), 2025 PF is 0.1-0.3 in every gap-up variant, and combining with live lowers PF (1.88 -> 1.76-1.79) and Sharpe (1.85 -> 1.55-1.65) while raising drawdown (5.9 -> 8.5-9.8%); the higher combined return is again just more capital deployed. The gap-down reversal is flat (PF 0.92). A true PEAD test needs earnings dates and surprise data, which the sandbox cannot fetch. Not added to challenger.py. Follow-ups: pairs/relative value (long-only spread z-score vs most-correlated peer); sleeve sizing at 5%; extend the universe if the bars cache grows.

## 2026-11-07 (run 16) - SPY-gate alternatives now that the breadth filter is live (own idea)
Source: none (own idea; follow-up of runs 12-13, asks whether breadth>=10% makes the SPY>200d gate redundant or replaceable). Script lab_gate.py. Rules: NEW live setup (A+E+F, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank), only the market gate changed. Same simulator (10% x 12, 4/day). Data through 2026-10-29. 8 variants incl. reference (multiple-comparison discount; nothing passed).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE SPY>200d (ref) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| no SPY gate | 697 | 68.3 | 1.73 | 61.2 | 6.4 | 1.64 | 2.65 | 1.89/.68/1.59/2.19/1.86/2.68 |
| not-bear regime | 639 | 67.8 | 1.76 | 56.1 | 5.9 | 1.58 | 2.65 | 1.89/.35/1.44/2.19/1.86/2.68 |
| SPY>50d | 487 | 69.6 | 2.00 | 49.4 | 4.8 | 1.68 | 3.14 | 1.73/.49/1.73/2.10/2.22/3.19 |
| SPY drawdown from 252d high > -10% | 620 | 68.1 | 1.76 | 55.8 | 5.9 | 1.77 | 2.65 | 1.89/.51/1.23/2.19/1.86/2.68 |
| SPY drawdown > -15% | 652 | 68.1 | 1.78 | 60.1 | 5.9 | 1.79 | 2.65 | 1.89/.67/1.39/2.19/1.86/2.68 |
| SPY>200d OR breadth>=25% | 676 | 68.8 | 1.80 | 64.4 | 5.9 | 1.75 | 2.63 | 1.89/.84/1.51/2.19/1.92/2.64 |
| SPY>200d AND 200d slope up | 581 | 68.5 | 1.82 | 54.4 | 5.9 | 1.82 | 2.65 | 1.84/.13/1.18/2.19/1.90/2.68 |

Verdict: NOT a promotion candidate; the SPY>200d gate stays. Every looser gate improves 2022 (PF 0.13 -> 0.35-0.84, still below 1) but lowers overall PF and Sharpe versus the live setup, and 2021-2026 other years are unchanged by construction. The best (OR breadth>=25%) adds +4.8 pts of return for -0.08 PF and -0.10 Sharpe and still loses money in 2022, so it is a trade-off, not an improvement. SPY>50d has the highest PF (2.00) and L12 PF (3.14) but fewer trades, lower return (49.4%) and 2021 worse, so it fails the "beats on return" test. The 2022 bear year is not rescued by any gate here; insurance is not free. Not added to challenger.py.
Follow-ups still untested: pairs/relative value (long-only spread z-score vs most-correlated peer); sleeve sizing at 5%; true PEAD needs earnings data.

## 2026-11-07 (run 17) - long-only pairs / relative-value reversion vs most-correlated peer (own idea; pairs was the open follow-up from runs 13-16)
Source: none fetched (classic Gatev/Goetzmann/Rouwenhorst distance-pairs idea, adapted; treated as an unverified hypothesis). Script lab_pairs.py. Rules: each stock gets one partner per calendar year = the universe stock with the highest daily-return correlation over the 252 sessions BEFORE that year (corr > 0.5, no lookahead). Spread = log(price / partner price); z = (today - mean) / sd over the prior 60 days. Long the laggard when z <= threshold, stock > own 200d, ATR/price < 9%, SPY>200d gate, 5-day cooldown, exit close > prior high, hold 7, stop 4 ATR; rank by -z. Same simulator (10% x 12, 4/day). Data through 2026-10-29. 5 variants x (standalone, +live, breadth>=10% standalone) (multiple-comparison discount; nothing passed so no year selection). The sleeve has no 2021 trades because partners need a full prior year.

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (breadth+rank) ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| z<-2, h7 | 1022 | 65.4 | 1.21 | 25.8 | 6.3 | 0.92 | 283 / 1.33 | -/.43/1.02/1.37/1.36/1.31 |
|   + LIVE | 1486 | 66.6 | 1.38 | 78.4 | 8.1 | 1.44 | 379 / 1.57 | 1.89/.32/1.13/1.48/1.63/1.54 |
| z<-2.5, h7 | 512 | 64.5 | 1.26 | 14.9 | 4.7 | 0.78 | 147 / 1.22 | -/.45/.99/1.77/1.27/1.22 |
| z<-2 & RSI2<10, h7 | 320 | 66.9 | 1.47 | 17.3 | 3.6 | 1.17 | 98 / 1.48 | -/.09/1.97/2.03/.77/1.64 |
|   + LIVE | 838 | 68.4 | 1.69 | 73.1 | 6.7 | 1.74 | 209 / 1.90 | 1.89/.11/1.61/2.13/1.61/1.92 |
| z<-2 & RSI2<10, breadth>=10% alone | 215 | 66.5 | 1.78 | 16.5 | 2.0 | 1.49 | 67 / 1.38 | -/.22/2.67/2.66/1.17/1.39 |
| z<-1.5 & RSI2<10, h7 | 528 | 63.1 | 1.35 | 23.0 | 5.7 | 0.98 | 152 / 1.54 | -/.16/1.61/1.60/1.08/1.57 |
|   + LIVE | 979 | 66.5 | 1.58 | 73.1 | 7.7 | 1.59 | 248 / 1.65 | 1.89/.14/1.82/1.84/1.43/1.66 |
| z<-2, h5 | 1098 | 64.1 | 1.18 | 23.9 | 9.0 | 0.88 | 304 / 1.31 | -/.33/.97/1.46/1.28/1.31 |

Verdict: NOT a promotion candidate. Peer-relative weakness alone is a weak edge (PF 1.18-1.35, 2023 about 1.0) well below the live setup (PF 1.88). Every combination lowers PF (1.88 -> 1.38-1.69), Sharpe (1.85 -> 1.44-1.74) and raises drawdown (5.9 -> 6.7-10.6); the extra return is only more capital deployed. The best idea, z<-2 with RSI2<10 and breadth>=10%, is a nice small sleeve on its own (PF 1.78, maxDD 2.0) but it is mostly the same oversold stocks the live rules already catch, 2025 PF is 0.77-1.17, and 2022 is a loss. It adds nothing the sector-peer ranking in the live bot does not already capture. Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; true PEAD needs earnings data; seasonality by month/weekday within the live setup; ETF cross-asset filters (bonds/VIX proxies) for the gate.

## 2026-11-07 (run 18) - intraday vs overnight decomposition of the recent decline, on the NEW live setup (web idea: Quantpedia)
Source: https://quantpedia.com/short-term-return-reversals-and-intraday-transactions/ (fetched; abstract-level only: intraday returns reverse the following week, overnight returns do not; no explicit trading rule, costs or performance given, so the rules below are my translation; unverified). Script lab_intraday.py.
Rules: on the live setup's trades (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank), compute over the 3 (or 5) sessions ending on the signal day: intraday = sum of ln(close/open), overnight = sum of ln(open/prior close). Use as a filter or as the ranking key. Same simulator (10% x 12, 4/day). Data through 2026-10-29. 8 variants incl. reference (multiple-comparison discount; no year selection since nothing passed).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| intraday3 < overnight3 | 453 | 68.4 | 1.75 | 38.0 | 4.7 | 1.36 | 3.23 | 1.29/.16/1.20/2.36/1.64/3.31 |
| intraday3 < -2% | 401 | 68.8 | 2.16 | 51.2 | 4.4 | 1.76 | 4.15 | 1.63/.06/1.26/3.17/1.91/4.15 |
| overnight3 > -1% | 349 | 68.8 | 1.50 | 17.5 | 4.3 | 0.97 | 4.64 | 1.16/.06/1.63/1.54/1.71/4.00 |
| intraday5 < 0 and ovn5 > intraday5 | 443 | 68.4 | 1.73 | 35.9 | 4.5 | 1.43 | 2.92 | 1.46/.16/1.07/2.52/1.71/2.66 |
| rank by most-negative intraday3 | 604 | 67.5 | 1.73 | 49.9 | 6.4 | 1.48 | 2.55 | 1.78/.13/1.11/2.37/1.55/2.40 |
| rank by intraday3 - overnight3 | 603 | 67.0 | 1.71 | 49.0 | 6.8 | 1.45 | 2.58 | 1.78/.13/1.17/2.14/1.63/2.40 |
| EXCLUDE intraday3 < overnight3 (opposite) | 217 | 72.4 | 1.90 | 17.6 | 4.1 | 1.39 | 1.40 | 5.31/0/1.38/2.57/1.66/1.52 |

Verdict: NOT a promotion candidate. The paper's direction is only weakly supported: the best filter (intraday 3-day return < -2%) lifts PF 1.88 -> 2.16 and last-12-month PF 2.65 -> 4.15, but cuts trades by a third and return 59.6% -> 51.2%, and loses to live in 2021 and 2023 (1.63 vs 1.89, 1.26 vs 1.42). Pure decomposition rules (intraday < overnight) reduce PF, return and Sharpe, and the opposite subset has PF 1.90 too, so the intraday/overnight split is not a clean separator here; the gain from "intraday < -2%" is mostly just a deeper-drop filter (it is correlated with the existing RSI2/3-day-drop rules). Ranking by intraday weakness is worse than the peer-weakness rank already live (PF 1.71-1.73 vs 1.88). Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; month/weekday seasonality within the live setup; ETF cross-asset (bond/VIX proxy) filters; true PEAD needs earnings data.

## 2026-11-07 (run 19) - VIXY volatility-regime and IWM/SPY risk-appetite filters on the LIVE setup (own idea; cross-asset follow-up of runs 16-18)
Source: none (own idea; TLT/HYG are not in the bars cache, so the cross-asset proxies are VIXY and IWM vs SPY). Script lab_vixy.py. Rules: LIVE setup (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank) filtered by signal-day state: VIXY close vs its 20d SMA (VIXY decays from futures roll, so only relative measures are used), VIXY 5d change, IWM/SPY 20d relative return. Same simulator (10% x 12, 4/day). Data through 2026-10-29. 8 rows incl. reference (multiple-comparison discount; nothing passed so no year selection). Subset rows drop signals on days lacking VIXY history.

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| VIXY > 20d SMA +10% (fear spike) | 76 | 77.6 | 3.90 | 12.6 | 1.1 | 3.46 | 20 / 1.86 | 23.8/-/9.5/4.2/2.9/1.4 |
| skip VIXY > SMA +25% (panic) | 591 | 68.5 | 1.82 | 54.4 | 5.9 | 1.75 | 136 / 2.65 | 1.57/.13/1.42/2.16/1.92/2.68 |
| VIXY 5d change < +15% | 571 | 68.0 | 1.77 | 49.2 | 6.3 | 1.59 | 132 / 2.65 | 1.45/.13/1.42/2.06/2.07/2.55 |
| VIXY above 20d SMA | 268 | 66.4 | 2.06 | 29.0 | 3.8 | 1.72 | 52 / 1.99 | 3.15/0/1.00/3.65/1.47/2.29 |
| VIXY below 20d SMA | 363 | 69.7 | 1.55 | 20.3 | 5.4 | 0.99 | 88 / 3.19 | 1.20/.21/1.67/1.03/1.91/2.89 |
| IWM 20d RS vs SPY > 0 | 217 | 74.2 | 2.57 | 27.6 | 3.0 | 1.86 | 48 / 5.18 | 0.80/-/1.31/8.53/3.96/4.77 |
| IWM 20d RS vs SPY < 0 | 407 | 65.4 | 1.47 | 21.4 | 7.5 | 1.03 | 89 / 1.97 | 3.13/.13/1.30/1.29/1.19/2.10 |

Verdict: NOT a promotion candidate. Skipping panic (VIXY spikes) only lowers PF and return, so the live bot should keep buying fear. Splitting by VIXY state is unstable: "VIXY above SMA" has PF 2.06 but halves return and 2023 is 1.00; "below SMA" has the best L12 (3.19) but 2024 PF 1.03. IWM>SPY risk-on looks attractive (PF 2.57, L12 5.18) but it cuts trades to 217 and return by 54%, and its edge flips sign by year (2021 PF 0.80 vs 3.13 for the opposite half; 2024-26 the reverse), a regime drift not a stable filter, and the fear-spike subset is tiny (n=76, 2021 PF 23.8 from a handful of trades). None beats live on return, and both subsets together re-add up to the live book, so they only say where the live edge was earned in each era. Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; month-of-year seasonality within the live setup; true PEAD needs earnings data; bond ETFs (TLT/HYG) would need adding to the bars cache.

## 2026-11-07 (run 20) - Connors "Double 7" (7-day closing low, exit at 7-day closing high) as a stock sleeve (web idea)
Source: https://strategyquant.com/blog/larry-connors-double-7-strategy-tested-on-spy-and-8-other-markets/ , https://quantifiedstrategies.substack.com/p/larry-connors-double-seven-trading-bad , https://therighttrader.com/learn/trading-strategies/double-sevens-strategy (search results only, not fetched; marketed/index-level backtests, treated as unverified). Script lab_double7.py.
Rules: long when close is the lowest close of the last n days (n=7 main; 5 and 10 as robustness), close > SMA200 (variant: SMA50>SMA200 too), SPY>200d gate, ATR/price < 6%, 3-day cooldown, enter at close (+0.05% slip), stop 4 ATR, exit when close >= 7-day closing high (max hold 15) or prior-high exit with hold 7. Same simulator (10% x 12, 4/day), 8 variants counted (5 base + 3 breadth/combination rows).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (breadth+rank) ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| D7 n7 >SMA200, exit 7d high, hold 15 | 1678 | 66.2 | 1.14 | 44.2 | 22.3 | 0.52 | 371 / 1.29 | 1.07/.29/1.36/1.13/1.20/1.31 |
| D7 n7 >SMA200, prev-high exit, hold 7 | 2719 | 64.6 | 1.07 | 21.5 | 20.6 | 0.32 | 638 / 1.16 | 1.02/.35/1.01/1.18/1.11/1.26 |
| D7 n7, SMA50>200, exit 7d high | 1659 | 67.0 | 1.15 | 47.6 | 21.6 | 0.56 | 366 / 1.36 | 1.08/.26/1.25/1.21/1.19/1.39 |
| D7 n5, SMA50>200, prev-high exit | 2882 | 63.8 | 1.10 | 37.2 | 24.6 | 0.43 | 675 / 1.42 | 1.03/.41/.98/1.10/1.12/1.50 |
| D7 n10, SMA50>200, prev-high exit | 2287 | 62.6 | 1.08 | 21.8 | 19.8 | 0.35 | 553 / 1.26 | 1.00/.24/1.24/1.13/1.12/1.25 |
| D7 n7 + breadth>=10% | 1123 | 64.8 | 1.10 | 21.3 | 19.1 | 0.32 | 295 / 1.61 | 1.06/.21/1.03/1.27/.95/1.74 |
| LIVE + D7 n7 (breadth), 12 slots | 1131 | 64.9 | 1.12 | 24.9 | 19.1 | 0.36 | 297 / 1.62 | 1.07/.21/1.03/1.31/.96/1.75 |

Verdict: NOT a promotion candidate. A plain n-day closing low is a much weaker trigger than RSI2/IBS: PF 1.07-1.15 on 1,600-2,900 trades, drawdown 20-25% (3-4x live), 2022 0.2-0.4, and several non-2022 years at 1.0. Adding the breadth filter does not rescue it (PF 1.10). The "combined" rows are dominated by Double-7 signals crowding out the live trades from the same 12 slots (equal-score sleeve, no priority for live), so they show a worse-than-live result; a priority-aware combination was not worth running since the sleeve alone is this weak and the live setup stays unchanged. Consistent with run 4 (10-day-low variants PF 1.26 and below). Not added to challenger.py.
Follow-ups still untested: month-of-year seasonality inside the live setup; sleeve sizing at 5%; bond ETFs (TLT/HYG) need adding to the bars cache; true PEAD needs earnings data.

## 2026-11-07 (run 21) - month-of-year seasonality inside the LIVE setup (own idea; open follow-up from runs 18-20)
Source: none (own idea). Script lab_moy.py. Rules: LIVE setup (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank), trades bucketed by signal month; then skip-month variants incl. a walk-forward pick (3 worst months chosen on 2021-23 only, judged on 2024-26). Same simulator (10% x 12, 4/day), data through 2026-10-29. About 16 comparisons (12 month buckets + 4 skip rows): heavy multiple-comparison discount.

Per-month PF (n / all / 2021-23 / 2024-26): Jan 200/1.76/0.07/3.65, Feb 87/1.08/2.25/0.73, Mar 61/1.16/-/1.10, Apr 93/3.74/5.09/2.78, May 68/1.50/0.57/5.00, Jun 152/2.20/1.30/4.78, Jul 88/7.55/(few losses)/4.80, Aug 121/1.13/0.60/3.80, Sep 183/0.74/0.33/1.71, Oct 131/3.23/-/2.91, Nov 100/2.78/2.32/3.49, Dec 153/2.43/-/1.48.

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| skip Sep | 527 | 71.2 | 2.08 | 61.0 | 5.2 | 2.02 | 117 / 2.68 | 2.72/.13/1.89/2.15/2.14/2.72 |
| skip Sep+Oct | 470 | 72.3 | 2.03 | 50.3 | 5.2 | 1.89 | 107 / 2.69 | 2.62/.13/1.79/2.36/1.85/2.74 |
| skip Jan+Feb | 515 | 69.1 | 1.97 | 53.9 | 5.9 | 2.07 | 122 / 2.61 | no 2022 trades; 1.89/-/1.29/1.88/2.56/2.63 |
| skip worst3 on 2021-23 (Jan, Sep, May) | 438 | 71.9 | 2.31 | 59.3 | 5.5 | 2.27 | 103 / 2.72 | 2.68/-/2.19/2.11/2.06/2.79 |

Verdict: NOT a promotion candidate. Month buckets are 60-200 trades each and flip sign between eras: Jan is 0.07 in 2021-23 but 3.65 in 2024-26, Aug 0.60 then 3.80, May 0.57 then 5.00, Feb 2.25 then 0.73. The walk-forward pick (Jan, Sep, May) therefore fails out of sample for two of its three months (Jan and May are strongly positive in 2024-26); its PF 2.31 is mostly the removal of the 2022 bear trades (Jan/Sep/May 2022 happened to hold all of them) and total return does not rise (59.3 vs 59.6). "Skip Sep" is the only one with a persistent hint (PF 0.74 overall, 2024-26 PF 1.71, still the weakest month), improves PF 1.88 to 2.08 and return 61.0 vs 59.6, but return gain is within noise, 2024 is slightly lower (2.15 vs 2.19), and it is one post-hoc cut out of 12 months, so it fails the discipline. No stable calendar effect inside the live setup, consistent with run 18 (weekdays). Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG need adding to the bars cache; true PEAD needs earnings data; re-check Sep in 2027 as out-of-sample evidence accrues.

## 2026-11-07 (run 22) - limit-order pullback entry and next-open entry on the LIVE setup (web idea: Connors-style "buy on limit below the close")
Source: https://strategyquant.com/blog/larry-connors-double-7-strategy-tested-on-spy-and-8-other-markets/ and general Connors/Quantified Strategies write-ups on limit entries (search results from run 20, not fetched; marketed backtests, unverified). Script lab_limit.py.
Rules: LIVE signals (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank). Instead of filling at the signal close, (a) buy at the NEXT open, or (b) place a buy limit at signal close - k*ATR for the next session only (fills at min(open, limit) if the low reaches it, else no trade), k = 0.25/0.5/1.0/1.5. Stop 4 ATR below the fill, exit when close > prior high, max hold counted from the signal day. Same simulator (10% x 12, 4/day), 0.05% slippage, data through 2026-10-29. 5 variants counted.

| Variant | Fill rate | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref (signal close) | - | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| next-open entry | 100% | 635 | 67.7 | 1.55 | 44.2 | 7.0 | 141 / 1.89 | 1.92/.19/1.12/1.91/1.28/1.93 |
| limit close-0.25 ATR | 54% | 374 | 66.6 | 1.89 | 34.5 | 5.5 | 88 / 3.61 | 2.42/.29/.90/2.30/1.68/3.37 |
| limit close-0.5 ATR | 38% | 271 | 67.2 | 2.08 | 28.7 | 3.3 | 62 / 3.61 | 2.52/.22/1.29/2.82/1.88/2.93 |
| limit close-1.0 ATR | 14% | 117 | 67.5 | 2.32 | 13.4 | 2.0 | 28 / 2.72 | 1.32/.21/1.25/22.8/3.65/2.60 |
| limit close-1.5 ATR | 6% | 51 | 74.5 | 2.83 | 6.9 | 0.7 | 7 / 1.54 | 1.36/.71/4.46/48.8/18.1/1.39 |

(Raw fills of the 1437 pre-slot signals: next-open 1437, 0.25 ATR 781 (54%), 0.5 ATR 542 (38%), 1.0 ATR 208 (14%), 1.5 ATR 86 (6%).)

Verdict: NOT a promotion candidate. Limit entries raise per-trade quality a little (PF 1.89-2.32) because a fill requires a further drop, i.e. they are just a deeper-dip filter, but they miss most signals so return collapses (59.6% -> 34.5% at 0.25 ATR, 13% at 1.0 ATR) and 2023 gets worse (0.90-1.29 vs 1.42). Deep-limit rows rest on tiny samples (2024 PF 22-49 from a handful of trades). The more useful finding is the opposite direction: entering at the NEXT OPEN instead of the signal close costs about 0.33 PF and 15 points of return (1.88 -> 1.55, 59.6% -> 44.2%, 2025 1.92 -> 1.28), so the live edge depends on getting filled near the signal-day close; execution at the open the next day (or a late-day order before the close) is not equivalent. Whoever runs live should keep entries as close to the signal-day closing price as possible. Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG need adding to the bars cache; true PEAD needs earnings data; check how the live bot's real fills compare with signal-day closes (slippage audit) once enough paper fills exist.

## 2026-11-07 (run 23) - same-symbol re-entry memory on the LIVE setup (own idea: skip/favour a signal if the stock's previous signal-trade lost recently)
Source: none (own idea). Script lab_reentry.py. Rules: LIVE setup (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank); history = the unfiltered live signal-trade list; a signal is skipped/kept depending on the same stock's previous trade that exited within N days. Same simulator (10% x 12, 4/day), data through 2026-10-29. 5 variants counted.

| Variant | Signals kept | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 1437 | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| skip if prev trade lost <=20d | 1425 | 599 | 69.1 | 1.90 | 60.3 | 5.9 | 136 / 2.64 | 1.87/.16/1.42/2.21/1.92/2.67 |
| skip if prev trade lost <=60d | 1395 | 593 | 69.0 | 1.87 | 57.9 | 5.7 | 135 / 2.61 | 1.77/.16/1.41/2.21/1.89/2.63 |
| skip any re-entry <=20d | 1326 | 561 | 69.7 | 1.87 | 54.1 | 5.6 | 125 / 2.52 | 1.83/.19/1.48/2.19/1.99/2.38 |
| only re-entry after loss <=20d | 12 | 6 | - | - | 0.1 | - | too few | - |
| only re-entry after win <=20d | 99 | 56 | 57.1 | 1.47 | 2.8 | 2.5 | 13 / 5.48 | tiny samples |

Verdict: NOT a promotion candidate. Re-entries within 20 days are rare (about 1% of signals after a loss, 8% after any trade), so the filter changes almost nothing (PF 1.87-1.90, return within +-1 point, which is noise). The signal generator's own cooldown already limits repeat entries. Re-entries after a win are weaker (PF 1.47 on 56 trades, small sample), so no hint that a stock "in play" is better or worse. Stock-level path dependence is not an edge here. Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG need adding to the bars cache; true PEAD needs earnings data; next run should be a WEB-sourced idea (e.g. an out-of-sample re-check of Sep weakness, or Quantpedia ideas not yet covered such as short-term reversal with an overnight-gap component).

## 2026-11-08 (run 24) - 52-week-high proximity conditioning of the LIVE setup (web idea: George-Hwang anchoring / short-term reversal by distance from 52w high)
Source: https://www.cxoadvisory.com/technical-trading/proximity-to-52-week-high-and-short-term-momentum-reversal/ (search result only, not fetched; academic claim treated as unverified hypothesis). Script lab_prox.py. Rules: LIVE signals (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank); filter or rank by close / max(close, prior 252d). Same simulator (10% x 12, 4/day), data through 2026-10-29. 9 variants counted (heavy multiple-comparison discount). Signals lacking 252d history dropped for non-ref rows (1348 of 1437 kept).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| within 10% of high | 462 | 67.3 | 1.53 | 23.6 | 3.9 | 2.54 | 1.19/.13/1.33/1.87/1.74/2.23 |
| within 20% of high | 550 | 68.5 | 1.80 | 47.4 | 6.2 | 2.44 | 1.95/.13/1.36/2.24/1.69/2.54 |
| >10% below high | 155 | 74.8 | 2.92 | 29.9 | 3.0 | 3.55 | 2023 1.25 / 2024 2.85 / 2025 2.5 / 2026 4.33 |
| >20% below high | 32 | 71.9 | 2.59 | 6.0 | 2.1 | tiny | tiny samples |
| rank nearest-high (tiebreak / replace) | 569 / 567 | 68.9 / 68.3 | 1.89 / 1.89 | 56.3 / 57.1 | 5.9 / 6.3 | 2.65 / 2.74 | replace: 2023 1.17 |
| rank farthest (tiebreak / replace) | 569 / 575 | 68.9 / 68.5 | 1.89 / 1.77 | 56.3 / 47.6 | 5.9 | 2.65 / 2.71 | replace worse |

Verdict: NOT a promotion candidate. The published idea (reversal strongest near the 52w high) is not supported: near-high entries are WEAKER (PF 1.53 within 10%), and the better side is the opposite, entries more than 10% below the high (PF 2.92, win 75%), but that is 155 trades, return 29.9% vs 59.6% (capital idle), 2021 is a few-trade outlier, and it is the reverse of the source's claim, i.e. found post hoc. Ranking by proximity is reshuffling noise (PF 1.77-1.89). Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG in bars cache; true PEAD needs earnings data; a size-up tier (not filter) for entries >10% below high.
