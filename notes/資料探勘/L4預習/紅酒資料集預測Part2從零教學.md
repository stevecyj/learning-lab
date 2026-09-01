# 紅酒資料集預測 Part 2：從零開始

## 這一課在做什麼？

**我們要先用 Lasso 從 11 個紅酒特徵中選出較有用的欄位，再用這些欄位建立二次多項式迴歸。**

Part 1 將 11 個原始特徵全部轉成二次多項式特徵，欄位數會由 11 增加到 77。Part 2 在前面加入「特徵選擇」，希望先減少特徵，再產生平方項和交互項。

用前端函式表示，概念類似：

```javascript
const selectedFeatures = lasso.select(originalFeatures)
const polynomialFeatures = createDegree2Features(selectedFeatures)
const predictedQuality = regressionModel.predict(polynomialFeatures)
```

Lasso 不會判定哪個化學成分「科學上一定無用」。它只是根據這份訓練資料、線性關係和我們設定的 `alpha`，將部分係數壓到 0。

## 完成 Part 2 後，你應該能回答

1. 為什麼不直接將 11 個特徵全部丟給多項式迴歸？
2. Lasso 和普通線性迴歸有什麼差別？
3. `alpha` 控制什麼？
4. `model.coef_ != 0` 為什麼會得到布林 mask？
5. `X_train.loc[:, mask]` 的 row 和 column 分別怎麼選？
6. 為什麼特徵選擇只能從訓練集學習？
7. 為什麼 Lasso 之前要標準化？
8. 特徵變少，是否代表預測一定更好？

## Part 1 和 Part 2 的差別

Part 1：

```text
11 個原始特徵
→ 二次多項式轉換
→ 77 個特徵
→ 線性迴歸
```

Part 2：

```text
11 個原始特徵
→ Lasso 特徵選擇
→ 保留較少的原始特徵
→ 二次多項式轉換
→ 線性迴歸
```

新增的關鍵問題是：

> 哪些輸入欄位值得留下來？

## Part 2 的完整流程

```text
讀取 CSV
→ 分離原始特徵 X 與答案 y
→ 先切分訓練集與測試集
→ 只用訓練集建立 Lasso 標準化規則
→ 用標準化後的訓練集訓練 Lasso
→ 找出非零係數，建立布林 mask
→ 訓練集與測試集使用同一個 mask
→ 建立二次多項式特徵
→ 只用訓練集建立第二組標準化規則
→ 訓練線性迴歸
→ 預測測試集
→ 用 MSE 和 R² 評估
```

## 先認識 Lasso

### 普通線性迴歸的任務

線性迴歸會找一組係數，使預測誤差盡量小：

```text
預測品質
= w₁ × fixed acidity
+ w₂ × volatile acidity
+ ...
+ w₁₁ × alcohol
+ 截距
```

`w₁` 到 `w₁₁` 是模型從訓練資料學到的係數。

### Lasso 多了一個限制

Lasso 除了希望預測誤差小，還會想辦法讓係數的絕對值變小。這個做法叫作 **L1 正則化**。

不必現在推導完整公式，先掌握結果：

```text
普通線性迴歸：主要追求訓練誤差小
Lasso：追求誤差小，同時壓縮特徵係數
```

當壓縮力量足夠，部分係數會變成 `0`。因此 Lasso 可以用來選擇特徵。

### `alpha` 是什麼？

```python
lasso = Lasso(alpha=0.1, max_iter=10000)
```

`alpha` 控制壓縮係數的力量：

- `alpha` 較大：壓縮較強，更多係數可能變成 0。
- `alpha` 較小：壓縮較弱，通常保留較多特徵。
- `alpha=0.1` 只是本課指定的示範值，不代表所有資料的最佳值。

正式專案應使用驗證集或交叉驗證選擇 `alpha`，不應根據最後測試集成績反覆調整。

## 為什麼 Lasso 之前要標準化？

紅酒欄位的量級差很多，例如：

```text
density                 約 1
pH                      約 3
total sulfur dioxide    可能數十到數百
```

Lasso 會直接對係數施加懲罰。若特徵的單位差很大，各係數的大小不能公平比較，選擇結果可能被測量單位影響。

```python
selection_scaler = StandardScaler()
X_train_scaled_for_lasso = selection_scaler.fit_transform(X_train)
X_test_scaled_for_lasso = selection_scaler.transform(X_test)
```

