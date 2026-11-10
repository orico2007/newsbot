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
