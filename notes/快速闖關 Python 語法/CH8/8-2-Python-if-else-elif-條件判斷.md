# 8-2 Python `if`、`elif`、`else`：條件判斷與程式分流

## 學習目標

完成這一節後，我應該能夠：

1. 用 `if` 在條件成立時執行一段程式碼。
2. 用 `if` / `else` 寫出二選一的分流。
3. 用 `if` / `elif` / `else` 寫出多選一的分流。
4. 分辨「同一條 `if` / `elif` / `else` 決策鏈」與「多個獨立 `if`」。
5. 正確使用冒號與四個空白的縮排。
6. 理解數字等非布林值在條件中的真假性（truthiness）。

---

## 一、`if`：條件成立才執行

`if` 會先計算條件。條件為 `True` 時，才執行縮排區塊內的程式；為 `False` 時，直接跳過該區塊。

```python
grade = 80

if grade >= 70:
    print("pass")
```

此例中 `grade >= 70` 的結果是 `True`，因此輸出：

```text
pass
```

可以把流程想成：

```text
開始 → 判斷 grade >= 70？ → 是：印出 pass → 結束
                            └→ 否：直接結束
```

### 語法規則

```python
if 條件:
    條件成立時執行的程式碼
```

- `if` 後面要放條件，行尾一定要有冒號 `:`。
- 下一行開始的程式區塊要縮排；Python 慣例是 **4 個空白**。
- 同一個區塊的每一行必須使用一致的縮排。

```python
temperature = 32

if temperature > 30:
    print("天氣炎熱")
    print("記得補充水分")

print("檢查完成")
```

前兩個 `print()` 屬於 `if`；最後一個沒有縮排，不屬於 `if`，所以一定會執行。

