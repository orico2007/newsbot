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

## 2026-11-16 (run 32) - profit-lock exits (breakeven stop / ATR trailing stop once in profit) on the vol60>=1.75% LIVE setup (own idea; no earlier run tested trailing/breakeven stops; PEAD still untestable because the repo has no historical earnings dates, only a forward-looking Nasdaq calendar fetch; a web search for Quantpedia short-term-reversal pages returned only index pages: https://quantpedia.com/strategies/combining-fundamental-fscore-and-equity-short-term-reversals needs fundamentals, not testable on daily bars). Script: lab_trail.py.
Rules: LIVE vol175 trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, prior-high exit, 10% x 12, 4/day). Added: once a close >= entry + trigger x ATR the stop is raised to entry (BE) or to max(entry, highest close - trail x ATR). 5 variants tried (multiple-comparison discount).

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| BE after +0.5 ATR | 311 | 71.1 | 2.76 | 56.8 | 4.9 | 101 / 3.34 | 2.44/.87/1.42/4.84/2.49/3.38 |
| BE after +1 ATR | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | identical to live |
| BE after +1.5 ATR | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | identical to live |
| trail 1.5 ATR after +1 ATR | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | identical to live |
| trail 1 ATR after +0.5 ATR | 311 | 71.1 | 2.73 | 55.8 | 4.9 | 101 / 3.34 | 2.26/.87/1.42/4.84/2.49/3.38 |

Verdict: NOT a promotion candidate. Profit-lock stops are inert at +1 ATR and above because the live prior-high exit already sells on the first close above the previous day's high, so a trade almost never reaches +1 ATR without exiting; at +0.5 ATR they only convert some winners into scratches (return 60.6 -> 56-57, DD 4.3 -> 4.9, 2023 PF 1.62 -> 1.42). The existing exit already acts as the profit-taking rule. Not added to challenger.py. Next: sector-ETF-relative drop; residual momentum sleeve; a web search on market-wide capitulation / VIX-spike proxies.

## 2026-11-16 (run 21) - re-tuning hold / stop / exit / trigger breadth / vol threshold under the NEW live base (own idea; parameters were tuned before the vol filter existed)
Source: a web search for RSI2 exit/hold variants returned only generic pages (mql5 RSI2 article, Quantified Strategies RSI pullback posts); no testable specific claim. Rules: live base (breadth>=10%, weakest-peer rank, vol60>=1.75%, SPY>200d, 10% x 12, 4/day); one parameter changed at a time. Script: lab_retune.py. 12 variants tried (multiple-comparison discount; 2026 not used to select).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (vol175) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| LIVE at 12% x 10 | 308 | 74.4 | 2.83 | 76.5 | 5.2 | 2.28 | 100 / 3.37 | same |
| hold 5 | 311 | 70.7 | 2.39 | 50.0 | 5.5 | 1.86 | 100 / 2.63 | 2.71/.87/1.35/4.39/1.93/2.48 |
| hold 10 | 306 | 75.8 | 2.91 | 62.0 | 5.0 | 2.27 | 100 / 3.86 | 2.75/.87/1.55/5.58/2.00/4.34 |
| hold 15 | 305 | 76.1 | 2.92 | 62.1 | 4.8 | 2.29 | 100 / 3.72 | 2.75/.87/1.59/5.38/2.05/4.17 |
| stop 3 ATR / 6 ATR | 308 | 74.4 | 2.66 / 2.79 | 57.9 / 60.0 | 4.3 | 2.17 / 2.25 | 100 / 3.16, 3.37 | worse or equal |
| exit close>MA5 | 304 | 71.7 | 2.33 | 51.2 | 5.0 | 1.88 | 99 / 2.63 | 3.14/.23/1.23/3.18/2.30/2.65 |
| + rule G (3 down days) | 560 | 70.0 | 1.70 | 55.5 | 9.9 | 1.57 | 170 / 2.03 | 1.74/.33/.80/3.16/1.90/2.16 |
| + rule H (RSI2<10, nocrash) | 512 | 68.9 | 1.89 | 62.7 | 8.8 | 1.69 | 153 / 2.25 | 1.65/.69/.91/3.37/2.25/2.47 |
| gate none | 365 | 72.6 | 2.35 | 59.9 | 5.0 | 1.85 | 102 / 3.25 | 2.41/.75/1.97/4.74/2.51/3.25 |
| vol>=1.5 + rule H | 647 | 67.7 | 1.63 | 56.4 | 10.1 | 1.42 | 188 / 2.16 | 1.33/.40/.90/2.62/1.95/2.33 |
| vol>=2.0 | 235 | 75.7 | 3.39 | 56.8 | 4.5 | 2.45 | 76 / 4.13 | 7.68/1.38/1.42/4.62/2.60/4.80 |

Verdict: NOT a promotion candidate; the live parameters (hold 7, stop 4 ATR, prior-high exit, A+E+F, SPY>200d gate) remain near a local optimum under the new base. Hold 10/15 gain only ~3% PF and ~1.5 return points with higher drawdown and worse 2023/2025 - within noise after 12 variants. Widening the trigger set (G, H, lower vol threshold) adds trades but cuts PF to 1.6-1.9 and doubles drawdown, i.e. the edge is concentrated in the strict triggers. vol>=2.0 has higher PF/Sharpe and fixes 2022 (1.38) but loses ~4 return points on fewer trades (235); it is just the continuation of the monotone vol gradient (runs 8, 16) with ever fewer trades, not an independent signal. Sizing 12% x 10 raises return 60.6 -> 76.5% for +0.9pt drawdown (already known from run 9). Not added to challenger.py. Next: sector-ETF-relative drop (needs sector map), pairs/relative value, true PEAD with earnings dates.

## 2026-11-16 (run 22) - industry-momentum conditioning of the LIVE setup (web idea: reversal works better in winning industries)
Sources: https://www.cxoadvisory.com/technical-trading/reviving-short-term-reversal/ , https://www.cxoadvisory.com/momentum-investing/short-term-reversal-by-industry , https://mysimon.rochester.edu/novy-marx/research/RRLP.pdf (search results only, pages not fetched; claims are for monthly reversals on all stocks, unverified for this 3-7 day daily setup). Rules: live setup trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day) kept only if the sector-peer mean (self excluded) 126d return, or 12-1 month return, at signal day passes a threshold. Same simulator. Script: lab_indmom.py. 10 variants tried (multiple-comparison discount; 2026 not used to select; data through 2026-10-29).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE (vol175) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| sector 126d > 0 | 242 | 74.4 | 3.20 | 52.7 | 3.6 | 2.45 | 75 / 3.72 | 3.59/.87/1.94/4.76/2.53/3.99 |
| sector 126d <= 0 | 53 | 75.5 | 2.10 | 4.9 | 1.0 | 1.85 | 25 / 2.37 | thin |
| sector 126d > 5% | 208 | 72.6 | 3.26 | 47.7 | 2.8 | 2.55 | 65 / 3.47 | 7.01/.87/2.33/4.39/2.18/3.77 |
| sector 12-1m > 0 | 256 | 73.4 | 2.97 | 50.5 | 3.7 | 2.47 | 90 / 3.04 | 3.69/.87/1.15/6.17/2.39/3.0 |
| sector 12-1m > 10% | 208 | 73.6 | 3.07 | 42.4 | 2.9 | 2.36 | 60 / 3.44 | 3.69/.87/1.13/5.95/1.92/3.91 |
| no-vol base (breadth+rank) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| no-vol + sector 126d > 0 | 470 | 67.9 | 1.88 | 45.8 | 5.1 | 1.82 | 106 / 2.83 | no gain |

Verdict: NOT a promotion candidate. Winning-industry filters raise PF modestly (2.83 -> 3.2) and lower drawdown, but they remove 14-30% of trades and 8-18 return points, so they fail the return bar; weak-sector trades are still profitable (PF 2.1, 1.9 without the vol filter), so the literature effect does not turn into a loss to avoid here. Without the vol filter the filter does nothing for PF. Consistent with a small, noisy gain after 10 variants. Not added to challenger.py. Possible use only as a sizing tilt (not tested). Next: true PEAD with earnings dates, pairs/relative value, trend-following sleeve uncorrelated with champion.

