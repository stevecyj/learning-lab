# 2-3 理解 Jupyter Notebook 的 Cell 與執行狀態

## 這一節要學會什麼

完成這一節後，我應該能夠：

1. 說明 `.ipynb`、Cell、Jupyter 介面與 kernel 的關係。
2. 使用 Code Cell 執行 Python，使用 Markdown Cell 記錄說明。
3. 看懂 `In [ ]`、`In [數字]` 與 `In [*]`。
4. 解釋為什麼畫面上的 Cell 順序不一定等於實際執行順序。
5. 找出 Notebook 的隱藏狀態與錯誤 kernel。
6. 用乾淨狀態驗證整份 Notebook 能否重現。

---

## 核心內容

### 1. Notebook 是可分段執行的文件

`.ipynb` 文件可以同時保存：

- Python 程式碼
- Markdown 說明
- 程式輸出與圖表
- Cell 的執行次數
- Notebook 與 kernel 的 metadata

Notebook 適合學習、資料分析、快速實驗與展示推導過程。它讓我先用小段程式驗證想法，再把成熟、需要重用的邏輯整理到 `.py` 模組。

### 2. Cell 是 Notebook 的基本單位

最常使用兩種 Cell：

| 類型 | 用途 | 範例 |
| --- | --- | --- |
| Code Cell | 執行 Python | `print("Hello")` |
| Markdown Cell | 寫標題、說明與結論 | `## 實驗結果` |

常用操作是 `Shift + Enter`：執行目前 Cell，然後移到下一個 Cell。

一份容易理解的 Notebook 通常按照下列節奏編排：

```text
Markdown：說明這一步要回答的問題
Code：執行一個小步驟
Markdown：解釋結果
Code：進行下一個步驟
```

### 3. `In` 顯示的是執行狀態

| 標記 | 意義 |
| --- | --- |
| `In [ ]` | 尚未執行，或執行編號已清除 |
| `In [3]` | 這是目前 kernel 的第 3 次執行 |
| `In [*]` | kernel 正在處理工作 |

`In [3]` 不保證程式成功。即使 Cell 發生錯誤，這次執行仍可能取得編號。`In [*]` 也不只代表單一 Cell 忙碌；同一個 kernel 一次通常只能處理一項工作，因此其他 Cell 也必須等待。

### 4. 畫面順序不等於執行順序

Notebook 允許任意選擇 Cell 執行。假設畫面依序是：

```python
price = 100
```

```python
total = price * 2
print(total)
```

```python
price = 500
```

若依畫面順序執行，`total` 是 `200`；若先執行第一格、第三格，再執行第二格，`total` 會是 `1000`。

所以閱讀 Notebook 時，不能只看 Cell 的排列，也要確認實際執行次序。完成後應從乾淨的 kernel 由上到下重跑。

### 5. Kernel 保存目前的記憶體狀態

執行：

```python
message = "Hello"
```

即使之後刪除這個 Cell，只要 kernel 尚未重新啟動，下面的程式仍可能成功：

```python
print(message)
```

這是隱藏狀態：畫面上已經找不到變數來源，記憶體卻仍保留它。這種 Notebook 在自己電腦上看似正常，交給別人或隔天重開時可能立刻失敗。

### 6. Jupyter 介面不等於 Python 執行環境

Notebook 或 JupyterLab 是操作介面，kernel 才是實際執行 Python 的程序。Kernel 又會使用某個 Python 環境中的直譯器與套件。

本專案的關係是：

```text
Jupyter Notebook／JupyterLab
          ↓
     Python kernel
          ↓
 uv 專案的 .venv
```

在 Notebook 中執行以下程式，可以確認 kernel 的來源：

```python
import sys

print(sys.executable)
print(sys.version)
```

`sys.executable` 應指向本專案，例如：

```text
/Volumes/data/Projects-practice/tibame/learning-lab/.venv/bin/python
```

若顯示 Anaconda、Homebrew、pyenv、系統 Python 或其他專案的路徑，代表選錯 kernel。此時即使已用 uv 安裝套件，Notebook 仍可能出現 `ModuleNotFoundError`。

---

## Python 專家最在乎什麼

### 1. 結果能否重現

專家最在乎的不是 Notebook 在目前畫面上能不能跑，而是：

> 清除所有舊狀態後，另一個人能否依畫面順序得到相同結果？

交付或提交前，應執行介面中的 `Restart Kernel and Run All Cells`（名稱可能略有差異）。這會：

1. 清除 kernel 記憶體。
2. 從第一個 Cell 開始依序執行。
3. 暴露漏掉的變數、匯入、資料載入與順序依賴。

### 2. Kernel 是否使用正確環境

遇到 `ModuleNotFoundError` 時，不要立刻重複安裝套件。先檢查：

```python
import sys
print(sys.executable)
```

確認環境正確後，再檢查 `pyproject.toml` 是否宣告依賴。新增專案套件時，回到終端機使用：

```sh
uv add <套件名稱>
```

這樣依賴才會記錄在 `pyproject.toml` 與 `uv.lock`，其他電腦才能重建。

### 3. 隱藏狀態是否被清除

以下現象都是警訊：

- 執行編號明顯跳動，例如 `In [12]`、`In [3]`、`In [9]`。
- 刪除定義變數的 Cell 後，程式仍可執行。
- 單獨重開 Notebook 後，原本正常的 Cell 突然失敗。
- 必須先手動挑幾格執行，整份 Notebook 才能運作。

處理方式不是重新亂按 Cell，而是重啟 kernel，再從頭執行並修正依賴順序。

### 4. 探索程式與可重用程式是否分工

Notebook 適合：

- 探索資料與畫圖
- 測試 API 或套件
- 驗證自動化流程的某一步
- 記錄實驗問題、過程與結論