`selection_scaler` 儲存從 `X_train` 算出的每欄平均值與標準差。Lasso 下一步使用 `X_train_scaled_for_lasso`。

這裡雖然也轉換了測試集，但本課的 Lasso 只用來取得 mask，不需要用 `X_test_scaled_for_lasso` 訓練。保留這個轉換只是示範測試資料也必須使用同一規則。

## 步驟 1：匯入工具並讀取資料

```python
from pathlib import Path

import pandas as pd
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

data_path = Path("../附件/L4 課程範例檔/dataset/winequality-red.csv")
wine = pd.read_csv(data_path)

print(wine.shape)
wine.head()
```

`wine` 儲存 1,599 瓶紅酒的完整表格，值來自 CSV。下一步會將它分成輸入 `X` 和答案 `y`。

成功條件：

```text
wine.shape == (1599, 12)
```

## 步驟 2：分離 `X` 與 `y`

```python
X = wine.drop(columns="quality")
y = wine["quality"]

print(f"X.shape: {X.shape}")
print(f"y.shape: {y.shape}")
```

- `X` 儲存 11 個化學特徵，來自刪除 `quality` 後的 `wine`。
- `y` 儲存每瓶紅酒的正確品質分數，來自 `wine["quality"]`。

預期結果：

```text
X.shape == (1599, 11)
y.shape == (1599,)
```

## 步驟 3：先切分資料

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=1,
)
```

變數內容：

- `X_train`：給特徵選擇器和最後模型學習的輸入。
- `X_test`：保留到最後測試的輸入。
- `y_train`：`X_train` 對應的正確答案。
- `y_test`：`X_test` 對應的正確答案。

`test_size=0.3` 表示保留 30% 當測試集。`random_state=1` 讓每次切分結果相同。

### 為什麼必須先切分？

若先在完整 `X` 上訓練 Lasso，Lasso 就已經利用未來測試集的資料決定保留哪些欄位。這叫作資料洩漏。

正確契約是：

```text
所有會「學到資料規則」的步驟，都只能對訓練集 fit。
```

## 步驟 4：為 Lasso 標準化訓練資料

```python
selection_scaler = StandardScaler()
X_train_scaled_for_lasso = selection_scaler.fit_transform(X_train)
```

完整寫法是：

```python
selection_scaler.fit(X_train)
X_train_scaled_for_lasso = selection_scaler.transform(X_train)
```

- `fit(X_train)` 計算每個訓練欄位的平均值和標準差。
- `transform(X_train)` 將這組規則套用到訓練資料。
- `X_train_scaled_for_lasso` 是 NumPy 二維陣列，下一步交給 Lasso。

## 步驟 5：訓練 Lasso

```python
lasso = Lasso(alpha=0.1, max_iter=10000)
lasso.fit(X_train_scaled_for_lasso, y_train)
```

- `lasso` 儲存尚未訓練的 Lasso 模型。
- `lasso.fit(...)` 使用標準化訓練特徵和 `y_train` 學習 11 個係數。
- `max_iter=10000` 將最大迭代次數調高，降低尚未收旂就停止的機會。

可將係數和欄位名對齊：

```python
lasso_coefficients = pd.Series(lasso.coef_, index=X.columns)
print(lasso_coefficients)
```

`lasso_coefficients` 儲存「欄位名 → Lasso 係數」的對應。

## 步驟 6：建立布林 mask

```python
mask = lasso.coef_ != 0
selected_columns = X.columns[mask]

print(mask)
print(selected_columns.tolist())
```

先將壓縮語法改寫成完整邏輯：

```python
mask_values = []

for coefficient in lasso.coef_:
    if coefficient != 0:
        mask_values.append(True)
    else:
        mask_values.append(False)
