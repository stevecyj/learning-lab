# 3-4 BMI 與圓面積計算練習

## 學習目標

完成這一節後，我應該能夠：

1. 把文字題目拆成輸入、計算與輸出三個步驟。
2. 使用 `/`、`*`、`**` 與括號正確表達數學公式。
3. 在計算前把 `input()` 回傳的字串轉成 `float`。
4. 分辨公分與公尺，先統一單位再計算 BMI。
5. 使用清楚的變數名稱，避免把 `weight` 誤寫成 `width`。
6. 驗證身高、體重與半徑必須是有效的正數。
7. 用測試資料與手算結果檢查程式是否合理。

---

## 一、先把題目翻譯成程式步驟

這一節有兩個練習：

1. 輸入身高與體重，計算 BMI。
2. 輸入圓的半徑，計算圓面積。

兩題都可以使用同一個解題骨架：

```text
讀取輸入
→ 統一單位並轉成數字
→ 套用公式
→ 顯示結果
```

寫程式前，先回答四個問題：

1. 使用者要提供哪些資料？
2. 每項資料的單位是什麼？
3. 要使用哪個公式？
4. 結果要顯示幾位小數及什麼單位？

先拆解步驟，比直接把公式寫成一長行更容易檢查。

---

## 二、練習一：計算 BMI

BMI 的公制公式是：

```text
BMI = 體重（公斤）÷ 身高（公尺）的平方
```

用 Python 表示：

```python
bmi = weight_kg / (height_m * height_m)
```

也可以使用 `**` 表示次方：

```python
bmi = weight_kg / height_m**2
```

兩種寫法的結果相同。第二種寫法更接近數學公式：

```text
height_m**2 = height_m 的 2 次方
```

### 為什麼括號很重要？

下面兩行看起來接近，意思卻不同：

```python
correct_bmi = weight_kg / (height_m * height_m)
wrong_bmi = weight_kg / height_m * height_m
```

`*` 與 `/` 的優先順序相同，會由左向右計算。因此第二行等同於：

```python
wrong_bmi = (weight_kg / height_m) * height_m
```

在 `height_m` 不為零時，除掉又乘回去，結果就是原本的 `weight_kg`，並不是 BMI。括號在這裡用來表達公式的結構。

### 單位必須先統一

公式要求身高使用「公尺」。如果身高是 `179` 公分，要先轉成 `1.79` 公尺：

```python
height_cm = 179
height_m = height_cm / 100
```

如果直接把 `179` 當作公尺代入，平方後的分母會放大一萬倍，答案就會嚴重錯誤。

以體重 `68.7` 公斤、身高 `179` 公分為例：

```python
height_cm = 179
weight_kg = 68.7

height_m = height_cm / 100
bmi = weight_kg / height_m**2

print(f"BMI：{bmi:.2f}")
```

輸出：

```text
BMI：21.44
```

### 完整互動版本

```python
height_cm = float(input("請輸入身高（公分）："))
weight_kg = float(input("請輸入體重（公斤）："))

if height_cm <= 0 or weight_kg <= 0:
    print("輸入錯誤：身高與體重必須大於 0。")
else:
    height_m = height_cm / 100
    bmi = weight_kg / height_m**2
    print(f"BMI：{bmi:.2f}")
```

這個版本讓使用者輸入較熟悉的公分，再由程式轉成公尺。變數名稱也包含單位：

- `height_cm`：以公分表示的身高。
- `height_m`：以公尺表示的身高。
- `weight_kg`：以公斤表示的體重。

這比只寫 `height`、`weight` 更不容易混用單位。

### BMI 的用途與限制

這一題的重點是練習程式輸入、單位換算與公式，不是進行醫療診斷。BMI 是根據身高與體重計算的篩檢指標，不能直接測量體脂，也應搭配其他健康資訊解讀；兒童與成人的解讀方式也不同。

---

## 三、練習二：計算圓面積

圓面積公式是：

```text
圓面積 = π × 半徑²
```

用 Python 表示：

```python
area = pi * radius**2
```

字幕中的入門版本把圓周率設為 `3.14`：

```python
radius = float(input("請輸入圓的半徑："))
pi = 3.14
area = pi * radius**2

print(f"圓面積：{area}")
```

使用 `float()` 是因為 `input()` 一定回傳 `str`。只有先轉成數字，才能進行乘法與次方運算。

### 使用標準函式庫的 `math.pi`

一般 Python 程式不必自己把 π 寫成 `3.14`，可以使用標準函式庫提供的 `math.pi`：

