# 誰在被迫交易：從第一性原理看選擇權避險與 GEX

產生方式：`python options-gex/make_figs.py`（需要 matplotlib、scipy）。定價用利率 0 的 Black-Scholes，年化波動 20%，現價與履約價 20,000 附近，全部是示意值。

| 檔名 | 圖號 | 放在 | 畫的是 |
|---|---|---|---|
| `fig01_payoff.png` | 圖 1 | §1.1 | 到期時 call 的價值：在 K 折彎的折線 |
| `fig02_value_curves.png` | 圖 2 | §1.2 | 剩 30／7／1 天的價值曲線疊在到期折線上；標出內含價值與時間價值 |
| `fig03_time_value.png` | 圖 3 | §1.2 | 時間價值對現價：K 處最大、往兩邊變小 |
| `fig04_outcomes.png` | 圖 4 | §1.4 | 1,000 個世界的結局直方圖：藍＝已在 K 之上（Delta），橘＝漲 100 點就跨過 K 的那格（Gamma） |
| `fig05_gamma_by_strike.png` | 圖 5 | §1.4 | 每個履約價的 Gamma（每 100 點 Delta 變幾個百分點）：左看到期時間，右看波動率 |
| `fig06_short_put.png` | 圖 6 | §1.5 | 賣出 put 三格：損益、Delta（賣方與 put 本身）、Gamma（賣方與買方） |
| `fig07_delta_speed.png` | 圖 7 | §1.5 | Delta＝線的高度、Gamma＝線的斜率：四種部位 |
| `fig08_triangle.png` | 圖 8 | §3.4 | 負 Gamma 避險虧損＝三角形面積 |
| `fig09_breakeven.png` | 圖 9 | §3.4 | 賣方一天的帳：Theta − ½ × Gamma × 漲跌²，損益兩平 ±209 點 |
| `fig10_gex_curve.png` | 圖 10 | §4 | 示意選擇權鏈（剩 7 天）→ GEX 曲線與 gamma flip（慣例假設） |
| `fig11_institutional.png` | 圖 11 | §5 | 真實資料：三大法人淨未平倉與合計（2026/7–9/30） |
| `fig12_weekly_sellers.png` | 圖 12 | §5.4 | 真實資料（大額交易人結構表 2025/7–2026/9）：週選 call／put 前 5 大買賣方佔未平倉比例、其中特定法人佔比（月中位數） |
| `fig13_charm_vanna.png` | 圖 13 | §6 | 賣出 1,000 口 19,500 put、指數不動：避險量隨時間與 IV 變小 |
| `fig14_real_gamma.png` | 圖 14 | §7 | 真實資料（2026/9/30）：每個履約價的 Gamma（慣例正負號）與 GEX 隨指數位置的變化 |
| `fig15_gamma_iv_mirror.png` | 圖 15 | §9 | 真實資料（2025/7–2026/9，285 天）：Gamma 總量相對常態 vs IV 相對常態；扣掉相對 IV 前後 Gamma 對隔天振幅的偏相關 |

## 真實資料（`data/`）

來源為 FinMind 轉載的臺灣期貨交易所公開資料：`TaiwanOptionDaily`（TXO 各序列結算價與未平倉）、`TaiwanOptionInstitutionalInvestors`（三大法人買賣權分計）、`TaiwanFuturesDaily`、`TaiwanOptionOpenInterestLargeTraders`（大額交易人未沖銷部位結構表）。

- `txo_chain_20260930.csv`：9/30 收盤、未到期的 TXO 各序列；IV 由結算價以 Black-76（利率 0）反推，遠期價由價平附近的買賣權平價求得；`g1pct`＝該序列未平倉的 Gamma × 1% × 遠期價（單位：小台口數）
- `txo_gamma_by_strike_20260930.csv`：上表按履約價加總
- `txo_institutional_oi_2026Q3.csv`：三大法人 call／put 買方、賣方未平倉口數與淨額
- `txo_large_traders_weekly_2025_2026.csv`：`TaiwanOptionOpenInterestLargeTraders` 週契約列（2025-07～2026-09）：前 5／前 10 大買賣方佔未平倉 %、前 10 大中特定法人口數
- `txo_daily_gamma_iv_2025_2026.csv`：每日（2025-07-29～2026-09-29，285 天）全部 Gamma 與價平 IV 各自相對過去 20 日中位數的對數值（`g_rel`、`iv_month_rel`、`iv_near_rel`）、IV 水位、隔天臺指期日盤相對振幅（`logR`）與控制變數（過去 5／20 日報酬 `r5`／`r20`、近 5 日振幅水位 `rv`、隔天星期 `wd1`）
