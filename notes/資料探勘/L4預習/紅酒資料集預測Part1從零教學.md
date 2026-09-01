# 紅酒資料集預測 Part 1：從零開始

## 這一課在做什麼？

**我們要讓電腦根據一瓶紅酒的 11 項化學測量值，預測它的品質分數 `quality`。**

如果用前端開發來比喻，可以把模型想成一個函式：

```javascript
const predictedQuality = model.predict({
  alcohol: 10.2,
  pH: 3.3,
  sulphates: 0.65,
  // 其餘化學特徵……
})
```

這個函式不是工程師親手寫一堆 `if...else`。模型會從歷史資料中找出計算規則。

Part 1 使用的是**迴歸**。輸出是連續數值，例如 `5.43`，不一定是整數。雖然原始品質分數是整數，這裡仍把問題當成「預測一個數值」，不是分類問題。

## 完成 Part 1 後，你應該能回答

1. `X` 和 `y` 分別存什麼，為什麼 shape 不同？
2. `PolynomialFeatures` 為什麼會增加欄位？
3. 為什麼要把資料分成訓練集和測試集？
4. 為什麼 scaler 只能用訓練集 `fit()`？
5. `model.fit()` 和 `model.predict()` 分別做什麼？
6. MSE 和 R² 如何判斷模型表現？
7. 最後得到的是預測結果，還是造成紅酒品質好壞的科學證明？

## 資料長什麼樣子？

專案中的資料檔有 1,599 筆紅酒資料與 12 個欄位：

- 11 個輸入欄位：酸度、糖分、氯化物、密度、pH、酒精濃度等化學測量值。
- 1 個答案欄位：`quality`，代表人工評定的品質分數。

這份資料實際出現的品質分數是 3～8，其中 5 和 6 最多。因此，模型比較容易學到常見分數，對非常少見的 3 或 8 通常較不可靠。

資料表可以想成：

```text
每一個 row    = 一瓶紅酒
每一個 column = 這瓶紅酒的一項資料
quality       = 希望模型學會預測的答案
```

## Part 1 的完整流程

```text
讀取 CSV
→ 做最低限度的資料檢查
→ 分離特徵 X 和答案 y
→ 建立二次多項式特徵
→ 切分訓練集與測試集
→ 用訓練集建立標準化規則
→ 用同一規則轉換訓練集與測試集
→ 訓練線性迴歸模型
→ 預測測試集
→ 用 MSE 和 R² 評估
```

## 步驟 1：匯入工具

```python
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
```

每個工具的責任如下：

- `pandas`：讀取及操作表格資料。
- `PolynomialFeatures`：從原始特徵建立平方項和交互項。
- `train_test_split`：把資料切成訓練集與測試集。
- `StandardScaler`：把不同量級的欄位轉到可比較的尺度。
- `LinearRegression`：建立線性迴歸模型。
- `mean_squared_error`、`r2_score`：評估預測表現。

這和前端 `import` 套件相同：目前只是取得工具，還沒有讀資料或訓練模型。

## 步驟 2：讀取 CSV

```python
import pandas as pd

wine = pd.read_csv(
    "../附件/L4 課程範例檔/dataset/winequality-red.csv"
)

wine.head()
```

`wine` 是 Pandas `DataFrame`，內容來自 `pd.read_csv(...)` 讀取的完整 CSV。下一步會先檢查它，再分成模型輸入 `X` 與答案 `y`。

### 這份專案資料是逗號分隔

專案裡這份 CSV 的第一行是：

```text
fixed acidity,volatile acidity,...,alcohol,quality
```

所以直接使用 `pd.read_csv(path)` 即可。**不要寫 `sep=";"`。**

如果錯寫：

```python
pd.read_csv(path, sep=";")
```

Pandas 會找不到分號，可能把整列讀成一個欄位。驗證方式是：

```python
print(wine.shape)
print(wine.columns)
```

成功條件：