```

`lasso.coef_ != 0` 是 NumPy 的向量化比較，它一次比較所有係數，產生和原始特徵數量相同的 `True`/`False` 陣列。

具體走一次：

```text
係數 = [0.12, 0.0, -0.08]
比較 = [0.12 != 0, 0.0 != 0, -0.08 != 0]
mask = [True, False, True]
```

結果會保留第 1 和第 3 個特徵，排除第 2 個。

## 步驟 7：對訓練集與測試集套用同一個 mask

```python
X_train_selected = X_train.loc[:, mask]
X_test_selected = X_test.loc[:, mask]
```

`DataFrame.loc` 的格式是：

```python
dataframe.loc[row_selector, column_selector]
```

所以：

```python
X_train.loc[:, mask]
```

表示：

- `:`：保留所有 row，也就是所有訓練紅酒。
- `mask`：只保留係數不是 0 的 column。

測試集不能自己重新選一次特徵。模型已經學會接收固定欄位，所以 `X_train_selected` 與 `X_test_selected` 必須有同樣的欄位及順序。

## 步驟 8：建立二次多項式特徵

```python
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train_selected)
X_test_poly = poly.transform(X_test_selected)
```

假設 Lasso 保留 `a`、`b`、`c` 三個特徵，二次轉換後會產生：

```text
a, b, c, a², a×b, a×c, b², b×c, c²
```

三個原始特徵會變成 9 個多項式特徵，而不是 Part 1 的 77 個。實際數量由 Lasso 選到幾個欄位決定。

可查看實際欄位名：

```python
print(poly.get_feature_names_out(selected_columns))
```

## 步驟 9：標準化多項式特徵

```python
poly_scaler = StandardScaler()
X_train_poly_scaled = poly_scaler.fit_transform(X_train_poly)
X_test_poly_scaled = poly_scaler.transform(X_test_poly)
```

`poly_scaler` 和前面的 `selection_scaler` 是兩個不同物件：

- `selection_scaler`：服務 Lasso，規則從 11 個原始特徵學到。
- `poly_scaler`：服務最後迴歸模型，規則從選擇後的多項式特徵學到。

它們的輸入欄位不同，不能混用。

## 步驟 10：訓練、預測與評估

```python
poly_model = LinearRegression()
poly_model.fit(X_train_poly_scaled, y_train)

y_pred = poly_model.predict(X_test_poly_scaled)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")
```

- `poly_model` 是線性迴歸模型；「多項式」來自前面輸入特徵的轉換。
- `fit(...)` 從訓練資料學習多項式特徵與品質分數之間的係數。
- `y_pred` 儲存模型對每筆測試紅酒的預測分數。
- MSE 越小越好。
- R² 越接近 1 越好；`0` 大致表示不比每次猜訓練平均值好。

MSE 和 R² 必須一起看，並與使用相同切分方式的其他模型比較。R² 不是「預測正確率」。

## 可直接執行的完整版本

```python
from pathlib import Path

import pandas as pd
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

# 1. 讀取資料
data_path = Path("../附件/L4 課程範例檔/dataset/winequality-red.csv")
wine = pd.read_csv(data_path)

# 2. 分離輸入特徵與答案
X = wine.drop(columns="quality")
y = wine["quality"]

# 3. 先切分，避免測試資料參與特徵選擇
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=1,
)

# 4. 用訓練集建立 Lasso 使用的標準化規則
selection_scaler = StandardScaler()
X_train_scaled_for_lasso = selection_scaler.fit_transform(X_train)

# 5. 訓練 Lasso
lasso = Lasso(alpha=0.1, max_iter=10000)
lasso.fit(X_train_scaled_for_lasso, y_train)

# 6. 取得非零係數對應的欄位
mask = lasso.coef_ != 0
selected_columns = X.columns[mask]

print(pd.Series(lasso.coef_, index=X.columns))
print(f"保留特徵數：{mask.sum()} / {len(mask)}")
print(f"保留欄位：{selected_columns.tolist()}")

# 7. 訓練集與測試集套用同一個 mask
X_train_selected = X_train.loc[:, mask]
X_test_selected = X_test.loc[:, mask]

# 8. 建立二次多項式特徵
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train_selected)
X_test_poly = poly.transform(X_test_selected)

print(f"原始特徵數：{X_train.shape[1]}")
print(f"Lasso 選擇後特徵數：{X_train_selected.shape[1]}")
print(f"二次多項式特徵數：{X_train_poly.shape[1]}")

# 9. 用訓練集建立多項式特徵的標準化規則
poly_scaler = StandardScaler()
X_train_poly_scaled = poly_scaler.fit_transform(X_train_poly)
X_test_poly_scaled = poly_scaler.transform(X_test_poly)

