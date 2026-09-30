# 誰在被迫交易：從第一性原理看選擇權避險與 GEX

產生方式：`python options-gex/make_figs.py`（需要 matplotlib、scipy）。定價用利率 0 的 Black-Scholes，年化波動 20%，現價與履約價 20,000 附近，全部是示意值。

| 檔名 | 圖號 | 放在 | 畫的是 |
|---|---|---|---|
| `fig01_payoff.png` | 圖 1 | §1.1 | 到期時 call 的價值：在 K 折彎的折線 |
| `fig02_value_curves.png` | 圖 2 | §1.2 | 剩 30／7／1 天的價值曲線疊在到期折線上；標出內含價值與時間價值 |
| `fig03_time_value.png` | 圖 3 | §1.2 | 時間價值對現價：K 處最大、往兩邊變小；剩 30／7／1 天 |
| `fig04_outcomes.png` | 圖 4 | §1.4 | 1,000 個世界的結局直方圖（現價 19,900、K＝20,000，剩 30 天／1 天）：藍＝已在 K 之上（Delta），橘＝19,900–20,000 那格（漲 100 點就跨過 K，高度＝Gamma） |
| `fig05_short_put.png` | 圖 5 | §1.4 | 賣出 put（K＝20,000、剩 30 天、權利金 508 點）三格：損益、Delta（賣方與 put 本身，正負號相反）、Gamma（賣方負、買方正） |
| `fig06_delta_speed.png` | 圖 6 | §1.4 | Delta＝速度、Gamma＝加速度：左圖賣 put／賣 call 兩條 Delta 線都往下走（負 Gamma），右圖買方兩條都往上走（正 Gamma） |
| `fig07_gamma_by_strike.png` | 圖 7 | §1.4 | 每個履約價的 Gamma：左圖看到期時間，右圖看波動率 |
| `fig08_triangle.png` | 圖 8 | §3.4 | 負 Gamma 避險虧損＝三角形面積（½ × 200 點 × 500 元） |
| `fig09_gex_curve.png` | 圖 9 | §4 | 示意選擇權鏈（剩 7 天）→ GEX 曲線與 gamma flip（慣例假設：造市商買 call、賣 put） |
| `fig10_institutional.png` | 圖 10 | §5 | 真實資料：臺指選擇權三大法人淨未平倉（2026/7–9/30） |
| `fig11_charm_vanna.png` | 圖 11 | §6 | 賣出 1,000 口 19,500 put、指數不動：避險量隨時間（charm）與 IV（vanna）變小 |
| `fig12_real_gamma.png` | 圖 12 | §7 | 真實資料（2026/9/30 收盤）：每個履約價的 Gamma，以及慣例假設下 GEX 隨指數位置的變化 |

## 真實資料（`data/`）

來源為 FinMind 轉載的臺灣期貨交易所公開資料：`TaiwanOptionDaily`（TXO 各序列結算價與未平倉）、`TaiwanOptionInstitutionalInvestors`（三大法人買賣權分計）、`TaiwanFuturesDaily`。

- `txo_chain_20260930.csv`：9/30 收盤、未到期的 TXO 各序列；IV 由結算價以 Black-76（利率 0）反推，遠期價由價平附近的買賣權平價求得；`g1pct`＝該序列未平倉的 Gamma × 1% × 遠期價（單位：小台口數）
- `txo_gamma_by_strike_20260930.csv`：上表按履約價加總
- `txo_institutional_oi_2026Q3.csv`：三大法人 call／put 買方、賣方未平倉口數與淨額