## 2026-11-16 (run 21) - failed-breakdown / Turtle-Soup reversal sleeve on top of the LIVE setup (web idea)
Source: search hits only (Quantified Strategies new-low / reversal-day pages, https://quantifiedstrategies.substack.com/p/new-low-trading-strategy , https://www.pulse.bot/stock-trading/news/reversal-day-strategy-for-the-markets-1fbb2118-59a3-415b-8f16-28b75dbc8c47/); not fetched, claims unverified. Rules: long at close when today's low undercuts the prior N-day low (N=10 or 20) but the close is back above that prior low; optional IBS>=0.5; optional vol60>=1.75%; close>SMA200, SPY>200d, ATR/price<6%, breadth>=10%; exit prior-high/hold 7/stop 4 ATR; 10% x 12, 4/day; sleeve ranked AFTER live signals. Script: lab_fbd.py. 8 variants (multiple-comparison discount). Data through 2026-10-29, 2026 not used to select.

| Variant | Trades | Win % | PF | Ret % | MaxDD | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE (vol175) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| N=10 alone | 1174 | 63.9 | 1.03 | 2.9 | 18.4 | 1.39 | .91/.28/1.03/.94/1.0/1.46 |
| N=10 ibs>=.5 + vol175 alone | 501 | 69.3 | 1.24 | 15.7 | 7.9 | 1.63 | 3.31/.29/1.11/1.05/.90/1.99 |
| N=20 ibs>=.5 + vol175 alone | 299 | 71.2 | 1.31 | 11.3 | 6.1 | 1.72 | 5.32/.14/1.11/1.18/1.15/1.88 |
|   + live combined | 518 | 72.0 | 1.98 | 64.0 | 5.6 | 2.32 | 2.7/.14/1.62/2.75/1.7/2.36 |
| (other 5 variants: PF 0.97-1.16 alone, combined PF 1.21-1.68) | | | | | | | |

Verdict: NOT a promotion candidate. Standalone, the failed-breakdown signal has no real edge on daily bars (PF 0.97-1.31, best only after stacking vol and IBS filters, which is the same exposure the live setup already captures). Every combination dilutes the live setup (PF 2.83 -> <=1.98, Sharpe 2.28 -> <=1.72, worse in 2022-2025 each year). Not added to challenger.py. Next ideas: sector-relative pairs with live signals, multi-day (2-5 day) holding-period decay by vol tier, true PEAD with earnings dates.

## 2026-11-16 (run 23) - SPY-hedge overlay (market-neutralising each trade) on the LIVE setup (own idea, previously untested)
Source: none (web search for new daily-bar reversion ideas returned only gap / Turnaround Tuesday / IBS / 5-day-low pages that earlier runs already cover: https://algomatictrading.substack.com/p/strategy-9-the-5-day-mean-reversion , https://financialnoob.substack.com/p/buy-on-gap-strategy-and-its-performance , https://quantifiedstrategies.substack.com/p/turnaround-tuesday-strategy-backtest). Rules: live trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day); each trade's pnl_pct reduced by h x SPY return over the same entry-to-exit dates (a short-SPY hedge, zero hedge cost assumed, which flatters it). Script: lab_hedge.py. 7 variants (multiple-comparison discount; 2026 not used to select).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE unhedged | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| hedge 0.25 x SPY | 308 | 74.4 | 2.80 | 56.7 | 4.0 | 2.26 | 3.27 | 2.44/.99/1.64/4.47/2.34/3.46 |
| hedge 0.5 x SPY | 308 | 74.4 | 2.74 | 52.8 | 3.6 | 2.21 | 3.17 | 2.47/1.22/1.66/4.08/2.17/3.51 |
| hedge 1.0 x SPY | 308 | 74.4 | 2.54 | 45.3 | 3.3 | 2.06 | 2.95 | 2.45/3.32/1.63/3.21/1.83/3.59 |
| hedge 1.0 x beta60 x SPY | 308 | 74.4 | 2.03 | 32.7 | 3.2 | 1.61 | 2.49 | 1.95/1.20/1.57/2.11/1.43/3.13 |
| hedge 0.5 x beta60 x SPY | 308 | 74.4 | 2.53 | 46.0 | 3.3 | 2.05 | 2.96 | 2.29/.94/1.67/3.39/1.97/3.33 |
| hedge 1.0 only if SPY<SMA50 | 308 | 74.4 | 2.77 | 56.0 | 3.7 | 2.23 | 3.21 | 2.23/.48/1.91/3.99/2.24/3.66 |

Verdict: NOT a promotion candidate. The strategy's edge is not market beta: every hedge lowers PF, return, Sharpe and last-12-month PF while only trimming drawdown (4.3 -> 3.3% at best) and turning 2022 positive (full hedge 3.32, but at -15 return points and the 2024-25 PF dropping). Even with a free hedge Sharpe falls, so a costly real hedge would be worse. The 2022 benefit is the only argument, and the live SPY>200d gate plus breadth filter already handle most of it. Not added to challenger.py. Next: true PEAD with earnings dates (needs data), universe/survivorship cross-check, trend-following sleeve uncorrelated with champion.

## 2026-11-17 (run 24) - hold period per volatility tier on the LIVE setup (own idea; follow-up listed in run 21)
Source: web search for new daily-bar reversion ideas (consecutive-down-days, 5-day-low, rubber-band, residual reversal pages on pulse.bot, quantifiedstrategies, cxoadvisory, robeco) only returned topics already covered in runs 4, 14, 15 and 21, so this is an own-idea run. Rules: live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, stop 4 ATR, exit prior high, 10% x 12, 4/day); each signal takes its max hold from its vol60 tier (cut 2.5%). Script: lab_holdtier.py. 9 variants (multiple-comparison discount; tier cut 2.5% chosen a priori, 2026 not used to select).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE hold 7 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| hold 5 all | 311 | 70.7 | 2.39 | 50.0 | 5.5 | 1.86 | 2.63 | 2.71/.87/1.35/4.39/1.93/2.48 |
| hold 10 all | 306 | 75.8 | 2.91 | 62.0 | 5.0 | 2.27 | 3.86 | 2.75/.87/1.55/5.58/2.00/4.34 |
| vol<2.5: hold 10, else 7 | 307 | 75.6 | 3.05 | 63.9 | 4.4 | 2.41 | 3.59 | 2.75/.87/1.73/5.43/2.51/3.73 |
| vol<2.5: hold 15, else 7 | 307 | 75.6 | 3.03 | 63.6 | 4.4 | 2.40 | 3.51 | 2.75/.87/1.73/5.43/2.51/3.61 |
| vol<2.5: 7, else 5 | 310 | 72.6 | 2.41 | 51.2 | 5.3 | 1.91 | 2.63 | 2.32/.87/1.40/4.26/2.21/2.47 |
| vol<2.5: 10, else 5 | 309 | 73.8 | 2.59 | 54.6 | 5.2 | 2.09 | 2.77 | 2.63/.87/1.53/4.81/2.21/2.65 |
| vol<2.5: 5, else 10 | 309 | 72.5 | 2.63 | 56.5 | 5.7 | 1.99 | 3.63 | 2.83/.87/1.29/5.02/1.76/3.96 |
| vol<2.5: 7, else 10 | 308 | 74.4 | 2.68 | 58.2 | 5.3 | 2.12 | 3.60 | 2.41/.87/1.62/4.85/2.00/3.91 |

Verdict: marginal, WATCH only (weak PROMOTION CANDIDATE, not added to challenger.py because per-tier hold needs a new post-processor and the gain is small). "Low-vol tier (vol60 1.75-2.5%) holds 10 days, high-vol tier holds 7" is >= live in every year and on PF (3.05 vs 2.83), return, Sharpe and L12 (3.59 vs 3.37), with max DD flat (4.4 vs 4.3). But the gain is +0.2 PF on ~9 comparisons, tied to an exit-time parameter the live bot already tuned (run 21 found hold 10 slightly better too), and the same direction (longer hold helps low-vol stocks) shows in hold 10 all. Shorter holds hurt everywhere (hold 5 PF 2.39), so the signal is that live hold 7 is near-optimal and a longer hold for the calmer tier is a small, plausible refinement. Expected live benefit is within noise. Next: PEAD with earnings dates (needs data), trend-following sleeve uncorrelated with champion, survivorship cross-check.


## 2026-11-17 (run 33) - washout-cascade conditioners on the LIVE setup: consecutive lower lows, N-day closing low, signal-day IBS, 5d depth in ATR (web-seeded)
Source: https://algomatictrading.substack.com/p/strategy-9-the-5-day-mean-reversion (idea only: "5-day washout, a close after a cascade of lower lows"; rules are paywalled, no numbers trusted), https://algotr.substack.com/p/the-mean-reversion-portfolio-that (IBS/RSI2/%B combo, paywalled, no rules). Search surfaced no other testable rule. Script: lab_lowcascade.py. Base = live trade list (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day). Each variant is a filter (or size tilt) on signal-day features. 13 variants tried (multiple-comparison discount; choose-early/confirm-late not needed because nothing passed).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE vol175 | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| lower-lows streak >=2 | 256 | 74.2 | 2.86 | 50.2 | 4.6 | 2.16 | 3.76 | 2.86/.87/1.28/4.66/2.48/4.09 |
| lower-lows streak >=3 | 194 | 74.2 | 3.02 | 38.0 | 3.0 | 2.36 | 3.52 | 3.62/1.89/1.14/6.38/2.85/3.40 |
| lower-lows streak <=1 | 78 | 71.8 | 1.86 | 7.0 | 2.4 | 1.16 | 2.31 | 1.34/-/1.18/3.33/2.48/1.58 |
| close = 10d closing low | 254 | 73.6 | 3.01 | 50.1 | 3.0 | 2.30 | 2.90 | 3.91/-/1.78/5.63/2.37/2.76 |
| close = 20d closing low | 97 | 69.1 | 2.07 | 11.4 | 1.9 | 1.30 | 2.21 | 2.4/-/1.24/3.69/1.4/2.18 |
| signal-day IBS <= 0.25 | 202 | 73.8 | 2.48 | 32.2 | 2.7 | 1.77 | 4.24 | 2.02/-/1.99/2.09/2.52/3.73 |
| signal-day IBS > 0.25 | 155 | 71.6 | 2.49 | 21.9 | 3.9 | 1.64 | 2.24 | 3.61/.75/.86/7.95/1.48/2.81 |
| 5d depth >= 3 ATR | 49 | 85.7 | 4.99 | 12.2 | 2.1 | 2.27 | 9.87 | thin (only 3 years have trades) |
| 5d depth < 3 ATR | 281 | 72.2 | 2.42 | 44.2 | 4.2 | 1.86 | 2.80 | 2.17/.75/1.63/4.28/1.63/2.85 |
| size LL>=3 x1.5 else x1 | 308 | 74.4 | 2.90 | 87.1 | 5.8 | 2.27 | 3.45 | 2.51/1.06/1.50/5.25/2.62/3.51 |
| size LL>=3 x1.25 else x0.75 | 308 | 74.4 | 2.91 | 66.4 | 4.7 | 2.26 | 3.47 | 2.53/1.11/1.48/5.40/2.65/3.54 |
| size LL>=3 x1.5 else x0.75 | 308 | 74.4 | 2.93 | 79.5 | 5.5 | 2.24 | 3.50 | 2.58/1.19/1.43/5.65/2.69/3.58 |

("close = 5d closing low" was identical to live: the live rules already force it.)
Verdict: NOT a candidate. Filtering by cascade depth raises PF a little (LL>=3 3.02, 10d low 3.01) but cuts total return by 17-37% because the trades removed were still profitable, and 2023 gets worse (1.14-1.28 vs 1.62). As a size tilt, Sharpe is flat or lower (2.24-2.27 vs 2.28): the extra return is just more exposure with higher drawdown. The "5d depth >= 3 ATR" bucket looks great (PF 5, L12 9.9) but has only 49 trades and 3 active years, so it is noise-sized. Lower-low streak is largely redundant with the already-tested down-close streak and the vol60 filter. Not added to challenger.py. Web claims (cascade washout edge) not confirmed on this universe.

Repo hygiene note: the lab_log.md on origin/main had lost runs 21-32 filed on a parallel branch (commit 59c69ed history); this run restored that full text and re-appended main's runs 21-24 sections. Run numbers 21-24 therefore appear twice with different topics.

## 2026-11-17 (run 34) - priority ranking of same-day signals by vol60 on the LIVE setup (own idea). Script: lab_volrank.py
Live (weakest-peer rank): n=308, PF 2.83, ret 60.6%, Sharpe 2.28. Rank vol60 high first: PF 2.74, ret 59.4%. Low first: PF 2.84, ret 60.5%. Per-day cap rarely binds on the filtered set, so ranking is irrelevant; no variant beats live on return. No edge, not added to challenger.py. (2 variants tried.)

## 2026-11-17 (run 35) - signal-weekday seasonality re-tested on the vol60>=1.75% LIVE setup (web-seeded: Turnaround Tuesday / day-of-week pages, https://quantifiedstrategies.substack.com/p/turnaround-tuesday-strategy-backtest , claims unverified). Script: lab_dow_live.py
Follow-up of run 18, which ran before the vol filter. Live setup (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day), trades filtered by signal weekday. 10 variants tried (multiple-comparison discount: with ~60-90 trades per day-slice, differences in PF are mostly noise).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| only Mon | 48 | 60.4 | 1.54 | 2.9 | 2.0 | 19 / 0.64 | -/1.38/1.74/1.15/1.14/0.50 |
| only Tue | 87 | 73.6 | 2.23 | 11.0 | 2.7 | 33 / 3.29 | 3.52/0/1.43/3.35/1.56/3.90 |
| only Wed | 93 | 78.5 | 4.40 | 19.3 | 0.9 | 28 / 3.32 | 2.03/-/31/18.8/4.18/2.46 |
| only Thu | 81 | 72.8 | 2.04 | 9.4 | 1.8 | 20 / 5.91 | 0.6/-/0.93/4.07/1.46/11.5 |
| only Fri | 73 | 76.7 | 3.52 | 14.8 | 1.8 | 22 / 24.1 | -/-/0.79/3.07/1.93/41 |
| skip Mon | 279 | 76.7 | 3.07 | 58.0 | 4.1 | 91 / 4.90 | 1.91/.26/1.40/4.93/2.88/5.21 |
| skip Tue | 259 | 75.3 | 3.02 | 50.9 | 2.8 | 79 / 3.43 | 2.45/1.89/1.81/5.46/2.54/3.20 |
| skip Wed | 242 | 71.9 | 2.42 | 37.7 | 4.1 | 79 / 3.15 | |
| skip Thu | 255 | 72.9 | 2.98 | 50.0 | 3.5 | 87 / 3.10 | |
| skip Fri | 256 | 73.4 | 2.50 | 42.1 | 4.1 | 83 / 2.69 | |

Verdict: NOT a promotion candidate. Monday-signal trades are the weakest slice (PF 1.54, 60% win, L12 PF 0.64, n=48), and skipping them lifts PF to 3.07 and L12 PF to 4.90, but total return falls (58.0 vs 60.6%), 2022 and 2023 get worse, and with 10 slices tried the Monday weakness is within what chance would produce. No "Turnaround Tuesday" edge on this setup (Tue PF 2.23 is below the average). Only watch item: Monday weakness persisting in 2026 live trades. Not added to challenger.py.

## 2026-11-17 (run 36) - walk-forward re-selection of the vol60 threshold (own idea: out-of-sample audit of the live vol60>=1.75% filter). Script: lab_wfvol.py
Source: none (own idea; no web run needed, runs 33 and 35 were web-seeded). Rules: base = live trade list without the vol filter (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day). For each year Y from 2022, the vol60 threshold from {0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0} is chosen using ONLY trades before Y (objective PF, or return), then applied to year Y; the yearly slices are chained. Year 2021 unfiltered (no history). 7 fixed + 2 walk-forward variants (multiple-comparison discount).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| fixed thr 0 (no filter) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| fixed 1.5 | 382 | 71.7 | 2.33 | 59.8 | 4.9 | 2.05 | 117 / 3.44 | 1.74/.19/1.66/3.15/2.10/3.52 |
| fixed 1.75 (LIVE) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| fixed 2.0 | 235 | 75.7 | 3.39 | 56.8 | 4.5 | 2.45 | 76 / 4.13 | 7.68/1.38/1.42/4.62/2.60/4.80 |
| fixed 2.5 | 139 | 74.8 | 3.30 | 35.8 | 2.5 | 2.07 | 43 / 4.08 | 3.99/-/1.91/4.37/2.02/5.42 |
| walk-forward, objective PF | 284 | 72.2 | 2.61 | 49.8 | 4.5 | 2.06 | 76 / 4.13 | 1.89/1.38/1.42/4.37/2.60/4.80 (chose 2.0,2.0,2.5,2.0,2.0) |
| walk-forward, objective return | 332 | 72.6 | 2.56 | 57.0 | 4.5 | 2.31 | 100 / 3.37 | 1.89/1.38/1.42/4.62/2.51/3.41 (chose 2.0,2.0,2.0,1.75,1.75) |

Verdict: the vol filter survives an honest out-of-sample selection. Choosing the threshold only from past data picks 1.75-2.5 in every year (never 0 or 1.25), and the chained out-of-sample result (PF 2.56-2.61, Sharpe 2.06-2.31, max DD 4.5%) is far above the unfiltered base (PF 1.88, DD 5.9%); the walk-forward by return reproduces live-like numbers (ret 57.0 vs 60.6%). Walk-forward never rescues 2023 (1.42) and 2022 only appears positive because the 2.0 threshold keeps few trades. The 2.0 threshold keeps winning PF and Sharpe each year but gives up return (56.8 vs 60.6%) from fewer trades, so no case to move off 1.75. No change; not added to challenger.py (not a new strategy). Confidence in the filter rises; it is not a lucky full-sample pick. Next: trend-following sleeve uncorrelated with champion, survivorship cross-check, true PEAD if earnings dates become available.

## 2026-11-17 (run 37) - risk-appetite leadership (IWM small-cap, QQQ growth vs SPY, 5d/20d) as conditioner of the LIVE setup (own idea; cross-asset filter from the seed list, follow-up of the XLP/XLU test). Script: lab_riskapp.py
Source: none (own idea). Live setup filtered by whether IWM or QQQ out/under-performed SPY over the last 5 or 20 days at signal time. 8 variants tried (multiple-comparison discount; slices are ~100-230 trades).

| Variant | Trades | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 2.32 | 100 / 3.39 | 2.41/.87/1.72/4.7/2.51/3.44 |
| IWM leads SPY 5d | 86 | 75.6 | 3.53 | 19.0 | 2.8 | 1.64 | 34 / 5.18 | .43/0/2.07/26/7.6/5.1 |
| IWM lags SPY 5d | 229 | 73.8 | 2.54 | 35.7 | 4.7 | 2.07 | 69 / 2.93 | 7.7/-/1.36/2.88/2.15/2.87 |
| IWM leads SPY 20d | 108 | 79.6 | 3.46 | 21.6 | 2.4 | 1.85 | 37 / 13.8 | .76/-/1.31/4.1/17/10.3 |
| IWM lags SPY 20d | 205 | 69.8 | 2.29 | 29.6 | 4.2 | 1.93 | 63 / 2.18 | 4.96/.87/1.43/3.6/1.26/2.5 |
| QQQ leads SPY 5d | 144 | 67.4 | 1.74 | 11.1 | 2.4 | 1.22 | 45 / 2.03 | 1.54/-/.97/2.15/2.04/1.88 |
| QQQ lags SPY 5d | 177 | 78.5 | 3.40 | 42.7 | 4.9 | 2.17 | 57 / 4.62 | 8.25/.87/1.53/12.2/1.89/5.9 |
| QQQ leads SPY 20d | 184 | 70.7 | 2.23 | 22.5 | 2.4 | 1.64 | 46 / 2.07 | 2.04/-/1.82/2.83/2.51/1.84 |
| QQQ lags SPY 20d | 136 | 80.9 | 4.47 | 37.3 | 2.3 | 2.62 | 58 / 4.89 | 4.7/.87/2.09/26.9/2.66/6.5 |

Verdict: NOT a candidate as a filter. "QQQ lags SPY" slices have much higher PF (3.4-4.5) and win rate (79-81%), but each drops 30-40% of total return since half the trades are removed, and 2022 is unchanged (.87). IWM slices are inconsistent (IWM leads: 2021 PF 0.43-0.76 then huge later, a regime artifact; IWM lags: PF 7.7 in 2021 then 1.3-2.9). Direction of effect differs between IWM and QQQ, a sign of noise. Only watch item: "QQQ lags SPY 20d" as a possible size tilt (up-size when growth lags) - worth one run if sizing tilts are revisited. Not added to challenger.py.

## 2026-11-17 (run 21) - FOMC-meeting cycle (pre-FOMC drift) on the live vol60>=1.75% setup (web idea)
Source: Lucca-Moench pre-FOMC announcement drift, https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf ; Quantpedia https://quantpedia.com/strategies/federal-open-market-committee-meeting-effect-in-stocks (search-level only, not fetched; index-level, other era, unverified for single-stock reversion). FOMC decision dates typed from memory of the Fed calendar (not verified; a wrong date would only add noise). Rules: live setup (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day); tag signals by trading-day offset to the decision day. Script: lab_fomc.py. 7 groupings (multiple-comparison discount; data through 2026-10-29, 2026 not used to select).

| Group | Trades | Win % | PF | Ret % | MaxDD | L12 n / PF |
|---|---|---|---|---|---|---|
| LIVE vol60>=1.75 (ref) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 |
| entry day -1 / 0 / +1 | 10 / 9 / 12 | 60 / 67 / 67 | 1.17 / 2.74 / 1.11 | ~0-1 | | too few |
| window -2..+1 | 34 | 64.7 | 1.84 | 2.9 | 1.4 | 9 / 1.0 |
| hold spans FOMC (-6..-1) | 60 | 75.0 | 3.28 | 13.6 | 2.4 | 21 / 5.32 |
| excluding window -2..+1 | 280 | 75.4 | 3.05 | 58.7 | 3.3 | 92 / 3.78 |
| post-FOMC +1..+5 | 36 | 77.8 | 3.93 | 5.0 | 0.9 | 14 / 11.96 |

Verdict: NOT a promotion candidate. The only visible pattern (signals right around the announcement are weaker, PF 1.84 on 34 trades) is within chance after 7 comparisons; excluding them lifts PF 2.83 -> 3.05 but lowers return 60.6 -> 58.7%, failing the return bar. No bucket has enough trades per year to judge. Not added to challenger.py. Next: true PEAD with earnings dates (earnings.py), sector-ETF-relative drop, per-stock reversion-hit-rate memory re-test on the vol-filtered set.

Repo hygiene (2026-11-17): the 28 entries below ("runs 6-33" of the 11-05..11-09 lineage) had been clobbered out of this file by a concurrent run; restored verbatim from 4679e88. Their run numbers overlap the numbering above; use the dates. Always `git pull --rebase` BEFORE editing this file.

## RESTORED ENTRIES (from 4679e88)

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

## 2026-11-08 (run 25) - exit-rule variants on the LIVE setup (web idea: Connors RSI(2) literature exits)
Sources (search results only, not fetched, unverified): https://tradingmarkets.com/?p=1581420 , https://therighttrader.com/learn/trading-strategies/rsi-2-strategy , https://backtrex.com/en/backtests/connors-rsi-2-nasdaq-100 . Script lab_exit.py. Rules: LIVE entries (A+E+F, SPY>200d, stop 4 ATR, breadth>=10%, weakest-peer rank), only the exit changed. Same simulator (10% x 12, 4/day), data through 2026-10-29. 6 rows counted (5 alternatives).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref (close > prior high, hold 7) | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| exit RSI2>70, hold 7 | 584 | 65.2 | 1.52 | 44.0 | 8.1 | 1.61 | 1.60/.11/1.01/2.36/1.66/1.61 |
| exit RSI2>70, hold 10 | 573 | 68.1 | 1.57 | 47.4 | 8.0 | 1.64 | 1.83/.10/1.16/2.52/1.34/1.70 |
| exit close > MA10, hold 12 | 545 | 65.5 | 1.38 | 36.6 | 13.2 | 1.65 | 1.54/.10/1.21/1.93/1.22/1.49 |
| exit close > MA5, hold 7 | 597 | 67.5 | 1.71 | 50.8 | 7.6 | 2.08 | 2.00/.10/1.06/2.30/2.02/2.10 |
| no signal exit, time stop 7 | 561 | 52.2 | 1.30 | 32.7 | 15.3 | 1.41 | 1.25/.03/.84/1.97/1.66/1.30 |

Verdict: NOT a promotion candidate. Every alternative is worse than the live "close above prior day's high" exit on PF, return, drawdown and last 12 months. The prior-high exit takes profit quickly at the first bounce; waiting for RSI2>70 or MA crossings gives back gains (win % and drawdown worsen). Pure time stop is clearly worst (PF 1.30, DD 15%), so the signal exit carries real value. Live exit stays. Only 2024 is better under RSI2 exits, a single year. Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG in bars cache; true PEAD needs earnings data; size-up tier for entries >10% below 252d high; profit-target / trailing-stop exits.

## 2026-11-08 (run 26) - size-up tier for LIVE entries >10% below their 252d high (follow-up of run 24)
Script lab_proxsize.py. Post-hoc scaling of the 604 taken live-setup trades (breadth>=10%, weakest-peer rank, SPY>200d); 569 have 252d history, 126 are >10% below high. Data through 2026-10-29. 3 sizing variants counted, but the 10% threshold came from run 24 on the same sample (post hoc).

| Variant | Ret % | MaxDD | Sharpe | PF 21/22/23/24/25/26 |
|---|---|---|---|---|
| flat 10% (live) | 59.6 | 5.9 | 1.85 | 1.89/.13/1.42/2.19/1.92/2.68 |
| 1.5x if far | 78.6 | 7.0 | 1.92 | 2.13/.13/1.44/2.29/1.99/2.81 |
| 1.5x far, 0.75x else | 68.3 | 6.1 | 1.92 | 2.37/.13/1.45/2.37/2.05/2.90 |
| 1.3x far | 70.8 | 6.6 | 1.90 | 2.03/.13/1.43/2.25/1.97/2.76 |

Split: 2021-23 return 9.0 -> 12.2 (1.5x), Sharpe 0.80 -> 0.91; 2024-26 46.5 -> 59.2, Sharpe flat 2.78. Unlike the SPY-dip size tier (run 10), the gain shows in the early period and in every year, but it is modest in Sharpe, costs ~1pt drawdown, the threshold is post hoc, and untested for capital limits (far entries cluster in washouts). Not promoted: needs per-trade sizing in the live bot and the 3-consecutive-weekly-run rule is not met (not tracked in challenger.py).
Follow-up: if it persists, add per-trade size multiplier support to the portfolio simulator and challenger.py, and test with real capital limits.

## 2026-11-08 (run 27) - Bollinger %B and 5-day-drop-size conditioning of the LIVE setup (web idea: Connors %B strategy)
Sources (search results only, not fetched, unverified): https://www.pulse.bot/stock-trading/news/larry-connors-b-strategy-a-simple-mean-reversion-edge-explained-643c3403-0b1c-4b94-a5e5-f387424c1505/ , https://www.pulse.bot/stock-trading/news/backtested-bollinger-bands-trading-strategy-dc419590-b797-4f6c-b961-21c073e81ab4/ . Script lab_pctb.py. Rules: LIVE signals (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank); filter or rank by %B(20,2) on the signal close, or by the 5-day close decline measured in units of the 14d mean absolute daily close change. Same simulator (10% x 12, 4/day), data through 2026-10-29. 8 variants counted (discount winners).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| %B<0 | 145 | 60.7 | 1.51 | 8.3 | 2.5 | 32 / 1.50 | 2.11/0/.75/2.82/1.47/1.37 |
| %B<0.1 | 252 | 66.7 | 1.68 | 17.3 | 3.2 | 51 / 1.81 | 1.85/0/1.11/2.15/2.95/1.44 |
| %B>=0.1 | 438 | 69.9 | 1.79 | 37.2 | 5.2 | 97 / 3.60 | 1.13/.19/1.26/2.26/1.66/4.17 |
| 5d drop >=4 | 307 | 73.3 | 2.16 | 31.8 | 4.6 | 61 / 5.37 | 2.13/.30/1.15/2.65/2.03/5.12 |
| 5d drop >=6 | 53 | 73.6 | 2.29 | 4.8 | 0.8 | 7 / 2.32 | tiny samples |
| 5d drop <6 | 588 | 69.0 | 1.89 | 58.7 | 6.1 | 135 / 2.63 | same as ref |
| rank biggest 5d drop first | 607 | 68.9 | 1.83 | 56.3 | 5.9 | 138 / 2.73 | 1.64/.13/1.41/2.31/1.81/2.62 |
| rank lowest %B first | 603 | 68.2 | 1.79 | 53.2 | 6.9 | 136 / 2.56 | 1.94/.13/1.21/2.20/1.77/2.49 |

Verdict: NOT a promotion candidate. The Connors claim (deeper below the lower band is better) fails: %B<0 entries are clearly worse (PF 1.51, win 61%, 2023 PF 0.75); the more extreme the oversold reading, the weaker, consistent with run 24 where far-from-high looked better only in count-limited slices. Requiring a large 5-day drop (>=4 average moves) lifts PF to 2.16 and last-12m to 5.4 but cuts return from 59.6% to 31.8% by idling capital, 2023 falls to 1.15, and the threshold was picked after seeing the quantiles; as a ranking it does nothing (PF 1.83). Same lesson as runs 24/26: quality-filtering the signals trades return for PF, no free gain. Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG in bars cache; true PEAD needs earnings data; profit-target / trailing-stop exits.

## 2026-11-08 (run 28) - profit-target, breakeven and trailing-stop exits on the LIVE setup (own idea; open follow-up from run 25)
Script lab_target.py. LIVE signals (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank), exit "close > prior high" kept; added: profit target at entry+k*ATR (intraday high fills at target, gap-up at open), stop to breakeven after a close >= entry+1 ATR, trailing stop from highest close. Same simulator (10% x 12, 4/day), data through 2026-10-29. 6 variants counted (discount winners).

| Variant | n | Win % | PF | Ret % | MaxDD | Sharpe | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| target 1.0 ATR | 609 | 70.9 | 1.78 | 49.0 | 5.9 | 1.84 | 2.37 | 1.74/.26/1.25/2.41/1.68/2.39 |
| target 1.5 ATR | 606 | 70.0 | 1.93 | 61.9 | 5.9 | 2.07 | 2.65 | 1.88/.26/1.47/2.48/1.80/2.66 |
| target 2.5 ATR | 604 | 69.0 | 1.89 | 61.2 | 5.9 | 1.91 | 2.75 | 1.88/.13/1.47/2.17/1.95/2.75 |
| breakeven after +1 ATR close | 604 | 68.5 | 1.88 | 59.0 | 5.9 | 1.86 | 2.65 | 1.84/.13/1.42/2.25/1.92/2.68 |
| trail 2 ATR | 619 | 67.7 | 1.62 | 46.7 | 6.4 | 1.41 | 1.78 | 1.88/.14/1.27/2.23/1.35/1.88 |
| trail 3 ATR | 607 | 68.9 | 1.79 | 55.8 | 5.9 | 1.65 | 2.51 | 1.92/.12/1.38/1.97/1.84/2.63 |

Verdict: NOT a promotion candidate. Breakeven stops change nothing; trailing stops and a tight 1 ATR target cut winners and are worse. Target 1.5 ATR is +0.05 PF / +2 pts return and better than live in only 3 of 5 non-2022 years (2025 worse, 2021/2026 flat): within noise of 6 comparisons, not worth live complexity. The prior-high exit already captures the bounce. Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG cross-asset filter (not in bars cache?); true PEAD needs earnings data.

## 2026-11-08 (run 29) - breadth-washout SIZE tier on the LIVE setup (own idea; follow-up listed in runs 13/26)
Source: none (own idea; web run 28-style searches already covered breadth). Script lab_breadthsize.py. Post-hoc scaling of the 604 taken LIVE trades (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank); the position weight is 10% x multiplier by the share of the universe with RSI2<10 on the signal day (quartiles of taken trades: 14% / 21% / 30%). Data through 2026-10-29. 5 variants counted (discount winners; scaling is not re-run through the slot simulator, so exposure caps are ignored).

| Variant | Ret % | MaxDD | Sharpe | PF 21/22/23/24/25/26 |
|---|---|---|---|---|
| flat (LIVE ref) | 59.6 | 5.9 | 1.85 | 1.89/.13/1.42/2.19/1.92/2.68 |
| 1.5x if breadth>=20% | 80.5 | 7.7 | 1.87 | 2.24/.10/1.43/2.03/2.06/2.71 |
| 1.5x if breadth>=30% | 73.5 | 6.5 | 1.95 | 2.26/.10/1.55/2.23/1.93/2.65 |
| 1.5x >=20%, 0.75x <15% | 75.2 | 7.2 | 1.87 | 2.35/.09/1.47/1.97/2.11/2.66 |
| 0.5x if breadth 10-15% | 50.3 | 5.1 | 1.88 | 2.06/.12/1.52/2.03/2.05/2.55 |
Split: 2021-23 Sharpe 0.80 -> 0.85-0.99, 2024-26 2.78 -> 2.90-2.96; 2022 gets worse (-3.3% -> -5.0%, 11 of its 14 trades are high-breadth).

Verdict: NOT a promotion candidate. The return gain (+14 to +21 pts) comes with a proportional rise in drawdown (5.9 -> 6.5-7.7); Sharpe is flat (1.85 -> 1.87-1.95), i.e. this is leverage, not edge. High-breadth trades are only slightly better than low-breadth ones (PF per year mixed: 2024 worse, 2022 worse). Same lesson as runs 10 and 26: sizing tiers on signal quality do not add risk-adjusted value. Not added to challenger.py. If Ori simply wants more return, raising base size is the equivalent lever.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG (not in bars cache); true PEAD needs earnings data.

## 2026-11-08 (run 30) - residual (SPY-beta-adjusted) 5-day reversal conditioning of the LIVE setup (web idea: Blitz/Huij/Lansdorp/Verbeek "short-term residual reversal")
Sources (search results only, not fetched, unverified): https://www.robeco.com/en-za/insights/2011/11/short-term-residual-reversal , https://econpapers.repec.org/RePEc:eee:finmar:v:16:y:2013:i:3:p:477-504 . Script lab_resid.py. Rules: LIVE signals (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank); residual = 5d stock return minus beta*5d SPY return, beta from 60d daily returns; filter by quartile/median of the residual (quantiles from all 1437 pre-slot signals) or re-rank by it. Same simulator (10% x 12, 4/day), data through 2026-10-29. 6 variants counted (discount winners).

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| resid below median | 350 | 70.3 | 1.92 | 35.6 | 5.7 | 97 / 2.64 | 1.69/.13/1.53/2.38/1.50/2.67 |
| resid above median | 343 | 66.5 | 1.51 | 17.1 | 5.3 | 51 / 2.77 | .85/.11/1.01/2.69/2.85/2.35 |
| bottom quartile | 192 | 75.0 | 2.60 | 30.0 | 2.2 | 67 / 2.82 | 5.18/.25/1.85/2.54/2.08/2.93 |
| top quartile | 181 | 66.3 | 2.17 | 16.8 | 2.1 | 25 / 3.40 | 1.96/.25/1.59/2.97/2.87/2.48 |
| rank most-negative resid first | 604 | 68.4 | 1.80 | 54.2 | 5.9 | 137 / 2.72 | 1.73/.15/1.27/2.00/1.98/2.59 |
| rank least-negative resid first | 607 | 67.9 | 1.79 | 53.9 | 6.5 | 136 / 2.61 | 1.77/.13/1.24/2.50/1.45/2.73 |

Verdict: NOT a promotion candidate. The residual-reversal claim is not confirmed as an add-on: both extreme quartiles beat the middle (non-monotonic, i.e. noise), the bottom quartile's PF 2.6 is driven by 2021 (5.18) and halves return (30% vs 59.6%) by idling capital, and ranking by residual in either direction is worse than the live weakest-peer ranking (PF 1.80 / 1.79 vs 1.88). Same lesson as runs 24/26/27: quality-filtering trades return for PF; the live ranking already captures the relative-weakness effect. Not added to challenger.py.
Follow-ups still untested: sleeve sizing at 5%; TLT/HYG (not in bars cache); true PEAD needs earnings data.

## 2026-11-08 (run 31) - risk-matched SIZE of the bear-regime sleeve on the LIVE setup (own idea; follow-up listed in runs 13/25-30)
Source: none. Script lab_sleeve5.py. LIVE setup (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank) plus the run-11/13 bear sleeve (SPY<200d, stock>own 200d, RSI2<5, breadth>=10%, prior-high exit), sleeve pnl scaled by weight w post-hoc (slots still one per trade; PF is computed on the scaled pnl so it is approximate). Same simulator (10% x 12, 4/day), data through 2026-10-29. 3 weights tried (sleeve rules and breadth threshold reused from run 13, nothing new tuned).

| Variant | n | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| + sleeve w=1.0 (10%) | 813 | 69.1 | 1.80 | 82.5 | 6.8 | 1.96 | 152 / 2.91 | 1.89/1.11/1.50/2.19/1.92/3.01 |
| + sleeve w=0.75 | 813 | 69.1 | 1.81 | 76.5 | 5.9 | 1.97 | 152 / 2.85 | 1.89/1.05/1.48/2.19/1.92/2.93 |
| + sleeve w=0.5 (5%) | 813 | 69.1 | 1.83 | 70.7 | 5.9 | 1.91 | 152 / 2.79 | 1.89/.96/1.46/2.19/1.92/2.85 |
| split 2021-23: LIVE -> +sleeve .5 | 221 -> 399 | 64.7 -> 66.7 | 1.38 -> 1.38 | 9.0 -> 13.3 | 5.9 -> 5.9 | 0.80 -> 0.93 | - | 2022 .13 -> .96 |
| split 2024-26: LIVE -> +sleeve .5 | 383 -> 414 | 71.5 | 2.25 -> 2.29 | 46.5 -> 50.7 | 5.2 -> 5.2 | 2.78 -> 3.06 | 152 / 2.79 | same |

Verdict: WATCH-LIST, supports run 13's PROMOTION CANDIDATE with a risk-matched size. At w=0.5-0.75 the sleeve adds +11 to +17 pts return and Sharpe 1.85 -> 1.91-1.97 with max drawdown unchanged at 5.9 (w=1.0 raises it to 6.8), lifts L12 PF 2.65 -> 2.79-2.85, never hurts 2021/2024/2025, and the gain shows in both the early selection period and the confirmation period. It does not beat live on PF (1.81-1.83 vs 1.88) and the 2022 rescue shrinks as w falls (PF 1.11 -> .96), so it is a diversifier, not an edge upgrade. Caveats unchanged from run 11/13: survivor universe flatters "above 200d in a bear market", only ~2 bear episodes, sleeve n small in the last year (21 trades). A live implementation would need the SPY<200d branch in mr.py (not done here; belongs to the daily improvement round). Not added as a new challenger row (run-13 row already tracks it).
Follow-ups still untested: TLT/HYG (not in bars cache); true PEAD needs earnings data; scale-in second tranche.

## 2026-11-08 (run 32) - market-state timing of the LIVE setup: SPY direction on the signal day and breadth deepening vs easing (own idea; search-only web seed: Connors/Quantified Strategies pullback pages, snippets not fetched, unverified: https://quantifiedstrategies.substack.com/p/rsi-pullback-strategy)
Script lab_turn.py. LIVE signals (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank), filtered by SPY 1-day / 3-day return on the signal day or by the day-over-day change in the RSI2<10 breadth share. Same simulator (10% x 12, 4/day), data through 2026-10-29. 6 variants counted (discount winners).

| Variant | n | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| SPY up on signal day | 200 | 69.5 | 1.74 | 13.1 | 3.0 | 1.07 | 45 / 3.97 | 1.34/.0/.98/1.71/1.23/4.52 |
| SPY down on signal day | 460 | 67.8 | 1.78 | 40.6 | 5.3 | 1.46 | 99 / 2.27 | 1.95/.14/1.51/2.2/1.87/2.11 |
| breadth easing (today<yesterday) | 165 | 68.5 | 1.44 | 7.9 | 3.4 | 0.72 | 41 / 2.56 | .72/1.47/1.2/1.25/1.63/3.41 |
| breadth deepening (today>=yesterday) | 503 | 69.0 | 1.96 | 51.5 | 4.6 | 1.72 | 107 / 2.56 | 1.99/.04/1.36/3.07/2.03/2.37 |
| SPY 3d return < -2% | 97 | 71.1 | 2.37 | 11.6 | 2.8 | 1.36 | 8 / 8.53 | 16.0/.06/.63/3.85/1.67/- |
| SPY 3d return >= -2% | 531 | 68.2 | 1.73 | 42.1 | 5.5 | 1.54 | 128 / 2.49 | 1.59/.16/1.4/1.98/1.68/2.4 |

Verdict: NOT a promotion candidate. Every filter lowers return and Sharpe versus live because it just idles capital (the live setup is already the best-selected subset). Breadth deepening has PF 1.96 vs 1.88 but 51.5% return vs 59.6% and is worse in 2023/2026; its complement (easing) is weak (PF 1.44), but this is consistent with simply "more washout = better" already captured by the breadth>=10% filter (run 12). SPY 3d < -2% looks great (PF 2.37) but is 97 trades with 2021 PF 16 and 2023 PF 0.63, i.e. a hand-full of episodes. SPY direction on the signal day carries no usable signal. Not added to challenger.py.
Follow-ups still untested: TLT/HYG (not in bars cache); true PEAD needs earnings data; scale-in second tranche.

## 2026-11-09 (run 33) - volatility-expansion conditioning of the LIVE setup: 5d/50d range ratio and signal-day range vs ATR (own idea; one web search for "ATR ratio filter on RSI2 mean reversion" returned only TradingView script pages, nothing fetched or usable)
Script lab_volx.py. LIVE signals (A+E+F, SPY>200d, hold 7, stop 4 ATR, breadth>=10%, weakest-peer rank) filtered by (a) mean high-low range of the last 5 days divided by the 50-day mean range, (b) signal-day range in ATRs. Same simulator (10% x 12, 4/day), data through 2026-10-29. 8 rows counted (discount winners).

| Variant | n | Win % | PF | Ret % | MaxDD | Sharpe | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 / 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| 5d/50d range >= 1.2 | 154 | 68.2 | 2.24 | 18.6 | 4.3 | 1.64 | 42 / 3.23 | 7.32/.99/1.19/2.31/1.21/4.27 |
| 5d/50d range < 1.2 | 503 | 69.2 | 1.79 | 40.6 | 4.6 | 1.71 | 104 / 2.68 | 1.46/.05/1.47/2.05/2.60/2.47 |
| 5d/50d range >= 1.0 | 341 | 69.8 | 2.17 | 41.0 | 4.8 | 1.82 | 77 / 3.63 | 4.21/.22/.95/2.49/1.80/4.03 |
| 5d/50d range < 1.0 (contraction) | 346 | 67.3 | 1.45 | 15.7 | 5.2 | 0.91 | 72 / 2.18 | .73/.06/1.61/2.00/2.15/2.03 |
| signal-day range >= 1.5 ATR | 128 | 64.1 | 1.96 | 13.4 | 2.2 | 1.21 | 21 / 5.77 | 1.42/0/2.93/2.69/1.55/6.04 |
| signal-day range < 1.5 ATR | 538 | 69.7 | 1.76 | 43.8 | 6.0 | 1.58 | 125 / 2.49 | 1.67/.21/1.43/1.92/1.71/2.56 |
| signal-day range < 1.0 ATR | 344 | 70.3 | 1.84 | 25.7 | 2.9 | 1.79 | 82 / 2.72 | 1.86/.05/1.66/1.71/1.54/3.27 |

Verdict: NOT a promotion candidate. Entries after volatility expansion (5d range >= 1.0x the 50d range) have a higher PF (2.17 vs 1.88) and contraction entries are clearly worse (PF 1.45, 2021 0.73), which fits the capitulation story seen in runs 5/6/12. But the filter cuts return 59.6 -> 41.0%, Sharpe is flat (1.82 vs 1.85), and 2023 PF falls to 0.95, so it fails the beat-on-return and year tests; the stricter >=1.2 cut has a 2021 PF of 7.3 on a handful of trades. Signal-day range gives nothing usable. Like runs 29-32, it idles capital without adding edge. Not added to challenger.py.
Follow-ups still untested: TLT/HYG filters (not in bars cache); true PEAD needs earnings data; scale-in second tranche.

## 2026-11-17 (run 38) - own-history oversold percentile (QPI-like) and SPY realized-vol regime as conditioners / size tilt of the vol60>=1.75% LIVE setup (web-seeded). Script: lab_qpi.py
Source: https://hn.jakechampion.name/reader/https://www.quantitativo.com/p/long-and-short-mean-reversion-machine (mirror of Quantitativo "Long & Short Mean Reversion"; fetched; trigger = 3-day QPI < 15, 20 slots, -5% stop, 6-bar exit, long sized down when VIX > 1.15 x its SMA15; the model-probability part is not reproducible and its claims are unverified). Translation: (a) percentile of the stock's own k-day return (k=3,5) within its prior 252 days, keep <= 5/10/15th pct; (b) VIX proxy = SPY 10d realized vol > 1.15 x its 15d SMA (keep calm days, or keep only stressed days). Applied to LIVE trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day). 8 filter variants + 2 size tilts = 10 tried (discount lucky winners).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| own 3d pct <= 10 | 172 | 74.4 | 3.52 | 40.5 | 2.0 | 66 / 4.12 | 4.9/.12/1.07/7.42/1.95/4.64 |
| own 5d pct <= 10 | 162 | 79.6 | 4.14 | 40.3 | 2.2 | 74 / 4.38 | 45/none/1.29/13.1/2.14/5.47 |
| own 5d pct <= 5 | 87 | 81.6 | 4.18 | 22.8 | 3.3 | 42 / 6.90 | 38/none/1.48/none/1.70/6.98 |
| own 5d pct <= 15 | 209 | 76.1 | 3.49 | 45.0 | 2.2 | 83 / 4.07 | 4.55/.12/1.34/7.24/2.17/4.84 |
| SPY rvol calm (not > 1.15x SMA15) | 231 | 73.6 | 2.29 | 29.9 | 3.3 | 78 / 3.22 | 1.14/.87/1.55/3.93/2.15/3.02 |
| SPY rvol stressed only | 91 | 73.6 | 3.94 | 25.0 | 2.7 | 26 / 3.64 | 127/none/1.66/7.12/1.86/4.86 |
| TILT 1.25x/0.75x if own 5d pct <= 10 | 308 | 74.4 | 3.22 | 68.5 | 3.9 | 100 / 3.78 | 2.99/.95/1.67/5.68/2.38/4.17 |
| TILT 1.25x/0.75x if own 3d pct <= 10 | 308 | 74.4 | 3.07 | 68.9 | 4.0 | 100 / 3.59 | 2.74/.57/1.60/5.35/2.35/3.76 |

Findings: a deeper-than-usual drop relative to the stock's OWN 5-day history raises PF (4.1 vs 2.9, win 80%) and L12 PF, but as a hard filter it halves the trade count and return (40% vs 62%) and 2023 is worse (1.29 vs 1.72), so it is not a replacement. As a size tilt it lifts PF to 3.22, return to 68.5, drawdown 3.9, but is below LIVE in 2023 and 2025 (1.67 vs 1.72, 2.38 vs 2.51) and is not better than the already-logged tilts (run52 PF 3.14, run30 3.25, run31 stacked 3.63). It is likely another proxy for dip depth, which the dispersion/SPY-dip tilts already capture. Stressed-SPY-vol days have PF 3.94 vs 2.29 on calm days (same direction as run 24/19 SPY-dip findings: trade more after market stress; the source's "size down in stress" is NOT supported here, the opposite holds on this setup). 2021 values of 38-127 come from 1-3 losers only and are noise.
Verdict: NOT a promotion candidate (no new variant added to challenger.py). Possible later check: include the own-history 5d percentile in the stacked tilt only if a future run shows it adds beyond run31 (untested; would be a 3rd tilt on ~300 trades, high overfit risk).