```text
wine.shape == (1599, 12)
```

### 路徑的坑

相對路徑是根據 **Python 目前工作目錄** 計算，不一定根據 `.ipynb` 檔案所在目錄計算。找不到檔案時先執行：

```python
from pathlib import Path

print(Path.cwd())
```

這行顯示 Python 從哪個資料夾開始尋找；它不是資料檔本身的位置。

## 步驟 3：先做最低限度的資料檢查

```python
print(wine.shape)
wine.info()
print(wine.isna().sum())
wine.describe().T
```

這四行分別回答：

- `shape`：有幾筆資料、幾個欄位。
- `info()`：欄位名稱、型別及非空值數量。
- `isna().sum()`：每個欄位有多少缺失值。
- `describe()`：平均值、標準差、最小值、最大值與四分位數。

Part 1 的 Notebook 假設資料已經整理成可直接建模的數值欄位，沒有在這裡實作完整清理。這是它依賴的假設，不代表正式專案都可以跳過資料檢查。

## 步驟 4：分離 `X` 與 `y`

```python
X = wine.drop(columns="quality")
y = wine["quality"]

print(X.shape)
print(y.shape)
```

`X` 是模型輸入，包含 `quality` 以外的 11 個欄位。`y` 則是每瓶紅酒的正確答案，也就是 `quality`；後面的訓練與評估都會用到它。

執行結果：

```text
X.shape == (1599, 11)
y.shape == (1599,)
```

為什麼不同？

- `X` 是二維表格：1,599 瓶紅酒，每瓶有 11 個特徵。
- `y` 是一維序列：1,599 瓶紅酒，每瓶只有一個品質答案。

在 JavaScript 中，可以粗略想成：

```javascript
const X = rows.map(({ quality, ...features }) => features)
const y = rows.map(row => row.quality)
```

### 常見坑

以下寫法會把 `quality` 也放進輸入：

```python
X = wine
```

這等於在考試時把答案一起交給模型，造成嚴重的資料洩漏。模型分數看起來會很好，但那不是有效預測。

## 步驟 5：建立二次多項式特徵

原始線性迴歸只會學類似這種關係：

```text
預測品質
= 酒精濃度的權重 × alcohol
+ 酸度的權重 × acidity
+ 其他欄位
+ 截距
```

但現實可能不是單純直線關係。例如，某項成分太低或太高都不好，或者酒精濃度與酸度搭配時才產生影響。

```python
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

print(X.shape)
print(X_poly.shape)
```

`poly` 是多項式特徵轉換器，記錄要建立哪些二次特徵。`X_poly` 是它根據原始 `X` 產生的新輸入，下一步會切成訓練集與測試集。

假設原本只有兩個欄位 `a`、`b`，二次轉換後會得到：

```text
a
b
a²
a × b
b²
```

在本資料中：

```text
原始 X.shape      = (1599, 11)
轉換後 X_poly.shape = (1599, 77)
```

row 仍是 1,599，因為紅酒數量沒變；column 從 11 增加到 77，因為每瓶紅酒多了平方項與兩兩交互項。

### `fit_transform()` 完整拆解

縮寫寫法：

```python
X_poly = poly.fit_transform(X)
```

完整寫法：

```python
poly.fit(X)
X_poly = poly.transform(X)
```

- `fit(X)`：確認輸入有幾個欄位，以及輸出要建立哪些組合。
- `transform(X)`：實際產生新欄位。

### 為什麼使用 `include_bias=False`？

`PolynomialFeatures` 預設會多建立一個永遠等於 1 的欄位。`LinearRegression` 本身已經會處理截距，因此教學中關掉這個重複欄位，資料會比較容易理解。

### 常見坑：degree 不是越高越好

`degree=3`、`degree=4` 會讓欄位數快速增加。模型可能把訓練資料中的偶然雜訊也背起來，造成：

```text
訓練資料表現很好
測試資料表現變差
```

這叫做**過度擬合**。

