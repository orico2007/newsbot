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

## 2026-11-09 (run 6) - stochastic pullback sleeve (web idea)
Source: https://quantifiedstrategies.substack.com/p/a-simple-stochastic-pullback-strategy (claims SPY: 195 trades, 74% win, PF 2.3; exact rules are paywalled/in an image, so parameters below are my own guesses; claimed numbers unverified, single index, cost-free). Rules: long when fast Stochastic %K (lookback N) < K, close > SMA200, SPY>200d gate, ATR/price < 6%, 3-day cooldown, enter at close (+0.05% slip), stop 4 ATR, exit close > prior high, max hold 7. Same simulator (10% x 12, 4/day), standalone and combined with champion (shared slots). Script: lab_stoch.py. 5 variants tried (multiple-comparison discount; no year selection, all reported).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| %K(5)<10 | 2113 | 61.9 | 1.10 | 28.9 | 15.0 | 519 / 1.2 | 1.29/.30/1.02/1.17/1.06/1.29 |
| %K(5)<5 | 1583 | 64.8 | 1.25 | 56.5 | 12.8 | 404 / 1.47 | 1.57/.35/1.13/1.27/1.14/1.48 |
|   + champion combined | 1784 | 64.2 | 1.22 | 57.8 | 13.3 | 445 / 1.33 | 1.46/.21/1.18/1.45/1.06/1.36 |
| %K(5)<20 | 2654 | 62.6 | 1.06 | 18.2 | 16.8 | 633 / 1.14 | - |
| %K(14)<10 | 1593 | 62.3 | 1.18 | 37.9 | 13.4 | 390 / 1.27 | 1.38/.17/1.37/1.17/1.03/1.34 |
| %K(5, 3-smoothed)<15 | 1549 | 64.9 | 1.19 | 36.4 | 9.5 | 399 / 1.17 | 1.38/.31/1.12/1.28/1.31/1.16 |