## 2026-11-17 (run 39) - PLACEBO / null-model audit of the LIVE setup (own idea; no web source). Script: lab_placebo.py
Question: does the RSI(2) pullback trigger add anything beyond "buy any uptrend stock (close>SMA50>SMA200) with vol60>=1.75% on a breadth>=10% day with SPY>200d", using the same exit (prior-high, hold 7, stop 4 ATR), same simulator (10% x 12, 4/day), data through 2026-10-29? Placebo candidates replace the RSI2 triggers (and skip the A/E/F extras atrpct4/price15/nocrash); random score (3 seeds) or peer-rank. 5 placebo conditions x 4 orderings = 20 rows counted.

| Variant | n | Win % | PF | Ret % | MaxDD | L12 n / PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE (signals, peer rank) | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| any uptrend stock, random (3 seeds) | ~1165 | ~66 | 1.09-1.17 | 15-30 | 11-16 | 357-362 / 1.04-1.39 | mixed, 2022 .48-.85 |
| any uptrend stock, peer-rank | 1168 | 63.5 | 0.96 | -7.6 | 20.6 | 362 / 0.98 | 2022 .35 |
| down close today, random (3 seeds) | ~1250 | ~63 | 1.05-1.24 | 8-51 | 13-20 | ~390 / 1.0-1.22 | 2022 ~.45 |
| 5d return < 0, random (3 seeds) | ~1130 | ~65 | 1.21-1.27 | 37-50 | 17-18 | ~350 / 1.45-1.64 | 2022 ~.34 |
| 5d return < -3%, random (3 seeds) | ~705 | ~66 | 1.17-1.22 | 20-27 | 17-19 | ~232 / 1.37-1.49 | 2022 ~.14 |
| IBS<0.25 only (no RSI2), random (3 seeds) | ~1065 | ~64 | 1.25-1.37 | 45-67 | 11-12 | ~349 / 1.40-1.69 | 2022 ~.59 |