當程式需要重複執行、測試或被後端服務呼叫時，應逐步移到 `.py`：

```text
learning-lab/
├── notebooks/
│   └── 01_jupyter_basics.ipynb
├── src/
│   └── calculator.py
└── tests/
    └── test_calculator.py
```

這與目前的學習目標直接相關：Notebook 可用來探索自動化、資料分析與 API 邏輯；成熟後的核心程式則放進可維護、可測試的模組。

### 5. 輸出與資料是否適合保存

`.ipynb` 會把輸出存進文件。提交 Git 前要檢查：

- 是否包含大型表格或圖片，造成檔案過大。
- 是否包含 token、密碼、個人資料或其他敏感內容。
- 輸出是否真有助於閱讀。
- `.ipynb_checkpoints/` 是否已排除在版本控制外。

---

## 開發上可採取的行動步驟

### 第一步：從 uv 專案啟動 Jupyter

```sh
cd /Volumes/data/Projects-practice/tibame/learning-lab
uv sync --locked
uv run jupyter notebook
```

如果目前使用 JupyterLab：

```sh
uv run jupyter lab
```

### 第二步：建立練習檔

建立：

```text
notebooks/01_jupyter_basics.ipynb
```

第一格改成 Markdown：

```markdown
# Jupyter Notebook 基礎練習

這份 Notebook 用來練習 Code Cell、Markdown Cell 與執行狀態。
```

第二格使用 Code Cell：

```python
print("Hello, Python")
```

兩格都使用 `Shift + Enter` 執行。

### 第三步：確認 kernel

新增 Code Cell：

```python
import sys

print(sys.executable)
print(sys.version)
```

確認路徑包含：

```text
learning-lab/.venv/
```

### 第四步：觀察跨 Cell 狀態

依序建立三格：

```python
number = 10
```

```python
result = number * 2
print(result)
```

```python
number = 100
```

先由上到下執行，記錄結果；再依「第一格 → 第三格 → 第二格」執行，比較第二格輸出的差異。

### 第五步：親自製造並清除隱藏狀態

1. 執行 `secret = "仍在記憶體中"`。
2. 刪除定義 `secret` 的 Cell。
3. 在另一格執行 `print(secret)`，確認它暫時仍成功。
4. 重新啟動 kernel。
5. 再執行 `print(secret)`，觀察 `NameError`。

這個練習用最短路徑證明：Notebook 畫面與 kernel 記憶體可能不一致。

### 第六步：從乾淨狀態驗證

使用：

```text
Restart Kernel and Run All Cells
```

確認：

- 所有 Cell 能由上到下執行。
- 沒有依賴已刪除的變數。
- `sys.executable` 仍指向專案 `.venv`。
- 執行編號重新從 `1` 開始並依序增加。

### 第七步：正常停止服務

回到啟動 Jupyter 的終端機，按 `Control + C`。只關閉瀏覽器分頁，不一定會停止 Jupyter Server 與 kernel。

---

## 我可以立刻採取的實作清單

- [ ] 從專案根目錄執行 `uv run jupyter notebook` 或 `uv run jupyter lab`
- [ ] 建立 `notebooks/01_jupyter_basics.ipynb`
- [ ] 建立一格 Markdown 標題與一格 `print()` 程式
- [ ] 熟悉 `Shift + Enter`
- [ ] 用 `sys.executable` 確認 kernel 指向 `.venv`
- [ ] 完成 `number` 的亂序執行實驗
- [ ] 完成刪除變數 Cell 的隱藏狀態實驗
- [ ] 執行一次 Restart Kernel and Run All Cells
- [ ] 確認 `.ipynb_checkpoints/` 不會被提交
- [ ] 不看筆記回答下方複習題

---

## 複習題

先從記憶回答：

1. `In [4]` 能否證明程式執行成功？為什麼？
2. 為什麼畫面完全相同的 Notebook 可能算出不同答案？
3. 什麼是隱藏狀態？
4. `sys.executable` 能協助判斷什麼問題？
5. 為什麼交付前要 Restart Kernel and Run All Cells？
6. 什麼時候應把 Notebook 程式移到 `.py`？

<details>
<summary>參考答案</summary>

1. 不能；數字只表示這是 kernel 收到的第幾次執行，錯誤的程式也可能取得編號。
2. Cell 可以亂序執行，kernel 中的變數值可能與畫面順序不同。
3. 畫面沒有呈現完整來源，但 kernel 記憶體仍保留先前執行產生的變數或物件。
4. 它顯示 kernel 實際使用的 Python，可用來判斷是否選錯環境。
5. 它能清除舊狀態，驗證 Notebook 能否依畫面順序完整重現。
6. 當邏輯已穩定，且需要重用、測試、自動執行或供後端服務呼叫時。

</details>

---

## 總結

這一節最重要的觀念是：

> Notebook 是一份可互動執行的文件；畫面保存 Cell，kernel 保存當下狀態，兩者不一定一致。

專業使用 Notebook 的最低標準有三項：

1. 確認 kernel 使用正確的 uv 專案環境。
2. 避免依賴亂序執行留下的隱藏狀態。
3. 交付前從乾淨 kernel 執行全部 Cell，確認結果可以重現。

先完成這份短練習，再繼續學 Python 語法。若任何步驟的結果與預期不同，可以直接把畫面訊息或錯誤貼給教學助理詢問。

## 官方參考資料

- [Jupyter Notebook：Running Code](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Running%20Code.html)
- [Jupyter：Kernels](https://docs.jupyter.org/en/latest/projects/kernels.html)
- [JupyterLab：Managing Kernels and Terminals](https://jupyterlab.readthedocs.io/en/stable/user/running.html)
- [Astral：Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)
