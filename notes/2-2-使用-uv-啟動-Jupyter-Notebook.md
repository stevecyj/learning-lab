# 2-2 使用 uv 啟動 Jupyter Notebook

## 這一節要學會什麼

完成這一節後，我應該能夠：

1. 說明 Jupyter、Jupyter Notebook、JupyterLab、Notebook 檔案與 kernel 的差別。
2. 將課程中的 Anaconda Navigator 操作換成 uv 指令。
3. 從目前專案的 Python 環境啟動 Jupyter Notebook。
4. 建立並執行一個 `.ipynb` Notebook。
5. 確認 Notebook 實際使用專案 `.venv` 裡的 Python。
6. 用「Restart Kernel and Run All」檢查 Notebook 能否從乾淨狀態執行。

---

## 一、這段課程實際在教什麼

課程畫面雖然有許多 Anaconda Navigator 按鈕，但核心流程只有四步：

```text
準備 Python 環境
→ 安裝 Jupyter 介面
→ 從專案資料夾啟動 Jupyter
→ 建立 Notebook 並用 Python kernel 執行程式碼
```

Anaconda Navigator 只是完成這些工作的圖形介面。使用 uv 時，不需要安裝 Anaconda，也不必尋找相同的按鈕。

### Anaconda 與 uv 的操作對照

| 課程中的 Anaconda 操作 | uv 專案中的做法 |
| ---------------------- | ---------------- |
| 建立環境 | `uv init --python 3.11` |
| 選擇某個環境 | 進入該專案資料夾 |
| Install Jupyter Notebook | `uv add notebook` |
| Launch | `uv run jupyter notebook` |
| 點選 Desktop 或課程資料夾 | 啟動前先用 `cd` 進入專案 |
| New → Python 3 | 建立使用 Python kernel 的 Notebook |
| Untitled | 尚未命名的 `.ipynb` 檔案 |

這一節的重點是知道「哪個環境正在執行程式碼」，而不是記住按鈕位置。

---

## 二、先分清 Jupyter 生態中的角色

| 名稱 | 角色 | 是否執行 Python |
| ---- | ---- | --------------- |
| Jupyter | 整套互動式運算工具的生態系 | 否 |
| Jupyter Notebook | 較聚焦於 Notebook 的瀏覽器介面 | 否 |
| JupyterLab | 可同時開啟 Notebook、終端機與文字檔的整合介面 | 否 |
| `.ipynb` | 儲存程式碼、文字、輸出與 metadata 的文件 | 否 |
| Python kernel | 接收儲存格內容並實際執行 Python 的程序 | 是 |

最重要的關係是：

```text
瀏覽器介面（Notebook 或 Lab）
              ↓
        Jupyter Server
              ↓
         Python kernel
              ↓
     專案環境中的 Python 與套件
```

Jupyter Notebook 與 JupyterLab 是不同的使用介面，但都能開啟同一種 `.ipynb` 檔案。它們不需要同時安裝：

- 想跟課程畫面接近：安裝 `notebook`。
- 想使用檔案總管、終端機與多分頁工作區：安裝 `jupyterlab`。
- 同時需要兩種介面時，才安裝兩者或使用包含完整工具組的 `jupyter` 套件。

