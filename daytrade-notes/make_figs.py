"""當沖研究筆記（實戰手法精讀）的圖。

圖 1、2 用 2019/7/30 夜盤 10800 週選擇權的收盤價當例子；圖 3、4 用期交所公開行情（經 FinMind 取得，存在 data/）重算。
成交均價以「開高低收四價平均」近似（拿不到逐筆成交）。

執行：在有 matplotlib 的環境下 `python daytrade-notes/make_figs.py`（字型路徑為 macOS 的黑體-繁）。圖輸出在本檔同一資料夾。
"""
import csv
import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

OUT = Path(__file__).parent
DATA = OUT / "data"
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

# 2019/7/30 夜盤收盤（7/31 到期的週選擇權）
STRIKE, CALL_PX, PUT_PX = 10800, 16.5, 25.0


def thousands(ax, axis="x"):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}")
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(fmt)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)


def option_lines(csv_name):
    """每檔有成交的選擇權換成一條線：買權＝履約價＋均價、賣權＝履約價－均價；份量＝均價×口數÷1萬。"""
    rows = list(csv.DictReader(open(DATA / csv_name)))
    lines, legs = [], {}
    for r in rows:
        vol = int(r["volume"])
        if vol == 0:
            continue
        o, h, l, c = (float(r[k]) for k in ("open", "high", "low", "close"))
        avg = (o + h + l + c) / 4
        strike = int(r["strike"])
        is_call = r["call_put"] == "call"
        legs.setdefault(strike, {})[r["call_put"]] = (avg, vol, c)
        lines.append({"strike": strike, "call": is_call, "avg": avg, "vol": vol,
                      "pos": strike + avg if is_call else strike - avg, "w": avg * vol / 1e4})
    # 遠期價：兩腿都有量的履約價，用「履約價＋買權均價－賣權均價」取中位數（跟線用同一種價格）
    syn = [k + v["call"][0] - v["put"][0] for k, v in legs.items()
           if "call" in v and "put" in v and min(v["call"][1], v["put"][1]) > 1000]
    fwd = statistics.median(syn)
    # 收盤時的遠期價（換算期貨刻度時，要跟期貨收盤價同一時間比）
    fwd_close = statistics.median([k + v["call"][2] - v["put"][2] for k, v in legs.items()
                                   if "call" in v and "put" in v and min(v["call"][1], v["put"][1]) > 1000])
    atm = min(legs, key=lambda k: abs(k - fwd))  # 價平＝離遠期價最近的履約價
    for ln in lines:  # 價平與價外＝賣方押方向的部位；價內的線都擠在遠期價附近
        ln["otm"] = ln["strike"] >= atm if ln["call"] else ln["strike"] <= atm
    return lines, fwd, fwd_close


def center(lines):
    w = sum(ln["w"] for ln in lines)
    return sum(ln["pos"] * ln["w"] for ln in lines) / w


# 圖1：賣方的損益兩平點
x = np.linspace(10650, 10950, 601)
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), sharey=True)
for ax, is_call in zip(axes, (True, False)):
    px = CALL_PX if is_call else PUT_PX
    pay = px - (np.maximum(x - STRIKE, 0) if is_call else np.maximum(STRIKE - x, 0))
    be = STRIKE + px if is_call else STRIKE - px
    ax.axhline(0, color=INK2, lw=1)
    ax.plot(x, pay, color=ORANGE if is_call else BLUE, lw=2.4)
    ax.fill_between(x, pay, 0, where=pay > 0, color=AQUA, alpha=0.15)
    ax.fill_between(x, pay, 0, where=pay < 0, color=ORANGE, alpha=0.12)
    ax.axvline(be, color=GRAY, ls=":", lw=1.2)
    ax.plot([be], [0], "o", color=INK, ms=6)
    name = "賣出 10800 買權，先收 16.5 點" if is_call else "賣出 10800 賣權，先收 25 點"
    ax.set_title(name, fontsize=11, color=INK2)
    rule = "履約價＋買權價" if is_call else "履約價－賣權價"
    ax.annotate(f"損益兩平 {be:,.1f}\n＝{rule}", (be, 0),
                xytext=(be + (-14 if is_call else 14), -95), ha="right" if is_call else "left",
                fontsize=10, color=INK, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))
    ax.text(0.04 if is_call else 0.96, 0.9, "線的這一側：賣方有賺", transform=ax.transAxes,
            ha="left" if is_call else "right", fontsize=9.5, color=AQUA)
    ax.set_xlabel("到期指數")
    ax.set_ylim(-140, 50)
    ax.set_xticks([10700, 10800, 10900])
    thousands(ax)