Verdict: NOT a promotion candidate. Stochastic oversold is a looser, noisier version of the RSI2/IBS signal: more trades, PF 1.06-1.25 (monotonic: the tighter the threshold, the better, converging toward the champion's RSI2<5), drawdown 9-17% vs 6%, and every combined portfolio is worse than the champion on PF and Sharpe. Adds no independent edge; marketed PF 2.3 did not replicate on single stocks. Not added to challenger.py. Next run should be an own idea (B): e.g. a sleeve with its own non-shared slots for the gap-recover signal, or why gap-recover fails 2023.

## 2026-11-09 (run 7) - gap-recover sleeve re-tested on top of the NEW live setup (own idea, follow-up of run 5)
Source: none (own idea). Runs 3-6 used the old baseline (PF 1.40); this re-tests the best complement (gap-down then close>open) against the current live champion (breadth>=10% gate + weakest-peer rank, PF 1.88). Rules: gap-recover long, close > SMA200, SPY>200d gate, ATR/price<6%, 3-day cooldown, stop 4 ATR, exit close > prior high, hold 7; sleeve signals also pass the breadth>=10% gate and are ranked by weakest sector peers (same as live); shared slots (10% x 12, 4/day). Script: lab_gap2.py. 6 variants (3 gap thresholds x 2 priority orders; priority order made no difference to the sleeve alone). Multiple-comparison discount applies; no year selection.

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE champion | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| gap<-1% alone | 927 | 66.6 | 1.21 | 25.9 | 9.4 | 0.74 | 295 / 1.34 | 1.07/.40/.95/1.30/1.84/1.35 |
|   + live | 1190 | 67.0 | 1.40 | 67.0 | 12.1 | 1.20 | 343 / 1.60 | 1.28/.35/1.07/1.61/1.84/1.64 |
| gap<-2% alone | 418 | 69.1 | 1.14 | 9.2 | 11.0 | 0.34 | 124 / 1.11 | 4.12/.18/.74/1.17/2.13/1.08 |
|   + live | 864 | 68.4 | 1.48 | 58.7 | 11.4 | 1.24 | 220 / 1.62 | 2.28/.14/.96/1.78/2.33/1.52 |
| gap<-3% alone | 194 | 73.2 | 1.39 | 10.9 | 3.8 | 0.65 | 69 / 0.95 | 4.90/.69/.96/1.51/2.21/.94 |
|   + live | 716 | 69.7 | 1.76 | 69.1 | 4.9 | 1.92 | 178 / 1.69 | 2.20/.20/1.43/2.32/1.92/1.65 |

Verdict: NOT a promotion candidate. Once the live breadth gate and peer ranking are applied, the gap-recover sleeve loses most of its earlier appeal: alone PF 1.14-1.39, L12 PF 0.95-1.34 (the -3% sleeve is flat/losing in the last 12 months and 2026), and 2023 is below 1 at every threshold. Combined with live, PF falls (1.40-1.76 vs 1.88) and last-12-month PF falls (1.60-1.69 vs 2.65); only gap<-3% raises return (69.1 vs 59.6%) and Sharpe (1.92 vs 1.85), with lower drawdown than other sleeves (4.9 vs 5.9 live), but it fails on PF, L12 and 2026. The earlier "good complement" read was an artifact of the weaker old baseline; the live filters already capture the same washout days. Gap-recover is closed as an idea. Not added to challenger.py. Next run should be web research (A): e.g. sector-relative reversion is already covered by the peer rank, so try post-earnings drift if earnings dates are available (earnings.py), or a documented market-breadth thrust/short-term reversal-after-selloff rule from Quantpedia.

## 2026-11-09 (run 8) - realized-volatility / beta / price conditioning of the LIVE setup (web idea)
Source: https://alphaarchitect.com/how-volatility-and-turnover-affect-return-reversals/ (claim: higher volatility -> faster, initially stronger reversals; unverified, other construction/market). Rules: take the live setup's trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day) and keep only signals by 60-day stdev of daily returns (vol60, %), SPY beta (60d), or price. Terciles computed on the whole sample (mild look-ahead); absolute thresholds reported too. Scripts: lab_beta.py, lab_beta2.py. 17 variants tried (multiple-comparison discount applies; no year selection, all reported).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE champion | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| vol60 low tercile (<1.42) | 240 | 67.1 | 1.24 | 4.8 | 3.7 | 0.65 | 21 / 2.0 | 1.11/.12/.92/1.46/2.69/1.06 |
| vol60 mid tercile | 211 | 66.4 | 1.18 | 4.0 | 4.5 | 0.41 | 48 / 1.69 | .60/.02/1.77/1.64/1.46/1.42 |
| vol60 high tercile (>=1.95) | 244 | 75.8 | 3.38 | 58.0 | 4.7 | 2.46 | 79 / 4.03 | 8.05/1.38/1.46/4.63/2.55/4.61 |
| beta high tercile (>=1.27) | 218 | 72.0 | 2.85 | 42.0 | 4.9 | 2.29 | 50 / 3.86 | 2.54/-/1.47/5.02/2.36/3.85 |
| beta low / mid tercile | 236 / 228 | 67 | 1.37 / 1.34 | 7.1 / 8.4 | 4.4 / 3.4 | .72 / .71 | 65 / 2.44, 31 / 1.86 | weak, 2024 PF 1.0 for low |
| price < $50 / >= $50 | 80 / 559 | 67.5 / 68.5 | 1.86 / 1.77 | 7.0 / 47.7 | 2.7 / 5.3 | 0.9 / 1.77 | 6 / 2.43, 131 / 2.69 | no signal |
| vol60 >= 1.5 | 382 | 71.7 | 2.33 | 59.8 | 4.9 | 2.05 | 117 / 3.44 | 1.74/.19/1.66/3.15/2.10/3.52 |
| vol60 >= 1.75 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| vol60 >= 2.0 | 235 | 75.7 | 3.39 | 56.8 | 4.5 | 2.45 | 76 / 4.13 | 7.68/1.38/1.42/4.62/2.60/4.80 |
| vol60 >= 2.5 | 139 | 74.8 | 3.30 | 35.8 | 2.5 | 2.07 | 43 / 4.08 | 3.99/-/1.91/4.37/2.02/5.42 |
| vol60 >= 3.0 | 86 | 77.9 | 3.22 | 24.0 | 2.4 | 2.09 | 34 / 3.83 | 2.16/-/2.33/4.31/1.81/5.24 |
| rank by vol60 (no filter) | 605 | 68.1 | 1.82 | 57.6 | 6.6 | 1.64 | 137 / 2.81 | no gain |
| vol>=2.0 first, others as filler | 607 | 69.0 | 1.92 | 62.4 | 5.9 | 1.82 | 138 / 2.84 | 2.02/.13/1.25/2.27/2.13/2.70 |

Verdict: PROMOTION CANDIDATE (filter, not rank): restrict live entries to stocks with 60d daily-return stdev >= ~1.75%. Dose-response is monotonic across thresholds 1.5 -> 3.0 (PF 2.33, 2.83, 3.39, 3.30, 3.22; win 72-78%), not a single lucky cutoff; the low/mid-vol terciles are poor (PF 1.2) so nearly all of the champion's edge sits in volatile stocks. At >=1.75: PF 2.83 vs 1.88, return 60.6 vs 59.6%, Sharpe 2.28 vs 1.85, drawdown 4.3 vs 5.9%, L12 PF 3.37 vs 2.65, and PF higher in 2021, 2023, 2024, 2025 and 2026 (2022 0.87 vs 0.13; every non-2022 year better). Caveats: (1) return is flat, not higher, because ~half the signals are dropped and the cash sits idle - the gain is risk-adjusted; pairing with more slots/larger size for the high-vol bucket is the obvious next test; (2) the cached universe is a fixed list and may favour survivors, so high-vol names that did well are overrepresented; (3) terciles used full-sample cutoffs, but fixed absolute thresholds agree; (4) 17 variants tried, but the effect is large and consistent across 6 years. Rank-only use (vol as priority) adds nothing, because the live rank already picks few signals per day. Added to challenger.py as "live_vol175" so the weekly job tracks it. The daily improvement task decides on any live change. Follow-ups: size-up (e.g. 15% per position or 8 slots at 15%) for vol60>=1.75 only; ATR% vs stdev as the volatility measure; check that vol filter is not just proxying high beta (beta-high tercile PF 2.85 overlaps).

## 2026-11-09 (run 9) - sizing up the vol60>=1.75% live setup, vol-vs-beta disentangling, early/late split (own idea, follow-up of run 8)
Source: none (own idea). Rules: LIVE setup (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR) filtered to 60d daily-return stdev >= 1.75%; vary only portfolio size/slots; split by SPY beta(60d); choose threshold on 2021-23, check on 2024-26. Script: lab_volsize.py. 12 portfolio/split variants plus 8 early/late rows (multiple-comparison discount; all reported, nothing dropped).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE 10x12 | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| vol>=1.75, 10x12 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| vol>=1.75, 12x10 | 308 | 74.4 | 2.83 | 76.5 | 5.2 | 2.28 | 100 / 3.37 | same |
| vol>=1.75, 15x8 (4/day) | 308 | 74.4 | 2.83 | 103.2 | 6.4 | 2.28 | 100 / 3.37 | same |
| vol>=1.75, 20x6 (3/day) | 295 | 73.9 | 2.73 | 137.7 | 8.5 | 2.29 | 96 / 3.10 | 2.29/.87/1.48/4.90/2.35/3.19 |
| vol>=1.75 & beta<1.0 | 83 | 71.1 | 2.12 | 7.9 | 1.6 | 1.37 | 44 / 2.66 | 1.36/0/3.38/5.34/1.54/2.22 |
| vol<1.75 & beta>=1.0 | 99 | 71.7 | 2.06 | 7.7 | 1.8 | 1.69 | 6 / - | 3.74/-/1.23/2.26/1.21/- |
| vol>=1.75 & beta<1.27 | 126 | 73.0 | 2.21 | 13.2 | 1.3 | 1.56 | 54 / 2.80 | 1.69/0/3.36/2.56/1.31/3.16 |
| vol<1.75 & beta>=1.27 | 40 | 65.0 | 1.41 | 1.3 | 1.0 | 0.66 | 1 / - | weak |
| EARLY 2021-23: vol>=0 / 1.5 / 1.75 / 2.0 | 221/125/99/72 | 64.7/65.6/70.7/73.6 | 1.38/1.51/1.89/2.49 | - | - | - | - | monotonic in threshold |
| LATE 2024-26: vol>=0 / 1.5 / 1.75 / 2.0 | 383/257/209/163 | 71.5/74.7/76.1/76.7 | 2.25/2.92/3.48/3.93 | - | - | - | L12 2.65/3.44/3.37/4.13 | monotonic in threshold |

Findings: (1) Sizing does not change PF/trade set at 10-15% (the 12-slot cap rarely binds for the filtered list); it only scales return and drawdown roughly linearly: 15x8 gives +103% / DD 6.4% vs live +60% / DD 5.9%, i.e. about 1.7x the return for ~0.5pt more drawdown. 20x6 reaches 138% but DD 8.5% and lower PF (fewer slots, signals dropped). (2) The vol effect is not just beta: vol>=1.75 with beta<1.0 still has PF 2.12, while high-beta but low-vol is weaker only when beta>=1.27 (PF 1.41); vol and beta both carry signal and overlap, samples in the cross cells are small (40-126 trades), treat as indicative only. (3) Out-of-sample style check: the dose-response (PF rising with the vol threshold) shows up in the early years alone (1.38 -> 1.89 -> 2.49) and again in the late years alone (2.25 -> 3.48 -> 3.93), and the 1.75 cutoff was fixed in run 8 on the full sample, so this is a consistency check rather than a sealed test. 2026 has not been held out here (it is inside the cached sample and is included in L12).
Verdict: PROMOTION CANDIDATE reaffirmed (vol60>=1.75% filter). Optional sizing: 15% x 8 positions, 4/day gives the best return/DD tradeoff of those tried; added to challenger.py as "lab: live setup + vol60>=1.75%, size 15% x 8" so the weekly job tracks it. Caveat unchanged: fixed universe may favour survivors; fewer trades (308 vs 604 over ~5.8y) means higher variance per trade, and larger sizes concentrate risk on volatile names (max loss per position bigger in dollars). Daily improvement task decides. Follow-ups: realistic gap/stop slippage stress for high-vol names (stop 4 ATR may fill worse), and test vol filter on the sector-ETF/bear sleeves.

## 2026-11-09 (run 10) - MAX / lottery effect as a conditioner of the LIVE setup, controlling for vol60 (web idea)
Source: https://nber.org/papers/w14804 (Bali/Cakici/Whitelaw "Maxing Out": stocks with extreme max daily return in the past month; claim is mostly about the cross-section of monthly returns, other construction; unverified here). Search results otherwise only returned TradingView scripts (no usable evidence). Rules: live setup (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day); keep signals by MAX = max daily return over the prior 21 sessions (%), alone and inside the vol60 buckets from run 8. Terciles full-sample (mild look-ahead; terciles 2.46 / 4.13). Script: lab_max.py. 17 variants (multiple-comparison discount applies; all reported).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE champion | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| MAX low tercile | 234 | 67.5 | 1.12 | 2.6 | 2.9 | 0.28 | 26 / 1.09 | 1.29/.08/.97/1.41/1.39/.82 |
| MAX mid tercile | 222 | 65.8 | 1.26 | 5.9 | 4.6 | 0.46 | 48 / 2.59 | .88/0/.91/1.82/1.41/1.88 |
| MAX high tercile (>=4.13) | 246 | 74.0 | 2.93 | 51.2 | 4.1 | 2.18 | 74 / 3.97 | 2.69/.40/1.22/4.27/2.90/4.65 |
| MAX>=3% | 356 | 70.5 | 2.33 | 53.9 | 5.9 | 1.93 | 103 / 3.52 | 1.98/.20/1.03/3.60/2.45/3.64 |
| MAX>=5% | 188 | 76.1 | 3.14 | 40.8 | 2.4 | 2.30 | 58 / 4.65 | 4.52/.06/2.10/2.89/2.34/6.33 |
| MAX>=6% / >=8% | 145 / 81 | 73.8 / 67.9 | 2.75 / 2.00 | 26.2 / 9.5 | 1.9 / 1.7 | 1.94 / 1.09 | 46 / 3.74, 29 / 2.62 | non-monotonic above 5% |
| vol>=1.75 (run 8 candidate) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| vol>=1.75 & MAX>=4% | 210 | 74.8 | 2.98 | 47.0 | 3.9 | 2.19 | 70 / 3.80 | 2.75/.87/1.17/4.85/2.71/4.43 |
| vol>=1.75 & MAX<4% | 116 | 73.3 | 2.02 | 9.5 | 2.8 | 1.09 | 32 / 2.35 | 1.94/-/1.20/5.47/2.06/1.76 |
| vol>=1.75 & MAX>=6% / <6% | 134 / 193 | 74.6 / 73.6 | 2.87 / 2.76 | 26.0 / 29.9 | 2.1 / 3.3 | 1.99 / 2.07 | 44 / 3.65, 60 / 3.10 | no difference |
| vol<1.75 & MAX<4% | 323 | 64.4 | 1.03 | 0.8 | 5.6 | 0.06 | 41 / 1.59 | 1.03/.05/1.14/1.04/1.44/1.27 |
| vol<1.75 & MAX>=4% | 52 | 71.2 | 2.08 | 3.5 | 1.3 | 1.28 | 5 / - | tiny sample |

Verdict: NOT a promotion candidate; MAX is largely a proxy for the vol60 effect already found in run 8. Alone it looks as good (MAX>=4%: PF 2.81, win 73%, L12 3.98) but 2023 is weak (1.03-1.22) and it is no better than vol60>=1.75 on return, drawdown or Sharpe. Controlling for vol, MAX adds little: inside vol>=1.75, MAX>=4% vs <4% is PF 2.98 vs 2.02 (return mostly from more trades), and MAX>=6% vs <6% is 2.87 vs 2.76 (no difference). The informative finding is the negative one: signals with vol60<1.75 AND MAX<4% (323 trades, over half of the low-vol bucket) have PF 1.03 and 0.8% return in 5.8 years, i.e. no edge at all, which reinforces the run 8 vol filter. Not added to challenger.py. Next: run 11 should be own idea (B): the slippage/gap stress on the vol60>=1.75 candidate (stop fills worse for volatile names) since the daily task may adopt it; or ATR% as the volatility measure.

## 2026-11-09 (run 11) - execution-cost and stop-gap slippage stress: LIVE vs vol60>=1.75% candidate (own idea, follow-up of runs 8-9)
Source: none (own idea). Rules: same trade sets as run 9 (LIVE setup, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day), baseline sim cost 0.05% per side. Subtract an extra round-trip cost (0.1 / 0.2 / 0.4%) from every trade and/or an extra 1-2% fill penalty on stop-outs (R <= -0.99), then rerun the portfolio simulator. Script: lab_slip.py. 17 variants (stress grid, all reported; nothing selected, so no winner bias).
Stop frequency: only 33 of 1437 raw LIVE trades (2 in the vol>=1.75 raw set of 638) hit the 4-ATR stop, and gaps beyond the stop are about 2, so stop slippage is nearly irrelevant; round-trip cost is what matters.

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE base | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| vol>=1.75 base | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| LIVE +0.1% rt | 604 | 69.0 | 1.74 | 50.2 | 6.3 | 1.61 | 2.49 | 1.74/.12/1.31/2.01/1.78/2.52 |
| vol>=1.75 +0.1% rt | 308 | 74.4 | 2.66 | 55.8 | 4.5 | 2.15 | 3.17 | 2.26/.78/1.52/4.44/2.36/3.21 |
| LIVE +0.2% rt | 604 | 69.0 | 1.61 | 41.4 | 6.6 | 1.37 | 2.33 | 1.61/.11/1.21/1.85/1.64/2.36 |
| vol>=1.75 +0.2% rt | 308 | 74.4 | 2.50 | 51.1 | 4.6 | 2.02 | 2.99 | 2.13/.70/1.43/4.14/2.21/3.03 |
| LIVE +0.4% rt | 604 | 69.0 | 1.37 | 25.4 | 7.3 | 0.89 | 2.04 | 1.36/.08/1.02/1.55/1.40/2.07 |
| vol>=1.75 +0.4% rt | 308 | 74.4 | 2.20 | 42.0 | 4.9 | 1.75 | 2.65 | 1.88/.55/1.26/3.59/1.94/2.68 |
| LIVE +0.4% rt, +2% on stops | 604 | 69.0 | 1.31 | 21.9 | 7.3 | 0.76 | 2.01 | 2023 PF 0.97 |
| vol>=1.75 +0.4% rt, +2% on stops | 308 | 74.4 | 2.19 | 41.8 | 4.9 | 1.74 | 2.65 | 1.80/.55/1.26/3.59/1.94/2.68 |
| vol>=1.75 same stress, 15% x 8 | 308 | 74.4 | 2.19 | 68.4 | 7.3 | 1.74 | 2.65 | same |
| stop penalty only (+1% / +2%) | LIVE PF 1.83 / 1.78; vol>=1.75 PF 2.82 / 2.81 | | | | | | | negligible |

Findings: (1) The unfiltered LIVE setup is fragile to execution cost: each extra 0.1% round trip costs about 0.13 PF and ~9 points of return; at +0.4% (total ~0.5% round trip, plausible for closing-auction market orders in smaller names) PF falls to 1.37, return 25%, Sharpe 0.89 and 2023 is at breakeven. (2) The vol60>=1.75% subset degrades much more gracefully (PF 2.83 -> 2.20, return 60.6 -> 42.0%, Sharpe 1.75, every non-2022 year still PF > 1.25) because its average trade is larger in % terms, so a fixed cost eats less. At every cost level it beats LIVE on PF, return, drawdown and Sharpe. (3) Stop gaps are a non-issue (stops rarely trigger). (4) With 15% x 8 under heavy stress the candidate still returns 68% at 7.3% drawdown, above LIVE base risk-adjusted. Caveat: costs are applied uniformly; real slippage is likely lower for liquid names but higher on the volatile ones the filter selects, which is why the 0.2-0.4% rows matter. Paper-trading fills can measure the true cost: compare the bot's logged fill prices against the signal-day close.
Verdict: strengthens the run 8/9 PROMOTION CANDIDATE (vol60>=1.75%); no new variant (already in challenger.py). Next: web-research run (post-earnings/sector-rotation or NR7-type ideas not yet tested), and an ATR% volatility measure.

## 2026-11-09 (run 12) - ATR% (ATR14/close) as the volatility measure on the LIVE setup, vs vol60 stdev (own idea, follow-up of runs 8-11)
Source: none (own idea). Rules: live setup (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day); keep signals by ATR% on the signal day, alone and crossed with vol60>=1.75. Terciles full-sample (1.83 / 2.44, mild look-ahead); early (2021-23) / late (2024-26) split. Script: lab_atr.py. 21 variants (multiple-comparison discount; all reported).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE champion | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| ATR% low tercile (<1.83) | 232 | 65.1 | 0.99 | -0.3 | 5.8 | -0.03 | 17 / 2.36 | .79/.05/.77/1.13/1.80/1.75 |
| ATR% mid | 221 | 67.0 | 1.39 | 8.6 | 4.0 | 0.75 | 43 / 1.75 | .67/.05/2.14/2.15/1.70/1.47 |
| ATR% high (>=2.44) | 250 | 74.0 | 2.92 | 50.8 | 4.3 | 2.22 | 87 / 3.49 | 5.31/.57/1.38/4.94/2.11/3.70 |
| ATR%>=2.5 | 237 | 75.1 | 2.99 | 48.8 | 4.3 | 2.13 | 83 / 3.69 | 4.96/1.89/1.02/4.87/2.35/4.03 |
| ATR%>=3 | 153 | 73.9 | 3.40 | 40.7 | 2.4 | 2.27 | 56 / 4.19 | 6.17/1.38/1.63/4.30/2.13/5.07 |
| ATR%>=3.5 | 102 | 74.5 | 3.14 | 27.2 | 3.1 | 1.80 | 40 / 4.38 | 4.28/-/1.12/4.17/1.34/6.45 |
| ATR%>=4 | 71 | 74.6 | 2.72 | 18.9 | 2.4 | 1.61 | 33 / 4.42 | 2.71/-/1.71/3.31/.96/6.99 |
| vol60>=1.75 (run 8 candidate) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| vol>=1.75 & ATR%<3 | 173 | 74.0 | 2.14 | 16.2 | 2.7 | 1.45 | 44 / 2.19 | 1.10/.26/1.81/4.45/2.72/1.68 |
| (ATR%>=3 is entirely inside vol>=1.75: vol<1.75 & ATR%>=3 has 0 signals) | | | | | | | | |
| EARLY ATR%>=0 / 3 / 4 | 221 / 48 / 17 | 64.7 / 75 / 76.5 | 1.38 / 2.74 / 2.13 | | | | | monotonic then small n |
| LATE ATR%>=0 / 3 / 4 | 383 / 105 / 54 | 71.5 / 73.3 / 74.1 | 2.25 / 3.74 / 2.92 | | | | | peak at 3 |

Findings: ATR% reproduces the vol60 result (low tercile has no edge, PF 0.99; high tercile PF 2.92) so the volatility effect is robust to the measure used, which lowers the chance it is an artifact of stdev. But ATR% is not better than vol60 as a filter: ATR%>=3 has a higher PF (3.40) and L12 PF (4.19) yet only 153 trades, return 40.7% vs 60.6% for vol60>=1.75, and it is a strict subset of it. Beyond ATR% 3 the PF falls (3.5: 3.14, 4: 2.72), with 2025 at 0.96-1.34, so there is no further dose-response gain. Inside vol>=1.75, the ATR%<3 half still has PF 2.14 but return of only 16%. Early-years-only check: threshold 3 gives PF 2.74 on 48 trades (vs 1.38 unfiltered), late 3.74, so the direction holds out of sample but the early sample is tiny.
Verdict: NOT a new promotion candidate; confirms the run 8 candidate (vol60>=1.75%) with an independent volatility measure. Prefer vol60>=1.75 over ATR% thresholds because it keeps twice the trades and the full return; ATR%>=3 would only make sense as a high-conviction tier (e.g. larger size) and is thin. Not added to challenger.py. Next: web-research run (post-earnings drift or pairs/relative-value idea not yet tested), or a two-tier sizing test (15% for ATR%>=3, 10% for the rest of vol>=1.75).

## 2026-11-10 (run 13) - volume-conditioned reversal (Campbell-Grossman-Wang) on the LIVE setup (web idea)
Source: https://dash.harvard.edu/bitstream/1/3128710/2/campbell_trading.pdf (claim: price declines on LOW volume reverse, declines on HIGH volume continue; other era/construction, unverified). Rules: live setup trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day); keep signals by signal-day volume / 20d-avg volume (r1) or 3-day average of it (v3); terciles full-sample (mild look-ahead) plus absolute cutoffs. Script: lab_volrev.py. ~22 variants (multiple-comparison discount; all reported).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE champion | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| r1 low tercile (<0.87) | 246 | 67.5 | 1.43 | 10.9 | 3.9 | 0.83 | 59 / 2.43 | 1.48/0/.88/1.38/1.19/2.74 |
| r1 mid | 265 | 69.8 | 1.78 | 19.7 | 2.9 | 1.64 | 56 / 2.11 | 1.03/.18/1.69/4.34/1.72/1.98 |
| r1 high (>=1.28) | 253 | 68.4 | 1.85 | 23.3 | 4.1 | 1.47 | 45 / 3.53 | 2.08/.10/1.08/2.53/1.80/3.01 |
| v3 low (<0.85) | 235 | 65.1 | 1.32 | 8.2 | 3.1 | 0.62 | 57 / 1.62 | .84/0/1.29/2.04/1.07/1.65 |
| v3 mid | 260 | 67.3 | 1.61 | 17.1 | 4.3 | 1.03 | 54 / 2.31 | 1.35/.04/.92/3.19/1.87/2.11 |
| v3 high (>=1.10) | 249 | 71.9 | 2.15 | 26.8 | 4.9 | 1.89 | 46 / 5.03 | 2.00/.33/1.58/2.35/1.75/4.70 |
| r1 >=1.0 / <1.0 | 392 / 312 | 67.1 / 67.9 | 1.81 / 1.51 | 35.1 / 16.2 | 4.8 / 4.1 | 1.57 / 1.03 | 74 / 2.93, 80 / 2.39 | |
| r1 >=1.5 / >=2.0 | 154 / 47 | 66.2 / 66.0 | 1.60 / 2.28 | 10.7 / 7.1 | | | 29 / 3.88, 4 | thin |

Verdict: NOT a promotion candidate; the paper's prediction (high-volume declines should NOT revert) is not supported: high-volume signals revert as well or slightly better (v3 high tercile PF 2.15, L12 5.03), and very-low-volume signals are the weakest (v3 low PF 1.32, r1 low 1.43). No bucket beats the champion on return (each tercile is a third of the trades, ~8-27% return) and 2023 is weak in several buckets. The gradient is monotonic but mild versus the volatility effect (PF 1.2 -> 3.4 across vol60 terciles, run 8), and volume likely correlates with it. At most a weak hint that skipping very-low-volume signals (v3<0.85) removes ~235 poor trades; untested in combination with the vol60>=1.75 candidate. Not added to challenger.py. Next: test v3 < 0.85 exclusion on top of vol60>=1.75, or a web idea on sector rotation/pairs not yet logged.

## 2026-11-10 (run 14) - idiosyncratic vs market-wide oversold reversion (web-inspired: short-term/residual reversal literature)
Source: https://www.quantconnect.com/research/15311/short-term-reversal-strategy-in-stocks/ , https://www.cxoadvisory.com/technical-trading/reviving-short-term-reversal/ (residual / market-adjusted short-term reversal, published on monthly cross-sections; search snippets only, unverified daily-bar translation).
Rules: long, RSI2<10, close > SMA200, SPY>200d gate, ATR/price<6%, 3-day cooldown, enter at close (+0.05% slip), stop 4 ATR, exit on close > prior high, max hold 7. Split by cause of the drop: rel = stock 3d return minus SPY 3d return; idio-N = rel < -N% AND SPY 3d > -1%; sys = SPY 3d < -2%. Same simulator (10% x 12, 4/day), standalone and combined with champion (shared slots). Script: lab_resid.py. 6 variants tried (multiple-comparison discount; data through 2026-10-29, 2026 not used to select anything).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| rsi2<10 (base) | 2083 | 63.9 | 1.20 | 60.5 | 14.6 | 490 / 1.15 | 1.19/.21/1.26/1.31/1.46/1.15 |
| idio-3 | 1296 | 61.1 | 1.03 | 4.4 | 12.1 | 329 / 0.96 | 1.11/.07/1.30/1.12/1.08/1.00 |
| idio-5 | 671 | 61.3 | 1.15 | 14.3 | 7.9 | 212 / 0.95 | 1.18/.08/1.97/1.34/1.19/.96 |
|   + champion combined | 1159 | 63.7 | 1.30 | 47.7 | 9.3 | 299 / 1.22 | 1.26/.08/1.72/1.53/1.40/1.18 |
| idio-8 | 197 | 62.9 | 1.45 | 12.8 | 2.6 | 59 / 1.45 | 1.38/0/3.99/1.12/1.45/1.55 |
| sys (SPY 3d < -2%) | 177 | 66.7 | 1.49 | 12.4 | 5.4 | 18 / 0.87 | 3.74/.24/1.15/2.57/1.61/.81 |
| not idio-5 | 1894 | 63.8 | 1.17 | 42.3 | 17.3 | 443 / 1.35 | 1.12/.20/1.01/1.37/1.40/1.32 |

Verdict: NOT a promotion candidate. Stock-specific drops (the residual-reversal prediction) do NOT revert better than market-wide ones on this universe: idio-3/5 are worse than the base trigger (PF 1.03-1.15, L12 PF below 1). Only the extreme idio-8 (197 trades) and sys (177 trades, L12 only 18 trades) reach PF ~1.45-1.5, both too few trades, erratic by year (2023 PF 3.99, 2022 PF 0) and consistent with chance after 6 variants. Combining with the champion lowers PF (1.30 vs 1.40) and doubles drawdown. Not added to challenger.py. Follow-ups: sector-ETF-relative (not SPY-relative) drop, which needs a stock-to-sector map; gap sleeve with its own non-shared slots; pairs/relative value.

## 2026-11-10 (run 15) - down-close streak length and SMA50 context inside the LIVE setup (lab_streak.py)
Live: n=604 PF 1.88 ret 59.6% Sharpe 1.85. Streak>=2: PF 1.79 / ret 51.7. Streak>=3: n=487 win 71.0 PF 2.03 ret 50.6 Sharpe 2.0 (2021 1.98, 23 1.50, 24 2.79, 25 1.98, 26 2.73). Streak<=2: n=204 PF 1.27 ret 6.3 (weak). close>SMA50 is already implied by the rules (identical to live). Result: longer streaks are better quality but the filter cuts total return (50.6 < 59.6), so it fails the return bar; 4 variants tried, selection discount applies. Not promoted, not added to challenger.py.


## 2026-11-10 (run 16) - stock-quality filters (126d momentum, 60d vol, SMA200 slope, 252d range position) on the LIVE setup (web-inspired: RSI2 + momentum/low-vol filter write-ups)
Source: web search only returned generic RSI(2) pages (https://www.mql5.com/en/articles/17636, https://dev.to/fmzquant/mean-reversion-rsi2-momentum-breakout-trading-strategy-with-moving-average-trend-filter-2iac); no testable specific claim, so this is an own-idea translation. Rules: live setup trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day); keep signals by feature on signal day; median splits full-sample (mild look-ahead). Script: lab_qual.py. 8 split variants + 6 fixed vol thresholds + 3 vol bands (multiple-comparison discount; all reported). NOTE: the vol60 result re-derives run 8 independently; the lab_log.md at HEAD had lost runs 8-13 in a concurrent overwrite, which this commit restores (the runs 6-7 written on 11-10 are renumbered 14-15).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| mom126 > median | 340 | 69.4 | 1.94 | 39.3 | 4.3 | 3.88 | 1.56/.19/1.22/2.2/1.96/3.97 |
| mom126 < median | 330 | 67.3 | 1.62 | 17.1 | 3.2 | 1.93 | 1.63/.07/1.73/1.81/1.67/1.92 |
| mom126 > 0 | 571 | 69.0 | 1.91 | 57.8 | 5.4 | 2.88 | 1.72/.16/1.48/2.19/1.82/2.99 |
| rvol60 < median | 336 | 64.3 | 1.07 | 2.1 | 5.9 | 1.56 | 1.06/.05/1.06/1.15/1.95/1.22 |
| rvol60 > median (1.64%) | 333 | 73.6 | 2.61 | 60.2 | 4.9 | 3.36 | 2.09/.87/1.52/4.19/2.18/3.43 |
| rvol60 > 1.4 / 1.6 / 1.8 / 2.0% | 418/350/286/229 | 70.6-75.5 | 2.14/2.59/2.86/3.42 | 55.9/62.2/55.8/55.5 | 4.9/4.9/4.3/4.5 | 2.83/3.45/3.32/4.08 | monotone in threshold |
| rvol60 bands <1.35 / 1.35-1.85 / >=1.85 | 217/213/273 | 67.3/66.2/74.7 | 1.16/1.20/3.07 | 3.0/4.4/58.0 | | 1.64/1.80/3.76 | only top band has edge |
| SMA200 rising | 566 | 68.2 | 1.86 | 53.9 | 5.9 | 2.57 | no gain |
| 252d range pos > median | 316 | 69.0 | 2.12 | 30.6 | 2.5 | 4.68 | 1.18/.19/1.85/2.45/3.25/4.04 |
| 252d range pos < median | 333 | 69.4 | 1.80 | 28.7 | 4.3 | 2.44 | 3.04/.08/1.05/2.29/1.64/2.52 |
| rank by HIGH rvol first (no filter) | 605 | 68.1 | 1.82 | 57.6 | 6.6 | 2.81 | no gain |
| early (2021-23) LIVE vs rvol>med | 221 vs 105 | 64.7 vs 69.5 | 1.38 vs 1.74 | 9.0 vs 8.9 | 5.9 vs 4.9 | | late: 2.25 vs 3.19 |

Verdict: no new candidate. Momentum, MA-slope and range-position filters only halve the trade count and the return (no PF/return improvement worth promoting). The volatility effect is the only real dose-response: PF rises monotonically with realized vol, the lowest two vol bands are worth ~3-4% return each (PF ~1.2) while the top band carries essentially all the profit; holds in both early and late years and with a second measure (ATR%, run 12). This independently re-confirms the run 8 PROMOTION CANDIDATE (vol60>=1.75%, already in challenger.py); nothing further to add. Caveat unchanged: highest-vol stocks cost more to trade (run 11). Next: sector-ETF-relative drop (needs sector map), pairs/relative value, true PEAD with earnings dates.

## 2026-11-10 (run 17) - pre-holiday effect and volume exclusion on the vol60>=1.75% candidate (web idea)
Source: https://quantpedia.com/strategies/pre-holiday-effect (search only returned the page list plus a commodities variant, https://quantpedia.com/pre-holiday-effect-in-commodities/?a=6080; claim of abnormal returns on the day before market holidays is index/other-era, unverified for single stocks). Rules: (a) tag LIVE-setup trades by whether the signal day is the last (k=1) or one of the last two (k=2) trading days before a market closure (gap of >=1 weekday in SPY dates; 61 / 121 such days); (b) standalone sleeve: buy close the last trading day before a closure, sell next close; close>SMA200 and SMA50>SMA200 trend, SPY>200d, ATR/price<6%, stop 4 ATR, ranked by weakest 3d return; (c) vol60>=1.75% candidate with signal-day 3-day relative volume v3>=0.85 / >=1.0 (follow-up suggested by run 13), and with pre-holiday signals excluded. Same simulator (10% x 12, 4/day). Script: lab_holiday.py. ~12 variants (multiple-comparison discount; all reported).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| LIVE signal on pre-holiday k=1 | 23 | 56.5 | 0.75 | -0.8 | 2.2 | 7 / 2.77 | -/-/.20/.27/1.36/- |
| LIVE excluding pre-holiday k=1 | 589 | 69.4 | 1.93 | 60.4 | 5.9 | 130 / 2.63 | 1.89/.13/1.48/2.43/1.91/2.62 |
| LIVE signal on pre-holiday k=2 | 43 | 62.8 | 1.15 | 0.6 | 2.7 | 9 / 3.69 | thin |
| standalone 1-day pre-holiday sleeve | 168 | 48.2 | 0.65 | -5.2 | 6.1 | 36 / 0.68 | 1.30/0/.32/.77/1.56/.44 |
|   + champion (shared slots) | 896 | 62.5 | 1.29 | 30.1 | 6.7 | 198 / 1.40 | 1.7/.11/1.18/1.47/1.24/1.34 |
| vol60>=1.75% candidate | 300 | 74.7 | 2.99 | 61.8 | 4.3 | 100 / 3.37 | 3.47/.87/1.54/5.22/2.45/3.41 |
|   + v3>=0.85 | 200 | 74.5 | 3.53 | 44.1 | 4.3 | 64 / 4.98 | 7.13/-/1.09/7.7/2.29/5.37 |
|   + v3>=1.0 | 130 | 73.8 | 3.05 | 25.6 | 3.4 | 42 / 6.33 | 4.83/-/1.05/5.38/1.83/6.05 |
|   excluding pre-holiday k=1 | 289 | 75.4 | 3.09 | 60.9 | 4.3 | 94 / 3.14 | 3.47/.87/1.79/5.73/2.22/3.37 |

Verdict: NOT a promotion candidate. The pre-holiday long effect does not exist in this stock universe on daily bars: the standalone sleeve loses money (PF 0.65, L12 0.68) and dilutes the champion (PF 1.88 -> 1.29 combined). Live-setup signals on the last pre-holiday day are weak (n=23, PF 0.75) but too few to act on; excluding them adds only ~1 return point (n=15 trades, noise-level). The v3 volume floor on top of vol60>=1.75% raises PF (2.99 -> 3.53) but cuts return from 61.8% to 44.1% and 2023 drops to PF ~1.1, so it fails the return bar and is a sample-shrinking filter, not a clear gain. The vol60>=1.75% candidate (already in challenger.py) stands unchanged. Not added to challenger.py. Next: sector-ETF-relative drop (needs sector map), pairs/relative value, true PEAD with earnings dates.

## 2026-11-10 (run 18) - option-expiration-week (monthly opex) calendar effect on the LIVE setup (web idea)
Source: Quantpedia "Option Expiration Week Effect" (https://quantpedia.com/strategies/option-expiration-week-effect/, search-level knowledge only, not fetched) and the Stoll-Whaley expiry-week literature; unverified, indices-era claims. Rules: LIVE setup trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day) tagged by trading-day offset from the third Friday (opex day). Script: lab_opex.py. 6 groupings tried (multiple-comparison discount); data through 2026-10-29, 2026 not used to select.

| Group | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF by year (21/22/23/24/25/26) |
|---|---|---|---|---|---|---|---|
| LIVE + vol60>=1.75 (ref) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| opex week (-4..0) | 96 | 68.8 | 1.99 | 10.9 | 3.4 | 33 / 2.63 | 5.7/-/.03/4.83/1.67/2.61 |
| week after opex (+1..+5) | 66 | 80.3 | 3.47 | 11.5 | 1.4 | 12 / 2.23 | 44/-/5.3/3.2/1.37/2.23 |
| not opex week | 222 | 75.2 | 2.90 | 41.7 | 3.6 | 68 / 4.08 | 1.47/.87/2.24/4.1/2.91/3.85 |
| entry -6..-1 (hold spans opex) | 109 | 67.0 | 1.53 | 8.0 | 3.7 | 38 / 2.47 | 1.27/-/.33/2.07/1.77/2.75 |

Verdict: NOT a promotion candidate. Opex-week and hold-spans-opex entries are somewhat weaker (PF 1.5-2.0 vs 2.9 elsewhere), but the gap is driven by 2023 (PF 0.03-0.33) on ~100 trades, the per-offset average returns are noisy with no monotonic pattern, and excluding them would just remove trades and return (41.7% vs 60.6%). Consistent with chance after 6 comparisons. No change to challenger.py. Next ideas: true PEAD/earnings-gap with earnings dates, relative-value pairs within sector, SPY-gap-day conditioning.

## 2026-11-10 (run 19, filed as "run 6" by a stale-clone session) - SPY-dip position sizing / priority on champion entries (own idea; follow-up of the 2026-11-05 fear-filter result in improvement_log.md and web hint that reversal strength rises after market declines: https://quantpedia.com/short-term-return-reversals-and-intraday-transactions/ , unverified)
Rules: champion entries and exits unchanged (A+E+F, SPY>200d, hold 7, stop 4 ATR, 10% x 12, 4/day). Only the size of each trade changes with SPY's 3-day change on the entry day: multiplier hi if < -1%, else lo (emulated by scaling the trade's pnl; PF below is therefore size-weighted). Script: lab_dipsize.py. 6 variants tried (multiple-comparison discount; the -1% threshold was inherited from the earlier fear-filter run, so it is NOT fully out-of-sample; only 4 sizing combos explored).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| 1.5x if dip, else 1x | 749 | 66.0 | 1.50 | 54.6 | 8.2 | 1.21 | 1.64 | 2.10/.13/1.29/1.76/1.34/1.60 |
| 1.5x if dip, else 0.5x | 749 | 66.0 | 1.70 | 49.6 | 7.3 | 1.39 | 1.93 | 2.85/.10/1.14/2.24/1.53/1.97 |
| 1.25x if dip, else 0.75x | 749 | 66.0 | 1.52 | 43.1 | 6.7 | 1.24 | 1.68 | 2.19/.12/1.27/1.82/1.37/1.65 |
| 2x if SPY 3d < -2% | 749 | 66.0 | 1.45 | 46.7 | 6.6 | 1.13 | 1.59 | 2.00/.13/1.39/1.63/1.30/1.58 |
| priority: deepest SPY dip first | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 1.50 | identical to champion (slots rarely bind) |
| control: lowest stock score first | 746 | 66.1 | 1.40 | 37.3 | 6.5 | 1.00 | 1.42 | worse |

Verdict: PROMOTION CANDIDATE (conditional) - dip-scaled sizing "1.5x if SPY 3d<-1% else 0.5x" (and the milder 1.25x/0.75x) beats the champion on PF, return, Sharpe, last 12 months and 4 of 5 non-2022 years (2023 is worse: 1.14 vs 1.39); max DD rises 6.2 -> 7.3%. Ranking by dip depth does nothing because slots almost never bind. Caveats before anyone promotes it: (1) PF is size-weighted so it is flattered versus a fixed-size PF; the fair read is return/Sharpe/DD. (2) The dip threshold was chosen after seeing the fear-filter result, so there is selection bias; the mild 1.25x/0.75x version is the safer test. (3) With 1.5x on up to 12 positions gross exposure can reach 180% of equity on deep-dip days (paper account margin 2x, but it is real leverage); a cap on total exposure is needed. (4) 2022 is still a loss. Added both multipliers to challenger.py as variants (callable post-processor) so the weekly job tracks them. NOTE: this run was made from a stale clone that overwrote runs 7-18; they were restored from 549127a. No live files touched.

## 2026-11-10 (run 20) - SPY-dip sizing re-tested on the NEW live setup (vol60>=1.75%, breadth>=10%, peer rank) (own idea, follow-up of run 19)
Source: none. Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day); only trade size scales with SPY 3-day change on entry day (PF size-weighted). Script: lab_dip_live.py. 4 variants (multiple-comparison discount; dip threshold -1% inherited from run 19, not out-of-sample).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (vol175) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| 1.5x if dip else 1x | 308 | 74.4 | 3.01 | 86.2 | 5.4 | 2.25 | 3.49 | 2.83/.93/1.57/5.17/2.62/3.64 |
| 1.5x if dip else 0.5x | 308 | 74.4 | 3.29 | 70.6 | 4.4 | 2.12 | 3.68 | 4.08/1.10/1.50/5.91/2.78/4.05 |
| 1.25x if dip else 0.75x | 308 | 74.4 | 3.05 | 65.6 | 4.4 | 2.23 | 3.52 | 2.97/.95/1.56/5.28/2.65/3.70 |
| control: 0.5x if SPY 3d>0 else 1x | 308 | 74.4 | 3.28 | 62.3 | 4.2 | 2.39 | 3.66 | 3.55/1.74/1.56/6.31/2.76/3.84 |

Verdict: NOT a promotion candidate. On the vol-filtered live set the dip-sizing edge mostly disappears: Sharpe is flat or lower (2.12-2.25 vs 2.28), the return gain comes only from added exposure (and drawdown 4.3 -> 5.4% for the 1.5x/1x version), and 2023 is slightly worse in every variant. The vol filter already concentrates trades in high-volatility, often post-dip conditions, so run 19's sizing signal is largely the same information. The calm-day shrink control scores similarly, confirming it is a generic exposure effect. Also a reminder that the run-19 variants in challenger.py are on the OLD champion list; they are tracking only. Not added as a live-setup variant.

Repo hygiene note: the original run-6 commit (7c81e67) was made from a stale clone and overwrote lab_log.md runs 7-18 and the live variants in challenger.py; this session restored them from 549127a and re-added the dip-sizing material as run 19. Future lab sessions must `git pull --rebase` BEFORE editing and never `git checkout <old commit> -- data/lab_log.md`.

## 2026-11-10 (run 21) - pullback depth in ATR units, distance under SMA10, relative strength vs SPY as conditioners of the LIVE vol60>=1.75% setup (web-inspired, no fetch)
Source: general Connors/Alvarez-style claim that deeper pullbacks revert harder, and residual-reversal / relative-strength literature (Quantpedia short-term reversal pages already cited in runs 14/19); unverified, search-level knowledge only. Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day) filtered by signal-day features: 3-day drop in ATR units, close's distance under SMA10 in ATR, 20d/60d return relative to SPY. Script: lab_depth.py. 8 variants tried (multiple-comparison discount; thresholds picked a priori, not tuned, 2026 not used to select).

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE (vol175) ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| 3d drop >= 1.5 ATR | 183 | 73.8 | 3.15 | 38.4 | 2.3 | 59 / 3.11 | 4.71/.26/1.49/6.8/2.08/3.12 |
| 3d drop >= 2.5 ATR | 38 | 68.4 | 2.46 | 5.5 | 1.9 | 12 / 3.10 | thin |
| 3d drop < 2.5 ATR | 286 | 74.5 | 2.61 | 50.0 | 4.7 | 93 / 3.41 | 2.17/.75/1.53/4.37/2.01/3.61 |
| close >= 2 ATR under SMA10 | 61 | 80.3 | 3.80 | 12.7 | 2.1 | 25 / 3.89 | 10.5/-/5.62/-/2.16/3.18 |
| close < 2 ATR under SMA10 | 275 | 73.1 | 2.62 | 46.5 | 4.4 | 87 / 3.11 | 2.12/.75/1.49/4.46/2.12/3.31 |
| RS 60d vs SPY > 0 | 263 | 74.1 | 2.78 | 52.3 | 4.2 | 85 / 3.46 | 2.4/.87/1.59/4.42/2.71/3.35 |
| RS 60d vs SPY <= 0 | 56 | 71.4 | 3.18 | 6.5 | 0.6 | 16 / 2.92 | thin |
| RS 20d vs SPY < -5% | 70 | 67.1 | 1.77 | 6.3 | 2.1 | 18 / 1.52 | 0.89/-/.99/4.0/9.85/1.59 |