Jupyter 官方將 kernel 定義為獨立執行程式碼的程序；Python Notebook 通常使用建立在 IPython 上的 `ipykernel`。[Jupyter Kernels 官方文件](https://docs.jupyter.org/en/latest/projects/kernels.html)

---

## 三、在目前專案中可以直接執行的步驟

這個專案已經由 uv 管理，因此不需要再次執行 `uv init`。

### 第一步：進入專案資料夾

```sh
cd /Volumes/data/Projects-practice/python-course
```

專案根目錄應包含：

```text
pyproject.toml
uv.lock
.python-version
```

### 第二步：安裝 Jupyter Notebook

若專案尚未加入 Notebook，執行：

```sh
uv add notebook
```

`uv add` 會把直接依賴寫入 `pyproject.toml`、更新 `uv.lock`，並同步專案的 `.venv`。

這一步只需做一次。之後換電腦時，應從版本控制取得專案，再用 `uv sync --locked` 依鎖檔重建環境，不要重新逐一安裝套件。

### 第三步：啟動 Jupyter Notebook

```sh
uv run jupyter notebook
```

終端機會啟動本機 Jupyter Server，瀏覽器通常會自動開啟。`uv run` 的作用是從目前 uv 專案環境執行指令，而不是使用其他位置碰巧找到的 Jupyter。

若未來改用 JupyterLab，則執行：

```sh
uv add jupyterlab
uv run jupyter lab
```

不要只把啟動指令改成 `jupyter lab`；如果專案沒有安裝 `jupyterlab`，就無法使用該指令。

### 第四步：建立 Notebook

在瀏覽器介面中：

1. 點選新增 Notebook。
2. 選擇 Python 3 kernel。
3. 將檔案命名為 `test123.ipynb`。
4. 建議把課程 Notebook 放進 `notebooks/` 資料夾。

如果資料夾尚未存在，可以另開終端機執行：

```sh
mkdir -p notebooks data
```

### 第五步：執行第一個儲存格

輸入：

```python
print("Hello, Jupyter")
```

按 `Shift + Enter` 執行目前儲存格並移到下一格。

再測試變數：

```python
name = "Steve"
print(name)
```

#### 輸入程式碼時善用自動補全

Jupyter Notebook 有自動補全功能，不需要每次都將名稱完整打完。

- 輸入部分名稱後按 `Tab`，可顯示或完成可用的名稱。例如輸入 `pri` 後按 `Tab`，可補成 `print`。
- 在物件後輸入句點再按 `Tab`，可查看它的方法與屬性。例如先執行 `name = "Steve"`，再輸入 `name.` 並按 `Tab`。
- 將游標放在函式呼叫中並按 `Shift + Tab`，可查看函式的參數與簡短說明。
- 在名稱後加上 `?` 並執行儲存格，可查看較完整的說明，例如 `print?`。

如果按 `Tab` 沒有反應，先確認儲存格已進入編輯模式，而且相關的變數、函式或套件匯入已在前面的儲存格執行過。

照著教學操作時，可以先理解程式碼的目的，再利用自動補全輸入；執行後主動改一兩個值觀察結果，通常比逐字照抄更有學習效果。

### 第六步：確認 Notebook 使用正確的 Python

新增一格並執行：

```python
import sys

print(sys.executable)
print(sys.version)
```

在 macOS 上，`sys.executable` 預期應指向目前專案，例如：

```text
/Volumes/data/Projects-practice/python-course/.venv/bin/python
```

如果顯示其他專案、Homebrew、pyenv 或系統 Python 的路徑，代表目前選錯 kernel。此時應在 Notebook 的 kernel 選單中改選專案 `.venv` 對應的 Python。

### 第七步：停止 Jupyter

回到啟動 Jupyter 的終端機，按：

```text
Control + C
```

若詢問是否關閉伺服器，輸入 `y`。

關閉瀏覽器分頁不一定會停止 kernel 或 Jupyter Server；JupyterLab 的 Running 面板也會列出仍在執行的 kernel。[JupyterLab：Managing Kernels and Terminals](https://jupyterlab.readthedocs.io/en/stable/user/running.html)

---

## 四、下一次重新開啟

不必重新安裝 Notebook，只要回到專案再啟動：

```sh
cd /Volumes/data/Projects-practice/python-course
uv run jupyter notebook
```

若是剛從 Git 取得專案，或 `uv.lock` 已經更新，先同步環境：

```sh
uv sync --locked
uv run jupyter notebook
```

---

## 五、容易忽略的細節

### 1. 「介面已開啟」不代表環境正確

Jupyter Notebook 或 JupyterLab 只是前端介面，真正執行程式的是 kernel。

如果 pandas 安裝在專案 A，但 Notebook 的 kernel 使用專案 B，就可能出現：

```text
ModuleNotFoundError: No module named 'pandas'
```

排查時先執行：

```python
import sys
print(sys.executable)
```

不要一看到缺少套件就立刻重複安裝。先確認 kernel，再確認依賴是否已寫入 `pyproject.toml`。

Astral 官方也建議從 uv 專案環境啟動 Jupyter，並在需要明確切分伺服器環境與專案環境時建立專用 kernel。[Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)

### 2. `uv add notebook` 與 `uv run --with jupyter` 的目的不同

```sh
uv add notebook
```

代表 Notebook 是專案的固定依賴，會記錄在 `pyproject.toml` 與 `uv.lock`。適合課程專案需要長期反覆使用的情況。

```sh
uv run --with jupyter jupyter lab
```

代表臨時提供 Jupyter 來執行目前專案，不一定把 Jupyter 本身寫成專案依賴。適合不想把開發介面列為專案固定依賴的情況。

這兩種方式都合理，差別在於 Jupyter 是否屬於「可重建的專案工具」。本課程為了步驟直觀，使用前者。

### 3. `.ipynb` 不是一般 `.py` 檔案

`.py` 主要是純文字 Python 程式碼；`.ipynb` 則是 JSON 文件，還會保存：

- 程式碼與 Markdown 儲存格
- 儲存格輸出與圖表
- 執行次數
- Notebook 與 kernel metadata

Jupyter Server 負責載入及儲存 Notebook，kernel 只負責執行傳給它的程式碼。[Jupyter Architecture 官方文件](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html)

一般而言：

```text
.ipynb：學習、探索、資料分析、展示推導過程
.py：可重用函式、模組、自動化流程與正式應用程式
```

當 Notebook 裡的程式碼逐漸穩定且需要重複使用時，可以把核心邏輯移到 `.py` 模組，Notebook 則保留分析流程與說明。

### 4. Notebook 的執行順序不一定等於畫面順序

第一格：

```python
price = 100
```

第二格：

```python
total = price * 2
print(total)
```

若先執行第二格，會得到 `NameError`。更隱蔽的情況是：第一格以前執行過，後來被修改或刪除，但舊變數仍留在 kernel 記憶體中，讓 Notebook 看起來正常。

提交或交付 Notebook 前，執行：

```text
Restart Kernel and Run All Cells
```

這會清空舊狀態，再依畫面順序執行所有儲存格。JupyterLab 提供對應的 Restart Kernel and Run All Cells 指令。[JupyterLab Commands](https://jupyterlab.readthedocs.io/en/stable/user/commands.html)

### 5. 套件應由專案管理，不要只在 Notebook 裡臨時安裝

在 Notebook 內執行 `%pip install ...`，可能只改變當下 kernel 使用的環境，也不一定更新 `pyproject.toml` 與 `uv.lock`。其他人重建專案時便無法知道 Notebook 需要哪些依賴。

課程中需要新套件時，優先回到終端機執行：

```sh
uv add pandas
```

再回 Notebook 測試：

```python
import pandas as pd
print(pd.__version__)
```

這樣，直接依賴會記在 `pyproject.toml`，解析後的精確版本則會寫入 `uv.lock`，兩者都能納入版本控制。

### 6. 版本控制 Notebook 時要留意輸出與差異

建議提交：

```text
notebooks/*.ipynb
pyproject.toml
uv.lock
.python-version
```

不要提交：

```text
.venv/
.ipynb_checkpoints/
```

Notebook 會把輸出一起存入 JSON。大型表格、圖片或敏感資料可能讓 Git 差異難以閱讀，甚至意外洩漏資料。提交前應檢查輸出是否真的需要保留。

### 7. 從專案根目錄啟動，讓相對路徑可預期

如果 Notebook 讀取：

```python
open("data/example.csv")
```

相對路徑會受到 kernel 工作目錄影響。固定先進入專案根目錄再啟動 Jupyter，可以減少「同一份 Notebook 在不同地方找不到檔案」的問題。

建議結構：

```text
python-course/
├── .python-version
├── pyproject.toml
├── uv.lock
├── notes/
├── notebooks/
│   ├── 01-python-basic.ipynb
│   └── 02-variables.ipynb
└── data/
```

---

## 六、常見問題的排查順序

### `jupyter: command not found`

1. 確認目前位於正確專案。
2. 執行 `uv sync --locked`。
3. 確認 `pyproject.toml` 已宣告 `notebook`。
4. 使用 `uv run jupyter notebook`，不要直接執行 `jupyter notebook`。

### `ModuleNotFoundError`

1. 用 `sys.executable` 確認 kernel 的 Python 路徑。
2. 用 `uv add <套件名稱>` 將缺少的套件加入專案。
3. 必要時重新啟動 kernel，再重新匯入套件。

### 重新開啟 Notebook 後突然不能執行

1. 檢查儲存格是否依賴錯亂的執行順序。
2. 執行 Restart Kernel and Run All Cells。
3. 將必要的匯入、變數與資料載入放在清楚且可依序執行的位置。

### 瀏覽器關掉了，但終端機仍在執行

這通常不是錯誤。瀏覽器只是介面，Jupyter Server 與 kernel 仍可能繼續執行。回到終端機按 `Control + C` 即可停止。

---

## 七、完成這一節的小練習

### 操作練習

1. 從專案根目錄啟動 Jupyter Notebook。
2. 建立 `notebooks/2-2-jupyter-basics.ipynb`。
3. 用一格 Markdown 寫下 Notebook 與 kernel 的差別。
4. 用一格 Python 顯示 `sys.executable`。
5. 建立兩個有前後依賴的儲存格。
6. 執行 Restart Kernel and Run All Cells，確認從乾淨狀態可成功執行。

### 不看筆記回答

1. 為什麼瀏覽器成功開啟，不代表 Notebook 用對 Python？
2. `uv add notebook` 與 `uv run --with jupyter jupyter lab` 的目的有何不同？
3. 為什麼 Notebook 提交前要 Restart Kernel and Run All Cells？
4. 為什麼不建議只在 Notebook 裡臨時安裝套件？

如果無法用自己的話回答，回到對應段落再操作一次，直到不看筆記也能說明原因。

<details>
<summary>參考答案</summary>

1. 瀏覽器只是 Jupyter 的操作介面；真正執行程式的是 kernel。即使介面成功開啟，kernel 仍可能連到其他專案或系統的 Python，所以還要用 `sys.executable` 確認實際的直譯器路徑。
2. `uv add notebook` 會把 Notebook 記錄為專案的固定依賴，並更新 `pyproject.toml`、`uv.lock` 與專案環境；`uv run --with jupyter jupyter lab` 則是臨時提供 Jupyter 來執行專案，不一定會把 Jupyter 寫入專案依賴。
3. Restart Kernel 會清除記憶體中殘留的舊變數與隱藏狀態；Run All Cells 再依畫面順序執行所有儲存格。這能驗證 Notebook 不依賴過去的亂序執行，其他人也能從乾淨狀態重現結果。
4. 在 Notebook 內執行 `%pip install ...` 可能只改變當下 kernel 的環境，不會完整記錄到 `pyproject.toml` 與 `uv.lock`。其他人或未來的自己重建專案時，就可能缺少必要套件；課程中應優先在終端機使用 `uv add <套件名稱>`。

</details>

---

## 八、重點流程

```text
進入專案
→ 由 uv 同步依賴
→ 從專案環境啟動 Jupyter
→ 建立 .ipynb
→ 確認 kernel 使用 .venv
→ 依順序執行儲存格
→ Restart Kernel and Run All 驗證
→ 正常停止 Jupyter Server
```

目前專案最常用的指令是：

```sh
cd /Volumes/data/Projects-practice/python-course
uv sync --locked
uv run jupyter notebook
```

最重要的觀念是：

> Jupyter Notebook 是操作與保存運算過程的介面；真正執行 Python 的，是它連接的 kernel 與背後的專案環境。

---

## 官方參考資料

- [Astral：Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)
- [Jupyter：Kernels](https://docs.jupyter.org/en/latest/projects/kernels.html)
- [Jupyter：Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html)
- [JupyterLab：Get Started](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html)
- [Jupyter Notebook：Notebook Basics](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Notebook%20Basics.html)