Verdict: NOT a new challenger; a CONFIRMATION of the live edge. Regime + volatility + washout filters alone give PF 1.0-1.4 with 11-20% drawdowns, versus PF 2.83 and 4.3% drawdown for the live signals. So the live result is not just "high-vol stocks bounce when the market washes out": the multi-condition RSI2 pullback selection (RSI2<5/10, IBS, extension, extras) carries most of the edge. Even IBS<0.25 alone, the closest placebo, reaches only PF 1.25-1.37. Caveats: placebo skips the A/E/F extras, and its higher trade count is fully drawn from the same slot budget; RSI2 is correlated with "5d return < 0" so this is not a pure independence test. Peer-rank beats random ordering only for the signal set (peer-rank on placebos is not better), which fits earlier runs where it helped modestly. No code change to challenger.py.
Follow-ups still untested: TLT/HYG (not in bars cache); true PEAD needs earnings data; scale-in second tranche.

## 2026-11-18 (run 40) - cross-asset "correlated stress" conditioners of the vol60>=1.75% LIVE setup (web-seeded). Script: lab_stress.py
Source: https://quantpedia.com/short-term-correlated-stress-reversal-trading/ (fetched; rule = same-day simultaneous decline in two risk-on assets, or risk-asset down + safe-haven up, enter at close, hold 1 day; results are images so no numbers read; threshold choice and in/out-of-sample status unstated; GLD/IEF/USO are NOT in the bars cache). Translation: use cached SPY/QQQ/IWM/XLU/XLP/VIXY same-day returns at the signal close as a filter on LIVE trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day; data through 2026-10-29). 8 variants tried (discount winners).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 2.32 | 100 / 3.39 | 2.41/.87/1.72/4.7/2.51/3.44 |
| SPY dn & XLU up | 102 | 77.5 | 4.04 | 23.8 | 2.4 | 1.80 | 29 / 14.1 | 5.19/-/1.23/8.51/2.35/30.9 |
| SPY dn & XLP up | 107 | 77.6 | 3.98 | 26.5 | 1.9 | 2.18 | 49 / 5.16 | 19.8/.26/1.40/8.52/2.66/6.02 |
| SPY dn & VIXY up | 207 | 78.3 | 4.12 | 53.4 | 2.3 | 2.82 | 72 / 4.11 | 10.6/-/2.66/5.5/2.86/4.28 |
| SPY, QQQ, IWM all dn | 196 | 76.0 | 3.53 | 42.8 | 4.2 | 2.34 | 59 / 4.34 | 7.84/.26/1.64/5.92/3.17/3.95 |
| NOT (SPY dn & XLU up) | 235 | 72.8 | 2.32 | 34.3 | 3.7 | 1.95 | 80 / 2.47 | 1.79/.75/1.87/4.37/1.96/2.11 |
| SPY dn & XLU dn | 160 | 74.4 | 2.60 | 25.5 | 2.4 | 1.83 | 53 / 1.94 | 125/1.63/2.63/3.65/2.46/1.16 |
| SPY dn & XLU, XLP dn | 118 | 75.4 | 2.73 | 16.6 | 2.4 | 1.62 | 28 / 1.72 | 127/-/2.46/2.48/5.40/1.06 |
| SPY up (control) | 92 | 67.4 | 1.69 | 7.6 | 3.0 | 0.84 | 31 / 4.04 | .55/0/.58/3.61/.57/4.83 |

Findings: the useful split is simply SPY down vs up on the signal day (SPY-up signals PF 1.69, SPY-down PF ~3.6+); "VIXY up" is nearly the same set as SPY down (207 of ~216 trades). Defensive-rotation variants (XLU/XLP up) have higher PF but 2022 is 0.26 or empty and 2023 1.2-1.4, with L12 PF 14 coming from 29 trades; they idle capital (return 24-27% vs 62%). "SPY dn & VIXY up" is the only one with higher PF (4.12), Sharpe (2.82), L12 PF (4.11) and lower drawdown (2.3), but return falls 61.7 -> 53.4 and 2022 has no trades, so it fails the beat-on-return test; it is essentially the SPY-down/IBS tilts of runs 19/20/30 (run30 tilt: PF 3.25, ret 67.5, keeps all trades), i.e. no new information. Cross-asset concordance adds nothing beyond SPY's own sign.
Verdict: NOT a promotion candidate; not added to challenger.py. Confirms run30 direction (market-down signal days are the better ones under the vol filter; a size tilt beats a hard filter). Follow-ups still untested: TLT/IEF/GLD/HYG (not in bars cache), true PEAD (no earnings data), scale-in second tranche, ticker-subset jackknife of the universe (next own-idea run).

## 2026-11-19 (run 41) - ticker / sector JACKKNIFE of the vol60>=1.75% LIVE setup (own idea; no web source this run, run 40 was web). Script: lab_jackknife.py
Question: is the live edge spread across the universe or carried by a few symbols / one sector? Trades = LIVE (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day; data through 2026-10-29), re-run through the same portfolio simulator after removing symbols. Diagnostic only: 13 sector drops + 3 top-k drops + 30 random draws (distribution, not a search for a winner).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| drop SMH (semis, 166 trades) | 233 | 71.7 | 2.16 | 29.4 | 3.1 | 79 / 2.55 | 1.56/0/1.42/3.52/1.68/2.64 |
| drop XLK (132 trades) | 246 | 73.6 | 2.59 | 38.9 | 3.6 | 84 / 3.14 | 1.85/1.89/1.47/3.66/4.58/2.54 |
| drop XLF | 280 | 75.7 | 3.15 | 59.3 | 3.6 | 98 / 3.31 | 3.66/.87/1.72/6.8/2.54/3.33 |
| drop XLY | 273 | 74.4 | 3.02 | 57.4 | 3.1 | 88 / 3.68 | 2.13/.87/1.89/5.0/2.73/3.7 |
| drop XLC | 288 | 74.3 | 2.77 | 55.3 | 4.3 | 94 / 3.32 | 2.37/.87/1.39/4.66/2.4/3.47 |
| other 8 sector drops (ITA, XBI, XLB, XLE, XLI, XLP, XLRE, XLV) | 294-306 | 73.9-75.0 | 2.78-3.03 | 57.2-61.3 | 3.9-4.6 | 90-100 / 3.08-4.17 | all years within ~0.3 of ref except 2022 (XLV drop: 1.60) |
| drop top-3 P&L symbols (NVDA, CRWD, KLAC; post-hoc, biased) | 286 | 72.0 | 2.23 | 39.2 | 4.7 | 96 / 2.96 | 1.8/.87/1.36/3.61/1.84/2.94 |
| drop top-5 | 275 | 70.9 | 2.04 | 31.4 | 3.9 | 93 / 2.60 | 1.8/.87/1.48/2.89/1.45/2.8 |
| drop top-10 | 249 | 69.9 | 1.72 | 19.9 | 3.9 | 88 / 2.40 | 1.3/.12/.95/2.84/1.34/2.37 |
| random 20% of symbols dropped, 30 draws | - | - | PF min 2.25 / p10 2.47 / median 2.81 / p90 3.08 | ret min 35 / median 49 / max 60 | 2.4-4.8 | - | - |

Findings: (1) The edge is real across the board but CONCENTRATED. 91 of 126 symbols traded; the semis/tech block (SMH 166 + XLK 132 sector labels, overlapping coverage of the high-vol60 names) supplies ~half of the trades and ~half of the return: without SMH return halves (60.6 -> 29.4%) and PF falls to 2.16, still >2 and positive in 5 of 6 years (2022 has no SMH trades). NVDA alone is 12% of P&L, top-10 symbols ~60%. (2) Dropping any other single sector leaves PF 2.8-3.15; financials/consumer-discretionary drops even raise PF. (3) Random 20% symbol removal keeps PF 2.25-3.33 (median 2.81 = ref) and return 35-60% (median 49%), so no single lucky ticker explains the result, but the live return figure is at the optimistic end of its jackknife distribution (ref 60.6 vs median 49), a useful haircut for expectations. (4) Dropping the 10 best symbols post-hoc (a deliberately harsh, biased test) still gives PF 1.72, above every non-vol60 variant in challengers.md.
Implication for the live bot: the vol60>=1.75% filter effectively means "trade high-beta semis/tech/growth"; correlated-sector exposure (run 8/10 sector caps were tested earlier, see lab_seccap) is the main risk, not the signal itself. Realistic expectation: PF ~2.2-2.8, return ~35-50% per backtest span, not 60%.
Verdict: robustness CONFIRMATION, not a promotion candidate; nothing added to challenger.py. Follow-ups still untested: TLT/HYG filters (not in bars cache), true PEAD (no earnings history), a semis-exposure cap (max N concurrent SMH names) re-tested under the vol60 base if lab_seccap predates it.

## 2026-11-19 (run 42) - open-position correlation (diversification) filter on the vol60>=1.75% LIVE setup (own idea, web-seeded by search hits only: https://quantpedia.com/testing-an-ai-assisted-research-workflow-for-multi-asset-pullback-strategy-discovery/ , not fetched, unverified). Script: lab_opencorr.py
Question: run 41 showed the edge is concentrated in correlated high-beta semis/tech. Does skipping a same-day signal that is highly correlated (60d daily-return corr) with the currently open positions improve risk-adjusted results? (Sector cap 2 was already tested in run 23.) Rules: LIVE trades, same 10% x 12, 4/day, sector cap 2, weakest-peer rank; a candidate is skipped if mean (or max) 60d correlation with open positions exceeds a threshold. The no-filter reference reproduces the live numbers exactly. 4 variants tried (no selection; all reported).

| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| skip if mean corr > 0.6 | 294 | 73.8 | 2.72 | 54.4 | 4.3 | 2.17 | 99 / 3.35 | 2.16/.87/1.41/4.86/2.36/3.39 |
| skip if mean corr > 0.5 | 277 | 72.6 | 2.47 | 45.6 | 3.7 | 1.94 | 97 / 3.24 | 1.83/.87/1.43/4.29/1.9/3.31 |
| skip if max corr > 0.8 | 297 | 74.1 | 2.76 | 56.6 | 4.3 | 2.22 | 96 / 3.16 | 2.41/.87/1.62/4.93/2.34/3.19 |
| skip if max corr > 0.7 | 286 | 73.1 | 2.62 | 50.3 | 4.3 | 2.13 | 94 / 3.13 | 2.15/.87/1.34/4.82/2.29/3.15 |

Findings: every threshold lowers PF, return, Sharpe and last-12m PF; max drawdown does not improve except at the harshest mean-corr cut (4.3 -> 3.7%, bought with -15 points of return). Trades skipped for being correlated were as good as the ones kept: the clustered high-beta signals are where the edge is, and diversification-by-correlation just removes edge. Consistent with run 23 (sector caps) and run 23-hedge (market-neutralising lowers PF).
Verdict: NOT a promotion candidate; nothing added to challenger.py. Closes the "concentration risk" thread (sector cap, SPY hedge, correlation filter all fail). Remaining untested: TLT/HYG filters (not in cache), true PEAD (no earnings history).

## 2026-11-20 (run 43) - 3-bar linear-regression-slope "hook" reversal sleeve (web idea). Script: lab_linreg.py
Source: https://algomatictrading.substack.com/p/strategy-4-a-mean-reversion-strategy (fetched; index futures, 2000-2025, claims ~69% win rate, no profit factor; exit variants shown only as images). Also read the intro of https://delphicalpha.substack.com/p/us-equity-cross-sectional-mean-reversion (cross-sectional N-bar loser/winner long-short; results paywalled, unusable). Scale-in second tranche was already tested earlier (lab_scalein.py), so removed from the follow-up list.
Rules (daily stock bars, cached universe): slope = (typical price[i] - typical price[i-2])/2 with typical = (H+L+C)/3; signal when slope[i] > slope[i-1] and slope[i-1] < slope[i-2], red candle (close<open), close > SMA200, SPY>200d gate, ATR/close <= 6%, 3-day cooldown. Entry at close, stop 4 ATR, hold 7, exit close>SMA5 or close>prior high. Same portfolio simulator (10% x 12, 4/day; data through 2026-10-29). 5 variants (+4 combo rows) tried.

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| hook, SMA5 exit | 2811 | 64.0 | 1.02 | 4.6 | 17.7 | 627 / 1.07 | .89/.37/1.27/1.11/.98/1.10 |
| hook, prior-high exit | 2634 | 64.5 | 1.08 | 24.6 | 18.2 | 587 / 1.18 | 1.01/.38/1.20/1.13/1.09/1.19 |
| hook + vol60>=1.75, SMA5 exit | 1665 | 65.5 | 1.20 | 42.5 | 12.2 | 464 / 1.13 | 1.57/.41/1.34/1.43/1.02/1.19 |
| hook + vol60>=1.75, prior-high exit | 1589 | 67.0 | 1.24 | 65.3 | 13.6 | 446 / 1.20 | 1.41/.44/1.26/1.52/1.16/1.24 |
| hook, no trend, vol60>=1.75, prior-high | 2086 | 65.2 | 1.16 | 55.1 | 14.7 | 569 / 1.04 | 1.27/.44/1.43/1.14/1.26/1.07 |
| LIVE + hook vol60 prior-high | 1662 | 67.5 | 1.29 | 87.6 | 13.4 | 464 / 1.29 | 1.56/.45/1.24/1.56/1.14/1.34 |
| LIVE + hook vol60 prior-high, breadth>=10% | 959 | 70.3 | 1.61 | 95.1 | 8.0 | 301 / 1.42 | 3.56/.55/1.41/2.15/1.37/1.42 |

Findings: the slope hook is essentially a "second day of a bounce" tick with no oversold requirement; on stocks it gives PF 1.02-1.24 with 12-18% drawdowns, near the placebo level of run 39. The 69% win rate in the source does not survive on stocks (64-67%, PF barely >1), consistent with the expectation that web backtests are optimistic. Combined with LIVE it adds return only by filling slots with lower-quality trades, which cuts PF to 1.3-1.6 and drawdown to 8-13% versus 4.3%; the sleeve crowds out live signals. 2022 is below 1 everywhere. Nothing in the hook beats the live RSI2/IBS pullback selection.
Verdict: NOT a promotion candidate; nothing added to challenger.py. Open follow-ups: TLT/HYG filters (not in cache), true PEAD (no earnings history), semis-exposure cap under vol60 base.