Verdict: NOT a promotion candidate. Deeper pullbacks only slightly raise PF while shrinking return (38% vs 61% for >=1.5 ATR) and 2022 collapses (0.26); the >=2 ATR-under-SMA10 subset has the best PF (3.8, 80% win) but just 61 trades / 12.7% return, so it is a sample-shrinking filter whose gain over 308 trades is within noise after 8 comparisons. Relative strength vs SPY is irrelevant (PF 2.78 vs 2.83) and weak 20d RS is worse. Confirms earlier runs: the vol60 filter already captures most of the selectable edge; further conditioning mostly removes trades. No change to challenger.py. Next: true PEAD with earnings dates, exposure cap for the 15% x 8 sizing candidate, pairs within sector.

## 2026-11-11 (run 22) - scaling in (half at signal close, add next close only if lower) on the LIVE vol60>=1.75% setup (web hint, own rules)
Source: https://quantifiedstrategies.substack.com/p/market-timing-scaling-in-and-the (fetched; gives NO exact rules or numbers, only the claim that scaling in raises average profit per trade but lowers total return because less capital works; a general RSI2/pullback search also returned only marketing-grade pages, unverified). Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day); leg 1 = 50% at signal close, leg 2 at next close, same exit price and stop as the live trade (emulated from the live trade's exit; trades exiting on day 1 get leg 1 only). PF/return are size-weighted. Script: lab_scalein.py. 4 variants tried (multiple-comparison discount; 2026 not used to select).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (vol175) ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| 50% + 50% next close if lower close | 308 | 74.4 | 3.00 | 39.9 | 3.3 | 2.37 | 100 / 4.02 | 2.38/2.01/1.43/4.92/2.76/4.18 |
| 50% + 50% next close always (control) | 308 | 74.4 | 2.93 | 50.1 | 3.4 | 2.25 | 100 / 3.74 | 2.28/1.99/1.69/4.65/2.49/3.74 |
| 50% + 75% next close if lower | 308 | 74.4 | 3.02 | 46.9 | 3.8 | 2.33 | 100 / 4.13 | 2.36/4.14/1.37/4.91/2.78/4.36 |
| full size only on next close, only if lower | 137 | 55.5 | 2.88 | 22.0 | 2.4 | 1.97 | 52 / 4.55 | thin |