## 步驟 6：切分訓練集與測試集

```python
X_train, X_test, y_train, y_test = train_test_split(
    X_poly,
    y,
    test_size=0.3,
    random_state=1,
)
```

切分後得到四個變數：

- `X_train`：給模型學習的特徵。
- `X_test`：最後用來考模型的特徵。
- `y_train`：`X_train` 每一列對應的正確品質。
- `y_test`：`X_test` 每一列對應的正確品質。

參數的意思：

- `test_size=0.3`：30% 資料當測試集，70% 當訓練集。
- `random_state=1`：固定隨機切分結果，讓每次執行都能重現同一結果。它不是模型分數，也不是切分比例。

本資料的結果：

```text
X_train.shape == (1119, 77)
X_test.shape  == (480, 77)
y_train.shape == (1119,)
y_test.shape  == (480,)
```

不能拿全部資料訓練，再用同一批資料評估。那就像先讓學生背考題和答案，再用同一份題目判斷他是否理解。測試集必須保持未見狀態，才能反映模型遇到新紅酒時的表現。

## 步驟 7：標準化訓練與測試資料

不同欄位的數值範圍差很多，例如密度接近 1，總二氧化硫可能是數十或數百。標準化會把每欄轉成以 0 為中心、標準差約為 1 的尺度。

```python
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

`scaler` 是標準化工具，會保存從訓練資料算出的每欄平均數與標準差，接著用同一組數值轉換訓練集和測試集。

第一行轉換：

```python
X_train = scaler.fit_transform(X_train)
```

完整形式是：

```python
scaler.fit(X_train)
X_train = scaler.transform(X_train)
```

它先從訓練集計算規則，再轉換訓練集。

第二行轉換：

```python
X_test = scaler.transform(X_test)
```

測試集只能套用剛才的規則，不能重新計算。

### 最重要的坑：測試集不能 `fit_transform()`

錯誤：

```python
X_test = scaler.fit_transform(X_test)
```

這會讓測試資料參與計算自己的平均數與標準差，相當於模型流程偷看測試資料，稱為**資料洩漏**。

正確：

```python
X_test = scaler.transform(X_test)
```

標準化只改變數值尺度，不會改變 row 數和 column 數：

```text
X_train.shape 仍是 (1119, 77)
X_test.shape  仍是 (480, 77)
```

## 步驟 8：建立並訓練模型

```python
model = LinearRegression()
model.fit(X_train, y_train)
```

`model` 剛建立時還沒有學過任何資料。執行 `fit(X_train, y_train)` 後，它會尋找 77 個特徵的係數，使預測值盡量接近 `y_train`。

可以把它想成模型學出這種函式：

```text
預測品質 = 特徵1 × 係數1 + 特徵2 × 係數2 + ... + 截距
```

`fit()` 不會回傳 1,119 個預測結果。它的結果是把學到的係數保存到 `model` 內部。

執行後可以查看：

```python
print(model.coef_)
print(model.intercept_)
```

- `model.coef_`：每個輸入欄位對應的係數。
- `model.intercept_`：公式中的截距。

係數只能解讀為這個模型在這份資料中學到的關聯，不能單獨證明某種化學成分造成品質改變。多項式特徵也讓係數比原始 11 欄更難直接解讀。

## 步驟 9：預測測試資料

```python
y_pred = model.predict(X_test)
```

`y_pred` 是訓練好的 `model` 根據 `X_test` 算出的 480 筆預測品質。下一步會拿它和真正答案 `y_test` 比較。

形狀是：

```text
y_pred.shape == (480,)
```

例如：

```text
y_test 某筆真正答案：6
y_pred 對同一筆預測：5.72
誤差：6 - 5.72 = 0.28
```

### 為什麼會預測出小數？

因為線性迴歸輸出連續數值。不要直接把預測值四捨五入後再計算本課的 MSE 和 R²；這會改變老師要求評估的原始模型輸出。

## 步驟 10：使用 MSE 評估

```python
mse = mean_squared_error(y_test, y_pred)
print("Mean squared error:", mse)
```

`mse` 保存所有測試資料「預測誤差平方」的平均值。

假設只有三筆資料：

```text
真正答案 y_test：[5, 6, 7]
預測結果 y_pred：[4, 6, 9]
誤差：             [1, 0, -2]
誤差平方：         [1, 0, 4]
MSE = (1 + 0 + 4) / 3 = 1.67
```

判讀方式：

- MSE 最小值是 0，代表每一筆都完全預測正確。
- MSE 越小越好。
- 因為誤差被平方，大錯誤受到的懲罰較重。
- MSE 沒有一個適用所有資料集的固定及格線，必須與其他模型或基準結果比較。

## 步驟 11：使用 R² 評估

```python
r2 = r2_score(y_test, y_pred)
print("R2 score:", r2)
```

`r2` 表示模型相對於「每一筆都猜測測試集平均值」改善了多少。

判讀方式：

- `R² = 1`：完全預測正確。
- `R² = 0`：大致不比全部猜平均值好。
- `R² < 0`：比全部猜平均值還差。

R² 不是「正確率」。例如 `R² = 0.29` 不能說模型有 29% 的預測正確率。

## 可直接執行的完整版本

```python
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

