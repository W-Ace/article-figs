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
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.axhline(0, color=INK2, lw=0.8)
ax.axhline(prem, color=GRAY, lw=1, ls="--")
ax.text(18_050, prem + 25, f"賺的上限＝收到的權利金 {prem:.0f} 點", color=INK2)
ax.plot(xs, pnl, color=ORANGE, lw=2.2)
for xm in (s5 - 1_000, s5 + 1_000):
    ym = prem - bs_put(np.array([xm]), k5, 30)[0]
    ax.plot([xm], [ym], "o", color=ORANGE, ms=7, mec="#ffffff", mew=1.5, zorder=5)
    ax.annotate(f"{'往上' if xm > s5 else '往下'} 1,000 點：{ym:+.0f} 點", xy=(xm, ym),
                xytext=(xm + 80, ym + (-230 if xm > s5 else -60)),
                color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.plot([s5], [0], "o", color=INK, ms=6, zorder=5)
ax.annotate("賣出時：指數 19,900", xy=(s5, 0), xytext=(s5 + 120, -260), color=INK2,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.text(18_700, -1_420, "左邊越來越陡：\n越跌，多頭曝險越大，賠得越快", color=ORANGE)
ax.text(20_550, -520, "右邊越來越平：\n越漲，多頭曝險越小，賺得越慢", color=ORANGE)
ax.set_xlim(18_000, 22_000)
ax.set_ylim(-1_550, 700)
ax.set_xlabel("指數（瞬間移動，時間沒有經過）")
ax.set_ylabel("賣方損益（點）")
ax.set_title("圖 5　賣出 put 的損益：往上賺得越來越慢，往下賠得越來越快", loc="left", color=INK)
thousands(ax)
save(fig, "fig05_short_put.png")

# 圖6：Delta＝速度、Gamma＝加速度；賣方／買方四條 Delta 線（K＝20,000、剩 30 天）
k6, days6 = 20_000, 30
sd6 = VOL * np.sqrt(days6 / 365)
xs6 = np.linspace(18_000, 22_000, 801)
p_above6 = lambda x: 1 - norm.cdf((np.log(k6 / x) + 0.5 * sd6**2) / sd6)  # 結局落在 K 之上的機率

fig, axes = plt.subplots(1, 2, figsize=(10, 5.4), sharey=True)
panels = [
    (axes[0], "賣方：Delta 隨指數往下走 → 負 Gamma", "down",
     [("賣 put", 1 - p_above6(xs6), BLUE, (18_150, 78)), ("賣 call", -p_above6(xs6), ORANGE, (18_150, -26))]),
    (axes[1], "買方：Delta 隨指數往上走 → 正 Gamma", "up",
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
    ax.text(0, -0.25, "指數 19,900 → 20,900：\n" + "；".join(moves) + f"\n→ 兩條線{word}一樣多",
            transform=ax.transAxes, color=INK, fontsize=10, va="top", linespacing=1.6)
    ax.set_title(title, loc="left", color=INK)
    ax.set_xlabel("指數（K＝20,000，剩 30 天）")
    ax.set_xlim(18_000, 22_000)
    ax.set_xticks(range(18_000, 22_001, 1_000))
    ax.set_ylim(-105, 105)
    thousands(ax)
axes[0].set_ylabel("Delta＝速度（每漲 1 點賺賠幾點，%）")
fig.suptitle("圖 6　Delta 是速度、Gamma 是加速度：看線往上還是往下走，不是看在 0 的哪一邊",
             x=0.01, ha="left", color=INK)
fig.text(0.01, 0.915, "藍底：Delta 為正（多頭，漲會賺）　橘底：Delta 為負（空頭，漲會賠）", color=INK2, fontsize=10)
fig.tight_layout(rect=(0, 0.02, 1, 0.92))
fig.savefig(OUT / "fig06_delta_speed.png", dpi=200, bbox_inches="tight", pad_inches=0.15)
plt.close(fig)

# 圖4：Gamma 對履約價（左：到期時間；右：波動率）
ks = np.linspace(18_500, 21_500, 601)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.8), sharey=False)
for days, c in [(30, BLUE), (7, ORANGE), (1, AQUA)]:
    g = bs_gamma(S0, ks, days) * 1_000
    a1.plot(ks, g, color=c, lw=2)
    lx, tx, ty = {30: (21_200, 20_950, 0.42), 7: (20_300, 20_750, 0.85), 1: (20_080, 20_300, 1.8)}[days]
    a1.annotate(f"剩 {days} 天", xy=(lx, bs_gamma(S0, lx, days) * 1_000), xytext=(tx, ty), color=c,
                arrowprops=dict(arrowstyle="-", color=c, lw=0.8))
a1.set_title("性質 2：越接近到期，越尖", loc="left", color=INK)
for vol, c in [(0.15, BLUE), (0.30, ORANGE)]:
    g = bs_gamma(S0, ks, 7, vol) * 1_000
    a2.plot(ks, g, color=c, lw=2)
    lx, tx, ty = {0.15: (20_250, 20_500, 0.9), 0.30: (21_000, 20_900, 0.5)}[vol]
    a2.annotate(f"波動 {vol:.0%}", xy=(lx, bs_gamma(S0, lx, 7, vol) * 1_000), xytext=(tx, ty), color=c,
                arrowprops=dict(arrowstyle="-", color=c, lw=0.8))
a2.set_title("性質 3：波動越高，越平（剩 7 天）", loc="left", color=INK)
for a in (a1, a2):
    a.axvline(S0, color=GRAY, lw=1, ls=":")
    a.set_xlabel("履約價（現價 20,000）")
    thousands(a)
a1.set_ylabel("Gamma（每 1,000 點 Delta 變多少）")
fig.suptitle("圖 7　每個履約價的 Gamma：以現價為中心的一個鼓包", x=0.01, ha="left", color=INK)
save(fig, "fig07_gamma_by_strike.png")

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