Verdict: NOT a promotion candidate. The source's claim reproduces qualitatively (lower return, because less capital is deployed; per-dollar efficiency slightly up), but the improvement in Sharpe is 2.28 -> 2.37, inside noise after 4 comparisons, and the 2022 PF jump (0.87 -> 2.0) comes from a handful of trades. The "always add" control gets most of the PF gain, so the "only if lower" condition adds little. Scaling in would also add a second order per trade (more execution complexity) for no clear edge; net return per unit of average capital is not better than the live 1x entry. No change to challenger.py. Next ideas: sector-concentration cap on simultaneous positions, VIX/term-structure proxy via ETFs, true PEAD with earnings dates.

## 2026-11-11 (run 23) - sector-concentration cap (max simultaneous positions per sector) on the LIVE vol60>=1.75% setup (own idea, from run 22 follow-up list)
Source: none (own idea). Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day); only the simulator's per-sector open-position cap varies (sector = ETF bucket in market.SECTOR_OF). Script: lab_seccap.py. 5 variants (multiple-comparison discount; 2026 not used to select). Live rules.yaml already has sector_cap: 2.

| Cap | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| none | 336 | 73.5 | 2.72 | 65.8 | 5.8 | 2.26 | 106 / 3.65 | 2.58/.87/1.54/4.68/1.98/3.70 |
| 1 | 240 | 71.7 | 2.44 | 35.5 | 3.9 | 1.89 | 75 / 2.34 | 1.76/.12/1.38/7.06/2.62/1.95 |
| 2 (LIVE) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| 3 | 328 | 74.1 | 2.75 | 63.6 | 5.0 | 2.26 | 106 / 3.54 | 2.58/.87/1.61/4.83/1.97/3.55 |
| 4 | 333 | 73.3 | 2.68 | 64.2 | 5.8 | 2.21 | 106 / 3.65 | 2.58/.87/1.47/4.59/1.98/3.70 |

Sector mix of the filtered signals is heavily SMH (166) and XLK (132) of 566 candidate trades, as expected from a high-volatility filter.

Verdict: NOT a promotion candidate; live cap 2 is already the best on PF and Sharpe. Cap 1 clearly hurts (return 35%, 2022 PF 0.12); caps 3-4 and none add ~3-5 return points but raise drawdown (4.3 -> 5.0-5.8%) and lower PF in 2023/2025. Differences between 2, 3 and none are within noise. No change to challenger.py or live rules. Next ideas: VIX/term-structure proxy via ETFs, true PEAD with earnings dates, web research on pairs/relative value (next run should be a WEB run).

## 2026-11-11 (run 24) - stop distance and max-hold re-check on the LIVE vol60>=1.75% setup (own idea; lab_stopvol.py)
Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, 10% x 12, 4/day); only stop (ATR) or hold varies. 6 variants (multiple-comparison discount; 2026 not used to select).

| Variant | n | Win % | PF | Ret % | MaxDD | Sharpe | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE stop4 hold7 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| stop 3 | 308 | 74.4 | 2.66 | 57.9 | 4.3 | 2.17 | 3.16 | worse in 4 yrs |
| stop 5 / 6 | 308 | 74.4 | 2.81 / 2.79 | 60.3 / 60.0 | 4.3 | 2.27 / 2.25 | 3.37 | ~equal |
| hold 5 | 311 | 70.7 | 2.39 | 50.0 | 5.5 | 1.86 | 2.63 | worse |
| hold 10 | 306 | 75.8 | 2.91 | 62.0 | 5.0 | 2.27 | 3.86 | 2.75/.87/1.55/5.58/2.00/4.34 |
| hold 12 | 306 | 75.8 | 2.87 | 61.3 | 5.0 | 2.25 | 3.68 | similar |

Verdict: NOT a promotion candidate. Stops beyond 4 ATR almost never trigger on this set (plateau), 3 ATR is worse. Hold 10 gives PF 2.91 / return 62.0 but 2023 and 2025 PF are lower (1.55 vs 1.62, 2.00 vs 2.51), max DD rises 4.3 -> 5.0, and Sharpe is flat: fails the all-but-one-year bar and is within noise. Live parameters (stop 4, hold 7) sit on a plateau. Not added to challenger.py. Next: VIX/term-structure ETF proxy, true PEAD with earnings dates.

## 2026-11-11 (run 25) - trend strength (ADX14, Kaufman efficiency ratio) as conditioner of the LIVE vol60>=1.75% setup (web idea)
Sources: https://quantifiedstrategies.substack.com/p/rsi-and-adx-trading-strategies-backtest , https://algotr.substack.com/p/stop-trading-in-chop-start-using (search listing only, not fetched; the common web claim is that mean reversion works best in low-ADX "chop" and trend-following in high ADX; unverified). Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day); keep only signals whose signal-day ADX(14, Wilder) or 10d efficiency ratio (|c-c10| / sum |dc|) falls in a bucket. ADX quartiles of live signals: 22 / 28 / 35. Script: lab_adx.py. 6 variants + 4 repeats without the vol filter (multiple-comparison discount; 2026 not used to select).

| Variant | n | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (vol175) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| ADX<20 | 72 | 68.1 | 1.47 | 4.3 | 3.3 | 0.72 | 17 / 3.84 | .62/0/.49/5.36/2.52/2.08 |
| ADX 20-30 | 146 | 72.6 | 2.65 | 22.0 | 2.4 | 2.44 | 49 / 2.71 | 7.86/-/1.54/4.71/2.11/2.51 |
| ADX>=25 | 192 | 75.0 | 3.66 | 45.6 | 2.5 | 2.27 | 64 / 3.81 | 27.7/1.89/2.67/4.69/1.65/4.45 |
| ADX>=30 | 126 | 75.4 | 3.89 | 29.1 | 1.8 | 1.92 | 41 / 4.03 | 22.8/1.89/2.99/4.75/1.49/6.92 |
| ER10<0.5 | 259 | 75.3 | 3.22 | 56.6 | 3.6 | 2.27 | 83 / 4.94 | 1.61/.75/2.01/6.96/2.13/5.82 |
| ER10>=0.5 | 82 | 73.2 | 1.92 | 7.6 | 1.8 | 1.38 | 26 / 1.04 | -/-/1.54/1.58/2.19/.69 |
| (no vol filter) ADX>=25 | 384 | 71.4 | 2.25 | 46.0 | 3.5 | 2.00 | 83 / 3.38 | 3.28/.19/1.77/2.22/1.78/3.58 |

Finding: the web claim is the OPPOSITE of what the data show here. Pullbacks inside a well-established trend (high ADX) revert better than those in low-ADX chop: ADX<20 has PF 1.47 (and 0.62/0.49 in 2021/2023), ADX>=25 has PF 3.66 and beats the live PF in 2021, 2022, 2023, 2026 and L12, ties 2024 (4.69 vs 4.74) and loses 2025 (1.65 vs 2.51). The same direction holds without the vol filter (PF 1.88 -> 2.25), so it is not just volatility in disguise. The efficiency ratio (choppy last 10 days, ER<0.5) is also a mild improvement (PF 3.22, L12 4.94) but keeps 84% of trades and is not a clear gain in return (56.6 vs 60.6).
Verdict: NOT a promotion candidate as a hard filter: ADX>=25 raises PF 2.83 -> 3.66 but cuts return 60.6 -> 45.6 (fewer trades fill fewer slots) and loses 2025; PF-only gains from trade-removal filters are exactly what the log already treats as weak. The low-ADX bucket (ADX<20, 72 trades, 4% return) is consistently poor and is the useful hint. Not added to challenger.py. Next: test "skip ADX<20" (removes only the weak tail) and ADX>=25 as a 15% size tier vs 10% (two-tier sizing), then VIX/term-structure ETF proxy and true PEAD. Next run should be an own-idea run.

## 2026-11-11 (run 26) - ADX tail-skip, ADX-tiered sizing and ADX ranking on the LIVE vol60>=1.75% setup (own idea; follow-up to run 25; lab_adxtier.py)
Source: none (own follow-up). Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day); signal-day ADX(14, Wilder) decides skip / size multiplier / rank. Tier sizing emulated by scaling each trade's pnl_pct (PF and return are size-weighted; exposure is higher than 10% x 12, so return is not free). 5 variants (multiple-comparison discount; 2026 not used to select).

| Variant | n | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (vol175) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| skip ADX<20 | 249 | 75.5 | 3.24 | 53.8 | 3.2 | 2.39 | 84 / 3.33 | 12.4/1.89/1.94/4.79/1.78/3.79 |
| ADX>=25 at 1.5x, else 1x | 308 | 74.4 | 3.01 | 92.3 | 5.6 | 2.28 | 100 / 3.47 | 3.18/1.06/1.79/4.58/2.35/3.64 |
| ADX>=25 1.5x, 20-25 1x, <20 0.5x | 308 | 74.4 | 3.18 | 87.9 | 5.0 | 2.29 | 100 / 3.44 | 5.06/1.36/1.92/4.56/2.13/3.79 |
| skip <20 + ADX>=25 at 1.5x | 249 | 75.5 | 3.32 | 83.7 | 4.5 | 2.32 | 84 / 3.46 | 14.8/1.89/2.08/4.62/1.74/3.96 |
| rank by highest ADX first | 307 | 73.3 | 2.80 | 59.5 | 4.3 | 2.26 | 100 / 3.33 | 2.41/.87/1.45/5.43/2.22/3.37 |

Verdict: NOT a promotion candidate. Skipping ADX<20 lifts PF 2.83 -> 3.24 and trims drawdown 4.3 -> 3.2, but return falls (53.8 vs 60.6), L12 PF is flat (3.33 vs 3.37) and 2025 is worse (1.78 vs 2.51); the 2021 PF of 12 rests on very few losers. Tiered sizing raises return only by taking more exposure (max DD 4.3 -> 5.0-5.6) with Sharpe unchanged (2.28-2.32), i.e. leverage, not edge. Ranking by ADX does nothing. ADX conditioning is therefore a weak-tail trim worth about +0.1 Sharpe, inside noise after 5 + 10 comparisons across runs 25-26. Not added to challenger.py. Next run should be a WEB run: pairs/relative value or overnight-vs-intraday drift; own ideas still open: VIX/term-structure ETF proxy, true PEAD with earnings dates.

## 2026-11-11 (run 27) - SPY regime conditioners (drawdown from 252d high, 20d realized vol, SPY vs SMA50/SMA200) on the LIVE vol60>=1.75% setup (own idea; a web search for RSI2 exit/ETF-sleeve write-ups only returned marketing-grade listings such as https://backtest.substack.com/p/the-2-period-rsi-a-simple-system , not fetched; exit rules and pairs were already tested in earlier runs)
Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day) filtered by SPY features on the signal day. Script: lab_spyreg.py. 8 variants (multiple-comparison discount; 2026 not used to select).