參考：[Python 官方教學：`if` Statements](https://docs.python.org/3/tutorial/controlflow.html#if-statements)、[PEP 8：縮排](https://peps.python.org/pep-0008/#indentation)

---

## 二、`if` / `else`：強迫二選一

`else` 表示「前面的 `if` 條件不成立時」。有 `else` 的情況下，兩個區塊中**必定剛好執行一個**。

```python
grade = 80

if grade >= 70:
    print("pass")
else:
    print("fail")
```

| `grade >= 70` | 執行結果 |
| --- | --- |
| `True` | `print("pass")` |
| `False` | `print("fail")` |

例如把 `grade` 改成 `60`，條件為 `False`，輸出就會是 `fail`。

```python
grade = 95

if grade > 90:
    print("excellent")
else:
    print("you have to practice more")
```

這個結構適合「成功／失敗」、「已登入／未登入」、「合法／不合法」這種只有兩種結果的情況。

---

## 三、`elif`：在前一個條件不成立後再判斷

`elif` 是 `else if` 的縮寫。它只能接在 `if` 後面，用來追加條件。

```python
grade = 80

if grade >= 70:
    print("pass")
elif grade < 60:
    print("fail")
```

執行順序是：

1. 先判斷 `grade >= 70`。
2. 第一個條件為 `False`，才判斷 `grade < 60`。
3. 若兩個條件都不成立，因為沒有 `else`，便不輸出任何內容。

`if` / `elif` / `else` 是同一條決策鏈：從上到下找第一個成立的條件，執行它的區塊後便離開整條鏈。因此只要條件互斥，能做出多選一的結果。

```python
grade = 80

if grade > 90:
    print("excellent")
elif grade > 60:
    print("good")
elif grade > 30:
    print("so so")
else:
    print("you have to practice more")
```

| 分數範圍 | 輸出 |
| --- | --- |
| 大於 `90` | `excellent` |
| `61` 到 `90` | `good` |
| `31` 到 `60` | `so so` |
| `30` 以下 | `you have to practice more` |

> 條件的順序很重要。若先寫 `elif grade > 30:`，那麼 `80` 已在此成立，後面更嚴格的 `grade > 60` 或 `grade > 90` 就永遠沒有機會判斷。處理成績區間時，通常應從最高門檻往下寫。

官方文件指出，一條 `if` 敘述可以有零個或多個 `elif`，而 `else` 是選用的。[Python 官方教學：`if` Statements](https://docs.python.org/3/tutorial/controlflow.html#if-statements)

---

## 四、`elif` 和兩個獨立 `if` 不一樣

以下程式有兩個**獨立**的 `if`：

```python
grade = 95

if grade > 90:
    print("excellent")

if grade > 60:
    print("good")
```

輸出是：

```text
excellent
good
```

原因是兩個 `if` 各自都會判斷一次；`95 > 90` 和 `95 > 60` 都是 `True`。若 `grade = 30`，則兩個條件都不成立，什麼也不會輸出。

相對地，若要「符合其中一個等第後就停止往下選」，應寫成：

```python
if grade > 90:
    print("excellent")
elif grade > 60:
    print("good")
```

| 想要的邏輯 | 選擇 |
| --- | --- |
| 每個規則都要各自檢查，可能同時執行多個區塊 | 多個獨立 `if` |
| 多個候選結果中只選一個 | `if` / `elif` / `else` |

---

## 五、複合條件：`and`、`or`、`not`

條件也可以由多個比較組合而成：

```python
a = 200
b = 33
c = 500

if a > b or a > c:
    print("a 至少比其中一個值大")
```

常用邏輯運算子如下：

| 運算子 | 意義 | 何時為真 |
| --- | --- | --- |
| `and` | 而且 | 兩邊都為真 |
| `or` | 或者 | 至少一邊為真 |
| `not` | 否定 | 把真假反轉 |

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("可以入場")

if not has_ticket:
    print("請先購票")
```

混用時，`not` 的優先順序最高、`and` 次之、`or` 最後。例如：

```python
result = a > b or a > c and True
```

等同於：

```python
result = (a > b) or ((a > c) and True)
```

若條件開始難讀，請直接加括號，讓判斷順序一眼清楚。

---

## 六、條件不只接受 `True` 與 `False`

Python 會把條件轉成布林判斷。對數字來說，`0` 是 falsy（視為假），非零數字是 truthy（視為真）：

```python
if 2:
    print("2 是 truthy")

if 0:
    print("這一行不會執行")
else:
    print("0 是 falsy")
```

輸出：

```text
2 是 truthy
0 是 falsy
```

也可以先用 `bool()` 驗證：

```python
print(bool(2))  # True
print(bool(0))  # False
```

實務上，條件最好直接表達意圖，例如 `if grade >= 60:`，而不是依靠裸露的數字或難懂的真假性。常見 falsy 值還包含 `False`、空字串 `""`、空串列 `[]`、空字典 `{}` 與 `None`。

參考：[Python 官方文件：Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)

---

## 七、常見錯誤

### 1. 忘記冒號

```python
# 錯誤
if grade >= 60
    print("pass")
```

```python
# 正確
if grade >= 60:
    print("pass")
```

### 2. 忘記縮排

```python
# 錯誤：print 不在 if 區塊內
if grade >= 60:
print("pass")
```

```python
# 正確
if grade >= 60:
    print("pass")
```

### 3. 在需要多選一時寫成多個 `if`

```python
# grade = 95 時會輸出兩行，不是只輸出 excellent
if grade > 90:
    print("excellent")
if grade > 60:
    print("good")
```

若各等第只能選一個，把第二個 `if` 改為 `elif`。

### 4. 把 `=` 當成比較

```python
# 錯誤
# if grade = 60:

# 正確：== 才是比較是否相等
if grade == 60:
    print("剛好 60 分")
```

---

## 八、立即練習：折扣資格判斷

先不要執行，先預測每一組輸入會輸出什麼；再貼到 Notebook 執行驗證。

```python
age = 15
is_member = True

if age < 12:
    print("兒童票")
elif age >= 65:
    print("敬老票")
elif is_member:
    print("會員票")
else:
    print("全票")
```

依序把 `age` 與 `is_member` 改成以下組合：

1. `age = 10`、`is_member = False`
2. `age = 70`、`is_member = True`
3. `age = 30`、`is_member = True`
4. `age = 30`、`is_member = False`

再挑戰：把規則改成「會員票只提供給 12 到 64 歲的人」，並確認兒童與長者即使是會員，也不會落入會員票分支。

---

## 本節重點

1. `if`：條件為真才執行；條件為假就跳過。
2. `if` / `else`：二選一，必定執行其中一個區塊。
3. `if` / `elif` / `else`：從上往下檢查，整條鏈至多執行一個分支。
4. 多個 `if`：每個都獨立判斷，可能執行多個區塊，也可能都不執行。
5. 冒號與縮排是 Python 條件區塊的語法；慣例是每層四個空白。
6. `0` 是 falsy，非零數字是 truthy；但實作時應優先寫出明確的比較條件。