## 2026-11-20 (run 44) - nominal share-price level and distance above the 252d low as conditioners of the vol60>=1.75% LIVE setup (own idea; no web source this run, run 43 was web). Script: lab_price.py
Rules: LIVE trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day; data through 2026-10-29), keep a signal only if the signal-day close satisfies the filter. Price quartiles of live trades: 72 / 135 / 250 USD. 8 variants tried (all reported; multiple-comparison discount applies).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| price >= 20 | 302 | 74.2 | 2.85 | 59.2 | 3.6 | 98 / 3.31 | 2.2/.87/1.78/4.74/2.51/3.34 |
| price >= 50 | 276 | 75.4 | 3.04 | 55.6 | 3.1 | 96 / 3.46 | 3.14/.87/1.74/4.62/2.64/3.39 |
| price >= 100 | 212 | 72.6 | 2.69 | 35.3 | 3.0 | 85 / 3.63 | 1.96/1.63/2.22/3.01/2.21/3.67 |
| price < 150 | 173 | 72.3 | 2.19 | 23.6 | 4.1 | 32 / 3.28 | 2.3/.22/1.11/4.15/1.53/2.86 |
| price < 300 | 263 | 74.1 | 2.71 | 49.7 | 4.1 | 73 / 2.85 | 2.29/.87/1.58/5.53/2.13/2.94 |
| 52w-low dist >= 50% | 206 | 74.3 | 3.22 | 46.8 | 4.0 | 65 / 4.73 | 2.95/0/1.46/5.8/2.42/5.66 |
| 52w-low dist >= 100% | 92 | 73.9 | 2.91 | 23.7 | 2.4 | 36 / 4.31 | 2.96/-/1.4/6.79/1.66/5.09 |
| 52w-low dist < 100% | 217 | 73.3 | 2.59 | 28.0 | 3.1 | 69 / 2.83 | 4.67/.87/1.4/3.71/2.32/2.86 |

Findings: no price tier lifts return; every filter shrinks the trade count and return (60.6 -> 55.6 best case) for at most a modest PF gain. Price >= 50 (PF 3.04, DD 3.1) mostly removes cheap-stock noise but its gain is a 2021 artifact (3.14 vs 2.41) and 2024 is slightly worse. "Far above the 52w low >= 50%" lifts PF (3.22) and L12 PF (4.73) but 2022 has zero PF (all trades lost) and return falls to 46.8; the >=100% bucket is the same effect with 92 trades. Stocks that have run far from their lows pull back better recently, but this is the same high-beta/semis concentration shown in run 41, not new information. Nothing passes the beat-on-return, last-12m and all-but-one-non-2022-year test.
Verdict: NOT a promotion candidate; nothing added to challenger.py. Remaining untested: TLT/HYG filters (not in cache), true PEAD (no earnings history), semis-exposure cap under vol60 base.

## 2026-11-20 (run 45) - depth of the regression-residual z inside the live zreg20<-1.5 setup, and a size tilt on it (own idea). Script: lab_zdepth.py
Rules: LIVE trades incl. zreg20<-1.5 (238 trades, data through 2026-10-29); bucket by z depth and test size x1.25/x1.5 when z<-2 (optionally x0.75 otherwise). 6 variants tried (multiple-comparison discount).
| Variant | Trades | Win % | PF | Ret % | Max DD % |
|---|---|---|---|---|---|
| LIVE | 238 | 78.6 | 4.41 | 63.6 | 2.5 |
| z in [-2.0,-1.5) | 125 | 79.2 | 3.97 | 26.3 | 2.0 |
| z in [-2.5,-2.0) | 95 | 74.7 | 3.33 | 18.6 | 1.7 |
| z < -2.5 | 56 | 75.0 | 3.24 | 10.4 | 2.5 |
| x1.25 if z<-2 | 238 | 78.6 | 4.38 | 74.5 | 2.8 |
| x1.5 if z<-2 | 238 | 78.6 | 4.36 | 86.1 | 3.2 |
| x1.25 if z<-2 else x0.75 | 238 | 78.6 | 4.35 | 64.7 | 2.6 |
Findings: deeper z is NOT better; PF and win rate fall with depth (3.97 -> 3.33 -> 3.24), so the filter is a threshold effect, not a dose-response. Tilting toward deeper z leaves PF flat/slightly lower; extra return is just extra exposure. Early (2021-23) and late (2024-26) halves agree (z<-2 PF 2.74 / 4.05 vs ref 2.99 / 5.25).
Verdict: NOT a promotion candidate; nothing added to challenger.py.

## 2026-11-20 (run 46) - CCI(14), Williams %R(14) and Keltner-depth conditioners of the vol60>=1.75% LIVE setup (web-seeded; sources https://www.quantifiedstrategies.com/williams-r-trading-strategy/ , https://quantifiedstrategies.substack.com/p/we-tested-williams-r-on-all-nasdaq - search snippets only, claims unverified). Script: lab_cci.py
Rules: LIVE trades (data through 2026-10-29); keep a signal only if the signal-day indicator passes. 9 variants tried (multiple-comparison discount applies). Quartiles: CCI -174/-132/-77, WR -96/-90/-74, Keltner depth (SMA20-close)/ATR20 0.54/1.28/1.79.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| CCI14 < -100 | 209 | 75.1 | 3.39 | 41.4 | 2.5 | 63 / 2.67 | 12.1/-/2.32/5.4/3.22/2.1 |
| CCI14 < -150 | 138 | 76.1 | 3.83 | 28.4 | 1.3 | 39 / 2.79 | 9.13/-/3.2/8.19/3.45/2.22 |
| CCI14 >= -100 | 129 | 71.3 | 2.14 | 16.9 | 3.1 | 43 / 6.2 | .95/0/.99/2.82/1.32/15.35 |
| WR14 < -90 | 151 | 75.5 | 3.15 | 31.0 | 2.1 | 51 / 3.39 | 4.36/-/3.14/2.9/3.12/2.83 |
| WR14 < -97 | 71 | 76.1 | 2.28 | 11.3 | 1.6 | 24 / 2.83 | 2.02/-/2.17/1.25/-/1.46 |
| WR14 >= -90 | 200 | 74.5 | 2.63 | 29.3 | 3.6 | 61 / 3.58 | 1.89/.75/.92/7.1/1.57/4.52 |
| Keltner depth >= 1.5 ATR | 127 | 71.7 | 2.55 | 20.2 | 1.8 | 40 / 2.09 | 11.93/-/1.46/2.33/2.71/1.9 |
| Keltner depth >= 2.5 ATR | 15 | 53.3 | 0.77 | -0.6 | 1.3 | 7 / 0.55 | too few |
Findings: deeper oscillator readings raise PF slightly (CCI<-100 3.39) but cut return by a third (60.6 -> 41.4) and the last-12-month PF falls (3.37 -> 2.67), so it fails the beat-on-return and last-12m tests; the PF gain is mostly a 2021 artifact (12.1). Williams %R adds nothing beyond the live IBS/RSI2 selection. Extreme Keltner depth (>=2.5 ATR) is a falling knife (PF 0.77, n=15), consistent with the run 45 finding that deeper is not better. The web claim of high win rates for Williams %R is not reproduced as an edge over the live setup.
Verdict: NOT a promotion candidate; nothing added to challenger.py.

## 2026-11-20 (run 47) - 1-day idiosyncratic drop (stock return minus 60d-beta x SPY return on the signal day) and stock-vs-market divergence as conditioners of the vol60>=1.75% LIVE setup (own idea; run 30 tested only the 5d residual, run 32 only SPY direction; no web source this run, run 46 was web). Script: lab_idio1.py
Rules: LIVE trades (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12, 4/day; data through 2026-10-29); keep a signal only if the signal-day feature passes. idio1 quartiles of live trades -2.59 / -1.51 / -0.55 %. 8 variants tried (multiple-comparison discount applies).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| idio1 < -2% | 128 | 67.2 | 2.19 | 19.0 | 3.0 | 50 / 4.5 | 1.62/.22/.77/4.4/.82/5.15 |
| idio1 < -4% | 36 | 72.2 | 3.69 | 9.4 | 0.9 | 15 / 4.59 | too few |
| idio1 >= -2% (market-driven) | 211 | 76.3 | 3.05 | 36.8 | 3.7 | 57 / 2.64 | 6.25/1.63/1.69/4.76/3.42/2.19 |
| idio1 >= -1% | 123 | 79.7 | 4.24 | 22.9 | 1.9 | 24 / 5.3 | 8.16/-/2.16/5.42/8.36/2.76 |
| stock<0 & SPY>0 (divergence) | 91 | 67.0 | 1.67 | 7.3 | 3.0 | 31 / 4.04 | .55/0/.58/3.47/.57/4.83 |
| SPY 1d < -0.5% (market-led) | 160 | 79.4 | 4.40 | 41.5 | 2.3 | 54 / 4.04 | 229.7/-/3.12/5.77/2.51/4.31 |
| stock 1d < -3% | 114 | 76.3 | 4.11 | 32.3 | 2.5 | 44 / 5.24 | 25.8/-/1.02/9.24/1.62/5.48 |
| stock 1d >= -1% | 75 | 74.7 | 2.23 | 6.6 | 1.6 | 20 / 3.59 | 1.37/-/.68/3.43/4.26/3.31 |

Findings: the weak side is clear: stock-specific (idiosyncratic) and divergence drops (stock down while SPY up) are the worst trades (PF 1.67-2.19, 2022/2023/2025 at or below 1) - consistent with news-driven drops continuing while market-wide washouts revert. The strong side (SPY down >0.5% on the signal day, PF 4.40, win 79.4%, DD 2.3) is the same information as run 30's SPY-day-IBS size tilt and the market-state timing of run 32, so it is not independent evidence. Every PF-raising filter cuts return by 30-60% (60.6 -> 41.5 best) and the 2021 PF values are artifacts of tiny samples; none passes beat-on-return. The only usable form would be a size tilt (up on SPY-down days, down on divergence days), which overlaps the existing run 30 PROMOTION CANDIDATE.
Verdict: NOT a promotion candidate; nothing added to challenger.py. Possible follow-up: check whether the divergence-day size-down adds anything on top of run 30's tilt.

## 2026-11-20 (run 48) - bullish outside / key reversal-day sleeve (web idea). Script: lab_revday.py
Source: https://www.pulse.bot/stock-trading/news/reversal-day-strategy-for-the-markets-1fbb2118-59a3-415b-8f16-28b75dbc8c47/ (search snippet only, not fetched; marketed backtest, unverified).
Rules: long at close when low < prior low AND close > prior high (outside reversal) [or key reversal: low<prior low, close>prior close and >open]; close>SMA200, SPY>200d, ATR%<6%, 3-day cooldown; exit close>SMA5 (or >prior high), hold 7, stop 4 ATR; simulator 10% x 12, 4/day. 6 variants tried (discount applies). Data through 2026-10-29.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| outside rev, s200 | 1637 | 54.3 | 0.99 | -1.8 | 9.1 | 345 / 0.96 | 1.38/.62/.95/1.06/.87/.99 |
| + prior 3 down closes | 467 | 57.4 | 0.99 | -0.7 | 5.9 | 103 / 1.07 | 1.51/.51/.96/.96/.85/.99 |
| + vol60>=1.75 | 767 | 53.7 | 1.01 | 0.4 | 7.8 | 217 / 0.86 | 1.35/.72/1.61/.63/.95/.94 |
| + vol60>=1.75, exit prev high | 751 | 68.6 | 1.21 | 19.1 | 7.3 | 211 / 1.15 | 1.37/.77/1.68/.79/1.3/1.24 |
| + down3 + vol60>=1.75 | 194 | 59.3 | 1.39 | 6.1 | 3.1 | 55 / 0.91 | 1.51/.71/3.02/1.23/1.18/.94 |
| key reversal, vol60>=1.75 | 1989 | 61.4 | 1.12 | 25.3 | 12.6 | 549 / 1.29 | .91/.59/1.26/1.06/1.25/1.22 |
Combined with LIVE: every combination lowers PF (best: LIVE + down3 sleeve PF 2.26 vs 2.83, return 66.1 vs 60.6, L12 PF 2.26 vs 3.37) - the extra return is just extra exposure at lower quality.
Findings: the reversal-bar pattern carries no edge by itself (PF ~1.0 standalone); the live setup's edge comes from multi-day washout + vol + breadth, not a single reversal candle.
Verdict: NOT a promotion candidate; nothing added to challenger.py.

## 2026-11-20 (run 49) - structural stops (signal-day low / 5d low) and weekend-avoidance (Friday) exits on the vol60>=1.75% LIVE setup (own idea; no earlier run tested a price-structure stop or a weekend exit; no web source this run, run 48 was web). Script: lab_stop.py
Rules: LIVE = A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, exit close>prior high, hold 7, 10% x 12, 4/day, data through 2026-10-29. Variants replace the 4 ATR stop with max(entry-4ATR, low[signal day or 5d]-k ATR), or add a Friday-close exit (any Friday, or only if in profit). 6 variants tried (discount winners).
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| stop = signal-day low - 0 ATR | 377 | 34.2 | 1.68 | 22.5 | 3.1 | 122 / 1.47 | 1.04/.69/1.53/2.68/2.17/1.18 |
| stop = signal-day low - 0.5 ATR | 345 | 55.9 | 1.68 | 30.8 | 4.3 | 113 / 1.86 | 1.2/.36/1.41/2.43/1.64/1.67 |
| stop = signal-day low - 1 ATR | 324 | 67.3 | 1.86 | 38.7 | 5.7 | 105 / 1.74 | 2.3/.43/1.26/2.93/1.61/1.71 |
| stop = 5d low - 0.5 ATR | 345 | 55.9 | 1.66 | 29.9 | 4.3 | 113 / 1.85 | 1.16/.36/1.41/2.35/1.62/1.65 |
| exit any Friday close | 333 | 61.3 | 1.83 | 30.9 | 5.3 | 105 / 1.78 | 3.14/.69/1.25/2.11/1.58/1.95 |
| exit Friday close only if in profit | 312 | 76.9 | 2.93 | 54.5 | 4.5 | 101 / 3.17 | 4.13/.87/1.58/4.73/2.46/3.32 |
Findings: tight structural stops destroy the edge (the reversion needs room to retrace below the signal-day low before it bounces; win rate 34-56% vs 74%). Forced weekend flattening also hurts (PF 1.83). Friday-exit-if-profitable is the only near-neutral variant: PF 2.93 vs 2.83 (2021 4.13 vs 2.41) but return 54.5 vs 60.6, L12 PF 3.17 vs 3.37, 2023 and 2025 lower; it fails the return and last-12-months tests and the PF gain is within noise. The existing 4 ATR stop and prior-high exit look well placed.
Verdict: NOT a promotion candidate; nothing added to challenger.py.
Follow-ups still untested: TLT/IEF/GLD/HYG (not in bars cache), true PEAD (no earnings data), mean-reversion half-life per stock as selector, next run should be web.

## 2026-11-20 (run 50) - prior-trend quality (60d log-price R^2 / slope, measured on the 60 days ending 5 days before the signal) and MACD(12,26,9) histogram depth as conditioners of the vol60>=1.75% LIVE setup (web-seeded by search only: https://medium.com/@constandinou.antonio/quant-post-3-1-a-guided-path-into-mean-reversion-8b33b3c279e4 , snippet only, unverified; the OU half-life idea itself was already covered by autocorr/stockmem/ER runs). Script: lab_trendq.py
Rules: LIVE = A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, exit close>prior high, hold 7, stop 4 ATR, 10% x 12, 4/day, data through 2026-10-29. Each variant is a pure filter on live signals. 9 variants tried (discount winners).
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| prior60 R2 >= 0.5 | 230 | 73.0 | 2.90 | 46.7 | 3.5 | 79 / 4.00 | 3.16/1.60/1.36/4.93/2.01/4.25 |
| prior60 R2 < 0.5 | 94 | 75.5 | 1.99 | 8.7 | 2.2 | 24 / 1.91 | 1.45/0/1.42/4.95/1.80/1.95 |
| prior60 slope > 0.10 | 261 | 74.7 | 2.94 | 53.7 | 3.3 | 84 / 3.33 | 3.39/.87/1.82/4.38/2.58/3.17 |
| MACD hist/price < -0.5% | 231 | 77.5 | 3.40 | 50.4 | 2.1 | 73 / 3.04 | 4.99/-/2.40/4.54/3.78/2.51 |
| MACD hist/price < -1% | 134 | 74.6 | 2.93 | 27.7 | 2.1 | 54 / 3.38 | 4.93/-/2.00/2.74/2.83/3.03 |
| MACD hist/price >= -0.5% | 99 | 67.7 | 1.87 | 9.3 | 3.1 | 31 / 4.23 | 1.07/0/.56/6.43/.57/10.2 |
Findings: smooth prior uptrends (R2>=0.5) lift PF slightly (2.90 vs 2.83) and L12 PF (4.00) and turn 2022 positive, but return falls 60.6 -> 46.7 because capacity goes unused; 2023 and 2025 get worse, so it fails the return and all-but-one-year tests. MACD depth < -0.5% has the best PF (3.40) but return 50.4 vs 60.6, L12 PF 3.04 < 3.37, and its 2022 has no trades. Slope>0 alone is a no-op (only 13 trades removed). Trade-quality filters here trade return for PF; with 9 variants tried, a PF gain of this size is inside multiple-comparison noise.
Verdict: NOT a promotion candidate; nothing added to challenger.py.
Follow-ups still untested: TLT/IEF/GLD/HYG (not in bars cache), true PEAD (no earnings data). Next run should be own idea.