```python
import math

radius = float(input("請輸入圓的半徑："))

if radius <= 0:
    print("輸入錯誤：半徑必須大於 0。")
else:
    area = math.pi * radius**2
    print(f"圓面積：{area:.2f}")
```

`math.pi` 提供以浮點數表示的 π 近似值，比手動寫 `3.14` 更精確，也能讓讀者一眼看出這是圓周率。

這裡把 `radius <= 0` 視為錯誤，是因為練習假設要計算一般、非退化的圓。純數學工具若允許半徑為零，可以改成只拒絕 `radius < 0`。輸入規則應由程式用途決定，不必在所有情況套用同一條規則。

### 核對教材中的數字

當半徑為 `3`，並使用 `3.14` 時：

```text
3.14 × 3² = 3.14 × 9 = 28.26
```

所以結果應是 `28.26`，不是字幕中的 `28.25`。

若使用 `math.pi`：

```python
import math

print(math.pi * 3**2)  # 約 28.2743338823
```

格式化成小數點後兩位會顯示：

```text
28.27
```

當半徑為 `5`、π 使用 `3.14` 時，面積為：

```text
3.14 × 5² = 78.5
```

這與字幕中的第二個結果相符。

---

## 四、字幕內容中需要特別修正的地方

### 1. `width` 應是 `weight`

字幕把 BMI 公式說成 `width` 除以身高平方。`width` 是「寬度」，BMI 需要的是「體重」，正確名稱應為：

```python
weight_kg
```

變數名稱不只要讓 Python 能夠執行，還應讓讀者知道資料代表什麼。

### 2. `179` 是公分，不是公尺

如果題目要求公尺，應直接輸入 `1.79`；若輸入 `179`，程式就必須先除以 `100`。

### 3. BMI 分母需要完整平方

應寫成：

```python
weight_kg / (height_m * height_m)
```

或：

```python
weight_kg / height_m**2
```

不能省略必要的括號後寫成 `weight_kg / height_m * height_m`。

### 4. 圓面積應是 πr²

字幕中的「r 平 π」應理解為：

```text
π × r²
```

而不是其他排列不明的公式。

### 5. 半徑 3 的教材答案算錯了

使用 `3.14` 時應為 `28.26`。看到教材答案時仍要用手算、另一種寫法或測試資料交叉核對。

---

## 寫計算程式時的檢查重點

1. **公式與單位必須一起確認**：公式正確但單位錯誤，仍會得到毫無意義的答案。
2. **名稱要包含資料意義**：`weight_kg`、`height_cm` 與 `radius` 比 `a`、`b` 或誤寫的 `width` 清楚。
3. **輸入是程式邊界**：`input()` 回傳字串，而且使用者可能輸入文字、零或負數，因此要轉型與驗證。
4. **計算和顯示要分開**：先保留完整精度完成計算，最後才用 `:.2f` 控制顯示。
5. **常數要有可信來源**：練習可以使用 `3.14`，實際 Python 程式通常使用 `math.pi`。
6. **測試不能只挑一組數字**：至少測試一般值、小數、零、負數與無法轉型的文字。
7. **錯誤結果也可能看起來合理**：程式能執行不代表公式正確，應先估算結果範圍再比對。
8. **BMI 只是篩檢指標**：健康領域的程式要避免把單一數字包裝成診斷結論。
9. **教材也需要驗算**：字幕可能有口誤或轉錄錯誤，應以可驗證的公式與測試為準，不能只依賴影片給出的結果。

### 進一步驗證特殊數值

目前先檢查數值大於零就足以完成練習。更嚴格的程式還會排除 `NaN` 與無限大：

```python
import math

value = float(input("請輸入數值："))

if not math.isfinite(value) or value <= 0:
    print("輸入錯誤：請輸入有限的正數。")
```

這是進階防護，不必在第一次練習時一次記住。

---

## 實作步驟

### 1. 啟動本專案的 JupyterLab

```bash
uv run jupyter lab
```

建立一個新的 Notebook，把 BMI 與圓面積分成兩組 Cell。

### 2. 先完成固定數值版本

不要先處理輸入，先確認公式：

```python
height_cm = 179
weight_kg = 68.7
height_m = height_cm / 100
bmi = weight_kg / height_m**2

print(f"BMI：{bmi:.2f}")
```

預期結果：

```text
BMI：21.44
```

### 3. 比較正確與錯誤的括號

```python
height_m = 1.79
weight_kg = 68.7

print(weight_kg / (height_m * height_m))
print(weight_kg / height_m * height_m)
```

執行前先預測兩行是否相同，再解釋第二行為何接近 `68.7`。

### 4. 把固定數值改成使用者輸入

