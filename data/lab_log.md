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

## 2026-11-14 (run 21) - equity-curve throttling: skip entries after the strategy's own recent losers (web-seeded)
Source: https://www.luxalgo.com/library/concept/equity-curve-based-throttling/ (concept page only; no testable numbers, treated as unverified hypothesis). Script: lab_eqcurve.py.
Rules: LIVE setup unchanged (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day). Shadow curve = the unfiltered live portfolio's closed trades; an entry is skipped if, among the last N trades that exited BEFORE the entry date, mean pnl < 0 (or win% below a threshold). CONTRA rows do the opposite (skip after winners) as a direction control. 8 variants tried (multiple-comparison discount; N=10/20/30 grid, no tuning beyond that).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (vol175) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| skip if last10 mean pnl<0 | 274 | 74.8 | 3.06 | 57.8 | 2.4 | 2.61 | 3.34 | 1.93/.87/2.30/4.74/2.88/3.38 |
| skip if last20 mean pnl<0 | 275 | 73.5 | 2.83 | 56.1 | 4.9 | 2.32 | 3.37 | 2.41/.87/1.43/4.67/2.72/3.41 |
| skip if last30 mean pnl<0 | 276 | 73.2 | 2.71 | 51.7 | 4.3 | 2.10 | 3.37 | 2.41/.87/1.57/5.47/2.02/3.41 |
| skip if last10 win%<50 | 291 | 75.3 | 3.13 | 62.5 | 2.4 | 2.65 | 3.37 | 2.41/.87/2.30/4.74/2.75/3.41 |
| skip if last20 win%<60 | 277 | 73.3 | 2.81 | 56.0 | 5.0 | 2.29 | 3.37 | 2.41/.87/1.41/4.67/2.72/3.41 |
| CONTRA skip after winners (N=10/20/30) | 49-65 | 69-79 | 1.2-2.8 | 1-9 | 2.4 | 0.3-2.1 | - | tiny samples |

Verdict: NOT a promotion candidate. Only the N=10 versions help (max DD 4.3 -> 2.4, Sharpe 2.28 -> 2.65, PF 3.13), and they do so by dropping just 17-34 trades; the N=20/30 windows give no gain and lower return, so the effect is not stable across the window grid. Last-12-month PF is unchanged (3.37, the filter never fires in that period), and the "better" years are only 2023 and 2025 with the rest equal. A win%<50 on 10 trades is a very small-sample signal, the shadow curve depends on the same trades being evaluated, and the contra rows show winners-only periods are simply the low-trade-count periods (not informative). Possible use as a drawdown guard only; needs live data (the live bot has too few closed stock trades) before it is worth tracking. Not added to challenger.py.

## 2026-11-15 (run 22) - market-conditioned exits (SPY state decides when to leave) on the LIVE setup (own idea)
Source: none (the web-seeded exit variants were already covered by runs 25/28/42; this ties the exit to the market, not the stock). Script: lab_mktexit.py.
Rules: LIVE setup entries (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day). Only the exit changes: the live exit is "close > prior high". 6 variants tried (multiple-comparison discount; SPY RSI2 thresholds 10/20/70/80 are not tuned, one-shot).

| Variant | Trades | Win % | PF | Ret % | MaxDD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| ignore prior-high exit while SPY RSI2<10 | 306 | 74.2 | 2.80 | 62.2 | 4.3 | 2.31 | 100 / 3.53 | 2.06/.65/1.68/4.85/2.45/3.64 |
| ignore prior-high exit while SPY RSI2<20 | 304 | 74.0 | 2.88 | 65.3 | 4.2 | 2.30 | 100 / 3.82 | 1.96/.65/1.75/4.89/2.45/4.04 |
| also exit if SPY RSI2>70 | 326 | 70.9 | 2.81 | 52.4 | 3.6 | 2.38 | 106 / 2.72 | 8.39/.87/1.53/4.33/2.12/2.77 |
| also exit if SPY RSI2>80 | 320 | 73.1 | 3.03 | 60.5 | 3.5 | 2.49 | 104 / 2.87 | 6.77/.87/1.73/5.08/2.23/2.87 |
| prior-high exit only if SPY closed up | 302 | 72.5 | 2.76 | 64.7 | 4.4 | 2.38 | 99 / 3.36 | 1.99/.65/1.74/4.68/2.49/3.40 |
| control: prior-high exit only if SPY closed down/flat | 298 | 60.1 | 1.71 | 41.4 | 4.7 | 1.22 | 94 / 2.09 | 1.09/0/1.63/2.39/2.14/1.57 |