axes[0].set_ylabel("賣方到期損益（點／口）")
fig.suptitle("圖 1　賣方的損益兩平點：他說的「莊家成本線」", x=0.02, ha="left", fontsize=14)
save(fig, "fig01_seller_breakeven.png")

# 圖2：買權＋賣賣權＝期貨多單；只買買權少了一塊
syn_px = STRIKE + CALL_PX - PUT_PX
x = np.linspace(10650, 10950, 601)
fut = x - syn_px
combo = (np.maximum(x - STRIKE, 0) - CALL_PX) + (PUT_PX - np.maximum(STRIKE - x, 0))
call_only = np.maximum(x - STRIKE, 0) - CALL_PX
fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.axhline(0, color=INK2, lw=1)
ax.plot(x, fut, color=INK, lw=5, alpha=0.18, label=f"期貨多單（{syn_px:,.1f} 買進）")
ax.plot(x, combo, color=BLUE, lw=2, ls="--", label="買 10800 買權＋賣 10800 賣權（先淨收 8.5 點）")
ax.plot(x, call_only, color=ORANGE, lw=2.2, label="只買 10800 買權（付 16.5 點）")
ax.fill_between(x, combo, call_only, where=x < STRIKE, color=ORANGE, alpha=0.10)
ax.annotate("跌的時候：只買買權最多賠 16.5\n少掉的這塊＝賣權那張保險", (10700, -40), xytext=(10655, 22),
            fontsize=9.5, color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
ax.annotate("漲的時候：每一格都比期貨少 25 點\n（沒賣賣權，就沒收到那 25 點）", (10900, 83.5), xytext=(10835, -95),
            fontsize=9.5, color=INK2, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))
ax.set_xlabel("到期指數")
ax.set_ylabel("到期損益（點／口）")
ax.set_ylim(-150, 165)
thousands(ax)
ax.legend(loc="upper left", fontsize=9, frameon=False)
ax.set_title("圖 2　買一口買權＋賣一口賣權＝一口期貨多單", loc="left", fontsize=14)
save(fig, "fig02_synthetic.png")

# 圖3：分界表怎麼來（2020/1/2 夜盤週選）
lines, fwd, _ = option_lines("txo_night_20200102_202001W2.csv")
lines = [ln for ln in lines if ln["w"] >= 2]
mid = center([ln for ln in lines if ln["otm"]])
fig, ax = plt.subplots(figsize=(7.2, 5.6))
for ln in lines:
    col = (ORANGE if ln["call"] else BLUE) if ln["otm"] else "#cfcdc6"
    ax.barh(ln["pos"], ln["w"], height=5, color=col)
    if ln["otm"] or ln["w"] >= 10:
        lab = f'{ln["strike"]:,} {"買權" if ln["call"] else "賣權"}  均價 {ln["avg"]:.1f}'
        ax.text(ln["w"] + 1, ln["pos"], lab, va="center", fontsize=8, color=INK2 if ln["otm"] else GRAY)