## 2026-11-20 (run 51) - information discreteness ("frog in the pan") of the pre-signal decline as conditioner of the vol60>=1.75% LIVE setup (web-seeded by search hit only: https://www3.nd.edu/~zda/Frog.pdf , Da/Gurun/Warachka; not fetched, unverified). Script: lab_infodisc.py
Rules: LIVE = A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, exit close>prior high, hold 7, stop 4 ATR, 10% x 12, 4/day, data through 2026-10-29. For a dip, ID_n = %up days - %down days over n=10/20 days (high = few big drops, "discrete"); mx_n = largest single down day / sum of all down days. Median splits, pure filters. 8 variants tried (discount winners); ties at the median make split counts overlap slightly.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| id10 continuous half | 111 | 73.0 | 2.65 | 17.4 | 2.6 | 32 / 6.59 | 1.98/0/.70/6.78/.94/37.5 |
| id10 discrete half | 224 | 74.6 | 2.91 | 39.8 | 1.9 | 74 / 2.73 | 3.17/-/2.50/3.97/3.14/2.28 |
| id20 continuous half | 162 | 75.3 | 2.95 | 29.0 | 2.7 | 53 / 4.54 | 4.57/0/1.74/6.34/1.79/5.18 |
| id20 discrete half | 188 | 73.4 | 2.54 | 28.7 | 2.7 | 57 / 2.88 | 1.95/-/1.47/3.86/1.77/2.95 |
| mx10 one day dominates | 169 | 74.0 | 3.47 | 35.6 | 2.6 | 55 / 8.68 | 1.69/.87/1.69/7.17/2.6/7.6 |
| mx10 spread over days | 173 | 71.7 | 2.18 | 21.9 | 2.7 | 52 / 1.87 | 3.62/-/1.44/3.39/1.4/2.2 |
| mx20 one day dominates | 165 | 73.9 | 2.91 | 30.3 | 3.0 | 55 / 5.97 | 1.92/.87/.95/4.25/2.51/5.64 |
| mx20 spread over days | 175 | 73.1 | 2.50 | 26.1 | 2.9 | 56 / 2.20 | 3.08/-/1.67/6.3/1.82/2.43 |
Findings: the paper's prediction (discrete-information drops revert more) is not supported by the ID measure: id10 and id20 point in opposite directions, so it is noise. The only consistent pattern is mx10: when one big down day dominates the 10-day drop, PF 3.47 vs 2.18 (spread-out slides), L12 8.7 vs 1.9 - plausibly the same "capitulation/shock day" information as the earlier ATR-drop/gap runs. But it halves return (35.6 vs 60.6), 2021 and 2023 are no better than live, and it is one of 8 variants tried.
Verdict: NOT a promotion candidate; nothing added to challenger.py. Possible low-priority follow-up: mx10 as a size tilt (up when one day dominates), overlapping run 28/33 shock-day findings.

## 2026-11-21 (run 52) - per-stock mean-reversion half-life and variance ratio as selectors of the vol60>=1.75% LIVE setup (web-seeded by search hits only, not fetched, unverified: https://medium.com/@constandinou.antonio/quant-post-3-1-a-guided-path-into-mean-reversion-8b33b3c279e4 , https://arxiv.org/html/2412.12458v1). Script: lab_halflife.py
Rules: LIVE = A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, exit close>prior high, hold 7, stop 4 ATR, 10% x 12, 4/day, data through 2026-10-29. Half-life = AR(1) on log-price deviation from 20d SMA over the 252 days before the signal; variance ratio VR(q) = Var(q-day returns)/(q*Var(1-day)) over 252 days (VR<1 = stock historically mean-reverting). Pure filters on live signals. First pass 6 tertile variants; robustness pass 10 more (16 total, discount winners).
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| half-life low third | 112 | 75.9 | 3.67 | 23.0 | 2.3 | 45 / 4.1 | 2.03/-/1.17/23.2/2.78/4.2 |
| half-life mid third | 103 | 69.9 | 1.73 | 8.4 | 3.9 | 35 / 1.97 | 52.6/0/.71/5.16/1.75/1.37 |
| half-life high third | 103 | 71.8 | 2.90 | 18.9 | 1.9 | 27 / 4.9 | -/1.63/2.01/2.36/1.58/6.45 |
| VR(5) low third | 103 | 81.6 | 5.14 | 22.2 | 1.0 | 41 / 6.56 | 2.45/-/2.75/43.9/3.74/6.56 |
| VR(5) < 1.0 | 185 | 75.7 | 3.48 | 39.7 | 2.9 | 73 / 3.38 | 2.84/-/2.51/16.7/1.87/3.82 |
| VR(5) >= 1.0 | 124 | 71.0 | 2.03 | 13.9 | 3.3 | 30 / 3.59 | -/0/.85/2.54/2.38/3.07 |
| VR(3) < 1.0 | 154 | 74.7 | 2.92 | 23.2 | 2.6 | 56 / 4.5 | 2.46/1.89/1.53/6.21/1.71/4.31 |
| VR(10) < 1.0 | 200 | 73.5 | 2.56 | 31.9 | 4.5 | 75 / 2.89 | 2.78/-/1.25/6.93/1.89/2.94 |
| VR(5, 120d) < 1.0 | 200 | 75.5 | 2.86 | 35.5 | 2.2 | 65 / 2.88 | 1.73/-/2.41/10.61/1.82/3.44 |
Findings: half-life is non-monotonic (low 3.67 / mid 1.73 / high 2.90), i.e. noise. VR(5) low third (PF 5.14) looks striking but does not replicate across windows/horizons (VR(3)<0.95 PF 2.8, VR(10)<0.95 PF 2.64, 120d window PF 2.8); every filtered subset is dominated by 2024 (PF 7-44, tiny n), 2022 has no trades, and in every case total return falls (22-40% vs 60.6%) because capacity goes unused. VR>=1 is weaker (PF 2.03), so a mild direction exists (historically mean-reverting stocks revert a bit better) but it never beats the champion on return, and 1 winner of 16 variants is what chance alone produces.
Verdict: NOT a promotion candidate; nothing added to challenger.py.
Follow-ups still untested: TLT/IEF/GLD/HYG (not in bars cache), true PEAD (no earnings data), mx10 one-day-dominates as size tilt (run 51). Next run should be own idea.

## 2026-11-21 (run 53) - size tilt on mx10 (share of the 10-day drop caused by the single largest down day), follow-up of run 51 (own idea, no web source). Script: lab_mxtilt.py
Rules: LIVE = A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, exit close>prior high, hold 7, stop 4 ATR, 10% x 12, 4/day, data through 2026-10-29. Size multiplier hi if mx10 >= threshold else lo (PF is size-weighted, same method as runs 30/31). Median mx10 = 0.36, p75 = 0.44. 4 variants tried (discount winners).
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| 1.25x if mx>=med else 0.75x | 308 | 74.4 | 3.00 | 64.7 | 4.2 | 100 / 4.12 | 2.2/.87/1.7/5.03/2.65/4.01 |
| 1.5x if mx>=med else 0.5x | 308 | 74.4 | 3.19 | 68.7 | 4.0 | 100 / 5.2 | 2.01/.87/1.8/5.33/2.79/4.8 |
| 1.5x if mx>=p75 else 1.0x | 308 | 74.4 | 2.86 | 71.1 | 5.1 | 100 / 3.77 | 2.22/.98/1.51/5.0/2.45/3.86 |
| 1.0x if mx>=med else 0.5x | 308 | 74.4 | 3.06 | 46.4 | 3.1 | 100 / 4.44 | 2.13/.87/1.73/5.13/2.7/4.24 |
Split check (1.5/0.5 tilt): <=2023 PF 1.84 vs live 1.89 (return 8.9 vs 9.8): no help early. >=2024 PF 4.19 vs 3.48 (return 55.0 vs 46.4).
Findings: the tilt lifts PF, return and L12 on the full sample, but the whole gain sits in 2024-2026; in the early years (2021-2023) it is neutral to slightly negative and 2021 gets worse. That fails the choose-early/confirm-late discipline, the mx10 signal was selected from a run-51 median split on the same data, and it is a scaled-pnl approximation that ignores position-size caps. Same shock-day information as runs 28/33.
Verdict: NOT a promotion candidate; nothing added to challenger.py.
Follow-ups still untested: TLT/IEF/GLD/HYG (not in bars cache), true PEAD (no earnings data). Next run should be web (actually fetched pages, not search snippets).

## 2026-11-21 (run 54) - "signal-day close is the lowest close of N days" filter on the vol60>=1.75% live setup (lab_lown.py). Own idea.
Results (n / PF / return): close=10d low 254 / 3.01 / 50.1%; not 10d low 72 / 1.59 / 5.2%; close=20d low 97 / 2.07 / 11.4%; not 20d low 234 / 3.23 / 46.9%. The 40d/60d sets were too small and crashed the row printer (empty set, no 'alpha' key; not fixed, lab-only). Result: extra-deep new lows are not better (20d low is worse); 10d low is mostly the existing set. Return falls in every subset. Verdict: NOT a candidate; nothing added to challenger.py.

## 2026-11-21 (run 55) - 12-1 month momentum (close[i-21]/close[i-252]-1) as conditioner of the vol60>=1.75% live setup (web-seeded by search hits only, not fetched, unverified: https://mysimon.rochester.edu/novy-marx/research/RRLP.pdf , https://www.quantconnect.com/research/15367/short-term-reversal/). Script: lab_mom121.py
Rules: live setup without the zreg step (ref PF 2.96, 289 trades), split on 12-1 momentum at the median (0.379) and at 0. 4 variants tried.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| ref | 289 | 74.4 | 2.96 | 58.6 | 4.3 | 100 / 3.37 | 3.69/.87/1.62/4.74/2.51/3.41 |
| mom >= median | 156 | 76.3 | 3.89 | 37.6 | 1.9 | 56 / 4.18 | 2.84/0/1.61/7.62/4.52/3.64 |
| mom < median | 151 | 72.2 | 2.14 | 17.2 | 3.3 | 48 / 2.79 | 44.9/-/1.55/2.11/1.53/3.44 |
| mom > 0 | 249 | 73.1 | 2.83 | 48.1 | 4.5 | 91 / 3.63 | 3.26/.87/1.22/4.64/2.36/3.64 |
| mom <= 0 | 46 | 80.4 | 3.97 | 7.4 | 0.8 | 11 / 2.02 | -/-/4.22/4.27/5.68/2.11 |
Findings: mild direction (winners-of-last-year dips revert better, PF 3.89 vs 2.14) but the filter halves trades and return (37.6 vs 58.6), 2021 and 2023 do not improve, 2022 has no trades; same pattern as runs 16/52. Not a candidate; nothing added to challenger.py.
Follow-ups untested: TLT/IEF/GLD/HYG (not in bars cache), true PEAD (no earnings data). Next run should be own idea.

## 2026-11-21 (run 56) - web fetch: "5-day mean reversion" (washout after a cascade of lower lows). Source (fetched): https://algomatictrading.substack.com/p/strategy-9-the-5-day-mean-reversion ; other search hits not fetched: https://quantifiedstrategies.substack.com/p/new-low-trading-strategy , https://strategyquant.com/blog/tuesday-reversal-strategy-tested-on-nasdaq-100-and-sp-500-stocks/
Result: page is paywalled after the overview, so no exact rules. Entry is "a close after a quick cascade of lower lows", exit is "signs of recovery" plus a hard time stop, with no thresholds given. Claimed (unverified) on Nasdaq-100 futures 2000-2025: 436 trades, win 67%, PF 1.58, max DD -10.7%, CAGR 4.95%.
Verdict: untestable as published. The cascade and new-low parts were already tested in run 33 (consecutive lower lows, N-day closing low) and run 54 (N-day low filter); the live setup has PF 2.83 against the claimed 1.58. No new backtest this run, nothing added to challenger.py.
Housekeeping: lab_lown.py crashes on the 40d/60d rows (empty subsets), lab-only and not fixed.
Next run: own idea, or a web page that is not paywalled (Quantpedia free pages, arXiv).

## 2026-11-21 (run 57) - SPY signal-day volume ratio (SPY vol / prior-20d avg) as filter and size tilt of the vol60>=1.75% live setup (own idea; no market-volume conditioner in runs 1-56, run 56 was web). Script: lab_spyvol.py
Rules: live setup (before zreg step), data through 2026-10-29. Median ratio on signal days 1.08. 8 variants tried (4 filters + 4 tilts; all correlated, same direction, so discount modestly). Tilt = PF-size-weighted like runs 30/31/53.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| filter ratio>=1.08 | 163 | 76.1 | 3.27 | 32.3 | 2.4 | 53 / 3.27 | 6.75/-/2.36/4.09/2.21/3.65 |
| filter ratio<1.08 | 170 | 68.8 | 1.94 | 18.7 | 4.1 | 54 / 3.01 | 1.22/.12/.86/4.03/1.68/2.81 |
| filter ratio>=1.2 | 123 | 77.2 | 3.95 | 29.1 | 2.2 | 32 / 3.15 | 91/-/4.34/4.64/1.8/3.95 |
| tilt 1.25x if >=1.08 else 0.75x | 308 | 74.4 | 3.16 | 66.7 | 3.6 | 100 / 3.45 | 2.97/1.37/1.98/4.99/2.68/3.63 |
| tilt 1.5x/0.5x | 308 | 74.4 | 3.56 | 73.0 | 2.9 | 100 / 3.53 | 3.75/2.37/2.51/5.28/2.84/3.88 |
| tilt 1.5x if >=1.2 else 1.0x | 308 | 74.4 | 3.12 | 84.3 | 4.4 | 100 / 3.40 | 3.13/1.24/1.9/4.96/2.54/3.60 |
| tilt 1.0x/0.5x | 308 | 74.4 | 2.83->3.28 | 48.2 | 2.5 | 100 / 3.48 | 3.2/1.62/2.14/5.08/2.73/3.71 |
Split (1.5/0.5 tilt, threshold fixed from full-sample median): <=2023 PF 3.00 vs live 1.89 (ret 15.6 vs 9.8); >=2024 PF 3.84 vs 3.48 (ret 49.6 vs 46.4). Unlike run 53, the gain is present in the early years too, and every single year improves (2022 included).
Findings: dips taken on heavier-than-normal market volume (capitulation days) revert better. Dropping the low-volume signals cuts return, so use it as a size tilt, not a filter. Challenger (1.25x/0.75x, fixed threshold 1.1): PF 3.17, ret 66.2%, DD 3.6%, L12 PF 3.48, beats champion in 6/6 years (2.95/1.37/1.98/5.03/2.74/3.59). Caveats: scaled-pnl approximation ignoring position caps; 2026 not sealed in this framework; threshold near the in-sample median; overlaps in spirit with the SPY-IBS and dispersion tilts (market-stress proxies), so stacking probably adds little: not tested.
Verdict: PROMOTION CANDIDATE (as a size rule, same class as runs 30/52). Added to challenger.py as "lab run57". Live files untouched.
Follow-ups: correlation with run30/52 tilts and stack of all three; true PEAD / TLT/HYG still impossible (no data). Next run should be web (fetch a non-paywalled page).

## 2026-11-21 (run 58) - stack / vote of the three market-state size tilts (dispersion pct>=0.5, SPY IBS<0.3, SPY volume ratio>=1.1) on the vol60>=1.75% live setup. Web seed: search hit only, not fetched, unverified: https://alphaarchitect.com/how-volatility-and-turnover-affect-return-reversals/ . Script: lab_tiltstack.py
Rules: live setup before the zreg step (308 trades); each trade gets a 1.25x/0.75x multiplier per flag; flags count per trade: 0 flags 124, 1 flag 210, 2 flags 196, 3 flags 108. 8 variants tried (each also shown normalised to mean multiplier 1 so extra leverage is not mistaken for edge). Tilts are PF-size-weighted approximations ignoring position caps.
| Variant | Mean mult | Win % | PF | Ret % | Max DD % | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 1.00 | 74.4 | 2.83 | 60.6 | 4.3 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| disp only (run52) | 1.00 | 74.4 | 3.14 | 70.3 | 3.9 | 3.76 | 2.93/.87/1.78/5.30/2.58/3.73 |
| SPY IBS only (run30) | 1.00 | 74.4 | 3.25 | 67.5 | 3.3 | 3.70 | 2.96/.95/2.18/5.20/2.87/3.49 |
| SPY vol only (run57) | 0.97 | 74.4 | 3.17 | 66.2 | 3.6 | 3.48 | 2.95/1.37/1.98/5.03/2.74/3.59 |
| stack disp x ibs (run31) | 1.01 | 74.4 | 3.63 | 79.2 | 3.0 | 4.17 | 3.74/.95/2.44/5.85/2.90/3.94 |
| stack all three (multiplied) | 1.00 | 74.4 | 4.05 | 87.8 | 2.8 | 4.33 | 4.37/1.45/3.08/6.24/3.05/4.23 |
| vote 0.5+0.25k | 0.86 | 74.4 | 3.48 | 62.0 (74.8 normalised) | 2.7 | 3.86 | 3.45/1.16/2.31/5.55/2.89/3.76 |
| vote 0.75+0.25k | 1.11 | 74.4 | 3.32 | 82.2 (71.5 norm.) | 3.8 | 3.74 | 3.17/1.08/2.12/5.35/2.80/3.68 |
| 1.5x if >=2 flags else 0.75x | 1.11 | 74.4 | 3.49 | 85.3 (74.6 norm.) | 3.4 | 4.05 | 3.42/1.74/2.15/5.18/3.15/3.85 |
Split, stack all three normalised to mean 1: <=2023 PF 3.52 vs live 1.89 (ret 18.7 vs 9.8); >=2024 PF 4.29 vs 3.48 (ret 57.7 vs 46.4). Every year improves and the stack is monotonic in the number of flags, with normalisation changing almost nothing (so it is not just leverage).
Findings: the three flags are different views of the same thing (a washed-out, high-volume, wide-dispersion market day) but they are not redundant: stacking beats every single tilt in every year, including 2022 (PF 1.45, the first time that year clears 1). Caveats: all three thresholds were picked in-sample on this same trade set (runs 30, 52, 57), so the stack carries three rounds of selection; flags correlate; the scaled-PnL approximation ignores caps and a 1.25^3 = 1.95x top size is above what 10% x 12 sizing could hold (3 flags = 108 trades get 1.95x, 0 flags = 124 get 0.42x); 2026 is not sealed. Treat as direction (more market stress -> bigger size), not as a precise PF of 4.
Verdict: PROMOTION CANDIDATE (size rule, strongest of the tilt family; the vote version 0.5+0.25k is the more conservative form, PF 3.48 / DD 2.7%). Added to challenger.py as "lab run58" (multiplied stack). Live files untouched. The daily improvement task should prefer a capped version (e.g. 0.5x to 1.5x) if it ever promotes this.
Follow-ups: a capped stack (clip multiplier 0.5-1.5) through the real portfolio simulator with position caps; true PEAD / TLT/HYG still impossible (no data). Next run should be own idea.