Verdict: NOT a promotion candidate. No variant moves PF/return meaningfully beyond noise: holding through market washouts (RSI2<20) gives PF 2.88 / return 65.3 / L12 3.82, but 2021 and 2022 get worse, only ~4 trades change, and it is one of 6 comparisons. The SPY-RSI2>80 exit lifts Sharpe slightly (2.49) and cuts drawdown (3.5) but L12 PF falls 3.37 -> 2.87 and 2021's PF is inflated by a tiny sample. The control (exit only on SPY-down days) is clearly worse (PF 1.71), which only confirms that the live exit already works best with market strength helping. The stock-level exit is not improved by market state. Not added to challenger.py. Next: true PEAD with earnings dates; relative-value pairs inside sector; cross-sectional stock 12-1m momentum sleeve with the vol60 filter.

## 2026-11-15 (run 23) - prior 21d/10d/5d return and distance-from-20d-high conditioning of the vol60>=1.75% LIVE setup (own idea; web search for a new Quantpedia short-term-reversal angle returned only index pages, https://quantpedia.com/strategies/short-term-reversal-in-stocks, no testable new rule). Script: lab_ret21.py.
Rules: LIVE setup (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day). Signals split at the full-sample median of the feature (mild look-ahead); each half re-run through the portfolio simulator. 8 variants (multiple-comparison discount).

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| ret21 > median (+1.4%) | 171 | 77.2 | 3.57 | 37.3 | 2.5 | 58 / 5.72 | 5.8/.12/1.48/4.35/2.81/8.09 |
| ret21 <= median | 163 | 71.2 | 2.08 | 19.1 | 3.4 | 48 / 2.23 | 1.73/-/1.04/4.59/2.37/1.9 |
| ret10 > / <= median (-4.2%) | 181 / 156 | 75.1 / 71.8 | 2.98 / 2.43 | 32.9 / 23.4 | 3.5 / 2.1 | 53 / 7.8 ; 54 / 2.03 | direction unstable |
| ret5 > / <= median (-5.3%) | 180 / 168 | 71.1 / 78.0 | 2.14 / 3.75 | 19.9 / 38.8 | 3.1 / 2.2 | 44 / 1.94 ; 69 / 4.54 | opposite sign of ret10 |
| dist from 20d high deeper / shallower | 167 / 169 | 74.3 / 75.1 | 2.81 / 2.98 | 34.3 / 23.9 | 2.9 / 2.1 | 67 / 3.57 ; 42 / 2.61 | no effect |

Verdict: NOT a promotion candidate. Each filter roughly halves the trade count and the return (37% or less vs 60.6%). The best, ret21 above median (PF 3.57, L12 5.72, 2026 PF 8.1), fails the return bar and collapses in 2022 (0.12); the ret10 and ret5 splits point in opposite directions, so the effect is not monotone and fits chance after 8 comparisons. Distance from the 20d high does nothing. Weak hint only: pullbacks inside a positive 1-month trend revert a bit better, consistent with the existing SMA50>SMA200 trend rule. Not added to challenger.py. Next: true PEAD with earnings dates, pairs inside sector, a non-overlapping sleeve (e.g. long-only gap-up continuation) to combine with the champion.

## 2026-11-15 (run 24) - SPY short-term trend (close vs SMA20) and 5d realized-vol state as conditioner of the LIVE setup (own idea). Script: lab_spysma.py.
4 variants (median split of SPY 5d realized vol, mild look-ahead). LIVE vol175: n=308, PF 2.83, ret 60.6, DD 4.3.
| Variant | n | Win % | PF | Ret % | DD | L12 PF |
|---|---|---|---|---|---|---|
| SPY > SMA20 | 162 | 74.1 | 2.49 | 20.8 | 2.4 | 2.92 |
| SPY <= SMA20 | 161 | 74.5 | 3.14 | 36.2 | 3.2 | 3.62 |
| SPY 5d rv > median | 170 | 73.5 | 3.11 | 36.2 | 3.8 | 2.75 |
| SPY 5d rv <= median | 156 | 73.7 | 2.28 | 18.8 | 2.4 | 4.38 |
Verdict: null. Win rate is identical across halves; PF differences come from a few years with tiny loss counts and the split halves return, failing the return bar. Mild hint (consistent with earlier fear-filter runs): signals during SPY weakness/higher vol are slightly better, already captured by the breadth filter. Not added to challenger.py.