# 1. 讀取完整資料。專案內這份 CSV 使用逗號分隔，因此不設定 sep=";"。
wine = pd.read_csv(
    "../附件/L4 課程範例檔/dataset/winequality-red.csv"
)

# 2. X 是模型輸入；y 是模型要預測的 quality。
X = wine.drop(columns="quality")
y = wine["quality"]

# 3. 從 11 個原始特徵建立平方項和兩兩交互項，共得到 77 個特徵。
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# 4. 70% 訓練、30% 測試；固定 random_state 讓結果可以重現。
X_train, X_test, y_train, y_test = train_test_split(
    X_poly,
    y,
    test_size=0.3,
    random_state=1,
)

# 5. scaler 只能從訓練資料學平均數與標準差。
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

# 6. 測試資料只能套用訓練集建立的規則，不能重新 fit。
X_test = scaler.transform(X_test)

# 7. model 從訓練資料學習特徵係數。
model = LinearRegression()
model.fit(X_train, y_train)

# 8. y_pred 儲存模型對 480 筆測試資料的預測。
y_pred = model.predict(X_test)

# 9. 用真正答案 y_test 和預測 y_pred 計算評估指標。
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("X 原始形狀：", X.shape)
print("X_poly 形狀：", X_poly.shape)
print("X_train 形狀：", X_train.shape)
print("X_test 形狀：", X_test.shape)
print("Coefficients：", model.coef_)
print("Mean squared error：", mse)
print("R² score：", r2)
```

使用目前專案中的資料與上述設定，結果大約是：

```text
X 原始形狀：(1599, 11)
X_poly 形狀：(1599, 77)
X_train 形狀：(1119, 77)
X_test 形狀：(480, 77)
MSE：約 0.431
R²：約 0.292
```

不同套件版本可能造成最後幾位小數略有不同，但 shape 應該一致。

## 怎麼讀這次的結果？

`MSE ≈ 0.431` 表示預測仍有誤差；它可以用來和其他模型比較，但不能直接翻譯成「平均差 0.431 分」，因為 MSE 使用的是平方誤差。

`R² ≈ 0.292` 表示這個模型相較於只猜平均品質，解釋了部分測試資料的變化，但表現不算特別強。這不是失敗：Part 1 的重點是建立一條正確、可檢查的建模流程，不是得到完美分數。

跑完後會拿到：

- 480 筆測試資料的預測分數 `y_pred`。
- 77 個多項式特徵的係數 `model.coef_`。
- 一個 MSE 和一個 R²，供我們評估及比較模型。

但這些數字不能證明：

- 「某成分必然造成品質提高」的因果結論。
- 對任何新紅酒都一定準確的保證。
- 可直接當成分類正確率的百分比。

## 最容易踩的坑

### 1. 用錯 CSV 分隔符

本專案資料是逗號分隔。讀取後一定檢查：

```python
assert wine.shape == (1599, 12)
```

### 2. 把 `quality` 留在 `X`

這會把答案洩漏給模型。`X` 應有 11 個原始欄位，不是 12 個。

### 3. 對測試集呼叫 `fit_transform()`

測試集只能 `transform()`。所有轉換規則都應由訓練集建立。

### 4. 忘記使用轉換後的資料

建立 `X_poly` 後，切分時必須傳入 `X_poly`，否則模型仍只會收到原始 11 個特徵。

### 5. 把 R² 當正確率

R² 衡量模型相對於平均值基準的解釋能力，不是答對幾成。

### 6. 覺得多項式一定比較好

增加欄位會提高模型表達能力，也會提高過度擬合風險。一定要看測試集指標，不能只看訓練集。

### 7. 把預測小數強制轉成整數

本課是迴歸。評估時應使用原始連續預測值，不要先四捨五入。

## 建議的一小時 Part 1 學習安排

### 0～10 分鐘：先建立全貌

先抓住這條主線：

```text
X 是輸入 → y 是答案 → 訓練模型 → 用測試集評估
```

不用先背演算法公式。

### 10～25 分鐘：跑到資料切分

依序執行：

```text
read_csv → X/y → PolynomialFeatures → train_test_split
```

每一步都印出 shape，確認 row 和 column 如何改變。

### 25～40 分鐘：理解標準化與訓練

確認自己能說出：

```text
X_train 可以 fit_transform
X_test 只能 transform
model.fit 使用 X_train 和 y_train
```

### 40～50 分鐘：理解預測與評估

比較 `y_test[:5]` 與 `y_pred[:5]`，實際看五筆答案和預測差多少：

```python
comparison = pd.DataFrame({
    "實際品質": y_test.to_numpy()[:5],
    "預測品質": y_pred[:5],
})

