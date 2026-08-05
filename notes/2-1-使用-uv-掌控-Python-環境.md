# 2-1 使用 uv 掌控 Python 環境

## 這一節要學會什麼

完成這一節後，我應該能夠：

1. 分辨 uv、Python、專案設定、虛擬環境與鎖檔的責任。
2. 說明為什麼 `uv python pin 3.11` 可能與 `requires-python = ">=3.13"` 衝突。
3. 在全新專案中明確指定 Python 3.11，不讓 uv 猜版本。
4. 在另一臺電腦或雲端主機上重建相同的專案環境。
5. 遇到錯誤時，依固定順序檢查，而不是同時修改 pyenv、uv 和專案設定。
6. 用 `uv add`、`uv remove` 管理專案套件。
7. 用專案的虛擬環境啟動 JupyterLab。
8. 確認 Notebook 實際使用的 Python 來自專案的 `.venv`。

---

## 一、先分清各個工具的責任

Python 專案環境分成五個層次：

| 層次                 | 作用                               | 本專案範例                   |
| -------------------- | ---------------------------------- | ---------------------------- |
| uv 執行檔            | 執行環境管理命令                   | `~/.local/bin/uv`            |
| Python 直譯器        | 執行 Python 程式                   | Python 3.11.14               |
| `.python-version`    | 指定開發此專案時預設使用的 Python  | `3.11`                       |
| `pyproject.toml`     | 宣告專案支援哪些 Python 版本與依賴 | `requires-python = ">=3.11"` |
| `.venv` 與 `uv.lock` | 隔離安裝環境；鎖定依賴解析結果     | `.venv/`、`uv.lock`          |

> uv 可以獨立安裝，但執行專案時仍然需要選擇 Python 直譯器。

「uv 不依賴 pyenv」不等於「uv 永遠自動選到 Python 3.11」。uv 仍可能找到系統、Homebrew、pyenv 或 uv 自己管理的 Python。

---

## 二、這次錯誤的原因

當時的專案設定是：

```text
.python-version    3.13
pyproject.toml     requires-python = ">=3.13"
```

接著執行：

```sh
uv python pin 3.11
```

uv 會先檢查 Python 3.11 是否符合專案宣告：

```text
3.11 是否符合 >=3.13？不符合。
```

因此 uv 拒絕寫入互相矛盾的設定，顯示：

```text
The requested Python version `3.11` is incompatible with
the project `requires-python` value of `>=3.13`.
```

這個錯誤與 uv 是否透過 pyenv 啟動無關。問題出在「要求使用的 Python」與「專案允許的 Python」互相衝突。

### 為什麼 `uv init` 會產生 3.13？

若初始化時沒有明確指定 Python：

```sh
uv init
```

uv 會依目前電腦可發現的 Python 與版本偏好選擇直譯器，所以不同電腦的結果可能不同。本機同時有 uv 管理的 Python 3.13.3 和 Homebrew Python 3.11.14。uv 預設偏好 managed Python，初始化時可能選到 3.13。

只依賴 `uv init` 自動選版，無法保證不同電腦會使用同一個版本。

---

## 三、建立全新專案的通用做法

### 推薦：初始化時就指定 Python

一般應用程式：

```sh
uv init --python 3.11
uv sync
uv run python --version
```

可安裝的 package 專案：

```sh
uv init --package --python 3.11
uv sync
uv run python-course
```

`--python 3.11` 會讓 uv 從第一步就建立一致設定：

```text
.python-version    3.11
requires-python    >=3.11
```

此時不必再執行 `uv python pin 3.11`，因為初始化已經完成 pin。

### 如果課程指定這三行

```sh
uv init
uv python pin 3.11
uv sync
```

這個流程能否成功，取決於第一步產生的 `requires-python` 是否允許 3.11。

執行 `uv init` 後先檢查：

```sh
cat .python-version
rg '^requires-python' pyproject.toml
```

若結果為：

```text
3.11
requires-python = ">=3.11"
```

便可繼續原流程。

若結果為：

```text
3.13
requires-python = ">=3.13"
```

而課程確定要求 Python 3.11，先將 `pyproject.toml` 改為：

```toml
requires-python = ">=3.11"
```

再執行：

```sh
uv python pin 3.11
uv sync
```

若要避免不同電腦選到不同版本，直接使用：

```sh
uv init --python 3.11
```

---

## 四、換電腦或雲端主機時怎麼做

### 1. 安裝獨立 uv

macOS／Linux：

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

確認 uv 的路徑不是 pyenv shim：

```sh
command -v uv
uv --version
```

預期路徑通常是：

```text
~/.local/bin/uv
```

### 2. 取得既有專案

```sh
git clone <repository-url>
cd <project-directory>
```

既有專案不要再執行 `uv init`。`uv init` 是建立新專案用的；重新執行可能重建設定，或與現有設定衝突。