## 2026-11-15 (run 25) - cross-sectional stock 12-1m momentum monthly sleeve, +/- vol60 tilt, combined with champion (web-seeded)
Source: https://quantpedia.com/strategies/momentum-factor-effect-in-stocks and https://quantpedia.com/optimization-of-equity-momentum/ (search results only; claims unverified, not relied on). Script: lab_xsmom.py (reuses lab_rotation.rotation on the stock universe).
Rules: first trading day of each month, rank universe stocks by 12-1m (or 6-1m) return, buy top N, hold 21 days, 0.05% slippage per side, optional SPY>200d gate, optional vol60>=1.75% filter on picks. Portfolio simulator 10% x 12, 4/day. 6 variants tried (multiple-comparison discount; no tuning beyond N=5/10/20 and lookback 6 vs 12).

| Variant | Trades | Win % | PF | Ret % | MaxDD % | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE vol175 champion | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| mom 12-1 top5 gate | 136 | 54.4 | 1.72 | 59.6 | 20.4 | 0.90 | 20 / 2.13 | 1.01/.10/1.08/4.72/1.42/2.68 |
| mom 12-1 top10 gate | 182 | 49.5 | 1.64 | 69.9 | 21.0 | 0.86 | 33 / 2.72 | 1.01/.10/1.03/3.02/1.19/3.18 |
| mom 12-1 top10 no gate | 232 | 53.9 | 1.84 | 121.8 | 17.2 | 1.05 | 37 / 3.09 | 1.01/.65/1.44/3.02/1.64/3.62 |
| mom 12-1 top10 gate + vol60>=1.75 | 160 | 51.2 | 1.82 | 84.3 | 20.2 | 0.98 | 30 / 2.97 | 1.01/.10/1.16/3.69/1.35/3.61 |
| mom 6-1 top10 gate | 192 | 49.5 | 1.49 | 48.3 | 20.8 | 0.79 | 36 / 1.83 | 1.42/.01/1.43/2.43/1.46/2.28 |
| mom 12-1 top20 gate (control) | 192 | 50.0 | 1.74 | 85.5 | 21.0 | 1.02 | 40 / 2.93 | 1.01/.10/1.03/3.18/1.18/3.43 |
| COMBINED champion + top10 no-gate | 483 | 64.0 | 1.91 | 195.0 | 15.9 | 1.14 | 116 / 3.18 | 1.31/.65/1.48/2.98/1.70/3.45 |
| COMBINED champion + top10 gate+vol | 406 | 64.5 | 1.92 | 143.8 | 17.3 | 1.04 | 109 / 3.10 | 1.31/.10/1.24/3.45/1.58/3.42 |

Verdict: NOT a promotion candidate. Standalone momentum earns real return (PF 1.6-1.8, 50-54% win) but with 17-21% max drawdown (champion 4.3%) and PF around 1.0 in 2021 and 2023; 2022 collapses when gated (0.10). Adding it raises combined return (up to 195%) but drops Sharpe 2.28 -> ~1.0-1.1 and PF 2.83 -> ~1.9, driven by a high-beta, highly correlated-to-market book that loses in selloffs, i.e. the opposite of an uncorrelated complement. Return gain is mostly leverage on market beta in a bull sample (2023-2026); vol60 tilt helps a little but is one of 6 comparisons. Not added to challenger.py. Next: pairs inside sector (relative value), true PEAD with earnings dates, momentum sleeve with market-neutral hedge (short SPY) to test whether the alpha survives beta removal.