ax.axhline(mid, color=INK, ls="--", lw=1.2)
ax.text(108, mid + 5, f"中線（價平與價外線的加權平均）{mid:,.0f}", fontsize=9.5, color=INK, ha="right")
ax.axhline(fwd, color=AQUA, ls=":", lw=1.2)
ax.text(108, fwd - 13, f"遠期價（合成期貨）{fwd:,.0f}", fontsize=9, color=AQUA, ha="right")
ax.set_xlim(0, 110)
ax.set_xlabel("份量＝均價（點）× 成交口數 ÷ 1 萬")
ax.set_ylabel("線的位置（指數點位）")
thousands(ax, "y")
ax.text(0.99, 0.02, "橘＝買權（履約價＋均價）　藍＝賣權（履約價－均價）\n灰＝價內：線都擠在遠期價附近，看不出賣方成本（價平兩邊都算）",
        transform=ax.transAxes, ha="right", fontsize=8.5, color=INK2)
ax.set_title("圖 3　分界表怎麼來：每檔選擇權換成一條線（2020/1/2 夜盤週選）", loc="left", fontsize=13)
save(fig, "fig03_line_profile.png")

# 圖4：2019/7/31 台指期 8 月合約與重建的線（換成期貨刻度）
lines, fwd, fwd_close = option_lines("txo_night_20190730_201907W5.csv")
fut_close_night = 10718.0  # 8 月台指期 7/31 清晨 04:59 收盤
basis = fwd_close - fut_close_night  # 週選合成價與 8 月期貨同一時間的差
otm = [ln for ln in lines if ln["otm"] and ln["w"] >= 3]
mid = center(otm) - basis
bars = list(csv.DictReader(open(DATA / "tx_201908_1min_20190731_day.csv")))
t = np.arange(len(bars))
close = np.array([float(b["close"]) for b in bars])
hi = np.array([float(b["high"]) for b in bars])
lo = np.array([float(b["low"]) for b in bars])
fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.fill_between(t, lo, hi, color=GRAY, alpha=0.25, lw=0)
ax.plot(t, close, color=INK, lw=1.1)
for ln in otm:
    y = ln["pos"] - basis
    col = ORANGE if ln["call"] else BLUE
    ax.axhline(y, color=col, lw=0.6 + ln["w"] / 25, alpha=0.8)
    ax.text(len(t) + 3, y, f'{y:,.0f}（{ln["strike"]:,}{"買權" if ln["call"] else "賣權"}，份量 {ln["w"]:.0f}）',
            va="center", fontsize=8.5, color=col)
ax.axhline(mid, color=INK, ls="--", lw=1)
ax.text(len(t) + 3, mid, f"{mid:,.0f}（中線）", va="center", fontsize=8.5, color=INK)
ticks = [i for i, b in enumerate(bars) if b["minute"][3:] == "00"]
ax.set_xticks(ticks)
ax.set_xticklabels([bars[i]["minute"] for i in ticks])
ax.set_xlim(0, len(t) + 1)
ax.set_ylim(10595, 10850)
thousands(ax, "y")
ax.set_ylabel("8 月台指期（點）")
ax.text(0.01, 0.015, f"線＝前一晚夜盤週選擇權重算，減 {basis:.0f} 點換成 8 月期貨刻度；粗細＝份量",
        transform=ax.transAxes, fontsize=8.5, color=INK2)
ax.set_title("圖 4　2019/7/31 台指期日盤與前一晚算出的線", loc="left", fontsize=13)
fig.tight_layout()
fig.subplots_adjust(right=0.70)
fig.savefig(OUT / "fig04_0731_lines.png", dpi=200)
plt.close(fig)

if __name__ == "__main__":
    print(f"圖 3 遠期價 {option_lines('txo_night_20200102_202001W2.csv')[1]:.1f}")
    print(f"圖 4 基差 {basis:.2f}、中線 {mid:.1f}")
    for ln in sorted(otm, key=lambda z: -z["pos"]):
        print(f'  {ln["strike"]} {"C" if ln["call"] else "P"} 均價 {ln["avg"]:.1f} 量 {ln["vol"]} 週選線 {ln["pos"]:.1f} 期貨線 {ln["pos"] - basis:.1f} 份量 {ln["w"]:.1f}')