### 3. 依鎖檔重建環境

```sh
uv sync --locked
uv run python --version
```

uv 會讀取 `.python-version`、`pyproject.toml` 與 `uv.lock`。若本機沒有符合要求的 Python，uv 預設可以自行下載。

### 4. Git 應提交哪些檔案

應提交：

```text
.python-version
pyproject.toml
uv.lock
```

不應提交：

```text
.venv/
```

原因：

- `.python-version`：讓其他電腦知道開發環境使用哪個 Python。
- `pyproject.toml`：記錄專案相容範圍與直接依賴。
- `uv.lock`：記錄精確解析出的依賴版本，而且支援跨平台。
- `.venv/`：是特定電腦建立的環境，應由 `uv sync` 重建。

Jupyter Notebook 本身的 `.ipynb` 檔案可以提交，自動產生的 `.ipynb_checkpoints/` 則應加入 `.gitignore`。提交前可先檢查：

```sh
git status --short
git check-ignore .venv .ipynb_checkpoints/checkpoint.ipynb
```

---

## 五、全域 Python pin 的定位

可以設定個人電腦的 uv 預設版本：

```sh
uv python pin --global 3.11
```

這是 uv 官方支援的持久設定。如果希望本機的新專案預設使用 3.11，全域 pin 很方便。

但它不會提交到 Git，也不會出現在另一臺電腦。專案要跨電腦使用，仍要靠專案內的 `.python-version`、`pyproject.toml` 與 `uv.lock`。

---

## 六、兩個版本設定的差別

### `.python-version = 3.11`

代表：

> 開發與執行這個專案時，預設選擇 Python 3.11 的最新可用 patch 版本。

例如可能實際使用 Python 3.11.14。

### `requires-python = ">=3.11"`

代表：

> 這個專案宣告支援 Python 3.11 或更新版本。

它不代表專案一定會在所有新版本上正確運作；那仍需要測試。

若專案只允許 Python 3.11 系列，可以宣告：

```toml
requires-python = ">=3.11,<3.12"
```

一般課程專案通常使用 `>=3.11` 即可。

---

## 七、環境錯誤的檢查順序

遇到 Python／uv 環境錯誤時，依序檢查，不要同時更換多個工具。

### 第 1 步：確認執行的是哪個 uv

```sh
command -v uv
uv --version
```

若顯示 `~/.pyenv/shims/uv`，代表 uv 仍由 pyenv shim 接管。

### 第 2 步：確認專案 pin

```sh
cat .python-version
```

### 第 3 步：確認專案相容範圍

```sh
rg '^requires-python' pyproject.toml
```

### 第 4 步：確認 uv 實際找到的直譯器

```sh
uv python find
uv run python --version
```

### 第 5 步：同步環境

```sh
uv sync
```

若是 CI 或要確認鎖檔沒有被自動更新：

```sh
uv sync --locked
```

---

## 八、快速判斷表

| 現象                                  | 原因                                    | 處理方式                                                 |
| ------------------------------------- | --------------------------------------- | -------------------------------------------------------- |
| `pyenv: version ... is not installed` | `uv` 解析到 pyenv shim                  | 安裝獨立 uv，確認 `command -v uv`                        |
| `3.11 is incompatible with >=3.13`    | Python pin 與 `requires-python` 衝突    | 確認專案需求後，調整 `requires-python`                   |
| 新電腦缺少 Python                     | 本機沒有符合 `.python-version` 的直譯器 | 執行 `uv sync`，讓 uv 自動取得，或先 `uv python install` |
| 套件版本在不同電腦不一致              | 沒有提交或使用 `uv.lock`                | 提交 `uv.lock`，使用 `uv sync --locked`                  |
| 啟動既有專案時設定混亂                | 對既有專案再次執行 `uv init`            | 不要 init，直接 `uv sync --locked`                       |

---

## 九、我應該記住的最短版本

### 新專案

```sh
uv init --python 3.11
uv sync
```

### 既有專案／換電腦

```sh
uv sync --locked
```

### 發生版本衝突

```sh
cat .python-version
rg '^requires-python' pyproject.toml
uv run python --version
```

新專案要明確指定 Python；既有專案要提交版本設定與鎖檔；換電腦後，安裝 uv 並同步即可。

---

## 十、安裝與管理專案套件

安裝套件時使用 `uv add`：

```sh
uv add pandas
uv add numpy matplotlib seaborn
```

`uv add` 會將直接依賴寫入 `pyproject.toml`，然後更新 `uv.lock` 與 `.venv`。

執行 `uv add` 後不必再執行一次 `uv sync`。

移除不再需要的套件：

```sh
uv remove 套件名稱
```

查看專案目前安裝的依賴：

```sh
uv tree
```