## 2026-11-15 (run 26) - gap-up continuation sleeve (web-seeded: earnings/runaway-gap drift proxy)
Sources (search results only, titles; claims unverified, not relied on): https://quantifiedstrategies.substack.com/p/gap-trading-strategies-with-backtest , https://www.quantifiedstrategies.com/runaway-gaps/ , https://financialnoob.substack.com/p/buy-on-gap-strategy-and-its-performance . Script: lab_gapup.py.
Rules: open > prior close by >= g%, close > open, IBS >= 0.6, volume >= k x 20d avg, close > SMA50 > SMA200, SPY>200d, ATR% <= 8; buy at close, stop 4 ATR, hold 10 or 20 days (no early exit), 10-day cooldown per stock. Same simulator (10% x 12, 4/day). 6 variants tried (multiple-comparison discount). Combined = LIVE vol60>=1.75% setup + sleeve.

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| gap>=3% vol>=2x h10 | 157 | 54.8 | 1.07 | 2.4 | 8.6 | 33 / 0.71 | 1.41/.14/1.46/1.61/.67/.93 |
| gap>=3% vol>=2x h20 | 148 | 52.0 | 1.06 | 2.5 | 9.9 | 30 / 0.56 | 1.32/0/1.31/1.93/.72/.66 |
| gap>=5% vol>=2x h10 | 88 | 50.0 | 1.01 | -0.1 | 9.7 | 19 / 0.43 | |
| gap>=2% vol>=1.5x h10 | 287 | 51.2 | 1.10 | 8.1 | 11.0 | 72 / 0.90 | |
| gap>=3% vol>=2x h10 + vol60 | 121 | 55.4 | 1.07 | 2.4 | 11.3 | 29 / 0.70 | |
| gap>=5% vol>=2x h20 | 86 | 52.3 | 1.34 | 11.9 | 7.2 | 18 / 0.60 | |
| COMBINED LIVE + best (gap5 h20) | 368 | 68.8 | 1.92 | 69.3 | 8.9 | 109 / 1.50 | 2.0/.2/1.78/3.08/1.54/1.51 |
| COMBINED LIVE + gap3 h10 | 449 | 67.0 | 1.65 | 54.4 | 7.3 | 128 / 1.45 | |

Verdict: NOT a promotion candidate. Gap-up continuation has no edge on daily bars of this universe: PF ~1.0-1.3, ~50-55% win, last-12-month PF below 1 in every variant (0.43-0.90), 2025/2026 negative. Every combination lowers the champion's PF (2.83 -> 1.4-1.9), Sharpe and doubles drawdown; the sleeve is not a useful complement. Consistent with the earlier finding that this universe pays for short-term reversion, not continuation (also 52wh run 1, xsmom run 25). Not added to challenger.py. Next: pairs/relative value inside sector; true PEAD with earnings dates (earnings.py exists); market-neutral hedge of the momentum sleeve.

## 2026-11-15 (run 27) - relative-value pairs reversion (stock vs its most-correlated peer), own idea (also a Quantpedia/QuantConnect pairs/residual-reversal theme; no new sources fetched). Script: lab_pairs.py (first logged run).
Rules: each stock's partner = highest-correlation stock over the 252 days BEFORE each calendar year (corr > 0.5, 505 stock-years). Signal: z of the 60d log spread (stock/partner) <= threshold, close > SMA200, SPY>200d gate, ATR% <= 9; buy at close, exit on prior-high or 7 days, stop 4 ATR, 5-day cooldown. Same simulator (10% x 12, 4/day). 5 variants tried (multiple-comparison discount). Reference is the live setup before the vol60 filter (breadth>=10% + peer rank, PF 1.88), so compare within this table only.

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref (breadth+rank) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 136 / 2.65 | .13/1.42/2.19/1.92/2.68 |
| z<-2 h7 | 1022 | 65.4 | 1.21 | 25.8 | 6.3 | 283 / 1.33 | .43/1.02/1.37/1.36/1.31 |
| z<-2.5 h7 | 512 | 64.5 | 1.26 | 14.9 | 4.7 | 147 / 1.22 | .45/.99/1.77/1.27/1.22 |
| z<-2 & rsi2<10 | 320 | 66.9 | 1.47 | 17.3 | 3.6 | 98 / 1.48 | .09/1.97/2.03/.77/1.64 |
| z<-2 h5 | 1098 | 64.1 | 1.18 | 23.9 | 9.0 | 304 / 1.31 | .33/.97/1.46/1.28/1.31 |
| z<-1.5 & rsi2<10 | 528 | 63.1 | 1.35 | 23.0 | 5.7 | 152 / 1.54 | .16/1.61/1.60/1.08/1.57 |
| z<-2 breadth>=10% alone | 481 | 65.7 | 1.41 | 22.5 | 3.9 | 157 / 1.26 | .44/1.38/1.75/1.39/1.31 |
| COMBINED LIVE + z<-2 & rsi2<10 | 838 | 68.4 | 1.69 | 73.1 | 6.7 | 209 / 1.90 | .11/1.61/2.13/1.61/1.92 |
| COMBINED LIVE + z<-1.5 & rsi2<10 | 979 | 66.5 | 1.58 | 73.1 | 7.7 | 248 / 1.65 | .14/1.43/1.84/1.43/1.66 |