# 10. 訓練線性迴歸、預測與評估
poly_model = LinearRegression()
poly_model.fit(X_train_poly_scaled, y_train)
y_pred = poly_model.predict(X_test_poly_scaled)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")
```

## 怎麼讀這次的結果？

在本專案目前的 scikit-learn 版本、`random_state=1` 和 `alpha=0.1` 下，可能看到類似：

```text
保留特徵數：3 / 11
保留欄位：['volatile acidity', 'sulphates', 'alcohol']
二次多項式特徵數：9
MSE: 0.4060
R²: 0.3330
```

請將它讀成：

1. Lasso 在這個設定下留下 3 個原始特徵。
2. 三個原始特徵產生 9 個二次多項式特徵。
3. 模型在測試集的 MSE 約為 0.406，R² 約為 0.333。
4. 這只能說明這條建模流程的測試表現，不能證明三個欄位是紅酒品質的唯一原因。

不同套件版本或參數可能產生小幅差異，應以自己實際執行結果為準。

## 特徵變少不等於預測一定更好

Lasso 特徵選擇的可能優點：

- 減少之後的多項式欄位數。
- 模型較容易計算與解釋。
- 可能降低無用特徵造成的干擾與過度擬合。

但也可能：

- `alpha` 太大，排除了真正有用的特徵。
- Lasso 依據線性關係選擇原始特徵，可能漏掉只在非線性關係中有用的特徵。
- 特徵數變少，但測試集 MSE 不一定降低。

因此要比較的是「相同測試資料上的評估結果」，不是只看特徵數量。

## 最容易踩的坑

### 1. 在完整資料上做 Lasso 特徵選擇

壞點：測試資料參與了欄位選擇，後面的測試不再是真正未見資料。

正確順序：先 `train_test_split`，再只用 `X_train` 和 `y_train` 訓練 Lasso。

### 2. 未標準化就使用 Lasso 選特徵

壞點：欄位單位差異會影響係數懲罰，選擇結果不公平。

正確動作：先用只 fit 訓練集的 `StandardScaler` 轉換資料。

### 3. 訓練集和測試集各自選特徵

壞點：兩邊可能出現不同欄位或欄位順序，模型無法正確對應。

正確動作：從訓練集得到一個 `mask`，兩邊套用同一個 mask。

### 4. 把零係數解釋成科學上永遠無用

Lasso 的結果依賴資料、切分方式、標準化和 `alpha`。零係數只表示這個模型在當前設定下未保留它。

### 5. 把 `alpha` 當作越大越好

`alpha` 太大可能將所有係數都壓成 0，造成沒有特徵能進入後續模型。

### 6. 用測試集反覆挑 `alpha`

測試集應只用於最後評估。反覆根據測試分數選參數，就是間接對測試集過度擬合。

## 建議的一小時 Part 2 學習安排

### 0～15 分鐘：理解任務

- 畫出 Part 1 與 Part 2 流程。
- 用一句話說明 Lasso 為什麼能選特徵。
- 說明 `alpha` 變大對特徵數的一般影響。

### 15～30 分鐘：執行到 mask

- 讀取資料。
- 切分訓練與測試集。
- 標準化訓練特徵。
- 訓練 Lasso，印出係數和 mask。

### 30～45 分鐘：追蹤 shape

記錄下列變數的 shape：

```text
X_train
X_train_selected
X_train_poly
X_train_poly_scaled
```

確認 row 數沒有因特徵工程改變，只有 column 數改變。

### 45～55 分鐘：訓練與評估

- 完成多項式轉換和第二次標準化。
- 用線性迴歸 `fit()` 與 `predict()`。
- 說明 MSE 和 R² 的判斷方式。

### 55～60 分鐘：不看答案重建流程

只看下面關鍵字重建程式：

```text
read_csv
drop
train_test_split
StandardScaler
Lasso
coef_
mask
loc
PolynomialFeatures
LinearRegression
predict
MSE / R²
```

## 最後用白話重講一次

Part 2 先把紅酒資料分成訓練集和測試集，確保測試資料不會幫忙決定特徵。因為原始欄位單位不同，先只用訓練集建立標準化規則，再用 Lasso 學習係數。

Lasso 會壓縮係數，部分係數會成為 0。程式將非零係數轉成 `True`，零係數轉成 `False`，得到布林 mask。訓練集和測試集都使用這個 mask，所以會保留相同的欄位。

接著，程式將選中的欄位轉成二次多項式特徵，再次只用訓練集建立標準化規則。最後，線性迴歸從訓練資料學習，對從未參與學習的測試紅酒預測，並用 MSE 和 R² 評估。

這套邏輯假設 CSV 欄位為可用數值、沒有缺失值，並且 `alpha=0.1` 至少選到一個特徵。它不包含用交叉驗證選擇 `alpha`，也不證明被 Lasso 保留的特徵對品質有因果關係。