| Variant | n | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (vol175) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| SPY within 3% of 252d high | 230 | 76.1 | 2.94 | 43.8 | 3.4 | 2.27 | 84 / 3.65 | 1.97/.87/1.13/5.71/3.92/3.09 |
| SPY >=3% below 252d high | 84 | 67.9 | 2.29 | 11.6 | 2.4 | 1.74 | 18 / 2.95 | thin |
| SPY 20d vol < 15% | 270 | 75.2 | 2.94 | 54.9 | 4.3 | 2.50 | 91 / 3.28 | 1.96/-/1.52/5.63/2.94/3.28 |
| SPY 20d vol >= 15% | 38 | 68.4 | 2.14 | 3.8 | 1.8 | 1.66 | 9 / 6.32 | thin |
| SPY > SMA50 | 236 | 76.3 | 3.20 | 48.3 | 2.9 | 2.15 | 72 / 4.06 | 1.93/0/2.24/5.71/3.29/3.84 |
| SPY < SMA50 (still >200d) | 86 | 65.1 | 1.85 | 8.9 | 2.7 | 1.49 | 33 / 2.54 | thin, 2023 0.29 |
| SPY within 5% of SMA200 | 45 | 71.1 | 2.04 | 4.3 | 1.2 | 1.08 | 10 / 1.37 | thin |

Verdict: NOT a promotion candidate. Every SPY-regime split removes trades and return (best: SPY>SMA50 PF 3.20 but return 48 vs 61 and 2022 PF 0.0; low-SPY-vol Sharpe 2.50 vs 2.28 but return 55 vs 61). Trades taken when SPY is weaker (below SMA50, in a 3%+ drawdown) are somewhat worse (PF 1.9-2.3) yet still profitable, so skipping them gives up about 10-12 return points for a small PF gain: the same trade-removal pattern as runs 21, 25, 26. The live breadth + SPY>200d gates already capture the regime information. No change to challenger.py. Next: true PEAD with earnings dates (earnings.py), or a high-vol-only sleeve on non-universe symbols (needs new data, so not testable here).

## 2026-11-11 (run 28) - robustness audit of the LIVE vol60>=1.75% filter: random symbol halves, drop-top-contributors, placebo (own idea; lab_robust.py)
Source: none (overfitting audit; no new strategy). Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day). Checks: (1) 200 random half-splits of the 126-symbol universe, does the vol filter raise per-trade PF inside each half; (2) remove the top 3/5/10 contributing symbols and re-run the portfolio; (3) even/odd symbol halves; (4) placebo: random same-size subsets of the unfiltered raw trades. No parameter selection, so no multiple-comparison discount beyond the earlier runs that chose 1.75%.

| Check | Result |
|---|---|
| Random symbol halves (200) | vol filter raises per-trade PF in 200/200; median +1.01, 5th percentile +0.58 |
| Placebo (638 random of 1437 raw trades), per-trade PF | mean 1.84, 95th pct 2.10, max 2.42 vs live 2.86 |
| LIVE (all symbols) | n=308, PF 2.83, ret 60.6%, DD 4.3, L12 PF 3.37 |
| minus top 3 (NVDA, KLAC, CRWD) | n=286, PF 2.23, ret 39.2, DD 4.7, L12 PF 2.96 |
| minus top 5 | n=271, PF 2.16, ret 35.0, L12 PF 3.14 |
| minus top 10 | n=248, PF 1.74, ret 20.5, L12 PF 2.40, 2022 PF 0, 2023 PF 0.98 |
| even-index symbols / odd-index symbols | PF 2.35 / 3.10; ret 21.1 / 35.1; L12 PF 3.00 / 4.15 |

Findings: the vol60 effect is not a lucky-sample artifact: it holds in every random half of the universe and the live per-trade PF (2.86) is far above the placebo maximum (2.42). BUT the dollar return is concentrated: the top 5 symbols (NVDA, KLAC, CRWD, AVGO, AMD) supply about a third of total P&L, and without the top 10 the return falls from 60.6% to 20.5% (PF 1.74, 2023 PF 0.98). Those names are ex-post winners from a hand-picked, hindsight-biased universe (survivorship), so live expectancy is probably closer to the "minus top 5/10" rows than to the headline 60%. The filter still helps there (PF 1.74-2.16 vs ~1.4-1.9 unfiltered).
Verdict: confirms the vol60>=1.75% rule is real, but advises sizing expectations on the PF 1.7-2.2 / return 20-35% range, not 2.83 / 60%. This weighs against the 15% x 8 sizing candidate (it would amplify concentration in the same few names); a per-symbol exposure view would be worth adding to the daily review. Not added to challenger.py. Next: true PEAD with earnings dates (needs data), VIX/term-structure proxy, or a universe-extension test if more symbols can be cached.

## 2026-11-11 (run 29) - earnings-proximity proxy: does the live earnings blackout/exit cost edge? (own idea; follow-up to the "true PEAD needs earnings data" note; lab_earnproxy.py)
Source: none fetched. Earnings dates are not available in the sandbox, so earnings days are inferred from daily bars: volume >= 2.5x the prior 20d average AND (open gap >= 3% or day move >= 5%), clusters merged within 15 bars (avg 13.8 spikes per symbol over 6.3 years, i.e. roughly quarterly plus other news). "Predicted" flag: a spike 60-67 trading days before a day inside entry+1..entry+8 (usable live). "Real" flag: spike inside entry+1..entry+7 (look-ahead, upper bound on effect). Same trade list and simulator (gap-open stop fills), no parameters tuned: 4 splits x 2 trade sets viewed.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| skip predicted-earnings | 269 | 73.2 | 2.79 | 48.5 | 3.3 | 94 / 3.38 | 2.75/.87/1.82/3.94/2.52/3.21 |
| only predicted-earnings | 49 | 79.6 | 3.24 | 10.0 | 1.3 | 7 / 4.07 | .88/-/2.08/7.0/2.97/- |
| skip real-earnings (look-ahead) | 283 | 73.1 | 2.41 | 41.0 | 4.3 | 96 / 2.96 | 2.88/1.6/1.15/3.24/2.48/2.86 |
| only real-earnings (look-ahead) | 35 | 80.0 | 5.98 | 14.8 | 1.1 | 5 / n/a | 1.15/0/5.03/24.9/1.41/- |
| no-vol base (breadth+rank) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| base, skip predicted-earnings | 543 | 68.1 | 1.73 | 43.2 | 5.0 | 128 / 2.59 | 1.83/.13/1.41/1.75/1.83/2.51 |
| base, only predicted-earnings | 87 | 77.0 | 2.87 | 13.0 | 2.1 | 11 / 6.44 | 1.3/-/1.54/4.2/4.1/- |
| base, skip real-earnings (look-ahead) | 572 | 68.0 | 1.68 | 40.9 | 5.6 | 131 / 2.37 | 1.92/.13/1.07/1.78/2.13/2.29 |

Findings: in this backtest, oversold-pullback trades whose hold window spans an earnings report do BETTER than the rest (PF 3.2-6.0, win 77-80%), in both trade sets and in 4 of 5 testable years; excluding them cuts return 60.6 -> 41-49 with no PF gain. The backtest has no earnings blackout, while the live bot does (bot.py earnings blackout + exit-before-report), so live likely forgoes roughly 10-20 return points of backtest edge (and the live PF/return will be lower than the backtest headline, in addition to the survivorship caveat from run 28). Caveats: the proxy is noisy (misses reports without a spike, includes non-earnings news spikes); the universe is hindsight-picked growth names whose post-report drift was strongly positive 2023-2025; positive skew from a few huge gap-ups (2024 PF 25 on ~10 trades); gap-down risk on a 10% position is real, and stops fill at the gap open here, so the loss tail is already counted.
Verdict: NOT a promotion candidate (nothing to add to challenger.py) and no live change from the lab. FLAG FOR THE DAILY IMPROVEMENT TASK: the earnings blackout/flatten rule appears to cost backtest return; a test with REAL dated earnings (earnings.py cache or a Nasdaq-calendar history, not reachable from here) would settle whether relaxing it for vol60>=1.75% names is worth the gap risk. Next: build a real earnings-date history from live runs' logs, or try an equal-weight sector ETF filter / VIXY-term proxy.

## 2026-11-11 (run 30) - signal-day candle structure (lower low, close below prior low, range expansion, red body) on the LIVE vol60>=1.75% setup (web-seeded; lab_candle.py)
Source: web search surfaced only generic reversal/"consecutive down days" pages (https://quantifiedstrategies.substack.com/p/turnaround-tuesday-strategy-backtest , https://quantpedia.com/strategies/short-term-reversal-in-stocks); Turnaround-Tuesday/weekday was already covered by run 18 (lab_dow.py), so the lower-low / close-below-prior-low variant of Connors-style pullbacks was tested instead. Unverified, rules are my own. Same trade list and simulator as the live setup (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day). 10 split variants + ref (heavy multiple-comparison discount; splits are not tuned thresholds). Note: sim re-runs each subset, so subset n values do not sum to 308.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| close < prior-day low | 282 | 75.9 | 3.27 | 62.1 | 2.4 | 95 / 3.35 | 2.48/.87/2.93/5.67/2.51/3.40 |
| close >= prior-day low | 56 | 66.1 | 1.50 | 3.1 | 3.3 | 11 / 6.32 | 1.47/-/.82/2.35/1.58/8.45 |
| close < min low of prior 3d | 274 | 75.9 | 3.25 | 60.5 | 2.4 | 94 / 3.39 | 2.48/.87/2.91/5.60/2.40/3.45 |
| not (close >= 3d min low) | 66 | 68.2 | 1.61 | 4.0 | 3.2 | 13 / 5.46 | 1.47/-/.84/2.41/2.81/5.98 |
| lower low today | 297 | 74.1 | 2.86 | 58.8 | 4.3 | 97 / 3.32 | no change vs ref |
| range >= 1.5x avg20 | 78 | 67.9 | 2.84 | 15.2 | 2.5 | 22 / 2.71 | 4.29/-/4.67/5.42/1.28/2.47 |
| red body >= 2% | 135 | 67.4 | 2.73 | 27.1 | 3.1 | 48 / 4.70 | 5.51/.50/.96/3.66/2.03/4.44 |
| red body < 2% | 213 | 76.1 | 2.39 | 26.7 | 3.4 | 62 / 2.25 | 1.70/1.63/1.61/5.39/1.68/2.63 |

Findings: almost every live signal already makes a lower low (96%) so that split is empty. The one informative cut is a close BELOW the prior day's low (92% of signals): excluding the 8-18% that close inside the prior range lifts PF 2.83 -> 3.27, return 60.6 -> 62.1 and cuts max drawdown 4.3 -> 2.4, with PF better in 2021/2023/2024, equal in 2022/2025/2026. But the excluded trades are few (56 / 66) and earn only ~3-4% return in 6 years, and the L12 PF is flat (3.35 vs 3.37), so it fails the "beats on last 12 months" test; it is a trimming of a weak tail, not a new edge. Range expansion and red-body size are not monotonic (body>=2% has 2023 PF 0.96, body<2% has 2022 PF 1.63), i.e. noise.
Verdict: NOT a promotion candidate; not added to challenger.py. Possible low-priority note for the daily task: "close < prior-day low" is a nearly free drawdown trimmer (DD 4.3 -> 2.4) but needs its own out-of-sample confirmation (not enough trades to trust). Next run: own idea (B) per alternation, e.g. real-earnings-date test if live logs now contain dated reports, or an equal-weight sector-ETF breadth filter.

## 2026-11-12 (run 31) - two-tier vol60 sizing: reduced-size trades for the lower-vol signals the live filter discards (own idea; lab_voltier.py)
Source: none (own idea, follows run 9/12 hint that vol is a conviction tier rather than a hard cut). Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day). vol60>=1.75 signals keep full size; signals with vol60 in [lo,1.75) are added at 0.5x or 0.33x size (pnl scaled; they still use a slot and rank after all full-size signals). 5 variants + 2 refs (small multiple-comparison discount; lo and k not tuned beyond this grid).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE vol>=1.75 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| no vol filter | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| lo 1.25 at 0.5x | 485 | 69.5 | 2.27 | 57.0 | 5.0 | 130 / 3.07 | 2.19/.17/1.44/3.06/2.23/2.97 |
| lo 1.0 at 0.5x | 559 | 68.9 | 2.24 | 59.8 | 5.0 | 137 / 3.08 | 2.26/.19/1.44/2.78/2.31/2.98 |
| lo 0 at 0.5x | 608 | 69.2 | 2.23 | 61.1 | 5.0 | 138 / 3.07 | 2.19/.19/1.36/2.93/2.31/2.98 |
| lo 1.25 at 0.33x | 485 | 69.5 | 2.41 | 57.1 | 4.8 | 130 / 3.16 | 2.29/.24/1.46/3.39/2.30/3.10 |
| lo 0 at 0.33x | 608 | 69.2 | 2.39 | 60.2 | 4.8 | 138 / 3.16 | 2.35/.25/1.40/3.32/2.36/3.11 |

Findings: adding the discarded low-vol signals at reduced size never raises return (57-61% vs 60.6%) and always lowers PF (2.2-2.4 vs 2.83), Sharpe (2.0-2.1 vs 2.28) and last-12m PF, and raises drawdown (4.8-5.0 vs 4.3). 2022 reverts from 0.87 to 0.17-0.25, so the low-vol trades are what makes the bear-year loss in the unfiltered setup. The low-vol signals have so little positive expectancy that they displace nothing useful and only add risk. Hard cut at 1.75 remains better than any tier.
Verdict: NOT a promotion candidate; not added to challenger.py. Confirms runs 8/9/12/28: vol60>=1.75% is a hard filter, not a sizing tier. Next: web run (pairs/relative value, overnight-vs-intraday drift), or true earnings-date test if data appears.

