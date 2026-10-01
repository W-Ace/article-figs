"""選擇權/GEX 文章示意圖（第 1–3 節）。數字皆為示意，定價用 r=0 的 Black-Scholes。

執行：在有 matplotlib＋scipy 的環境下 `python options-gex/make_figs.py`（字型路徑為 macOS 的黑體-繁）。圖輸出在本檔同一資料夾。
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from scipy.stats import norm

OUT = Path(__file__).parent
font_manager.fontManager.addfont("/System/Library/Fonts/STHeiti Medium.ttc")
plt.rcParams.update({
    "font.family": "Heiti TC",
    "axes.unicode_minus": False,
    "font.size": 11,
    "axes.edgecolor": "#b5b4ae",
    "axes.labelcolor": "#52514e",
    "xtick.color": "#52514e",
    "ytick.color": "#52514e",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#ebeae6",
    "grid.linewidth": 0.8,
    "figure.facecolor": "#ffffff",
    "axes.facecolor": "#ffffff",
})
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRAY = "#0b0b0b", "#52514e", "#9a9993"
S0, K, VOL = 20_000, 20_000, 0.20


def bs_call(s, k, days, vol=VOL):
    t = days / 365
    d1 = (np.log(s / k) + 0.5 * vol**2 * t) / (vol * np.sqrt(t))
    return s * norm.cdf(d1) - k * norm.cdf(d1 - vol * np.sqrt(t))


def bs_gamma(s, k, days, vol=VOL):
    t = days / 365
    d1 = (np.log(s / k) + 0.5 * vol**2 * t) / (vol * np.sqrt(t))
    return norm.pdf(d1) / (s * vol * np.sqrt(t))


def thousands(ax, axis="x"):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}")
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(fmt)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)


# 圖1：到期報酬折線
s = np.linspace(19_000, 21_000, 401)
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(s, np.maximum(s - K, 0), color=BLUE, lw=2)
ax.axvline(K, color=GRAY, lw=1, ls=":")
ax.text(K + 20, 850, "K＝20,000", color=INK2)
ax.text(19_150, 60, "S 低於 K：值 0", color=INK2)
ax.text(20_420, 250, "S 高於 K：值 S − K\n（斜率 1）", color=INK2)
ax.set_xlabel("到期結算價 S")
ax.set_ylabel("call 價值（點）")
ax.set_title("圖 1　到期那一刻：call 的價值是一條在 K 折彎的線", loc="left", color=INK)
thousands(ax)
save(fig, "fig01_payoff.png")

# 圖2：到期前被平均成曲線
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(s, np.maximum(s - K, 0), color=GRAY, lw=1.5, ls="--")
ax.annotate("虛線：到期那一刻\n的價值（圖 1 的折線）", xy=(20_150, 150), xytext=(20_540, 30),
            color=GRAY, fontsize=10, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))
ax.axvline(K, color=GRAY, lw=1, ls=":")
ax.text(K - 30, 870, "K＝20,000\n（履約價，四條線都一樣）", color=INK2, ha="right")
for days, c in [(30, BLUE), (7, ORANGE), (1, AQUA)]:
    ax.plot(s, bs_call(s, K, days), color=c, lw=2)
# 直接標籤：讀出現價 20,000 時各條線的價值
for days, c, ty in [(30, BLUE, 560), (7, ORANGE, 300), (1, AQUA, 120)]:
    v = bs_call(np.array([K]), K, days)[0]
    ax.plot([K], [v], "o", color=c, ms=6, mec="#ffffff", mew=1.5, zorder=5)
    ax.annotate(f"剩 {days} 天：值 {v:.0f} 點", xy=(K, v), xytext=(19_080, ty),
                color=c, arrowprops=dict(arrowstyle="-", color=c, lw=0.8))
# 現價 20,500、剩 30 天：拆成內含價值＋時間價值
xb = 20_500
vb = bs_call(np.array([xb]), K, 30)[0]
for y0, y1, c in [(0, xb - K, GRAY), (xb - K, vb, BLUE)]:
    ax.annotate("", xy=(xb, y0), xytext=(xb, y1),
                arrowprops=dict(arrowstyle="<->", color=c, lw=1.2, shrinkA=0, shrinkB=0))
ax.text(xb + 25, (xb - K) / 2 - 40, f"內含價值\n{xb - K:,} 點", color=INK2)
ax.text(xb - 25, (xb - K + vb) / 2 + 60, f"時間價值\n{vb - (xb - K):.0f} 點", color=BLUE, ha="right")
ax.set_xlabel("現價（今天的指數）")
ax.set_ylabel("call 價值（點）")
ax.set_title("圖 2　同一張 call 在到期前：離到期越遠，折線被平均得越平滑", loc="left", color=INK)
ax.set_xlim(19_000, 21_000)
ax.set_ylim(-20, 1_000)
thousands(ax)
save(fig, "fig02_value_curves.png")

# 圖3：時間價值對現價（同一張 K＝20,000 的 call，剩 30／7／1 天）
fig, ax = plt.subplots(figsize=(7, 3.8))
for days, c, lx, tx, ty in [(30, BLUE, 20_700, 20_780, 330), (7, ORANGE, 20_250, 20_420, 200), (1, AQUA, 20_060, 20_180, 95)]:
    tv = bs_call(s, K, days) - np.maximum(s - K, 0)
    ax.plot(s, tv, color=c, lw=2)
    ly = bs_call(np.array([lx]), K, days)[0] - max(lx - K, 0)
    ax.annotate(f"剩 {days} 天", xy=(lx, ly), xytext=(tx, ty), color=c,
                arrowprops=dict(arrowstyle="-", color=c, lw=0.8))
ax.axvline(K, color=GRAY, lw=1, ls=":")
ax.text(K - 30, 480, "K＝20,000", color=INK2, ha="right")
ax.set_xlabel("現價（今天的指數）")
ax.set_ylabel("時間價值（點）")
ax.set_title("圖 3　時間價值在 K 最大，往兩邊變小；越接近到期越集中在 K", loc="left", color=INK)
ax.set_xlim(19_000, 21_000)
ax.set_ylim(0, 500)
thousands(ax)
save(fig, "fig03_time_value.png")

# 圖4：1,000 個世界的結局（現價 19,900、K＝20,000）；指數漲 100 點時哪些世界跨過 K
s_now, k4, n_worlds, w = 19_900, 20_000, 1_000, 100
edges = np.arange(16_800, 23_000 + w, w)


def p_below(x, days):  # 結算價低於 x 的機率（現價 s_now，r=0 對數常態）
    sd = VOL * np.sqrt(days / 365)
    return norm.cdf((np.log(x / s_now) + 0.5 * sd**2) / sd)


fig, axes = plt.subplots(2, 1, figsize=(8, 6.2), sharex=True, sharey=True)
for ax, days in zip(axes, (30, 1)):
    counts = n_worlds * np.diff(p_below(edges, days))
    colors = [ORANGE if lo == s_now else BLUE if lo >= k4 else "#c9c8c2" for lo in edges[:-1]]
    ax.bar(edges[:-1], counts, width=w * 0.9, align="edge", color=colors, lw=0)
    above = n_worlds * (1 - p_below(k4, days))
    band = n_worlds * (p_below(k4, days) - p_below(s_now, days))
    ax.axvline(k4, color=INK2, lw=1, ls=":")
    ax.text(0.01, 0.93, f"剩 {days} 天", transform=ax.transAxes, color=INK, fontsize=13, va="top")
    tx, ha = 0.99, "right"
    ax.text(tx, 0.93 if days == 30 else 0.78,
            f"藍色：已在 K 之上的世界 {above:.0f} 個 → Delta {above / 10:.1f}%\n"
            f"橘色：落在 19,900–20,000 的世界 {band:.0f} 個\n"
            f"指數漲 100 點，橘色全部跨過 K：\n"
            f"{above:.0f} ＋ {band:.0f} ＝ {above + band:.0f} 個 → Delta {(above + band) / 10:.1f}%",
            transform=ax.transAxes, ha=ha, va="top", color=INK2, linespacing=1.5, fontsize=10)
    ax.annotate(f"{band:.0f} 個", xy=(s_now + w * 0.45, band), xytext=(s_now - 900, band + 25),
                color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_ylabel("世界數（每 100 點一格）")
axes[0].text(k4 + 40, 80, "K＝20,000", color=INK2)
axes[0].text(s_now - 40, 80, "現價 19,900", color=INK2, ha="right")
axes[0].axvline(s_now, color=GRAY, lw=1, ls="--")
axes[1].axvline(s_now, color=GRAY, lw=1, ls="--")
axes[0].set_ylim(0, 200)
axes[1].set_xlabel("到期結算價")
axes[1].set_xlim(16_800, 23_000)
thousands(axes[1])
fig.suptitle("圖 4　1,000 個世界的結局：橘色那格越高，指數一動 Delta 就變越多（＝Gamma 越大）",
             x=0.01, ha="left", color=INK)
save(fig, "fig04_outcomes.png")

# 圖5：賣出 put 的損益（現價 19,900、K＝20,000、剩 30 天、權利金約 508 點；指數瞬間移動）
def bs_put(s_, k, days, vol=VOL):
    return bs_call(s_, k, days, vol) - s_ + k  # r=0 買賣權平價


s5, k5 = 19_900, 20_000
prem = bs_put(np.array([s5]), k5, 30)[0]
xs = np.linspace(18_000, 22_000, 801)
pnl = prem - bs_put(xs, k5, 30)
sd5 = VOL * np.sqrt(30 / 365)
p_below5 = lambda x: norm.cdf((np.log(k5 / x) + 0.5 * sd5**2) / sd5)  # 結局落在 K 之下的機率＝賣方 Delta
dlt = p_below5(xs) * 100                      # 賣方 Delta（%）
gam = np.gradient(dlt, xs) * 100              # 指數每漲 100 點，Delta 變幾個百分點
marks = (s5 - 1_000, s5, s5 + 1_000)
fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(7.2, 8.6), sharex=True,
                                 gridspec_kw={"height_ratios": [1.25, 1, 1]})
for ax in (a1, a2, a3):
    for xm in marks:
        ax.axvline(xm, color=GRAY, lw=0.9, ls=":")
    ax.axvline(k5, color=INK2, lw=0.8, ls="--")
# ① 損益
a1.axhline(0, color=INK2, lw=0.8)
a1.axhline(prem, color=GRAY, lw=1, ls="--")
a1.text(18_050, prem + 30, f"賺的上限＝收到的權利金 {prem:.0f} 點", color=INK2, fontsize=10)
a1.plot(xs, pnl, color=ORANGE, lw=2.2)
for xm in marks:
    ym = prem - bs_put(np.array([xm]), k5, 30)[0]
    a1.plot([xm], [ym], "o", color=ORANGE, ms=6, mec="#ffffff", mew=1.5, zorder=5)
    a1.text(xm + 60, ym - 150 if xm != s5 else ym - 170, f"{ym:+.0f} 點" if xm != s5 else "賣出時（指數 19,900）", color=INK, fontsize=10)
a1.text(20_050, -1_300, "K＝20,000", color=INK2, fontsize=9)
a1.set_ylim(-1_550, 700)
a1.set_ylabel("① 賣方損益（點）")
a1.set_title("① 損益：往上賺得越來越慢，往下賠得越來越快", loc="left", color=INK, fontsize=11)
# ② Delta：put 本身（買方）與賣方，正負號相反
a2.axhline(0, color=INK2, lw=0.8)
a2.plot(xs, -dlt, color=GRAY, lw=1.8, ls="--")
a2.plot(xs, dlt, color=BLUE, lw=2.2)
for xm in marks:
    ym = float(np.interp(xm, xs, dlt))
    a2.plot([xm], [ym], "o", color=BLUE, ms=6, mec="#ffffff", mew=1.5, zorder=5)
    a2.text(xm + 60, ym + 6, f"+{ym:.0f}%", color=BLUE, fontsize=10)
    a2.plot([xm], [-ym], "o", color=GRAY, ms=5, zorder=5)
    a2.text(xm + 60, -ym - 14, f"−{ym:.0f}%", color=GRAY, fontsize=10)
a2.text(21_950, 95, "賣方的 Delta（正的：他是多頭）", ha="right", va="top", color=BLUE, fontsize=10)
a2.text(21_950, -80, "put 本身（買方）的 Delta（負的）", ha="right", va="bottom", color=GRAY, fontsize=10)
a2.set_ylim(-105, 105)
a2.set_ylabel("② Delta（%）")
a2.set_title("② Delta＝速度：賣方剛好是 put 本身的相反數", loc="left", color=INK, fontsize=11)
# ③ Gamma：買方正、賣方負
a3.axhline(0, color=INK2, lw=0.8)
a3.plot(xs, -gam, color=GRAY, lw=1.8, ls="--")
a3.fill_between(xs, gam, 0, color=ORANGE, alpha=0.18, lw=0)
a3.plot(xs, gam, color=ORANGE, lw=2.2)
for xm in marks:
    ym = float(np.interp(xm, xs, gam))
    a3.plot([xm], [ym], "o", color=ORANGE, ms=6, mec="#ffffff", mew=1.5, zorder=5)
    a3.text(xm - 70 if xm < s5 else xm + 110, ym + (0.45 if xm > s5 else -0.6), f"{ym:.1f}", color=ORANGE, fontsize=10,
            ha="right" if xm < s5 else "left")
a3.text(21_950, 4.3, "買方的 Gamma（正的）", ha="right", va="top", color=GRAY, fontsize=10)
a3.text(21_950, -3.2, "賣方的 Gamma（負的）\n在 K 附近最負", ha="right", va="top", color=ORANGE, fontsize=10)
a3.text(18_060, 4.3, "Gamma＝加速度：指數每漲 100 點，\nDelta 變幾個百分點", va="top", color=INK2, fontsize=9.5)
a3.set_ylim(-4.8, 4.8)
a3.set_ylabel("③ Gamma")
a3.set_title("③ Gamma＝加速度：賣方一直是負的，買方一直是正的", loc="left", color=INK, fontsize=11)
a3.set_xlabel("指數（瞬間移動，時間沒有經過；虛線＝K，點線＝19,900 與上下 1,000 點）")
a3.set_xlim(18_000, 22_000)
thousands(a3)
fig.suptitle("圖 6　賣出 put（K＝20,000、剩 30 天）：損益、Delta、Gamma 放在同一條橫軸",
             x=0.01, ha="left", color=INK)
save(fig, "fig06_short_put.png")

# 圖9：賣出一口剩 30 天價平 call、做好 Delta 避險後，一天的損益＝Theta − ½ × Gamma × 漲跌²
T9 = 30 / 365
th9 = S0 * VOL * norm.pdf(0.5 * VOL * np.sqrt(T9)) / (2 * np.sqrt(T9)) / 365   # 每天的 Theta（點）
g9 = bs_gamma(S0, S0, 30)                                                       # 每點的 Gamma
be = np.sqrt(2 * th9 / g9)
mv = np.linspace(-500, 500, 401)
pl9 = th9 - 0.5 * g9 * mv**2
fig, ax = plt.subplots(figsize=(7, 3.9))
ax.axhline(0, color=INK2, lw=0.8)
ax.fill_between(mv, pl9, 0, where=pl9 >= 0, color=BLUE, alpha=0.18, lw=0)
ax.fill_between(mv, pl9, 0, where=pl9 < 0, color=ORANGE, alpha=0.18, lw=0)
ax.plot(mv, pl9, color=INK, lw=2.2)
for x in (-be, be):
    ax.axvline(x, color=GRAY, lw=1, ls=":")
    ax.plot([x], [0], "o", color=INK, ms=6, zorder=5)
ax.text(be + 15, 2.5, f"±{be:.0f} 點：損益兩平\n≈ 剩 1 天的散開範圍（第 1.2 節）", color=INK, fontsize=10)
ax.text(0, th9 + 1.2, f"指數沒動：賺一天的 Theta 約 {th9:.1f} 點", ha="center", color=BLUE, fontsize=10)
ax.text(-480, -9, "動得比預期大：\n避險虧損超過 Theta", color=ORANGE, fontsize=10)
ax.set_ylim(-17, 11)
ax.set_xlabel("當天指數漲跌（點）")
ax.set_ylabel("賣方當天損益（點／口）")
ax.set_title("圖 9　賣方一天的帳：Theta 收入 − ½ × Gamma × 漲跌²", loc="left", color=INK)
save(fig, "fig09_breakeven.png")
print("breakeven", round(th9, 2), g9, round(be, 1))

# 圖6：Delta＝速度、Gamma＝加速度；賣方／買方四條 Delta 線（K＝20,000、剩 30 天）
k6, days6 = 20_000, 30
sd6 = VOL * np.sqrt(days6 / 365)
xs6 = np.linspace(18_000, 22_000, 801)
p_above6 = lambda x: 1 - norm.cdf((np.log(k6 / x) + 0.5 * sd6**2) / sd6)  # 結局落在 K 之上的機率

fig, axes = plt.subplots(1, 2, figsize=(10, 6.0), sharey=True)
panels = [
    (axes[0], "賣方：指數越高，Delta 越小\n線往右下斜 → 負 Gamma", "down",
     [("賣 put", 1 - p_above6(xs6), BLUE, (18_150, 78)), ("賣 call", -p_above6(xs6), ORANGE, (18_150, -26))]),
    (axes[1], "買方：指數越高，Delta 越大\n線往右上斜 → 正 Gamma", "up",
     [("買 call", p_above6(xs6), BLUE, (18_150, 16)), ("買 put", p_above6(xs6) - 1, ORANGE, (18_150, -84))]),
]
for ax, title, way, lines in panels:
    ax.axhspan(0, 105, color="#eef4fb", zorder=0)
    ax.axhspan(-105, 0, color="#fdf0ea", zorder=0)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.axvline(k6, color=GRAY, lw=1, ls=":")
    moves = []
    for name, y, c, (lx, ly) in lines:
        ax.plot(xs6, y * 100, color=c, lw=2.2)
        vals = []
        for x0 in (19_900, 20_900):
            y0 = np.interp(x0, xs6, y) * 100
            vals.append(y0)
            ax.plot([x0], [y0], "o", color=c, ms=6, mec="#ffffff", mew=1.5, zorder=5)
            dx, ha = (70, "left") if way == "down" else (-70, "right")
            ax.text(x0 + dx, y0 + 5, f"{y0:+.0f}%", color=c, fontsize=10, ha=ha)
        ax.text(lx, ly, name, color=c, fontsize=12)
        moves.append(f"{name}：{vals[0]:+.0f}% → {vals[1]:+.0f}%（{vals[1] - vals[0]:+.0f}）")
    word = "往下掉" if way == "down" else "往上升"
    ax.text(0, -0.40, "指數 19,900 → 20,900：\n" + "；".join(moves) + f"\n→ 兩條線{word}一樣多",
            transform=ax.transAxes, color=INK, fontsize=10, va="top", linespacing=1.6)
    ax.set_title(title, loc="left", color=INK)
    ax.set_xlabel("指數（K＝20,000，剩 30 天）\n← 低於 K：put 價內、call 價外　｜　高於 K：put 價外、call 價內 →", fontsize=10)
    ax.set_xlim(18_000, 22_000)
    ax.set_xticks(range(18_000, 22_001, 1_000))
    ax.set_ylim(-105, 105)
    thousands(ax)
axes[0].set_ylabel("Delta＝速度（每漲 1 點賺賠幾點，%）")
fig.suptitle("圖 7　Delta＝線的高度（速度），Gamma＝線的斜率（加速度）",
             x=0.01, ha="left", color=INK)
fig.text(0.01, 0.915, "藍底：Delta 為正（多頭，漲會賺）　橘底：Delta 為負（空頭，漲會賠）　正負號看高度，Gamma 看斜率", color=INK2, fontsize=10)
for ax, name, y, lab, ty in ((axes[0], "賣 put", 1 - p_above6(xs6), "斜率＝Gamma\n往下斜＝負", 62), (axes[1], "買 call", p_above6(xs6), "斜率＝Gamma\n往上斜＝正", 40)):
    y0, y1 = np.interp(19_900, xs6, y) * 100, np.interp(20_900, xs6, y) * 100
    ax.annotate("", xy=(20_900, y1), xytext=(19_900, y0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6, shrinkA=6, shrinkB=6))
    ax.text(21_050, ty, lab, color=INK, fontsize=10, va="center")
fig.tight_layout(rect=(0, 0.02, 1, 0.92))
fig.savefig(OUT / "fig07_delta_speed.png", dpi=200, bbox_inches="tight", pad_inches=0.15)
plt.close(fig)

# 圖4：Gamma 對履約價（左：到期時間；右：波動率）
ks = np.linspace(18_500, 21_500, 601)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.8), sharey=False)
for days, c in [(30, BLUE), (7, ORANGE), (1, AQUA)]:
    g = bs_gamma(S0, ks, days) * 10_000
    a1.plot(ks, g, color=c, lw=2)
    lx, tx, ty = {30: (21_200, 20_950, 4.2), 7: (20_300, 20_750, 8.5), 1: (20_080, 20_300, 18)}[days]
    a1.annotate(f"剩 {days} 天", xy=(lx, bs_gamma(S0, lx, days) * 10_000), xytext=(tx, ty), color=c,
                arrowprops=dict(arrowstyle="-", color=c, lw=0.8))
a1.set_title("性質 2：越接近到期，越尖", loc="left", color=INK)
for vol, c in [(0.15, BLUE), (0.30, ORANGE)]:
    g = bs_gamma(S0, ks, 7, vol) * 10_000
    a2.plot(ks, g, color=c, lw=2)
    lx, tx, ty = {0.15: (20_250, 20_500, 9), 0.30: (21_000, 20_900, 5)}[vol]
    a2.annotate(f"波動 {vol:.0%}", xy=(lx, bs_gamma(S0, lx, 7, vol) * 10_000), xytext=(tx, ty), color=c,
                arrowprops=dict(arrowstyle="-", color=c, lw=0.8))
a2.set_title("性質 3：波動越高，越平（剩 7 天）", loc="left", color=INK)
for a in (a1, a2):
    a.axvline(S0, color=GRAY, lw=1, ls=":")
    a.set_xlabel("履約價（現價固定在 20,000，換不同履約價）")
    thousands(a)
a1.set_ylabel("Gamma（每 100 點，Delta 變幾個百分點）")
fig.suptitle("圖 5　每個履約價的 Gamma：以現價為中心的一個鼓包", x=0.01, ha="left", color=INK)
save(fig, "fig05_gamma_by_strike.png")

# 圖5：負 Gamma 避險虧損＝三角形面積
fig, ax = plt.subplots(figsize=(7, 3.6))
px = np.array([20_000, 20_200])
ex = np.array([0, 500])
ax.fill_between(px, ex, color=ORANGE, alpha=0.3, lw=0)
ax.plot(px, ex, color=ORANGE, lw=2)
ax.text(20_120, 130, "面積＝½ × 200 點 × 500 元\n＝5 萬元", color=INK, ha="center")
ax.annotate("漲到 20,200 時：\n每點虧 500 元", xy=(20_200, 500), xytext=(20_035, 440),
            color=INK2, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.set_xlim(19_990, 20_230)
ax.set_ylim(0, 560)
ax.set_xlabel("指數")
ax.set_ylabel("淨空頭曝險（元／點）")
ax.set_title("圖 8　還沒調整避險前，曝險從 0 長到 500 元／點：虧損是三角形面積", loc="left", color=INK)
thousands(ax)
save(fig, "fig08_triangle.png")
print("done")

# ── 第 4 節以後 ──────────────────────────────────────────────
import pandas as pd

DATA = OUT / "data"


def put_delta(S, K, days, vol=VOL):
    T = days / 365
    return norm.cdf((np.log(S / K) + 0.5 * vol**2 * T) / (vol * np.sqrt(T))) - 1


# 圖9：示意選擇權鏈 → GEX 曲線（剩 7 天、IV 20%；慣例假設：造市商買進 call、賣出 put）
chain = {19_400: (0, 4_000), 19_600: (0, 6_000), 19_800: (500, 5_000), 20_000: (3_000, 3_000),
         20_200: (5_000, 500), 20_400: (6_000, 0), 20_600: (4_000, 0)}


def gex_at(S, days=7):
    return sum((c - p) * bs_gamma(S, K, days) * 0.01 * S for K, (c, p) in chain.items())


fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 6.4), sharex=True, gridspec_kw={"height_ratios": [1, 1.3]})
ks = np.array(list(chain))
a1.bar(ks, [chain[k][0] for k in ks], width=140, color=BLUE)
a1.bar(ks, [-chain[k][1] for k in ks], width=140, color=ORANGE)
a1.axhline(0, color=INK2, lw=0.8)
from matplotlib.patches import Patch
a1.legend(handles=[Patch(color=BLUE, label="call：造市商淨買進（＋Gamma）"),
                   Patch(color=ORANGE, label="put：造市商淨賣出（－Gamma）")],
          loc="upper left", frameon=False, fontsize=10)
a1.set_ylabel("造市商淨部位（假設，口）")
a1.set_ylim(-6_800, 9_000)
a1.set_title("假設的選擇權鏈（剩 7 天）", loc="left", color=INK, fontsize=11)
xs9 = np.arange(19_000, 21_001, 20)
gv = np.array([gex_at(x) for x in xs9])
a2.axhspan(0, 2_000, color="#eef4fb", zorder=0)
a2.axhspan(-2_000, 0, color="#fdf0ea", zorder=0)
a2.plot(xs9, gv, color=INK, lw=2.2)
a2.axhline(0, color=INK2, lw=0.8)
a2.axvline(20_000, color=GRAY, lw=1, ls=":")
a2.annotate("gamma flip：GEX 由負轉正\n（約 20,000）", xy=(20_000, 0), xytext=(19_020, 700), color=INK,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
a2.text(20_980, 650, "GEX 為正：漲了賣、跌了買\n（避險單逆著價格，壓抑波動）", ha="right", va="top", color=BLUE, fontsize=10)
a2.text(19_020, -150, "GEX 為負：漲了買、跌了賣\n（避險單順著價格，放大波動）", va="top", color=ORANGE, fontsize=10)
a2.set_ylim(-1_700, 1_800)
a2.set_ylabel("GEX（每 1% 要買賣的小台口數）")
a2.set_xlabel("假想指數移到這個位置（未平倉、IV、剩餘天數都不變）")
thousands(a2)
fig.suptitle("圖 10　把每個履約價的 Gamma 加起來：指數在哪裡，造市商的避險單就往哪個方向推", x=0.01, ha="left", color=INK)
save(fig, "fig10_gex_curve.png")

# 圖10：三大法人選擇權淨未平倉（真實資料，2026-07～09）
io = pd.read_csv(DATA / "txo_institutional_oi_2026Q3.csv", parse_dates=["date"])
fig, axes = plt.subplots(1, 2, figsize=(10, 3.9), sharey=True)
for ax, cp in zip(axes, ("買權", "賣權")):
    ends = []
    for who, c in (("自營商", BLUE), ("外資", ORANGE), ("投信", AQUA), ("三大法人合計", GRAY)):
        if who == "三大法人合計":
            s = io[io.call_put == cp].groupby("date").net.sum()
            ax.plot(s.index, s.values, color=c, lw=1.4, ls="--")
        else:
            s = io[(io.call_put == cp) & (io.institutional_investors == who)].set_index("date").net
            ax.plot(s.index, s.values, color=c, lw=1.8)
        ends.append([float(s.values[-1]), who, c, s.index[-1]])
    ends.sort(key=lambda e: e[0])
    for i in range(1, len(ends)):  # 標籤太近就往上推
        if ends[i][0] - ends[i - 1][0] < 1_700:
            ends[i][0] = ends[i - 1][0] + 1_700
    for y, who, c, x in ends:
        ax.text(x, y, f" {who}", color=c, fontsize=9.5, va="center")
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_title(f"{'call' if cp == '買權' else 'put'}：淨未平倉（買方 − 賣方，口）", loc="left", color=INK, fontsize=11)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m/%d"))
    thousands(ax, "y")
fig.text(0.01, 0.885, "0 以上＝淨買進、0 以下＝淨賣出（口數，不等於 Gamma，見第 5.3 節）", color=INK2, fontsize=9.5)
fig.suptitle("圖 11　臺指選擇權三大法人淨部位（2026/7–9/30）：自營商大多是淨買進，不是淨賣出", x=0.01, ha="left", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.9))
fig.subplots_adjust(right=0.88)
fig.savefig(OUT / "fig11_institutional.png", dpi=200)
plt.close(fig)

# 圖11：價格不動，避險量也會變（charm：時間；vanna：IV）
dd = np.linspace(30, 0.2, 300)
fig, ax = plt.subplots(figsize=(7, 3.9))
for v, c, lab in ((0.25, ORANGE, "IV 25%"), (0.20, BLUE, "IV 20%"), (0.15, AQUA, "IV 15%")):
    y = -1000 * np.array([put_delta(20_000, 19_500, d, v) for d in dd])
    ax.plot(dd, y, color=c, lw=2)
    ax.text(12, np.interp(12, dd[::-1], y[::-1]) + 8, lab, color=c, fontsize=10)
for d in (30, 7, 1):
    y = -1000 * put_delta(20_000, 19_500, d)
    ax.plot([d], [y], "o", color=BLUE, ms=6, mec="#ffffff", mew=1.5, zorder=5)
    ax.text(d - 0.4, y - 32 if d == 30 else y + 14, f"剩 {d} 天：{y:.0f} 口", color=BLUE, fontsize=10)
ax.invert_xaxis()
ax.set_xlabel("剩餘天數（指數一直停在 20,000）")
ax.set_ylabel("造市商需要放空的小台（口）")
ax.set_title("圖 12　賣出 1,000 口 19,500 put：價格沒動，避險量也會自己變小", loc="left", color=INK)
ax.set_ylim(0, 420)
save(fig, "fig12_charm_vanna.png")

# 圖12：真實 9/30 收盤的 Gamma 分布與規模（真實資料）
gb = pd.read_csv(DATA / "txo_gamma_by_strike_20260930.csv")
gb = gb[(gb.strike >= 42_000) & (gb.strike <= 54_000)]
ch = pd.read_csv(DATA / "txo_chain_20260930.csv")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.0), gridspec_kw={"width_ratios": [1.5, 1]})
a1.bar(gb.strike, gb.call_gamma_1pct, width=80, color=BLUE)
a1.bar(gb.strike, -gb.put_gamma_1pct, width=80, color=ORANGE)
a1.axhline(0, color=INK2, lw=0.8)
a1.axvline(47_940, color=INK2, lw=1, ls="--")
a1.text(47_850, a1.get_ylim()[1] * 0.93, "加權指數 47,940", color=INK2, fontsize=10, ha="right")
a1.text(42_100, a1.get_ylim()[1] * 0.75, "call（記正）", color=BLUE, fontsize=10)
a1.text(42_100, a1.get_ylim()[0] * 0.8, "put（記負）", color=ORANGE, fontsize=10)
a1.set_xlabel("履約價")
a1.set_ylabel("每 1% 對應的小台口數")
a1.set_title("每個履約價的 Gamma（依美股慣例給正負號：call 記正、put 記負）", loc="left", color=INK, fontsize=10)
thousands(a1)
shifts = np.linspace(-0.06, 0.04, 41)
conv = []
for sh in shifts:
    F2 = ch.F * (1 + sh)
    T = ch["T"]
    d1_ = (np.log(F2 / ch.K) + 0.5 * ch.iv**2 * T) / (ch.iv * np.sqrt(T))
    g = norm.pdf(d1_) / (F2 * ch.iv * np.sqrt(T)) * 0.01 * F2 * ch.oi
    conv.append(g[ch.cp == "call"].sum() - g[ch.cp == "put"].sum())
a2.axhline(0, color=INK2, lw=0.8)
a2.plot(shifts * 100, conv, color=INK, lw=2)
a2.axvline(0, color=GRAY, lw=1, ls=":")
a2.set_xlabel("指數相對 9/30 收盤變動（%）")
a2.set_ylabel("慣例假設下的 GEX（小台口數）")
a2.set_title("若照美股慣例假設對手方", loc="left", color=INK, fontsize=11)
thousands(a2, "y")
fig.suptitle("圖 13　真實資料（2026/9/30 收盤）：全部 Gamma 合計每 1% 約 5,400 口小台，日盤期貨成交約 30 萬口",
             x=0.01, ha="left", color=INK)
fig.tight_layout()
fig.savefig(OUT / "fig13_real_gamma.png", dpi=200)
plt.close(fig)
print("done 9-12")