Verdict: NOT a promotion candidate. Pair-spread reversion has a mild positive edge standalone (PF 1.2-1.5, win 63-67%) but is weaker than the champion in every year, and the strongest variant (z<-2 & rsi2<10) is mostly the RSI2 rule already in the champion, with 2022 collapsing (0.09) and 2025 below 1. Combining adds return (60 -> 73%) but lowers PF (1.88 -> 1.58-1.69) and Sharpe and raises drawdown, so it is not a clean complement; the signals are largely the same oversold stocks the champion already trades (correlated, not diversifying). Long-only pairs here is not true market-neutral relative value. Not added to challenger.py. Next: true PEAD with earnings dates; momentum sleeve with a SPY hedge; sector-ETF-relative drop (needs sector map).

## 2026-11-15 (run 28) - capitulation-bar reversion sleeve: big ATR-sized down day + volume spike (web-seeded)
Sources (search results only, titles; claims unverified, not relied on): https://www.tradingview.com/script/WWuTjyDx-Capitulation-Stretch-Reversion-Jayadev-Rana/ , https://quantifiedstrategies.substack.com/p/turnaround-tuesday-strategy-backtest . Script: lab_climax.py. (Turnaround Tuesday itself is already covered by the weekday split in lab_dow.py.)
Rules: one-day drop (prior close - close)/ATR14 >= k, optional volume >= m x 20d avg and IBS cap, close > SMA50 > SMA200, SPY>200d, ATR% <= 9; buy at close, exit on prior high, hold 7, stop 4 ATR, 5-day cooldown. Same simulator (10% x 12, 4/day). 6 variants tried (multiple-comparison discount).

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| drop>=2ATR vol>=2x | 70 | 55.7 | 1.08 | 0.8 | 3.7 | 9 / 2.9 | -/0/1.25/.53/1.52/2.9 |
| drop>=3ATR vol>=2x | 13 | 69.2 | 0.72 | -0.6 | 1.3 | 1 | too few |
| drop>=2ATR vol>=2x IBS<=.2 | 46 | 58.7 | 1.50 | 2.8 | 2.8 | 8 / 8.6 | -/-/1.41/.52/8.9/8.6 |
| drop>=2ATR no vol filter | 134 | 57.5 | 1.11 | 1.9 | 7.0 | 18 / 3.2 | 1.41/0/1.8/.6/1.09/3.7 |
| drop>=3ATR vol>=2x + vol60 | 3 | 66.7 | 0.33 | -0.8 | 1.1 | 1 | too few |
| drop>=2ATR vol>=3x | 19 | 57.9 | 0.86 | -0.4 | 1.8 | 1 | too few |
| COMBINED LIVE + drop2 vol2 | 365 | 71.0 | 2.20 | 51.2 | 4.7 | 106 / 3.01 | 2.5/.82/1.35/2.22/2.37/2.94 |
| COMBINED LIVE + drop2 vol2 IBS<=.2 | 347 | 72.3 | 2.57 | 61.2 | 4.7 | 107 / 3.48 | 2.5/.87/1.39/2.99/2.59/3.57 |

Verdict: NOT a promotion candidate. Capitulation bars inside an uptrend with SPY>200d are rare (13-134 trades in 5+ years) and have no edge as a standalone sleeve (PF 0.7-1.5, 56-59% win, ~0-3% return). The only variant that looks good (IBS<=.2) has 46 trades and its PF is carried by 2025-26 (8.9/8.6 on 8 recent trades) while 2024 is 0.52 - small-sample luck among 6 comparisons. Combining dilutes the champion's PF (2.83 -> 2.2-2.6) with no return gain. Panic-day size is not a better selector than the champion's RSI2/breadth/vol60 logic. Not added to challenger.py. Next: true PEAD using earnings.py dates; momentum sleeve with SPY hedge; sector-ETF-relative drop.