## 2026-11-12 (run 32) - breadth trend (washout deepening vs easing), breadth depth split and SPY signal-day direction on the LIVE vol60>=1.75% setup (web-seeded breadth-thrust/capitulation idea, unverified, rules my own; lab_breadthtrend.py)
Source: no page fetched; general breadth-thrust/capitulation literature framing (e.g. https://quantpedia.com/ search results), treated as an unverified hypothesis. Same trade list and simulator as the live setup (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day). 10 split variants + ref (heavy multiple-comparison discount; binary splits, no tuned thresholds). Subset sims are re-run, so subset n values do not sum to 308.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| breadth rising vs yesterday | 249 | 73.9 | 3.06 | 50.0 | 3.7 | 79 / 3.56 | 3.8/.12/1.49/5.03/3.04/3.18 |
| breadth falling vs yesterday | 94 | 72.3 | 1.85 | 9.1 | 2.8 | 32 / 3.74 | .41/-/1.0/2.63/1.81/6.48 |
| breadth 3d change > 0 | 272 | 72.8 | 2.65 | 47.9 | 3.5 | 90 / 3.18 | 2.26/.12/1.62/4.06/2.18/3.43 |
| breadth >= 20% | 187 | 76.5 | 3.45 | 38.0 | 2.4 | 52 / 4.16 | 7.05/.26/1.93/4.35/2.95/4.64 |
| breadth 10-20% | 150 | 70.7 | 1.91 | 17.3 | 4.4 | 55 / 3.11 | 1.15/1.38/.96/4.48/.56/3.22 |
| SPY up on signal day | 92 | 67.4 | 1.69 | 7.6 | 3.0 | 31 / 4.04 | .55/0/.58/3.61/.57/4.83 |
| SPY down on signal day | 242 | 75.2 | 3.04 | 49.3 | 4.2 | 75 / 3.19 | 7.57/1.89/1.56/4.29/2.93/2.97 |
| SPY 3d < -1% | 155 | 77.4 | 3.84 | 39.1 | 2.5 | 49 / 4.17 | 103.8/-/1.39/8.43/2.33/5.27 |
| SPY 3d >= -1% | 175 | 71.4 | 2.05 | 18.8 | 2.5 | 57 / 2.89 | 1.54/.75/1.53/3.16/1.38/2.74 |

Findings: the pattern is a dose-response in market stress, consistent with runs 12, 19, 20: deeper washout (breadth >=20%) and a falling SPY (3d < -1%) give PF 3.4-3.8 with lower drawdown, while shallow-stress signals give PF 1.7-2.1. But every restrictive filter cuts return heavily (38-50% vs 60.6%) because cash sits idle, and 2022 gets worse (breadth rising: 0.12 vs 0.87). The new dimension tested, breadth trend (easing vs deepening), is not stable: "deepening" is poor in 2021/2023 but excellent in 2026 (PF 6.5), so it is noise on small n (94). No variant improves return or all non-2022 years vs the live setup.
Verdict: NOT a promotion candidate; not added to challenger.py. Confirms that stress depth is a risk-adjusted tilt, not a new edge; size tilts were already tested in runs 19/20 without a promotion. Next: web run on pairs/relative value or a real earnings-date test if dated report data becomes available.

## 2026-11-12 (run 33) - no-bounce time stop (exit at day-k close if still below entry) on the LIVE vol60>=1.75% setup (own idea; lab_nobounce.py)
Same trade list/simulator as live (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day, stop 4 ATR, hold 7, exit close>prior high). 4 variants + ref.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| day 2 close < entry -> exit | 331 | 59.2 | 1.83 | 33.4 | 4.9 | 106 / 1.99 | 2.78/.34/1.27/2.31/1.59/1.96 |
| day 3 close < entry -> exit | 326 | 65.6 | 2.07 | 42.8 | 4.7 | 102 / 2.17 | 2.21/.69/1.46/3.18/1.64/2.17 |
| day 4 close < entry -> exit | 314 | 67.8 | 2.31 | 47.6 | 4.5 | 101 / 2.19 | 3.35/.72/1.47/3.58/2.12/2.02 |
| day 3 close < entry-1% -> exit | 323 | 68.4 | 2.06 | 43.1 | 4.5 | 102 / 2.17 | 2.21/.69/1.54/2.91/1.66/2.18 |

Findings: every early-cut variant is worse on PF, return, drawdown and the last 12 months; the later the cut, the less damage. Positions still under water at day 2-4 recover often enough (the edge sits in the late bounce) that cutting them converts future winners into small losses. Consistent with run 24 (hold 5 worse) and run 28 (trailing/breakeven exits worse).
Verdict: NOT a promotion candidate; not added to challenger.py. Exit side of the live setup remains on a plateau. Next: pairs/relative value, or a real earnings-date test if dated data appears.

## 2026-11-12 (run 34) - weekly short-term reversal sleeve: buy last-week losers on the last session of the week (web-seeded, own rules; lab_weekly.py)
Source (unverified hypothesis, search results only, no page fetched): https://www.quantconnect.com/learning/articles/investment-strategy-library/short-term-reversal-strategy-in-stocks , https://quantpedia.com/strategies/momentum-and-reversal-combined-with-volatility-effect-in-stocks . Rules: last session of each ISO week, SPY>200d gate (live gate2), stock above SMA50>SMA200 (except one variant), 5-day return <= -5% (or -8%), vol60>=1.75% (except one variant), ATR/close<=8%; rank by most negative 5d return; enter at close, hold 5 (or 10) sessions, stop 4 ATR; live portfolio simulator (10% x 12, 4/day). 5 variants tried (multiple-comparison discount applies; all lost anyway). LIVE ref here = live trade list without the F-score ranking tweak (PF 2.88 vs logged 2.83, immaterial).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| weekly r5<=-5%, vol60>=1.75, hold5 | 206 | 56.8 | 1.27 | 13.0 | 8.0 | 69 / 1.39 | 1.04/.77/.55/1.70/1.47/1.34 |
|   + live combined | 429 | 66.9 | 1.77 | 58.2 | 7.7 | 136 / 2.01 | 1.59/.78/1.01/2.23/2.00/1.93 |
| weekly r5<=-8% | 78 | 47.4 | 0.85 | -4.0 | 6.2 | 30 / 0.84 | .77/-/1.28/.55/1.22/.73 |
|   + live combined | 348 | 70.1 | 2.04 | 50.9 | 4.3 | 116 / 1.92 | 1.96/.87/1.63/2.80/2.39/1.69 |
| weekly r5<=-5%, no vol filter | 247 | 57.1 | 1.27 | 14.5 | 9.4 | 77 / 1.48 | 1.09/.54/.48/1.81/1.30/1.44 |
|   + live combined | 468 | 66.5 | 1.75 | 61.4 | 8.1 | 144 / 2.09 | 1.59/.56/.93/2.34/1.87/2.02 |
| weekly r5<=-5%, vol60>=1.75, no trend filter | 592 | 51.0 | 1.30 | 42.3 | 14.1 | 178 / 1.45 | 1.48/.08/2.14/.78/1.34/1.78 |
|   + live combined | 809 | 57.8 | 1.52 | 101.0 | 9.9 | 244 / 1.66 | 2.08/.12/1.98/1.18/1.35/2.01 |
| weekly r5<=-5%, vol60>=1.75, hold10 | 191 | 50.8 | 1.13 | 8.5 | 18.6 | 63 / 1.54 | .67/.07/.31/1.31/1.40/1.80 |
|   + live combined | 405 | 65.9 | 1.50 | 44.8 | 9.8 | 127 / 2.05 | 1.16/.07/.79/1.62/2.04/2.06 |

Findings: a fixed weekly calendar entry on last-week losers has almost no edge on daily bars of this universe (PF 0.85-1.30, win 47-57%, 2023 PF 0.31-0.55). Combining it with the live setup always lowers PF (1.5-2.0 vs 2.88), Sharpe and raises drawdown; the only combined line with higher return (no trend filter, 101%) pays for it with 2022 PF 0.12 and drawdown 9.9%. The live edge comes from the event trigger (washout/breadth + multi-day pullback + vol60), not from generic one-week reversal; waiting for a calendar day removes the timing that makes the live trades work.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: true earnings-date PEAD test if dated data appears; otherwise sector-relative momentum rotation as a standalone with a lower-correlation filter, or cross-asset (TLT/GLD/UUP daily) risk filters if those symbols exist in the cache.

## 2026-11-12 (run 35) - defensive-sector leadership (mean XLP/XLU return minus SPY) as a cross-asset risk-off conditioner of the LIVE vol60>=1.75% setup (own idea from the cross-asset filter seed list; only XLP/XLU/VIXY exist in the cache, no TLT/GLD/UUP; lab_defens.py)
Source: none (own idea). Same trade list and simulator as live (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day). Binary split on sign, no tuned thresholds; 4 variants (mild multiple-comparison discount). Subset sims are re-run, so n values do not sum to 308.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| defensives lead SPY, 5d | 200 | 79.0 | 3.92 | 49.7 | 3.0 | 53 / 3.76 | 8.71/.87/2.30/13.25/2.61/4.18 |
| defensives lag SPY, 5d | 127 | 65.4 | 1.64 | 9.5 | 2.6 | 52 / 3.09 | 1.15/-/.71/2.08/.71/3.13 |
| defensives lead SPY, 20d | 98 | 76.5 | 3.51 | 19.9 | 1.8 | 30 / 2.68 | 5.24/.87/4.02/18.47/2.50/2.50 |
| defensives lag SPY, 20d | 222 | 73.0 | 2.61 | 36.2 | 3.9 | 73 / 3.66 | 1.93/-/1.18/3.98/2.44/4.33 |

Findings: the 5-day split is the interesting one: when defensives are outperforming SPY on the signal day (a risk-off tape), signals have PF 3.9 vs 1.6 when they are not, and the "lag" group has PF <1 in 2023 and 2025. But the filter keeps only 49.7% return vs 61.7% (idle cash), the last-12m PF is about equal (3.76 vs 3.39), 2022 is unchanged, and the 20d version is worse on return and L12. It restates the dose-response in market stress found in runs 12, 19, 20 and 32 (more fear means a better bounce) through a different proxy, so it is not a new independent edge. Skip-the-lag-group as a hard filter does not raise return; as a size tilt it would repeat runs 19/20.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: web run (pairs/relative value, overnight vs intraday drift on the single-stock universe) or true earnings-date test if dated data appears.

## 2026-11-12 (run 36) - liquidity tier (20d dollar volume percentile) as conditioner of the LIVE vol60>=1.75% setup (web-seeded; lab_dvol.py)
Source: https://www.dimensional.com/us-en/insights/q-and-a-on-short-run-reversals-with-mamdouh-medhat-and-robert-novy-marx (Medhat & Novy-Marx: short-run reversal is a liquidity-provision premium, claimed stronger in smaller / less liquid / more volatile stocks; unverified hypothesis, other universe). Rules: 20d average dollar volume (close x volume), cross-sectional percentile among the cached universe on the signal day; split the LIVE trade list (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day). 7 variants tried (4 splits + 3 follow-ups), so discount lucky winners.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| low liquidity half | 108 | 72.2 | 1.40 | 4.6 | 2.5 | 36 / 1.15 | 2.43/-/.71/2.50/1.16/1.20 |
| high liquidity half | 218 | 73.4 | 3.45 | 53.2 | 2.7 | 66 / 5.83 | 2.40/.87/2.02/5.84/2.43/5.97 |
| bottom third | 64 | 64.1 | 1.17 | 1.2 | 1.7 | 18 / 0.88 | 1.59/-/.47/3.02/.29/.93 |
| top third | 170 | 73.5 | 3.81 | 41.1 | 2.8 | 52 / 8.06 | 83.7/1.60/1.83/5.95/1.81/9.52 |
| skip bottom third | 256 | 76.2 | 3.38 | 59.5 | 3.4 | 84 / 4.54 | 2.71/.87/2.22/5.44/2.40/5.14 |
| rank by liquidity pct (high first) | 307 | 73.3 | 2.70 | 57.9 | 4.3 | 100 / 3.53 | 2.41/.87/1.42/5.25/1.87/3.65 |
| size 1.5x top half / 0.5x low half (post-processor, PF size-weighted, exceeds 10% cap) | 308 | 74.4 | 3.41 | 97.7 | 4.8 | 100 / 4.60 | 2.40/.87/2.02/5.51/2.96/4.70 |

Findings: the paper's direction does NOT hold here. Inside this (large-cap, survivor-biased) universe the LEAST liquid third is the weak spot: PF 1.2 and L12 PF 0.9, with PF <1 in 2023 and weak in 2025/2026, while the top half has PF 3.5 and L12 PF 5.8. Dropping the bottom third raises PF 2.88 -> 3.38 and L12 3.39 -> 4.54, is better in 5/5 non-2022 years (2022 equal), cuts max drawdown 4.3 -> 3.4, but total return is slightly lower (59.5 vs 61.7, 52 fewer trades, idle cash). Ranking by liquidity does not help; the size tilt raises return but is a leverage-like post-processor (15% positions) like run 19, so I do not count it. Caveats: only 64 trades in the bottom third, so the evidence is thin; single-factor split chosen after seeing the half-split (mild snooping); today's survivors.
Verdict: WATCHLIST / conditional, not a clean PROMOTION CANDIDATE (misses the strict "return higher" bar by 2 points; improves risk-adjusted quality only). Added to challenger.py as "lab run36: ... skip bottom-third 20d dollar volume" (PF 3.29, ret 57.9, L12 PF 4.51 vs the old-champion row in that file) so the weekly job tracks it. Next: confirm on future out-of-sample months before any live change; web run next (industry-adjusted reversal signal, per the same source, or pairs/relative value).

## 2026-11-12 (run 37) - overnight vs intraday decomposition of the signal-day drop as conditioner of the LIVE vol60>=1.75% setup (web-seeded; lab_ovnintra.py)
Sources: https://quantpedia.com/short-term-return-reversals-and-intraday-transactions/ , https://personal.lse.ac.uk/polk/research/TugOfWar.pdf (Lou-Polk-Skouras: intraday and overnight returns behave differently; unverified, only search snippets read, rules are my own). Rules: on the signal day, overnight = open/prev close - 1, intraday = close/open - 1; split the LIVE trade list (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day) by which part dominates the drop, by a gap-down cut at -0.5%, and by close vs open. 6 variants tried, no tuned thresholds (mild multiple-comparison discount). Subset sims re-run.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| overnight part dominates | 132 | 72.0 | 2.23 | 16.4 | 3.7 | 36 / 1.92 | 5.66/1.63/.60/6.41/1.30/2.64 |
| intraday part dominates | 216 | 72.7 | 2.76 | 40.3 | 2.5 | 73 / 4.07 | 2.00/.50/2.33/3.38/2.49/3.58 |
| gap down < -0.5% | 178 | 73.6 | 2.68 | 29.5 | 4.1 | 53 / 2.55 | 6.46/1.63/1.43/6.17/1.08/3.45 |
| no gap | 168 | 72.0 | 2.47 | 26.2 | 3.2 | 52 / 4.91 | 1.57/.50/1.42/3.09/3.92/3.58 |
| closed below open | 277 | 73.6 | 2.80 | 55.0 | 4.2 | 92 / 3.36 | 2.14/.12/1.86/4.89/2.16/3.46 |
| closed above open | 54 | 74.1 | 2.30 | 5.2 | 1.5 | 15 / 2.46 | -/-/.61/2.55/4.57/1.86 |

Findings: no stable split. Year-by-year PF flips sign of the difference between the overnight and intraday groups (overnight better in 2021/2022/2024, worse in 2023/2025/2026), and the gap/no-gap split does the same, so there is no consistent conditioner; every subset has lower return than the live set (idle cash). The medians (overnight -0.6%, intraday -1.6%) say most of the drop is intraday in this universe, consistent with the dip being bought after weakness building during the session, but the live rules already capture that. Nothing beats the live row on PF, return, L12 and years together.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: pairs/relative-value or a true earnings-date test if dated data appears; own-idea run next (e.g. cooldown after a stopped-out trade in the same symbol).

## 2026-11-12 (run 38) - same-symbol re-entry memory re-tested on the NEW live vol60>=1.75% setup (own idea; follow-up of run 23's old-baseline test; lab_reentry2.py)
Source: none (own idea). Rules: LIVE trade list (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day); skip a signal if the same symbol's previous signal-trade exited within N days (any, or only if it lost). History = unfiltered live list (path-independent approximation). 3 variants (the "only after loss" variant is degenerate: it keeps 1 signal, since it drops all first entries; discarded).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| skip if prev trade lost <=20d | 307 | 73.3 | 2.75 | 58.5 | 4.3 | 100 / 3.31 | 2.41/.87/1.47/4.63/2.50/3.35 |
| skip if prev trade lost <=60d | 301 | 73.4 | 2.82 | 58.3 | 3.8 | 99 / 3.27 | 2.71/.87/1.51/4.63/2.47/3.29 |
| skip any re-entry <=20d | 283 | 73.1 | 2.70 | 51.5 | 3.6 | 92 / 3.19 | 2.27/.87/1.67/4.37/2.57/3.05 |

Findings: a stock that bounced-or-lost recently is not a worse candidate; every skip variant lowers PF, return and L12 PF (return -3 to -10 points) for at most a 0.5-point drawdown gain. Consistent with run 23: no same-symbol memory effect. Live re-entries are fine as is.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: web run (industry-adjusted reversal or pairs/relative value).

## 2026-11-12 (run 39) - beta-adjusted residual shock z-score (Asymmetric Idiosyncratic Reversal) as conditioner of the LIVE vol60>=1.75% setup (web-seeded; lab_resz.py)
Source: https://www.nber.org/papers/w35840 (Asymmetric Reversals: negative idiosyncratic shocks reverse more than positive ones; only the abstract was read, claim unverified, rules are my own). Rules: residual = stock daily return - beta x SPY return (beta from a 120d window ending ~60d before the signal); z3 = sum of the last 3 residuals / (residual stdev over the prior ~60d x sqrt 3). Split/rank the LIVE trade list (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day). 6 variants tried, no tuned thresholds (median/tertiles). Subset sims re-run.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| z3 below median (idiosyncratic drop) | 169 | 71.6 | 2.78 | 31.4 | 2.7 | 59 / 3.64 | 4.13/.12/1.21/4.81/1.79/3.54 |
| z3 above median (market-driven drop) | 173 | 74.6 | 2.70 | 26.5 | 2.8 | 48 / 3.08 | 1.28/-/2.23/3.82/2.32/3.55 |
| z3 bottom tertile (most idiosyncratic) | 109 | 65.1 | 2.05 | 13.6 | 2.9 | 40 / 2.35 | 2.35/.26/1.59/4.16/1.05/2.15 |
| z3 top tertile | 123 | 73.2 | 2.39 | 14.9 | 2.1 | 31 / 3.49 | 1.01/-/1.70/3.18/2.88/5.41 |
| skip top tertile | 217 | 73.7 | 3.01 | 44.3 | 2.9 | 77 / 3.39 | 3.46/.87/1.55/5.53/2.26/3.21 |
| rank by most negative z3 | 308 | 73.7 | 2.79 | 59.2 | 4.3 | 100 / 3.48 | 2.41/.87/1.38/5.46/2.21/3.58 |

Findings: the literature direction (bigger negative idiosyncratic shock = stronger reversal) does not hold: the most idiosyncratic tertile is the WORST (PF 2.05, win 65%), the two halves have near-equal PF, and the effect is non-monotone and flips by year. Ranking by z3 slightly lowers PF and return. Within vol60>=1.75% candidates the residual size adds no information (consistent with runs 14, 21, 35: stock-specific vs market-wide does not matter once the breadth/peer/vol filters are applied).
Verdict: NOT a promotion candidate; not added to challenger.py. Next: own-idea run (e.g. correlation of the candidate with the held book, or max positions per signal-day cluster) or a true earnings-date test if dated data appears.

## 2026-11-13 (run 40) - industry-adjusted reversal (stock 3d return minus same-sector peer mean 3d return) as conditioner of the LIVE vol60>=1.75% setup (web-seeded; lab_indadj.py)
Source: https://www.dimensional.com/us-en/insights/q-and-a-on-short-run-reversals-with-mamdouh-medhat-and-robert-novy-marx (industry-adjusted reversal claimed stronger; unverified, other universe, rules are my own; earlier "pairs" idea was already tested in run 17). Rules: idio = stock 3d % minus mean 3d % of its sector peers (lab_sector.feats); split/rank the LIVE trade list (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day). 6 variants tried, no tuned thresholds (median/tertiles); mild multiple-comparison discount.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| idio below median (lags sector) | 179 | 77.7 | 3.12 | 37.2 | 3.2 | 59 / 3.38 | 11.2/-/1.11/5.23/2.22/3.59 |
| idio above median | 158 | 70.3 | 2.48 | 21.0 | 2.3 | 50 / 3.74 | 1.25/.75/1.95/3.74/3.53/3.30 |
| idio bottom tertile | 125 | 74.4 | 3.21 | 27.7 | 2.4 | 47 / 3.24 | 160/-/1.42/5.95/1.62/3.35 |
| idio top tertile | 115 | 67.8 | 2.59 | 14.4 | 1.2 | 39 / 3.18 | 1.09/0/2.43/4.35/3.24/2.94 |
| skip idio bottom tertile | 209 | 71.3 | 2.05 | 22.5 | 3.4 | 62 / 2.87 | 1.10/.87/1.34/3.27/2.29/2.93 |
| rank by most negative idio | 308 | 73.7 | 2.70 | 58.5 | 4.3 | 100 / 3.37 | 2.41/.87/1.38/5.69/1.89/3.43 |

Findings: direction mildly matches the literature (stocks lagging their sector win 77.7% vs 70.3%, PF 3.1 vs 2.5), but the gain is small, L12 PF is unchanged (3.38 vs 3.37), 2023 and 2025 are worse than live, and the 2021 PF is tiny-sample noise (few losers). Return falls 60.6 -> 37.2 because half the trades are dropped. Ranking by idio instead of peer weakness lowers PF and return. The live peer-weakness rank already captures the sector component.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: own-idea run (e.g. correlation of candidate with held book / per-day cluster cap) or earnings-date test if dated data appears.

## 2026-11-13 (run 41) - signal-day cluster size, per-day cap and position cap on the LIVE vol60>=1.75% setup (own idea; follow-up listed in runs 39-40; lab_cluster.py)
Source: none (own idea). Rules: LIVE trade list (A+E+F, SPY>200d, breadth>=10%, vol60>=1.75, hold 7, stop 4 ATR, 10% x 12, 4/day). Cluster = number of base signals on the signal date (84 days with 1, 68 with 2, 26 with 3, then a long tail up to 24). Variants: per_day 1/2/3/6, max_pos 8/16, subsets by cluster size and by 3-signal-day trailing heat (median split). 10 variants tried; discount accordingly.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| per_day 1 | 208 | 70.7 | 2.22 | 25.4 | 3.3 | 66 / 2.63 | 2.79/.87/1.25/3.44/1.51/2.61 |
| per_day 2 | 281 | 73.3 | 2.67 | 49.8 | 4.2 | 91 / 3.27 | 2.25/.87/1.43/4.20/2.58/3.17 |
| per_day 3 | 300 | 73.7 | 2.76 | 56.8 | 4.3 | 98 / 3.20 | 2.29/.87/1.63/4.57/2.23/3.44 |
| per_day 6 | 311 | 74.0 | 2.84 | 61.8 | 4.3 | 100 / 3.39 | 2.41/.87/1.60/4.75/2.51/3.44 |
| max_pos 8 or 16 | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | identical to LIVE |
| cluster 1-2 signals only | 160 | 69.4 | 2.31 | 22.4 | 3.6 | 55 / 2.87 | 2.03/.75/.98/3.74/2.14/3.13 |
| cluster 3+ signals only | 177 | 75.7 | 2.82 | 31.3 | 3.1 | 55 / 3.79 | 2.67/-/2.39/3.97/2.06/3.62 |
| cluster 5+ signals only | 103 | 82.5 | 4.53 | 25.3 | 1.8 | 38 / 4.98 | 2.26/-/91/10.4/2.92/4.11 |
| 3-day heat <= median | 156 | 67.3 | 1.84 | 14.7 | 4.6 | 41 / 1.80 | 1.80/.87/.58/7.20/.97/1.94 |

Findings: (1) The position cap never binds on this filtered setup (8, 12 and 16 slots give identical results), so 12 slots is more than needed and nothing is gained by tuning it. (2) The 4/day cap barely matters (6/day adds 3 trades and nothing else; 1-3/day cuts return and PF), so live 4 is fine. (3) Isolated signals (1-2 per day) are clearly weaker (PF 2.3, win 69%) than clustered ones (3+: PF 2.8, win 76%; 5+: PF 4.5, win 82%), the same market-wide washout effect already captured by the breadth>=10% gate and the SPY-dip sizing tests (runs 19-20, 32). Skipping the sparse days would halve return (61.7 -> 31) for a small PF gain and 2023 is worse in the 3+ subset only by sample size, so it is not worth a rule. The 5+ subset PF is inflated by years with almost no losers (2023 PF 91).
Verdict: NOT a promotion candidate; not added to challenger.py; no live change suggested. Next: web-research run (e.g. VIX proxy via VIXY term structure, true PEAD if dated earnings data appears, or a short-hold overnight sleeve variant).

## 2026-11-13 (run 42) - exit rules (RSI2>70, close>SMA5/SMA10, prior-high OR RSI2>70, prior-high AND SMA5) re-tested on the LIVE vol60>=1.75% setup (own idea; run 25 was on the old setup; lab_exit2.py)
5 variants vs live (n=308, win 74.4, PF 2.83, ret 60.6, DD 4.3, L12 PF 3.37). rsi70: PF 2.04, ret 47.3; prior-high OR rsi70: PF 2.78, ret 58.1, L12 3.30 (2024 better, 2021/2023/2025 worse); ma5: PF 2.33, ret 51.2; ma10: PF 1.70, ret 39.1; prior-high AND ma5: PF 2.32, ret 54.2. Every variant is below live on PF, return and last 12 months.
Verdict: NOT a promotion candidate; not added to challenger.py. The live "close > prior high" exit stays.

## 2026-11-13 (run 43) - own-stock same-calendar-month seasonality (Heston-Sadka 12-month cycle) as conditioner of the LIVE vol60>=1.75% setup (web-seeded; lab_seas.py)
Sources: https://www.nber.org/papers/w20815.pdf , https://quantpedia.com/strategies/12-month-cycle-in-cross-section-of-stocks-returns , https://rhsmith.umd.edu/news/seasonality-stock-market-returns (search snippets only; claim unverified, rules are my own). Rules: seasonal = mean return of the stock in the same calendar month over the prior 2-5 completed years (needs >=2 years, so only 261 of 308 live trades, 2023+, qualify). Split/rank the LIVE trade list (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day). 7 variants tried, no tuned thresholds (median/tertiles).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref (all) | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 1.72/4.70/2.51/3.44 |
| LIVE ref (with feature) | 261 | 74.7 | 3.00 | 53.0 | 4.3 | 100 / 3.39 | 1.72/4.70/2.51/3.44 |
| seasonal >= median | 142 | 75.4 | 3.06 | 30.4 | 2.3 | 59 / 3.15 | 1.93/4.27/2.40/3.36 |
| seasonal < median | 138 | 72.5 | 2.59 | 18.6 | 2.9 | 44 / 4.01 | 1.80/5.11/1.30/3.65 |
| seasonal top tertile | 101 | 73.3 | 2.66 | 19.2 | 1.9 | 39 / 2.43 | 1.06/5.86/1.74/2.76 |
| seasonal bottom tertile | 92 | 72.8 | 2.50 | 11.5 | 2.0 | 24 / 3.28 | 1.76/6.20/1.45/2.94 |
| skip bottom tertile | 187 | 74.9 | 2.99 | 38.7 | 3.3 | 79 / 3.44 | 1.94/4.31/2.04/3.67 |
| rank by highest seasonal | 258 | 74.0 | 2.89 | 50.5 | 4.3 | 100 / 3.39 | 1.50/4.73/2.33/3.44 |

Findings: no seasonal effect inside the live setup. Win rate and PF are flat across halves/tertiles (73-75% win), the top tertile is not better than the bottom, L12 PF flips sign of the difference (top tertile 2.43 vs below-median 4.01), and ranking by seasonal leaves PF unchanged while lowering return. Only ~3.5 years of eligible trades, so power is low, but nothing points the right way.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: own-idea run (e.g. gap between signal close and next open as entry-timing check, or true PEAD if dated earnings data appears).

## 2026-11-13 (run 44) - strategy self-timing: skip/favour new entries by the LIVE setup's own last K closed trades (own idea; untested meta-filter; lab_meta.py)
Source: none (own idea; "trade the equity curve" concept, rules are my own). Rules: LIVE trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75, hold 7, stop 4 ATR, 10% x 12, 4/day). History = trades of the LIVE ref portfolio closed strictly before the signal date (needs K closed trades, otherwise allowed). 6 variants tried, thresholds not tuned beyond the single round value each; mild multiple-comparison discount.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| skip if last10 win%<50 | 291 | 75.3 | 3.18 | 63.6 | 2.4 | 100 / 3.39 | 2.41/.87/2.54/4.70/2.75/3.44 |
| skip if last10 mean pnl<0 | 274 | 74.8 | 3.12 | 58.8 | 2.4 | 95 / 3.36 | 1.93/.87/2.54/4.70/2.88/3.41 |
| skip if last20 mean pnl<0 | 275 | 73.5 | 2.88 | 56.9 | 4.9 | 100 / 3.39 | 2.41/.87/1.52/4.67/2.72/3.44 |
| only if last10 win%<=70 (after weak stretch) | 121 | 70.2 | 2.07 | 13.6 | 2.6 | 38 / 3.86 | 2.66/-/.58/2.58/2.16/3.01 |
| only if last10 mean pnl<=1% | 125 | 70.4 | 2.19 | 14.5 | 2.6 | 29 / 3.12 | 2.18/-/1.47/4.50/2.41/2.01 |
| skip if last5 has >=2 stops (pnl<-3%) | 280 | 75.7 | 3.18 | 62.2 | 3.4 | 96 / 3.35 | 2.18/.87/2.19/4.70/2.75->3.50/3.44 |