comparison
```

### 50～60 分鐘：不看答案重建流程

從空白 cell 寫出：

```text
讀資料 → X/y → 多項式 → 切分 → 標準化 → fit → predict → MSE/R²
```

卡住時只回頭看該步驟，不要整段複製。

## 最後用白話重講一次

我們先讀入 1,599 瓶紅酒。每瓶有 11 個化學特徵，以及一個已知的品質答案。接著把答案 `quality` 從輸入資料移除，避免模型偷看答案。

因為原始特徵之間可能有平方或搭配關係，我們用 `PolynomialFeatures` 把 11 個特徵擴充成 77 個。然後把資料分成訓練集與測試集，只用訓練集計算標準化規則，再把相同規則套到測試集。

`LinearRegression.fit()` 從訓練資料學出係數，`predict()` 使用這些係數預測 480 筆從未參與訓練的測試資料。最後，MSE 告訴我們平方誤差有多大，R² 告訴我們模型相較於只猜平均值改善多少。

這套流程假設 CSV 欄位已是可用數值、`quality` 可以當作連續目標，而且訓練集與測試集來自相近的資料分布。它不處理完整資料清理、不證明化學成分和品質之間的因果關係，也不保證模型能準確預測所有未來紅酒。

## Part 2 會在 Part 1 前面多做什麼？

Part 1 把所有多項式特徵交給線性迴歸。Part 2 會先用 Lasso 判斷哪些原始特徵值得保留，再進入類似的多項式、切分、標準化、訓練與評估流程。

因此，先把 Part 1 的資料生命週期弄懂：

```text
資料從哪裡來 → 每次轉換後 shape 是什麼 → 哪些資料可以參與 fit → 最後拿什麼評估
```

理解這條主線後，Part 2 只是多加入「先選哪些特徵」這個步驟。
