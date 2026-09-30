# 誰在被迫交易：從第一性原理看選擇權避險與 GEX

產生方式：`python options-gex/make_figs.py`（需要 matplotlib、scipy）。定價用利率 0 的 Black-Scholes，年化波動 20%，現價與履約價 20,000 附近，全部是示意值。

| 檔名 | 圖號 | 放在 | 畫的是 |
|---|---|---|---|
| `fig01_payoff.png` | 圖 1 | §1.1 | 到期時 call 的價值：在 K 折彎的折線 |
| `fig02_value_curves.png` | 圖 2 | §1.2 | 剩 30／7／1 天的價值曲線疊在到期折線上；標出內含價值與時間價值 |
| `fig03_outcomes.png` | 圖 3 | §1.4 | 結局分布：Delta＝K 右邊的面積，Gamma＝K 處的高度 |
| `fig04_gamma_by_strike.png` | 圖 4 | §1.4 | 每個履約價的 Gamma：左圖看到期時間，右圖看波動率 |
| `fig05_triangle.png` | 圖 5 | §3.4 | 負 Gamma 避險虧損＝三角形面積（½ × 200 點 × 500 元） |
