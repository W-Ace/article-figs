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

# 圖3：結局分布，Delta＝K 右邊面積、Gamma＝K 處高度
days, k3 = 30, 20_500
sd = VOL * np.sqrt(days / 365)
x = np.linspace(16_000, 23_500, 1_501)
dens = norm.pdf(np.log(x / S0) + 0.5 * sd**2, scale=sd) / x  # 對數常態（r=0）
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(x, dens, color=INK2, lw=1.5)
right = x >= k3
ax.fill_between(x[right], dens[right], color=BLUE, alpha=0.25, lw=0)
strip = (x >= k3 - 100) & (x <= k3)
ax.fill_between(x[strip], dens[strip], color=ORANGE, alpha=0.85, lw=0)
ax.axvline(S0, color=GRAY, lw=1, ls=":")
ax.text(S0 - 60, dens.max() * 1.05, "現價 20,000", color=INK2, ha="right")
ax.set_ylim(0, dens.max() * 1.15)
p_above = 1 - norm.cdf(np.log(k3 / S0) + 0.5 * sd**2, scale=sd)
ax.annotate(f"藍色面積＝結局落在 K 之上的機率\n≈ call 的 Delta（這裡約 {p_above:.2f}）",
            xy=(21_300, dens[np.searchsorted(x, 21_300)] * 0.5), xytext=(21_700, dens.max() * 0.75),
            color=BLUE, arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
ax.annotate("橘色：K 下方 100 點內\n的結局，標的上移 100\n點就跨過 K。Gamma\n看的就是 K 這裡的高度",
            xy=(k3 - 50, dens[np.searchsorted(x, k3 - 50)] * 0.85), xytext=(16_050, dens.max() * 0.5),
            color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
ax.text(k3 + 30, dens.max() * 0.93, "K＝20,500", color=INK2)
ax.axvline(k3, color=GRAY, lw=1, ls=":")
ax.set_yticks([])
ax.set_xlabel("到期結算價（剩 30 天、年化波動 20%）")
ax.set_ylabel("可能性")
ax.set_title("圖 4　結局分布：Delta 是 K 右邊的面積，Gamma 是 K 處的高度", loc="left", color=INK)
thousands(ax)
save(fig, "fig04_outcomes.png")

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
ax.set_title("圖 6　還沒調整避險前，曝險從 0 長到 500 元／點：虧損是三角形面積", loc="left", color=INK)
thousands(ax)
save(fig, "fig06_triangle.png")
print("done")
