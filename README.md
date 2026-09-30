# article-figs

文章用的示意圖。Google Docs 只能從公開網址插圖，所以圖放在這個公開 repo，文件裡的圖都從這裡抓。

圖裡的數字都是示意用的假設值，不是真實報價或部位。

## 結構

一篇文章一個資料夾，每個資料夾裡有：

- `README.md`：圖的索引（檔名、圖號、放在文章哪一節、畫的是什麼）
- 產生圖的程式（改圖一律改程式再重跑，不手動修圖）
- 輸出的 PNG，檔名 `figNN_描述.png`，NN 是兩位數圖號

## 文章

| 資料夾 | 文章 |
|---|---|
| [`options-gex/`](options-gex/) | 誰在被迫交易：從第一性原理看選擇權避險與 GEX |

## 插進 Google Docs 的網址

用含 commit SHA 的 raw 網址，避免 GitHub 快取拿到舊圖：

```
https://raw.githubusercontent.com/W-Ace/article-figs/<commit SHA>/<資料夾>/<檔名>.png
```