```python
height_cm = float(input("請輸入身高（公分）："))
weight_kg = float(input("請輸入體重（公斤）："))
```

保留原本的單位換算與 BMI 公式，依序測試：

```text
179、68.7
165.5、52.3
0、68.7
abc、68.7
```

### 5. 比較 `3.14` 與 `math.pi`

```python
import math

radius = 3

print(3.14 * radius**2)
print(math.pi * radius**2)
```

觀察兩者的差異，再分別格式化成小數點後兩位。

### 6. 加入錯誤處理

把上一節學過的 `try`、`except ValueError` 與正數驗證加入兩個程式。錯誤訊息要說明是哪一項資料、需要什麼格式。

### 7. 將計算整理成函式

等熟悉函式後，可以把輸入和計算分開：

```python
def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return weight_kg / height_m**2
```

這樣便能在沒有 `input()` 的情況下直接測試多組資料。

## 練習檢查清單

- [ ] 執行 `uv run jupyter lab`
- [ ] 用 `179` 公分與 `68.7` 公斤算出 BMI `21.44`
- [ ] 比較有括號與沒有括號的 BMI 算式
- [ ] 用自己的話解釋為什麼公分要除以 `100`
- [ ] 把 BMI 程式改成接受 `input()`
- [ ] 驗證身高與體重都必須大於零
- [ ] 用半徑 `3` 驗算 `3.14 × r²` 等於 `28.26`
- [ ] 比較 `3.14` 與 `math.pi` 的計算結果
- [ ] 測試輸入 `abc` 時發生的 `ValueError`
- [ ] 不看筆記回答下方複習題

---

## 複習題

先關掉參考答案，從記憶回答：

1. BMI 的公制公式是什麼？身高與體重各使用什麼單位？
2. 身高 `179` 公分要如何轉成公尺？
3. 為什麼 `weight_kg / height_m * height_m` 不是正確的 BMI 算式？
4. `height_m * height_m` 可以用哪個次方運算式代替？
5. 為什麼 `input()` 外面需要使用 `float()`？
6. `width` 與 `weight` 在這份練習中有何不同？
7. 圓面積公式如何用 Python 表示？
8. 半徑為 `3`、π 使用 `3.14` 時，圓面積是多少？
9. `3.14` 與 `math.pi` 有何差別？
10. 為什麼程式成功執行，仍不能證明答案正確？
11. 為什麼 BMI 程式不應把計算結果直接當成醫療診斷？

<details>
<summary>參考答案</summary>

1. `BMI = 體重（公斤）/ 身高（公尺）²`；體重使用公斤，身高使用公尺。
2. 除以 `100`：`height_m = 179 / 100`，結果是 `1.79` 公尺。
3. 因為 `*` 與 `/` 會由左向右計算，它等同 `(weight_kg / height_m) * height_m`，不是用身高平方當分母。
4. 可以寫成 `height_m**2`。
5. 因為 `input()` 回傳 `str`；必須先轉成數字，才能進行除法、乘法與次方運算。
6. `width` 是寬度，`weight` 才是體重；BMI 公式需要的是體重。
7. 可以寫成 `area = math.pi * radius**2`；若題目指定 π 為 `3.14`，則寫成 `area = 3.14 * radius**2`。
8. `3.14 × 3² = 28.26`。
9. `3.14` 是手動輸入的近似值；`math.pi` 是 Python 標準函式庫提供、精度更高且意義更清楚的 π 常數。
10. 程式只會忠實執行寫下的指令；如果公式、單位或括號寫錯，仍可能順利產生一個錯誤數字。
11. BMI 是篩檢指標，不直接測量體脂，個人健康還要搭配其他資料並由合適的專業人員解讀。

</details>

---

## 本節重點

這一節最重要的流程是：

> 讀取輸入 → 確認單位 → 轉成數字 → 驗證範圍 → 套用有正確括號的公式 → 格式化輸出 → 用已知答案驗算。

這兩個練習的重點，是把自然語言、單位與公式準確翻譯成程式。若結果和預期不同，檢查時應一併提供輸入、公式、實際輸出與手算過程。

## 官方參考資料

- [Python 3.11：`input()` 與 `float()`](https://docs.python.org/3.11/library/functions.html)
- [Python 3.11：運算式與運算子優先順序](https://docs.python.org/3.11/reference/expressions.html#operator-precedence)
- [Python 3.11：`math.pi`](https://docs.python.org/3.11/library/math.html#math.pi)
- [CDC：About Body Mass Index](https://www.cdc.gov/bmi/about/index.html)
- [CDC：BMI Frequently Asked Questions](https://www.cdc.gov/bmi/faq/index.html)