## 2026-11-15 (run 29) - short-term volatility expansion (sd5/sd60, sd20/sd60, signal-day TR/ATR14) as conditioner of the vol60>=1.75% LIVE setup (own idea; follow-up of runs 12 and 28). Script: lab_volratio.py.
Rules: LIVE vol175 trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day) split at the median of each feature. 6 variants tried (multiple-comparison discount); 2026 not used to choose.

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| sd5/sd60 > med | 160 | 70.6 | 3.15 | 33.4 | 2.9 | 57 / 3.61 | 5.25/-/1.23/6.76/1.65/3.44 |
| sd5/sd60 <= med | 177 | 74.6 | 2.26 | 21.9 | 3.6 | 51 / 3.06 | 1.27/.75/1.70/3.38/2.23/3.73 |
| sd20/sd60 > med | 160 | 72.5 | 2.60 | 28.6 | 3.1 | 61 / 4.18 | 3.22/.12/1.23/2.44/2.21/4.78 |
| sd20/sd60 <= med | 170 | 76.5 | 3.30 | 29.9 | 2.2 | 46 / 2.77 | 1.88/-/2.03/9.67/3.48/2.36 |
| TR/ATR14 > med | 170 | 73.5 | 3.09 | 35.0 | 2.3 | 53 / 4.08 | 1.77/1.89/2.14/8.12/2.16/3.77 |
| TR/ATR14 <= med | 180 | 75.0 | 2.48 | 24.9 | 2.9 | 59 / 2.63 | 6.25/0/1.34/3.30/1.66/3.10 |

Verdict: NOT a promotion candidate. The two vol-ratio splits point in opposite directions (sd5 high better, sd20 high worse) and flip sign year to year, i.e. noise. Only TR/ATR14 > median looks good (PF 3.09, 2022 even 1.89) but it beats live in only 3/5 non-2022 years (2021 and 2025 lower), halves the trade count and return, and is 1 of 6 comparisons; consistent with run 28 that bigger signal-day bars are not a reliable selector. Not added to challenger.py. Next: true PEAD with earnings.py dates; momentum sleeve with SPY hedge; sector-ETF-relative drop.

## 2026-11-15 (run 30) - SPY signal-day close location (IBS) and overnight-gap vs intraday split as conditioner / size tilt of the vol60>=1.75% LIVE setup (own idea; web search for market-wide selloff reversion returned only substack/blog index pages, e.g. https://backtest.substack.com/p/buying-weakness-on-the-nasdaq-100, nothing testable and not relied on). Script: lab_spyibs.py.
Rules: LIVE vol175 trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day) split by SPY's own signal-day IBS = (close-low)/(high-low), SPY open-to-close return and SPY overnight gap (all known at the close). Size tilts emulated by scaling pnl (PF size-weighted). 11 comparisons tried (multiple-comparison discount). Earlier SPY 1d return skips were already tested (improvement_log); IBS/intraday/gap were not.

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| SPY IBS<0.3 only | 153 | 77.8 | 3.62 | 34.6 | 2.3 | 45 / 4.45 | 8.0/-/2.93/4.33/2.88/3.19 |
| SPY IBS>=0.3 only | 187 | 69.5 | 1.85 | 18.1 | 4.3 | 65 / 2.51 | 1.12/.75/.64/3.39/1.5/3.33 |
| SPY intraday<0 | 218 | 76.1 | 3.36 | 50.9 | 3.3 | 75 / 3.41 | 9.67/.26/2.11/3.96/2.79/3.27 |
| SPY intraday>=0 | 118 | 66.1 | 1.57 | 7.3 | 3.4 | 30 / 2.38 | .6/1.38/.81/5.03/.73/2.9 |
| SPY gap<-0.3% | 131 | 76.3 | 3.05 | 23.4 | 3.3 | 46 / 2.98 | -/-/1.3/7.07/1.29/4.43 |
| tilt 1.25x if SPY IBS<0.3 else 0.75x | 308 | 74.4 | 3.25 | 67.5 | 3.3 | 100 / 3.70 | 2.96/.95/2.18/5.20/2.87/3.49 |
| tilt 1.5x / 0.5x | 308 | 74.4 | 3.78 | 74.6 | 2.5 | 100 / 4.10 | 3.72/1.10/3.04/5.80/3.30/3.58 |
| tilt IBS<0.5 1.25x / 0.75x | 308 | 74.4 | 3.12 | 72.6 | 3.9 | 100 / 3.37 | 2.81/.72/1.94/5.52/2.68/3.45 |