課程若要求 `pip install <package>`，在這個專案中改用 `uv add <package>`。不要只在 Notebook 裡執行 `!pip install`；那樣安裝的套件不會自動寫入 `pyproject.toml` 與 `uv.lock`，換電腦後便無法靠鎖檔完整重建。

---

## 十一、用 JupyterLab 上課

本專案已經將 JupyterLab 加入依賴，進入專案目錄後可直接啟動：

```sh
cd python-course
uv run jupyter lab
```

`uv run` 會在執行命令前檢查 `uv.lock` 與 `.venv`，並在專案環境內執行 JupyterLab。不必先手動啟用虛擬環境：

```sh
source .venv/bin/activate
```

如果只想臨時啟動 Jupyter，不把它加入專案依賴，可以使用官方文件中的 `uv run --with jupyter jupyter lab`。本專案已經執行過 `uv add jupyterlab`，直接使用 `uv run jupyter lab` 即可。

啟動後，Terminal 會顯示類似下面的網址：

```text
http://localhost:8888/lab
```

瀏覽器若沒有自動開啟，將 Terminal 顯示的完整網址複製到瀏覽器。不要把 token 網址傳給其他人。

停止 JupyterLab 時，回到啟動它的 Terminal 按 `Ctrl+C`。只關閉瀏覽器分頁，Jupyter server 與 Notebook kernel 可能仍在執行。

### 確認 Notebook 用對了 Python

在 Notebook 的 Cell 執行：

```python
import sys

print(sys.executable)
print(sys.version)
```

macOS 上的直譯器路徑應指向目前專案，例如：

```text
/path/to/python-course/.venv/bin/python3
```

若路徑指向 Anaconda、pyenv 的其他環境或另一個專案，先停止 JupyterLab，回到 `python-course` 目錄後重新執行：

```sh
uv run jupyter lab
```

---

## 十二、本專案的檢查清單

以下是本次檢查結果：

| 檢查項目         | 命令                              | 目前結果                 |
| ---------------- | --------------------------------- | ------------------------ |
| Python pin       | `cat .python-version`             | `3.11`                   |
| 專案相容範圍     | `rg '^requires-python' pyproject.toml` | `requires-python = ">=3.11"` |
| 實際直譯器       | `uv run python --version`         | Python 3.11.14            |
| JupyterLab       | `uv run jupyter lab --version`    | 4.6.2                    |
| 直接依賴         | `uv tree --depth 1`               | `jupyterlab`、`pandas`     |
| 鎖檔是否與設定一致 | `uv lock --check`                 | 通過                     |

這些版本會隨後續安裝或升級而改變。結果不同時，先檢查 `pyproject.toml` 與 `uv.lock`，不要直接刪除 `.venv` 或重新執行 `uv init`。

---

## 十三、複習題

先不要看答案，嘗試從記憶回答。

1. 獨立安裝 uv，是否代表 uv 永遠使用同一個 Python？
2. `.python-version` 與 `requires-python` 各自控制什麼？
3. 為什麼 `uv python pin 3.11` 不能搭配 `requires-python = ">=3.13"`？
4. 建立新專案時，哪個命令能避免 uv 自動猜 Python？
5. 換到另一臺電腦後，為什麼不應重新執行 `uv init`？
6. 哪三個專案檔案應提交到 Git，以便重建環境？
7. `uv python pin --global 3.11` 為什麼不能取代專案內的版本設定？
8. `uv add pandas` 會更新哪些專案狀態？
9. 為什麼啟動 JupyterLab 時使用 `uv run`？
10. 如何確認 Notebook 使用的是專案 `.venv` 裡的 Python？

<details>
<summary>參考答案</summary>

1. 不會；uv 仍需要從可用來源選擇 Python 直譯器。
2. `.python-version` 選擇開發時預設直譯器；`requires-python` 宣告專案相容範圍。
3. 因為 Python 3.11 不符合「最低需要 Python 3.13」的條件。
4. `uv init --python 3.11`。
5. `uv init` 用來建立新專案；既有專案已有設定，只需 `uv sync --locked`。
6. `.python-version`、`pyproject.toml`、`uv.lock`。
7. 全域 pin 是單機個人設定，不會隨 Git 專案移動到其他電腦。
8. 它會更新 `pyproject.toml`、`uv.lock` 與 `.venv`。
9. `uv run` 會檢查並同步專案環境，再於該環境內啟動 JupyterLab。
10. 在 Notebook 執行 `print(sys.executable)`，確認路徑指向目前專案的 `.venv`。

</details>

---

## 官方參考資料

- [Installing uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Creating projects](https://docs.astral.sh/uv/concepts/projects/init/)
- [Python versions](https://docs.astral.sh/uv/concepts/python-versions/)
- [Working on projects](https://docs.astral.sh/uv/guides/projects/)
- [Managing dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)
- [Project structure and files](https://docs.astral.sh/uv/concepts/projects/layout/)