Findings: no "hot hand" (the "only after weak/cool stretch" variants are clearly worse), and the cold-streak skip is mildly protective: skipping after a last-10 win rate below 50% removes 17 trades, lifts PF 2.88 -> 3.18, nearly halves max drawdown (4.3 -> 2.4), no year is worse, but it only changes 2023 and 2025, L12 is identical (the gate never fired in the last 12 months) and the effect rests on ~17 trades in 2 years. The 20-trade window does nothing. Important implementation caveat: the gate was computed from the hypothetical LIVE-ref history; live, skipped periods produce no closed trades, so the gate would freeze unless shadow (paper-only) trades of skipped signals are tracked.
Verdict: NOT a promotion candidate (L12 not improved, tiny sample, needs shadow-trade bookkeeping); not added to challenger.py. Watch-list idea: revisit when more data accumulates. Next: web-research run (VIXY term structure / true PEAD if dated earnings data appears).

## 2026-11-13 (run 45) - stock-specific reversion tendency (trailing lag-1 autocorrelation; the stock's own earlier signal results) as conditioner of the LIVE vol60>=1.75% setup (web-seeded; lab_stockmem.py)
Sources: web search for RSI2/gap entry-timing write-ups returned mostly marketing-grade pages; the one fetched, https://www.quantrocket.com/blog/buy-or-sell-down-gaps/ (large down-gaps in stocks keep falling intraday, small gaps in uptrends recover; 2014-2020, 1-min data, no multi-day test), only confirmed that next-open/gap entry timing was already covered by runs 5/7/22, so I switched to a new idea with my own rules (Lo-MacKinlay style autocorrelation; unverified). Rules: (a) lag-1 autocorrelation of daily returns over the trailing 252 sessions on the signal day (negative = mean-reverting stock); (b) mean pnl of the same symbol's earlier closed rule signals (all-universe signal list, closed strictly before the signal date, needs >=3). Split/rank the LIVE trade list (breadth>=10%, weakest-peer rank, vol60>=1.75, 10% x 12, 4/day). 8 variants tried, median/tertile cuts only, no tuning.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref (all) | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| LIVE ref (with autocorr) | 290 | 74.5 | 3.02 | 60.0 | 4.3 | 100 / 3.39 | 3.83/.87/1.72/4.70/2.51/3.44 |
| autocorr < median | 157 | 73.2 | 2.84 | 25.1 | 2.2 | 60 / 3.89 | 2.59/.12/1.64/6.59/2.17/3.76 |
| autocorr >= median | 154 | 74.0 | 2.75 | 28.5 | 3.2 | 42 / 3.02 | -/-/1.57/4.37/1.56/3.22 |
| autocorr bottom tertile | 108 | 73.1 | 2.49 | 13.1 | 1.7 | 48 / 2.99 | 2.56/.26/.77/5.92/1.82/2.87 |
| autocorr top tertile | 99 | 69.7 | 2.42 | 15.8 | 3.7 | 28 / 3.51 | -/-/.86/5.84/1.18/3.34 |
| rank by lowest autocorr | 291 | 74.2 | 2.96 | 59.0 | 4.3 | 100 / 3.39 | 3.83/.87/1.45/5.85/2.18/3.46 |
| LIVE ref (with own history) | 245 | 76.3 | 3.70 | 60.5 | 2.6 | 100 / 3.39 | tiny-n 2021 / 0 / 3.36/5.70/2.51/3.44 |
| own-history mean pnl > 0 | 179 | 74.3 | 3.76 | 42.4 | 2.3 | 68 / 3.55 | 2021 n tiny/0/2.75/7.04/2.43/3.68 |
| own-history mean pnl <= 0 | 78 | 76.9 | 2.90 | 12.3 | 1.2 | 37 / 2.95 | -/0/2.01/3.38/3.77/2.91 |
| rank by own-history pnl | 246 | 76.4 | 3.77 | 60.7 | 2.7 | 100 / 3.52 | 2021 n tiny/0/2.99/6.11/2.51/3.63 |