## 2026-11-21 (run 59) - CAPPED version of the run-58 three-tilt stack (multiplier clipped), follow-up to run 58. Own idea (no web this run; runs 56-58 were web-seeded). Script: lab_tiltcap.py
Rules: live vol60>=1.75% setup before zreg (308 trades). Multiplier = product of three 1.25x/0.75x flags (disp pct>=0.5, SPY IBS<0.3, SPY vol ratio>=1.1), clipped. PF-size-weighted approximation (not the real simulator with position caps). 4 variants tried; thresholds were chosen in-sample in runs 30/52/57, so selection bias remains.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| uncapped stack (run 58) | 308 | 74.4 | 4.05 | 87.8 | 2.8 | 4.33 | 4.37/1.45/3.08/6.24/3.05/4.23 |
| clip 0.5-1.5 | 308 | 74.4 | 3.70 | 73.5 | 2.7 | 4.10 | 3.79/1.45/2.53/5.69/3.05/3.94 |
| clip 0.6-1.6 | 308 | 74.4 | 3.65 | 77.1 | 2.9 | 4.10 | 3.63/1.45/2.45/5.62/2.99/4.01 |
| clip 0.75-1.25 | 308 | 74.4 | 3.29 | 67.7 | 3.4 | 3.84 | 3.08/1.36/1.99/5.09/2.91/3.74 |
| 3-level 0.75/1.0/1.5 by flag count | 308 | 74.4 | 3.26 | 74.7 | 3.7 | 3.65 | 3.02/.87/2.13/5.46/2.62/3.69 |
Split (clip 0.5-1.5, normalised to mean 1): <=2023 PF 2.98 vs live 1.89 (ret 16.1 vs 9.8); >=2024 PF 4.08 vs 3.48 (ret 54.4 vs 46.4).
Placebo (2000 shuffles of the multipliers across trades, same normalisation): median PF 2.86, p95 3.09, p99 3.18, real 3.31 (live 2.86), so the ordering of the multipliers beats random assignment at >99%, though this does not remove the in-sample threshold selection.
Findings: capping keeps most of the gain (PF 3.70 vs 4.05, return 73.5 vs 87.8, DD 2.7) and still beats the live setup in all six years, including 2022 (1.45). Max size 1.5x of a 10% slot is 15%, within a plausible cap. Same caveats as run 58: in-sample thresholds, scaled-PnL approximation, 2026 not sealed.
Verdict: PROMOTION CANDIDATE (the more deployable form of the run-58 stack; prefer this over the uncapped one). Added to challenger.py as "lab run59" (verified through challenger.py: PF 3.7 / ret 73.5). Live files untouched. Real position-cap simulation remains untested.
Next run: web (fetch a non-paywalled page, e.g. Quantpedia free page or arXiv).

## 2026-11-21 (run 60) - web check (no testable rules) + run-59 capped size stack through an exposure-cap simulator. Script: lab_capsim.py
Web: fetched https://alphaarchitect.com/what-drives-momentum-and-reversal/ (Barardehi/Bogousslavsky/Muravyev, day vs night signals). Summary page only: no lookbacks, breakpoints or returns given, and it contradicts itself on overnight reversal. Intraday reversal / overnight-no-reversal was already tested in runs 18 and 30 (lab_ovnintra.py). Nothing new to backtest; unverified.
Own test (follow-up named in runs 58/59): take the 308 live vol60>=1.75% trades actually selected by the portfolio simulator (10% x 12, 4/day), size each by base 10% x multiplier, compounding at exit, with a total-exposure cap (entries scaled down to the remaining room, skipped if <2%). 15 variants (5 sizings x 3 caps), all on the same trades.
| Sizing | Cap | Ret % | Max DD % | PF | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|
| flat 10% (live) | any | 60.6 | 4.3 | 2.83 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| clip 0.5-1.5 | none/120/100 | 73.5 | 2.7 | 3.70 | 4.10 | 3.79/1.45/2.53/5.69/3.05/3.94 |
| clip 0.5-1.5 normalised to mean 1 | none/120/100 | 81.3 | 2.9 | 3.70 | 4.10 | same |
| clip 0.75-1.25 | any | 67.7 | 3.4 | 3.29 | 3.84 | 3.08/1.36/1.99/5.09/2.91/3.74 |
| uncapped stack | 120 / 100 | 87.8 / 86.1 | 2.8 | 4.05 / 4.00 | 4.33 / 4.21 | 4.37/1.45/3.08/6.24/3.05/4.23 |
Peak concurrent exposure: flat 80% of equity; clip 0.5-1.5 90.5%. Extra caps at 80% (ret 71.7, PF 3.65) and 60% (ret 69.0, PF 3.57, 4 trades skipped) cost little.
Findings: position/exposure caps do not bind (a 120% or 100% cap changes nothing for the clipped stack), so the run-59 approximation holds in a cap-aware simulator: clip 0.5-1.5 gives PF 3.70, return 73.5 vs 60.6, DD 2.7 vs 4.3, better in all six years incl. 2022. Remaining caveats unchanged: the three thresholds were chosen in-sample on these trades (runs 30/52/57), 2026 not sealed, and the sizer ignores real cash/margin and fill effects.
Verdict: confirms the run-59 PROMOTION CANDIDATE (clip 0.5-1.5); already in challenger.py as "lab run59", no change. Live files untouched.
Next run: own idea (this one was web + validation), or a non-paywalled web page with explicit rules.

## 2026-11-22 (run 61) - WALK-FORWARD audit of the run-58/59 three-tilt size stack (own idea; web was run 60). Script: lab_wftilt.py
Rules: live vol60>=1.75% setup before zreg (638 trades in the raw generator list incl. pre-simulator overlap, 261 in 2023-26). Each test year 2023..2026, the three flag thresholds (dispersion pct {.3-.7}, SPY IBS {.2-.5}, SPY vol ratio {.9-1.3}) are re-fitted on ONLY earlier years (objective: single-tilt PF, 1.25x/0.75x), then applied as the clip 0.5-1.5 stack to that year. Chained out-of-sample path. Trials: 14 grid cells x 4 folds, one reported path. PF/return from the scaled-PnL approximation (caps shown not to bind in run 60).
| Variant (2023-26 only) | Trades | Win % | PF | Ret % | Max DD % | L12 PF | PF 2023/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE flat | 261 | 74.7 | 3.00 | 53.0 | 4.3 | 3.39 | 1.72/4.70/2.51/3.44 |
| walk-forward clip 0.5-1.5 | 261 | 74.7 | 3.67 | 60.0 | 2.9 | 3.65 | 2.93/5.91/2.61/3.95 |
| walk-forward, normalised to mean multiplier 1 | 261 | 74.7 | 3.67 | 62.9 | 3.0 | 3.65 | same |
| fixed in-sample thresholds (.5/.3/1.1) clip 0.5-1.5 | 261 | 74.7 | 3.83 | 61.6 | 2.7 | 4.13 | 2.86/5.63/3.05/3.98 |
Chosen thresholds (disp, ibs, vol) per test year: 2023 (.3,.4,1.2); 2024 (.3,.2,1.2); 2025 (.3,.4,1.2); 2026 (.6,.2,1.2). Mean multiplier 0.96.
Findings: with thresholds chosen only from the past, the stack still beats flat sizing in every test year (PF 3.67 vs 3.00, DD 2.9 vs 4.3, last-12m PF 3.65 vs 3.39), and gives up only a little to the in-sample thresholds (3.83). The fitted thresholds are stable in direction (dispersion low-to-mid, IBS low, volume ratio 1.2 every year), so the effect is not a product of the exact in-sample cut-offs. Weaknesses: the 2023 fit window holds only ~89 trades (2022 has 7), so 2023's gain (1.72 -> 2.93) comes from a weakly fitted model; return gain is modest (60.0 vs 53.0) because the clip limits upside; 2022 (the weak year) cannot be audited this way; 2026 is not sealed. The three market-state flags remain correlated, so treat the size rule as direction, not a precise PF of ~3.7.
Verdict: supports the existing run-59 PROMOTION CANDIDATE (clip 0.5-1.5 stack); nothing new added to challenger.py (already tracked as "lab run59"). Live files untouched.
Follow-ups: true PEAD / TLT / HYG still impossible (no data). Next run should be web (fetch a non-paywalled page with explicit rules).

## 2026-11-22 (run 62) - SPY drawdown from its N-day closing high as filter / size tilt of the vol60>=1.75% live setup (own idea; web search this run returned only Quantified Strategies SPY-index pages with no stock-level rules: https://quantifiedstrategies.substack.com/p/the-classical-mean-reversion-strategy, unfetched, unverified). Script: lab_spydd.py
Rules: live vol60>=1.75% setup before zreg (308 trades); signal-day SPY close / max(SPY close, last N days) - 1 for N = 20, 60, 120; filter at -2/-4/-6% and 1.25x/0.75x size tilt. 19 variants tried (discount lucky ones).
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| only SPY dd20 <= -2% | 127 | 74.8 | 3.56 | 29.8 | 3.0 | 4.46 | n/a(few)/-/1.47/6.12/1.90/7.53 |
| only SPY dd20 <= -4% | 36 | 77.8 | 4.16 | 6.6 | 0.6 | 4.34 (n=7) | 36.5/-/4.56/5.45/1.73/3.92 |
| only SPY dd120 <= -4% | 41 | 80.5 | 4.70 | 7.7 | 0.6 | 4.34 (n=7) | 36.5/-/5.16/7.09/2.23/3.92 |
| complement dd20 > -2% | 194 | 73.2 | 2.28 | 25.2 | 3.5 | 2.74 | 1.59/0/1.56/4.15/2.53/2.32 |
| size tilt dd20<=-2% 1.25/.75 | 308 | 74.4 | 3.11 | 63.3 | 3.7 | 3.63 | 2.94/1.45/1.78/4.90/2.51/4.00 |
| size tilt dd60<=-4% 1.25/.75 | 308 | 74.4 | 2.95 | 48.1 | 3.2 | 3.49 | 2.69/.87/1.80/4.79/2.46/3.47 |
Findings: signals taken when SPY is already down >=2% from its 20d high have higher PF (3.56 vs 2.28) in every year with enough trades, but filtering halves the return (29.8 vs 61.7), and the deep-drawdown buckets are tiny (36-41 trades, 7 in the last 12 months). As a size tilt it (PF 3.11) is no better than the existing single tilts (disp 3.14, SPY IBS 3.25, vol ratio 3.17) and well below the run-59 stack, and 2022 is only fixed by dd20 (1.45), likely because it overlaps the same washed-out-market information as those flags (not tested for overlap this run). Treat as a fourth view of the same market-stress effect, not a new edge.
Verdict: no promotion, not added to challenger.py (redundant with run 58/59 flags; only direction confirmed: more market stress -> better reversion). Live files untouched.
Next run: web (fetch a page with explicit stock-level rules); optionally test whether dd20 adds anything on top of the run-59 stack.

## 2026-11-22 (run 63) - SPY 20d drawdown (<=-2%) as a 4th flag on the run-59 clipped 3-tilt stack (own idea; follow-up to run 62). Script: lab_ddstack.py
Rules: live vol60>=1.75% setup before zreg (308 trades); multiplier = product of 1.25/0.75 per flag, clipped 0.5-1.5. 2 variants (x2 normalisation).
| Variant | Trades | Win % | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 2.32 | 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| 3-tilt clip | 308 | 74.4 | 3.79 | 74.8 | 2.7 | 2.45 | 4.13 | 3.79/1.45/2.86/5.63/3.05/3.98 |
| 4-tilt (+dd20) clip | 308 | 74.4 | 3.95 | 73.1 | 2.4 | 2.41 | 4.33 | 3.99/2.41/2.98/5.49/3.19/4.35 |
Findings: the dd20 flag overlaps the other three (53-65% co-occurrence), PF +0.16 but return and Sharpe are slightly lower, 2022 gain (1.45 -> 2.41) rests on few trades; 2024 is worse. Not an independent improvement.
Verdict: no promotion, not added to challenger.py. Live files untouched.

## 2026-11-22 (run 64) - "falling knife" conditioners: stock's 20d return and age of the decline (days since 60d closing high) on the vol60>=1.75% live setup (own idea; web search for stock-level pullback rules returned only generic pages, e.g. https://www.pulse.bot/stock-trading/news/buy-weakness-win-big-the-5-day-low-trading-strategy-89cc6501-8f84-4450-99be-3ca7240658ad/ and https://quantpedia.com/testing-an-ai-assisted-research-workflow-for-multi-asset-pullback-strategy-discovery/, unfetched, no testable rules). Script: lab_age.py
Rules: live setup before zreg (308 trades). Filters on signal day: age = days since 60d closing high (<=5/10/20/30); 20d return (> -3/-5/-7.5/-10%); size tilts. 21 variants tried (discount lucky ones).
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| 20d ret > -5% | 275 | 75.6 | 3.35 | 57.8 | 3.6 | 4.56 | 2.81/.87/1.76/5.28/2.78/5.44 |
| 20d ret <= -5% (removed) | 49 | 61.2 | 1.33 | 2.6 | 2.2 | 1.36 | 1.53/-/.77/1.96/.56/1.36 |
| age <= 20 | 276 | 75.0 | 3.18 | 61.4 | 3.6 | 3.63 | 3.33/.87/1.85/5.51/2.39/3.79 |
| age > 20 (removed) | 37 | 67.6 | 0.85 | -0.8 | 2.5 | 0.98 | .42/-/.27/2.13/-/.96 |
| 20d > -5% & age <= 20 | 253 | 75.1 | 3.36 | 54.4 | 2.9 | 4.42 | 2.67/.87/1.92/5.45/2.66/5.22 |
| size 1.25x if 20d > -5% else 0.5x | 308 | 74.4 | 3.14 | 78.6 | 4.9 | 3.97 | 2.61/.87/1.81/4.92/2.66/4.34 |
| size 0.5x if 20d <= -5% else 1x | 308 | 74.4 | 3.09 | 59.6 | 4.0 | 3.85 | 2.57/.87/1.79/4.88/2.64/4.15 |
Split: <=2023 PF 2.06 vs 1.96 live; >=2024 PF 4.30 vs 3.48.
Findings: signals on stocks already down >5% over 20 days (49 trades) or whose high is >20 days old (37 trades) are the weak ones (PF 1.33 / 0.85): the reversion works on sharp dips inside an intact short-term trend, not on slow bleeds. The filter is better than live in every year with data (2022 unchanged), but as a filter total return falls slightly (57.8 vs 61.7), and the effect rests on ~50 trades chosen from 21 variants, so the exact -5% cut is probably lucky; 2026 not sealed. As a size tilt it (PF 3.14) is on par with the existing single tilts (3.14-3.25) and was not stacked with the run-59 stack.
Verdict: no promotion, not added to challenger.py. Direction (avoid slow-bleed names) is the only takeaway. Live files untouched.
Next run: optionally test whether the 20d-return flag adds to the run-59 clipped stack; otherwise web with a fetchable rule page (WebFetch not directly available this run, search only).

## 2026-11-22 (run 65) - EWMA (RiskMetrics) volatility forecast as replacement/addition for the vol60>=1.75% filter (web-seeded). Script: lab_ewma.py
Source (fetched): https://setup4alpha.substack.com/p/low-drawdown-nasdaq-mean-reversion - says only "EWMA-based volatility forecast" + close>SMA200 + a Connors/Alvarez condition + limit entries; no parameters, results only in images, paid rules; unverified. Other search hits not fetched (low-volume pullback pages, Quantified Strategies new-low/RSI-drop pages; volume and N-day-low ideas already tested in runs 6, 54).
Rules: live trade list WITHOUT the vol filter (A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12, 4/day); filter by EWMA vol of daily returns (lambda .94 / .97, 250d seed) at the signal close. 13 variants tried (discount lucky ones).
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref vol60>=1.75 | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| EWMA.94 >=1.75 | 284 | 74.6 | 2.95 | 57.1 | 4.6 | 93 / 4.02 | 3.54/.57/1.69/3.82/2.17/4.52 |
| EWMA.94 >=2.0 | 218 | 74.8 | 3.23 | 51.2 | 4.2 | 72 / 4.13 | 6.89/.87/1.41/4.36/2.31/4.96 |
| EWMA.97 >=1.75 | 303 | 75.9 | 3.00 | 63.6 | 4.4 | 98 / 3.63 | 3.88/.87/1.60/4.83/2.21/3.78 |
| EWMA.97 >=2.0 | 226 | 74.8 | 3.18 | 51.7 | 4.7 | 71 / 3.95 | 3.63/.87/1.56/4.44/2.76/4.66 |
| EWMA.94 >=1.5 | 368 | 71.7 | 2.37 | 58.2 | 4.8 | 112 / 2.98 | 2.65/.31/1.67/2.90/1.98/2.92 |
| vol60>=1.75 & vol falling (EWMA94<vol60) | 218 | 74.8 | 2.75 | 36.0 | 3.4 | 64 / 2.91 | 1.23/-/1.63/6.62/4.89/2.30 |
| vol60>=1.75 & vol rising | 112 | 71.4 | 2.90 | 21.1 | 2.2 | 40 / 4.40 | 14.3/.12/1.17/2.62/1.52/7.14 |
(other rows: EWMA.94>=2.25 n155 PF3.35 ret39.7; EWMA.97>=2.25 n179 PF3.41 ret44.8; vol60&EWMA94>=1.5/2.0 n296/213 PF2.87/3.20.)
Findings: EWMA.97>=1.75 is essentially the same filter as vol60>=1.75 (303 vs 308 trades, PF 3.00 vs 2.88, return 63.6 vs 61.7) and is worse in 2023 and 2025, better in 2021 and 2026; a rewording, not a new edge. Higher thresholds raise PF only by cutting return (51 vs 62), the same trade-off as the vol60 threshold walk-forward (run 36). Rising vs falling vol split is erratic across years (2021 14.3 vs 1.2; 2024 2.6 vs 6.6). Nothing beats live on PF, return, L12 and all-but-one year together.
Verdict: no promotion, not added to challenger.py. Live files untouched. Next: web run should fetch a page with explicit rules (Algomatic/Quantified Strategies pages with numbered strategies), or test whether the run-64 20d-return flag adds to the run-59 clipped stack.