Early/late check (threshold 0.3 was the first one tried, not tuned): IBS<0.3 vs live in 2021-23 PF 4.29 vs 1.89; in 2024-26 PF 3.31 vs 3.48 (equal-ish), so the effect is concentrated in the early years, and the late years are neutral rather than contradicting.
Verdict: PROMOTION CANDIDATE (as a size tilt, NOT as a filter). Days where SPY closes near its daily low (a market sell-off into the close) have much better reversion follow-through (PF 3.6 vs 1.9 elsewhere); intraday<0 shows the same thing. As a filter it halves return so it fails the return bar, but as a mild 1.25x/0.75x size tilt it beats live in every year including 2022 (0.87 -> 0.95), return 60.6 -> 67.5, max DD 4.3 -> 3.3, L12 PF 3.37 -> 3.70. Caveats: 11 comparisons, the three SPY features are strongly overlapping (one idea, not three), 2024-26 alone is only neutral, and it is the same economic story as the SPY-3d dip tilt (run 19/20, which did not hold on the new setup) and the dispersion tilt (run 52), so tilts may be partly redundant with each other; test stacking before any promotion. Added to challenger.py as "lab run30" variant for weekly tracking. Live rules NOT changed (the daily improvement task decides). Next: stack run30 + run52 tilts; true PEAD with earnings dates; sector-ETF-relative drop.

## 2026-11-16 (run 31) - stacking the run30 (SPY IBS) and run52 (dispersion) size tilts on the vol60>=1.75% LIVE setup (own idea; the follow-up named in run 30). Script: lab_stack.py. No web source this run (run 30 and 29 were own ideas; next run should be web).
Rules: LIVE vol175 trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day). Tilt D = 1.25x if cross-sectional dispersion trailing-250d percentile >= 0.5 else 0.75x; tilt I = 1.25x if SPY day IBS < 0.3 else 0.75x. Stack = product (or additive). PF is size-weighted. Data through 2026-10-29 (bars cache). 5 variants + 4 unscaled 2x2 cells (multiple-comparison discount; thresholds were fixed by runs 30/52, nothing re-tuned).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| D tilt only | 308 | 74.4 | 3.14 | 70.3 | 3.9 | 2.33 | 100 / 3.76 | 2.93/.87/1.78/5.30/2.58/3.73 |
| I tilt only | 308 | 74.4 | 3.25 | 67.5 | 3.3 | 2.35 | 100 / 3.70 | 2.96/.95/2.18/5.20/2.87/3.49 |
| STACK multiplicative | 308 | 74.4 | 3.63 | 79.2 | 3.0 | 2.34 | 100 / 4.17 | 3.74/.95/2.44/5.85/2.90/3.94 |
| STACK additive | 308 | 74.4 | 3.62 | 77.5 | 2.9 | 2.36 | 100 / 4.13 | 3.69/.93/2.46/5.88/2.94/3.83 |
| STACK 1.15/.85 each | 308 | 74.4 | 3.28 | 71.2 | 3.5 | 2.36 | 100 / 3.82 | 3.10/.91/2.05/5.37/2.75/3.70 |

2x2 cells (unscaled, n / PF): D&I 91 / 4.63; D only 87 / 2.13; I only 70 / 3.12; neither 111 / 1.62. Each condition is true on roughly 40-55% of signals; both-true 91 of 308 trades, so the two are partly independent, ordering is monotone (neither < one < both).
Verdict: the tilts stack in the expected direction: better than either alone and better than live in every year (2022 0.87 -> 0.95, 2023 1.62 -> 2.44), return 60.6 -> 79.2, DD 4.3 -> 3.0, L12 PF 3.37 -> 4.17. Caveats: Sharpe does not improve (2.28 -> 2.34), so much of the gain is a leverage-like effect of sizing up on days that are already the best; PF is size-weighted, so part of the PF gain is mechanical; the 'neither' cell is still PF 1.62, i.e. fine but worse; the 'D only/I only' cells in some years have a handful of trades. Both tilts come from one family (market-wide stress days), so this is one idea, not two. PROMOTION CANDIDATE only as a mild size rule (1.15x-1.25x / 0.75x-0.85x); not as a filter. Added to challenger.py as "lab run31" for weekly tracking. Live rules NOT changed. Next: web-seeded idea (true PEAD with earnings dates if earnings.py has history; residual-momentum), and check tilt implementability in bot sizing (needs live dispersion percentile + SPY IBS at the close).