Findings: no stock-level reversion memory. Low-autocorrelation ("mean-reverting") stocks do not beat high-autocorrelation ones (PF 2.84 vs 2.75; tertiles go the wrong way: bottom 2.49 vs top 2.42, win rate 73 vs 70), ranking by autocorrelation leaves PF/return flat. Own-history sign gives PF 3.76 vs 2.90 but the comparison base (with-history subset, PF 3.70) already shows the gain is a sample-selection effect (early 2021 trades drop out because they have no history), so the positive group is no better than its parent; returns fall to 42%. Years with real counts do not agree (2025: 2.43 vs 3.77).
Verdict: NOT a promotion candidate; not added to challenger.py. Per-stock memory adds nothing beyond vol60>=1.75. Next: own-idea run (e.g. true PEAD if dated earnings data appears; VIXY-based term-structure proxy is limited by the cache).

## 2026-11-13 (run 46) - "4% momentum burst" continuation sleeve: buy big up-days on volume, short hold (web-seeded, own rules; lab_burst.py)
Sources: https://tikamalma.substack.com/p/4-momentum-burst-detailed-research , https://www.thepatternsite.com/Volume.html (search-result titles only, not fetched; claims unverified). Rules: stock close >= +X% vs prior close, volume > 1.5x 20d avg (variants), close in top 25% of day range, SMA50>200 trend, SPY>200d, ATR%<6%, 5-day cooldown per symbol; enter like other sleeves, stop 4 ATR, fixed hold 3/5/10 days; 10% x 12, 4/day. Compared alone and added to the LIVE vol60>=1.75% trade list. 6 variants tried, none tuned beyond the round values.

| Variant (alone) | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| burst 4%, vol1.5x, hold5 | 504 | 51.4 | 1.13 | 13.1 | 13.2 | 119 / 0.88 | 2.65/.63/1.35/.82/1.06/.90 |
| burst 4%, vol1.5x, hold3 | 527 | 51.4 | 1.09 | 7.3 | 14.8 | 123 / 0.99 | 2.69/.65/1.07/.74/1.13/1.01 |
| burst 4%, vol1.5x, hold10 | 449 | 50.1 | 1.20 | 28.0 | 16.3 | 108 / 1.14 | 2.92/.57/1.21/.86/1.18/1.11 |
| burst 6%, vol1.5x, hold5 | 288 | 50.3 | 1.09 | 5.1 | 9.9 | 69 / 0.87 | 2.02/.15/1.44/.92/1.15/.93 |
| burst 4%, no vol filter, hold5 | 856 | 51.2 | 1.26 | 60.3 | 22.5 | 223 / 1.58 | 1.70/.66/1.13/1.01/1.03/1.70 |
| burst 4%, vol2x, close top 10%, hold5 | 170 | 50.0 | 1.12 | 3.9 | 8.5 | 35 / 0.60 | 2.54/.12/1.70/1.18/.92/.68 |

Combined with LIVE (same simulator, 12 slots shared): every variant lowers PF (2.88 -> 1.45-1.80) and raises drawdown (4.3 -> 6-18%); the best combined return is 144% for the no-volume variant but with PF 1.44 and 17.7% drawdown, i.e. it is just more risk taken; 2022 gets much worse in all.
Findings: no continuation edge after big up-days on daily bars in this universe; win rate ~50%, PF ~1.1, and only 2021 looks good (bull-market beta). The sleeve is not diversifying: it is long-only, regime-gated by the same SPY>200d filter, and takes slots from the high-PF live trades.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: own-idea run (e.g. sizing by per-stock realized downside, or true PEAD if dated earnings data appears).

## 2026-11-13 (run 47) - idle-cash overlay: park unused capital of the LIVE setup in SPY (own idea; portfolio-level; lab_cashspy.py)
Source: none (own idea; motivated by runs 9/32/35/36 repeatedly noting that restrictive filters leave cash idle). Rules: LIVE trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75, hold 7, stop 4 ATR, 10% x 12, 4/day). Each day the cash fraction = 1 - 10% x open positions; overlay earns cash fraction x SPY daily return, either only when the prior SPY close > SMA200 or always, at 100% or 50% of cash. Daily series with trade pnl booked on exit date (so MaxDD is realised-only, same basis for all rows). 4 variants tried; no tuning.

| Variant | Ret % | MaxDD | Monthly Sharpe | Last 12m ret % | Return by year 21/22/23/24/25/26 |
|---|---|---|---|---|---|
| LIVE alone | 61.6 | 4.3 | 1.96 | 21.2 | 5.7/-0.1/4.2/18.1/5.8/17.3 |
| cash->SPY if SPY>200d, 100% | 127.7 | 19.1 | 1.32 | 25.8 | 18.7/-15.1/13.9/38.3/14.4/25.3 |
| cash->SPY if SPY>200d, 50% | 93.1 | 9.5 | 1.65 | 23.6 | 12.1/-7.8/9.1/28.0/10.2/21.4 |
| cash->SPY always, 50% | 111.5 | 13.1 | 1.58 | 26.3 | 12.1/-9.6/16.1/28.0/13.1/24.0 |
| cash->SPY always, 100% | 167.7 | 25.3 | 1.24 | 31.3 | 18.7/-19.3/28.8/38.3/19.9/30.8 |
| SPY buy&hold (same window) | 83.1 | 25.4 | 0.83 | 12.0 | 13.0/-19.5/24.3/23.3/16.3/12.9 |

Findings: the overlay is just SPY beta added on top. Return rises, but Sharpe falls (1.96 -> 1.24-1.65), drawdown grows 2-6x, and 2022 turns from flat (-0.1%) to -8..-19% (the SPY>200d gate does not avoid the 2022 bear, it lags). The live setup's value is its near-zero market exposure (~uncorrelated, PF 2.9, DD 4.3%); diluting that with index beta contradicts the goal. A user who wants more return should use the already-logged size-up (15% x 8) or run the sleeve next to a separately held index position by choice, not inside the bot.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: web-research run (e.g. sector-level washout / VIXY term-structure proxy, or true PEAD if dated earnings data appears).

## 2026-11-13 (run 48) - overbought-fade SHORT sleeve in bear regimes (Connors-style RSI2 short; web-seeded topic, own rules; lab_short.py)
Sources: search only (https://www.quantconnect.com/research/15367/short-term-reversal/, https://quantifiedstrategies.substack.com/p/turnaround-tuesday-strategy-backtest; result titles, not fetched; claims unverified). Rules: stock RSI2 > 95 (or 98) at close, stock < SMA200, SPY < SMA200 (or sweep "bear" regime, or no gate, or no stock trend), short at close, stop 4 ATR, fixed hold 5 (or 3) days, 5-day cooldown per symbol; 10% x 12, 4/day; compared alone and added to the LIVE vol60>=1.75% list. 6 variants, no tuning.

| Variant (alone) | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF by year |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| short r2>95, SPY<200d, stk<200d, hold5 | 288 | 42.7 | 0.92 | -5.9 | 21.5 | 9 / 0.30 | -/1.25/.28/-/.41/.30 |
| short r2>98, same | 135 | 46.7 | 0.99 | -0.6 | 8.1 | 3 / 0.0 | -/1.06/.38/-/.91/0 |
| short r2>95, "bear" regime gate | 161 | 37.9 | 0.71 | -11.4 | 19.2 | 9 / 0.30 | -/.95/.05/-/.52/.30 |
| short r2>95, no market gate | 1140 | 47.2 | 0.89 | -22.3 | 38.2 | 193 / 0.65 | .59/1.51/.74/.79/.88/.57 |
| short r2>95, SPY<200d, no stock trend | 468 | 44.2 | 0.95 | -4.8 | 26.2 | 29 / 0.47 | -/1.25/.33/-/.70/.47 |
| short r2>95, hold3 | 325 | 47.1 | 0.90 | -6.3 | 18.0 | 9 / 0.84 | -/1.19/.23/-/.46/.84 |

Combined with LIVE: every variant lowers PF (2.88 -> 1.09-1.89) and raises drawdown (4.3 -> 7.7-16.5%); the least-bad (r2>98) gives 60.7% return / PF 1.89, i.e. nothing gained.
Findings: shorting overbought stocks in bear regimes has no edge on this universe; win rate 38-47%, PF <=1, only 2022 (the one sustained bear) is above 1 and even that is thin; 2023 and 2025 bear-gate bounces destroy it. Confirms the standing skepticism on shorts (violent bear-market rallies in a survivor universe of large caps).
Verdict: NOT a promotion candidate; not added to challenger.py. Next: own-idea run (e.g. sizing by per-stock realized downside; true PEAD if dated earnings data appears).

## 2026-11-14 (run 49) - downside semi-deviation, up/down vol asymmetry and worst-day crash history as selectors on the LIVE setup (own idea; follow-up listed in run 48; lab_downvol.py)
Source: none (own idea). Rules: LIVE trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day). Features over the last 60 daily returns: downside semi-deviation sqrt(mean(min(r,0)^2)), upside semi-deviation, worst single-day return. Variants: (a,b) drop the vol60 filter and require downside dev >=1.3 / >=1.5; (c,d) inside LIVE split by down/up ratio <1 vs >=1; (e,f) inside LIVE split by worst day > -8% vs <= -8%. 6 variants, thresholds not tuned (one pass), so a luck discount of roughly 1-in-6 applies to any "winner".

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF by year 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| breadth only (no vol filter) | 605 | 68.6 | 1.79 | 52.3 | 5.6 | 137 / 2.59 | 2.04/.13/1.35/1.93/1.71/2.66 |
| no vol filter, downside dev >=1.3 | 180 | 73.3 | 2.84 | 36.4 | 3.7 | 55 / 3.75 | 6.29/0.0/1.22/3.36/1.90/4.81 |
| no vol filter, downside dev >=1.5 | 131 | 74.8 | 3.32 | 31.4 | 2.7 | 43 / 5.21 | 3.58/-/1.51/3.59/2.80/5.98 |
| LIVE & down/up ratio <1 | 289 | 74.0 | 2.69 | 53.4 | 4.7 | 96 / 3.11 | 2.43/.87/1.55/4.76/2.32/3.06 |
| LIVE & down/up ratio >=1 | 26 | 76.9 | 5.07 | 5.1 | 0.5 | 5 / n.a. | 0/-/.87/6.08/5.04/- |
| LIVE & worst day > -8% | 269 | 72.9 | 2.62 | 42.6 | 3.8 | 88 / 2.86 | 3.18/.87/1.53/5.62/1.46/3.13 |
| LIVE & worst day <= -8% | 55 | 70.9 | 2.25 | 9.7 | 2.2 | 16 / 5.01 | .44/-/.55/2.48/3.83/4.20 |

Findings: downside semi-deviation is just another face of the vol60 filter (it selects the same high-vol names); it reaches PF 2.8-3.3 but at roughly half the trades and half the return (31-36% vs 61.7%), with 2023 weaker (1.2-1.5 vs 1.72) and 2021 wildly unstable. Splitting LIVE by down/up asymmetry or by crash history gives no usable improvement: the "bad" halves (ratio<1, worst day > -8%) hold most of the return, the other halves are tiny samples (26 and 55 trades, 5 and 16 in the last 12 months) with erratic yearly PF. No monotone, stable pattern, so no edge beyond vol60 itself.
Verdict: NOT a promotion candidate; not added to challenger.py. Live vol60>=1.75% remains the better selector (same PF band, double the return). Next: web-research run (e.g. sector-level washout / VIXY proxy, or true PEAD if dated earnings data appears).

## 2026-11-14 (run 50) - sector-level washout (share of same-sector peers with RSI2<10 on the signal day) as conditioner of the LIVE setup (web-seeded; lab_secwash.py)
Source: search only (https://sentimentrader.com/blog/massive-capitulation-in-the-utilities-sector; result titles only, not fetched; claims unverified). Rules: LIVE trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75, hold 7, stop 4 ATR, 10% x 12, 4/day); peer RSI2<10 share computed per signal over same-sector symbols (>=3 peers). Variants tried: 6 (thresholds 10/20/35/50% plus a rank variant); all post-hoc, so any winner is discounted for multiple comparisons.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF by year 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| sector washout >=20% | 216 | 71.8 | 2.73 | 37.8 | 3.8 | 67 / 3.87 | 2.45/.12/1.09/4.85/2.16/4.79 |
| sector washout <20% | 112 | 75.9 | 2.29 | 15.3 | 2.4 | 39 / 2.56 | 2.49/-/2.07/4.52/1.63/2.14 |
| sector washout >=35% | 158 | 71.5 | 2.50 | 22.4 | 2.8 | 50 / 3.89 | 2.46/0/1.03/5.37/1.54/4.78 |
| sector washout <10% | 63 | 76.2 | 1.83 | 4.9 | 1.4 | 22 / 1.34 | .65/-/4.19/10.07/1.16/1.38 |
| sector washout >=50% | 115 | 72.2 | 2.70 | 18.4 | 2.0 | 33 / 4.07 | 3.56/0/1.57/5.38/1.49/5.10 |
| rank by highest sector washout | 308 | 74.0 | 2.82 | 60.6 | 4.3 | 100 / 3.39 | 2.41/.87/1.58/4.67/2.51/3.44 |

Findings: no useful separation. Every washout threshold has lower PF than the live reference over the full period and about half the return; the high-washout buckets look better only in the last 12 months (PF 3.9-4.1 on 33-67 trades) while 2022 and 2023 get worse (2022 PF 0-0.12). Ranking by sector washout changes nothing (already captured by peer-weakness rank and the market breadth gate). Sector washout is just a thinner copy of the market breadth filter.
Verdict: NOT a promotion candidate; not added to challenger.py. Next: own-idea run (e.g. VIXY/vol-term proxy, or true PEAD if dated earnings data appears).

## 2026-11-14 (run 51) - cross-sectional return dispersion (universe stdev of 1d returns, trailing-250d percentile) as conditioner of the LIVE setup (own idea; lab_disp.py)
Rules: LIVE trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75, hold 7, stop 4 ATR, 10% x 12, 4/day); dispersion percentile uses only prior 250 days. Variants tried: 4 (split at 0.5 and 0.8); post-hoc, discount for multiple comparisons.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF by year 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| dispersion pct >= 0.5 | 167 | 74.3 | 3.79 | 40.2 | 2.1 | 67 / 4.76 | 4.97/.87/1.78/7.28/2.49/4.63 |
| dispersion pct < 0.5 | 168 | 74.4 | 2.13 | 19.2 | 3.9 | 42 / 2.12 | 2.31/-/1.10/3.54/2.54/2.08 |
| dispersion pct >= 0.8 | 82 | 73.2 | 3.78 | 21.0 | 2.1 | 39 / 4.04 | 115.9/0/.23/11.45/1.83/4.01 |
| dispersion pct < 0.8 | 239 | 74.5 | 2.47 | 35.5 | 3.6 | 65 / 3.05 | 1.87/-/1.95/3.27/2.17/3.23 |

Findings: the upper-half bucket has higher PF in every year (>= live in all 6) and lower drawdown, but halves the trade count so total return falls (40.2 vs 61.7%, capital sits idle); win rate is identical (74%), so the gain is in loss size, not hit rate. The top-quintile cut is unstable by year. The ">=0.5" effect is likely partly the same stress information as the breadth gate.
Verdict: NOT a promotion candidate (fails total-return bar); not added to challenger.py. Possible follow-up: use it as a size tilt (1.5x above median / 0.75x below) rather than a filter.