## 2026-11-22 (run 66) - run-64 "20d return > -5%" flag stacked on the run-59 clipped 3-tilt stack (own idea; no web this run, run 65 was web). Script: lab_ret20stack.py
Rules: live vol60>=1.75% setup before zreg (308 trades); multiplier = product of 1.25/0.75 per flag (disp rank>=.5, SPY IBS<.3, SPY vol ratio>=1.1, optional 4th: stock 20d ret > -5%), clipped 0.5-1.5. 3 variants (x2 normalisation). The -5% cut was itself picked among 21 variants in run 64, so every gain here is optimistic.
| Variant | Trades | PF | Ret % | Max DD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 2.88 | 61.7 | 4.3 | 2.32 | 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| 3-tilt clip | 308 | 3.79 | 74.8 | 2.7 | 2.45 | 4.13 | 3.79/1.45/2.86/5.63/3.05/3.98 |
| 4-tilt (+r20>-5%) | 308 | 3.82 | 85.6 | 3.1 | 2.54 | 4.44 | 3.53/1.45/2.68/5.84/3.14/4.31 |
| 3-tilt, zero size if r20<=-5% | ~259 effective | 4.40 | 66.0 | 2.3 | 2.69 | 5.25 | 3.96/1.45/3.07/6.25/3.70/5.63 |
Findings: r20 flag overlaps the others 43-51%. As a 4th tilt: PF flat (3.82 vs 3.79), return up (85.6 vs 74.8) mostly from larger average size (mean mult 1.06 vs 0.94; normalised return 78.8 vs 80.8 is no better), 2021/2023 slightly worse. As a hard filter on the stack: PF 4.40, Sharpe 2.69, L12 PF 5.25, better than the 3-tilt stack in every year, but un-normalised return falls (66.0 vs 74.8) because 49 trades are removed; the normalised figure (86.4) is just leverage. Gain rests on the in-sample -5% cut.
Verdict: no promotion, not added to challenger.py. Mildly supportive evidence that avoiding slow-bleed names is real, but wait for forward data (2026 not sealed). Live files untouched.
Next run: web (fetch a page with explicit stock-level rules).

## 2026-11-22 (run 67) - signal-day opening gap (vs prior close / prior low, scaled by vol60) and "open above SMA20" as conditioners of the vol60>=1.75% live setup (web-seeded). Script: lab_gapday.py
Source (fetched): https://www.quantrocket.com/blog/buy-or-sell-down-gaps/ (Sep 2020, 2014-2020 minute data, Zipline): buying gap-downs (open < prior low - 1 std, top-decile dollar volume, prior close > SMA20) loses intraday; small gaps with the open still above SMA20 recover, large gaps break the trend; claims are chart-only, no costs, unverified, different horizon (intraday). Also searched, paywalled/not testable: https://concretumgroup.substack.com/p/identifying-stocks-to-fade . Translation to daily bars: gap = open[i]/close[i-1]-1 on the SIGNAL day, z = gap/vol60.
Rules: live setup before zreg (308 trades, same simulator 10% x 12, 4/day). 17 variants tried (discount lucky ones).
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| gap z <= -1.0 | 44 | 77.3 | 4.65 | 9.9 | 0.8 | 16 / 10.27 | -/-/.43/10.6/1.19/13.8 |
| gap z <= -0.5 | 118 | 78.0 | 3.96 | 26.4 | 2.0 | 39 / 4.57 | -/0/1.33/7.63/2.00/4.67 |
| gap z > -0.5 | 222 | 70.7 | 2.14 | 28.9 | 3.7 | 67 / 2.61 | 1.65/1.89/1.59/3.51/1.82/2.44 |
| gap z > -1.0 (drop deepest gaps) | 281 | 73.3 | 2.56 | 48.0 | 4.9 | 89 / 2.93 | worse than live |
| open < prior low | 152 | 74.3 | 3.00 | 25.8 | 2.4 | 50 / 2.33 | 22.0/-/1.34/8.88/1.42/2.79 |
| open >= prior low | 189 | 73.0 | 2.45 | 30.5 | 3.7 | 55 / 5.20 | 1.65/.12/1.52/3.12/2.82/4.51 |
| open > SMA20 (trend intact) | 108 | 75.0 | 3.35 | 23.8 | 2.4 | 34 / 8.35 | 1.38/0/1.61/9.63/1.60/18.7 |
| open <= SMA20 | 228 | 73.7 | 2.48 | 33.8 | 3.2 | 69 / 2.36 | 4.50/-/1.42/3.31/2.71/2.05 |
| gap >= 0 | 106 | 71.7 | 2.09 | 13.3 | 2.3 | 34 / 15.15 | 1.03/.28/1.72/1.48/3.15/8.34 |
| intraday o->c < 0 | 277 | 73.6 | 2.80 | 55.0 | 4.2 | 92 / 3.36 | ~live |
(buckets overlap/partition the same 308 trades; subsets are not additive in the simulator.)
Findings: the web claim (small gaps recover, big gaps keep falling) is NOT supported on daily signal-day gaps: the deeper the signal-day gap-down in vol units, the HIGHER the PF (gap z<=-0.5: PF 3.96 vs 2.14 for the rest), the opposite direction of the source, but returns halve and the deep buckets are small (15-44 trades) and erratic by year (2022 PF 0, 2023 0.43-1.33). Other splits flip sign between full sample and last 12 months (gap>=0: PF 2.09 full, 15.2 L12; open<prior low: 3.0 full, 2.3 L12), the signature of noise. Nothing beats live on PF, return, L12 and all-but-one year together. The effect, if any, is another view of "sharp, capitulating drop reverts better", already captured by zreg/vol60.
Verdict: no promotion, not added to challenger.py. Live files untouched.
Next run: own idea (stock/market cross-section not yet tried: e.g. exit timing by days-in-trade pnl, or a non-reversion family).

## 2026-11-22 (run 68) - stock relative strength vs SPY (20d/60d/120d) and 60d up-day share as conditioners of the vol60>=1.75% live setup (own idea; no web this run, run 67 was web). Script: lab_rs60.py
Rules: live setup before zreg (308 trades, same simulator 10% x 12, 4/day); signal-day stock N-day return minus SPY's N-day return (N = 20, 60, 120), and share of up-closes in the last 60 days; split into terciles of the 308 trades, plus rs60 > 0 / > -5%. 21 variants tried (discount lucky ones). Terciles overlap-free per metric but not additive across metrics.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 100 / 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| rs20 top third | 123 | 74.8 | 3.14 | 23.2 | 2.3 | 41 / 5.31 | 4.75/.26/1.30/5.18/1.20/10.1 |
| rs60 top third | 123 | 77.2 | 3.83 | 33.5 | 2.6 | 46 / 5.27 | n/a/-/1.90/3.83/1.94/7.91 |
| rs60 bottom third | 116 | 69.8 | 1.57 | 7.2 | 3.0 | 24 / 1.49 | .53/0/1.11/3.71/3.94/1.56 |
| rs120 top third | 122 | 76.2 | 3.78 | 36.1 | 2.0 | 47 / 5.15 | 3.41/.22/2.42/7.52/1.94/7.26 |
| up-day share top third (>0.55) | 92 | 75.0 | 4.89 | 23.0 | 0.9 | 30 / 6.07 | 4.41/-/2.79/5.26/6.06/4.85 |
| up-day share bottom third (<=0.50) | 129 | 70.5 | 1.71 | 11.1 | 3.4 | 41 / 1.97 | 1.82/0/1.49/2.97/.71/2.64 |
| rs60 > 0 (removes 45) | 263 | 74.5 | 2.84 | 53.4 | 4.2 | 85 / 3.48 | ~live |
Findings: dip-buys in stocks that have been stronger than SPY over 60-120 days, and whose last 60 days had many up-closes (steady uptrend, sharp dip), revert better (PF 3.8-4.9 vs 1.6-1.7 for the weakest third). This agrees with runs 64/66 (slow-bleed names are the weak ones) rather than adding a new edge, and run 16 already tested 126d momentum. Caveats: terciles of ~120 trades, thresholds chosen from the sample; as filters each keeps only 30-40% of the return (23-36% vs 61.7%) so the PF gain is bought by dropping trades; the best-looking cut (up-share top third, PF 4.89, DD 0.9) is the max over 21 variants and 2022 has no trades there; rs60 > 0 alone does nothing (PF 2.84). 2026 not sealed.
Verdict: no promotion, not added to challenger.py. Direction (prefer steady-uptrend names) is consistent with runs 64/66; could be tested as a size tilt on the run-59 stack once forward data accumulates. Live files untouched.
Next run: web (fetch a page with explicit stock-level rules).

## 2026-11-22 (run 69) - "Capitulation Stretch Reversion" sleeve (web idea). Script: lab_capstretch.py
Source: https://in.tradingview.com/script/WWuTjyDx-Capitulation-Stretch-Reversion-Jayadev-Rana/ (fetched; claimed SPY daily PF ~1.67, ~67% win, in-sample, unverified). A second page (quantifiedstrategies 3-days-down overnight) was paywalled, rules not readable.
Rules: close>SMA200, SPY>200d, ATR%<6%; bar i-1 closed >= k ATR below EMA5 after N consecutive lower closes; enter at close of bar i if it closes up; exit close>SMA5 (EMA5 proxy), stop 3 ATR, hold 10 (last two variants: prior-high exit, hold 7, stop 4 ATR); 3-day cooldown; simulator 10% x 12, 4/day; data through 2026-10-29. 6 variants x (standalone, +breadth>=10%, combined with LIVE) tried; discount winners.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 100 / 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 |
| k0.5 nd2 (paper defaults) | 2236 | 63.2 | 1.06 | 11.5 | 18.9 | 553 / 1.28 | 1.3/.35/.87/.96/1.14/1.38 |
| k1.0 nd2 | 870 | 62.1 | 1.04 | 3.1 | 13.2 | 198 / 1.37 | 1.77/.14/1.01/.92/.83/1.55 |
| k1.5 nd3 | 130 | 65.4 | 1.40 | 4.5 | 4.5 | 22 / 1.99 | 4.73/.34/.17/3.76/.56/1.98 |
| k1.0 nd2 + vol60>=1.75 | 398 | 64.6 | 1.39 | 18.5 | 7.3 | 117 / 1.82 | 3.49/.26/1.12/1.57/.87/2.19 |
| k1.0 nd2 + vol60>=1.75, prevhl, hold7, stop4 | 396 | 73.0 | 1.54 | 27.8 | 9.3 | 116 / 2.22 | 3.32/.37/1.29/1.88/.78/2.64 |
| + breadth>=10% (same) | 220 | 74.1 | 1.70 | 18.9 | 6.4 | 68 / 3.84 | 4.32/.37/.85/3.81/.67/8.53 |
| LIVE + k1.0 vol60 sleeve (breadth>=10%) | 453 | 72.6 | 2.01 | 60.3 | 7.5 | 144 / 3.04 | 2.21/.34/1.10/3.85/1.27/3.59 |
| LIVE + k1.5 nd3 vol60 sleeve | 328 | 73.5 | 2.63 | 61.1 | 5.2 | 106 / 3.42 | 2.41/2.08/1.41/4.66/1.85/3.5 |
Verdict: NOT a promotion candidate. As published (PF ~1.06, 19% drawdown, 2022 0.35) the rule has no edge on daily stocks; the paper's SPY result does not transfer. Vol60 + breadth + live-style exit lift it to PF 1.5-1.7 but that is the live filters doing the work, and the sleeve is overlapping with LIVE (combined PF falls 2.83 -> 2.0, 2025 and 2023 worse). Nothing added to challenger.py. Live files untouched.
Next run: own idea.

## 2026-11-23 (run 70) - steady-uptrend SIZE tilt (60d up-day share > 0.55; rs60 vs SPY > 0) as extra flag on the run-59 clipped stack (own idea; follow-up of run 68; no web this run, run 69 was web). Script: lab_uptilt.py
Rules: live vol60>=1.75% setup before zreg (308 trades, 10% x 12, 4/day). Flags: up-share>0.55, rs60>0. Multiplier 1.25x/0.75x per flag, product clipped to 0.5-1.5x, normalised to mean 1 (PF is size-weighted). 6 variants + 3x2 split-sample + 2000-shuffle placebo. Data through 2026-10-29 cache.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.88 | 61.7 | 4.3 | 3.39 | 2.41/.87/1.72/4.70/2.51/3.44 |
| run-59 stack (3 flags) | 308 | 74.4 | 3.79 | 80.8 | 2.8 | 4.13 | 3.79/1.45/2.86/5.63/3.05/3.98 |
| up-share tilt alone | 308 | 74.4 | 3.13 | 68.0 | 3.9 | 3.66 | 2.61/.95/1.76/4.85/2.87/3.63 |
| rs60 tilt alone | 308 | 74.4 | 2.85 | 62.4 | 4.5 | 3.42 | ~live |
| 3 flags + up-share | 308 | 74.4 | 3.98 | 85.7 | 2.7 | 4.33 | 4.09/1.58/2.99/5.90/2.92/4.29 |
| 3 flags + rs60 | 308 | 74.4 | 3.71 | 78.5 | 2.9 | 4.12 | 3.62/1.45/2.74/5.37/3.20/3.90 |
| 3 flags + up + rs60 | 308 | 74.4 | 3.84 | 82.2 | 2.8 | 4.24 | 3.75/1.52/2.86/5.59/3.07/4.12 |
Split: <=2023 up-share alone PF 2.07 vs live 1.96 (stack+up 3.41 vs stack 3.19); >=2024 3.77 vs 3.48 (stack+up 4.24 vs 4.08). Placebo (shuffled up-share multipliers): median 2.85, p95 3.00, p99 3.07; real 3.09 - only just above p99, from one of ~6 variants.
Findings: rs60 adds nothing. Up-share tilt gives a small, same-direction gain in both halves (+0.1-0.25 PF), but 2025 is slightly worse inside the stack (3.05 -> 2.92) and the stack's gain over the run-59 reference is only +5%, within noise given the variants tried and that the three run-59 flags are themselves unproven forward. 2026 not sealed.
Verdict: no promotion, nothing added to challenger.py. Possible forward-data re-check only. Live files untouched.
Next run: web (find stock-level rules with a fetchable page; avoid more conditioners on the live setup - this family is saturated).

## 2026-11-23 (run 71) - residual (beta-adjusted) 12-1m momentum and low-volatility / low-beta monthly sleeves (web idea). Script: lab_resmom.py
Sources: https://quantpedia.com/strategies/residual-momentum-factor , https://quantpedia.com/strategies/low-volatility-factor-effect-in-stocks (search hits only, pages not fetched; published results are other eras/markets, treated as unverified).
Rules: monthly (first trading day), hold 21 bars, buy top-N of cached universe at close, 0.05% slip; SPY>200d gate where stated. resmom = sum of 12-1m residual returns (252d regression on SPY) / residual stdev; lowvol = lowest 60d return stdev; lowbeta = lowest 60d beta. Simulator 10% x 12; LIVE ref = vol60>=1.75% live setup (308 trades). 6 variants tried, each standalone and combined; discount any winner.
| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 PF | PF 2021/22/23/24/25/26 | corr vs LIVE |
|---|---|---|---|---|---|---|---|---|
| LIVE ref | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 3.37 | 2.41/.87/1.62/4.74/2.51/3.41 | - |
| resmom top10 gate | 190 | 47.4 | 1.15 | 10.4 | 22.3 | 1.75 | .25/.05/1.38/1.23/2.51/2.09 | 0.03 |
| rawmom 12-1 top10 gate (control) | 182 | 49.5 | 1.64 | 69.9 | 21.0 | 2.72 | 1.01/.10/1.03/3.02/1.19/3.18 | 0.27 |
| lowvol60 top10 gate | 192 | 49.0 | 1.18 | 6.4 | 4.5 | 1.04 | 1.36/.96/1.27/.79/1.86/1.13 | -0.10 |
| lowvol60 top20 no gate | 244 | 52.9 | 1.19 | 11.0 | 7.9 | 0.97 | 1.36/.98/.91/2.46/1.02/1.08 | 0.10 |
| lowbeta60 top10 gate | 185 | 45.9 | 0.98 | -1.7 | 10.2 | 1.03 | 1.97/.43/.68/.92/1.27/1.10 | -0.03 |
| LIVE + resmom top10 | 444 | 62.8 | 1.51 | 60.8 | 18.6 | 2.21 | .82/.05/1.46/1.8/2.4/2.43 | |
| LIVE + rawmom top10 | 434 | 64.1 | 1.82 | 129.0 | 15.4 | 2.79 | 1.39/.11/1.19/3.25/1.41/3.0 | |
| LIVE + lowvol60 top10 gate | 474 | 65.4 | 1.93 | 70.7 | 5.4 | 2.44 | 1.7/1.17/1.42/2.08/2.15/2.53 | |
Findings: residual momentum is worse than plain momentum here (PF 1.15 vs 1.64, 2021-22 near zero) - the Blitz improvement does not appear on this small survivor universe. Low-vol/low-beta sleeves are near-zero-correlated with LIVE and keep max DD ~5%, but their standalone PF is 1.0-1.2 and L12 ~1.0, so combining only dilutes LIVE (PF 2.83 -> 1.93) for +10 points of return; the gain in 2022 (0.87 -> 1.17) comes from the sleeve being roughly flat that year, not an edge. Raw momentum adds return but with 15-21% drawdowns and a dead 2022.
Verdict: NOT a promotion candidate; nothing added to challenger.py. Live files untouched.
Next run: own idea; avoid more factor sleeves (momentum / low-vol are now tested in 5 forms). Untested: quarter-end/window-dressing calendar, Amihud illiquidity as selector.

## 2026-11-23 (run 72) - Amihud illiquidity conditioner on live vol60+zreg setup. Script: lab_amihud.py
LIVE n=238 PF 4.41 ret 63.6%. Liquid third PF 6.13 (ret 27.2), middle 3.74 (16.4), illiquid 2.51 (11.9; 2025 PF 0.48). Skip-illiquid: PF 5.01, ret 47.4%, DD 0.8, L12 PF 5.57 vs 5.03; early PF 4.10 vs 2.99, late 5.36 vs 5.25 (2024 weaker 9.2 vs 11.7). 4 variants tried, discount applies. Verdict: fails total-return bar; not a candidate; nothing added to challenger.py. Live files untouched.
Next run: quarter-end/window-dressing calendar, or earnings-proximity proxy.
