# 4-3 Python 邏輯、成員、同一性與位元運算

## 學習目標

完成這一節後，我應該能夠：

1. 使用 `and`、`or` 與 `not` 組合條件，並理解短路求值。
2. 知道 `and` 與 `or` 回傳的是運算元之一，不一定是 `True` 或 `False`。
3. 使用 `in` 與 `not in` 檢查容器中的成員。
4. 分辨 `==` 的值相等與 `is` 的物件同一性。
5. 避免使用 `is` 比較數字、字串等一般值。
6. 使用 `&`、`|`、`^`、`~`、`<<` 與 `>>` 操作整數位元。
7. 在執行程式前，先預測結果，再用 `bin()`、`bool()`、`id()` 驗證心智模型。

---

## 一、先把四組運算分清楚

| 類別 | 運算子 | 回答的問題 |
| --- | --- | --- |
| 邏輯運算 | `and`、`or`、`not` | 條件如何組合？ |
| 成員測試 | `in`、`not in` | 某個值是否屬於容器？ |
| 同一性測試 | `is`、`is not` | 兩個名稱是否參照同一個物件？ |
| 位元運算 | `&`、`\|`、`^`、`~`、`<<`、`>>` | 整數的位元如何組合或移動？ |

字幕將 operator 稱為「運算元」，但兩者不同：

- operator 是運算子，例如 `and`、`in`、`is`、`&`。
- operand 是運算元，例如 `x and y` 中的 `x` 與 `y`。

---

## 二、邏輯運算：`and`、`or`、`not`

### 先從布林值理解

```python
x = True
y = False

print(x and y)  # False
print(x or y)   # True
print(not x)    # False
print(not y)    # True
```

若兩邊都是 `bool`：

- `x and y`：兩邊都為真才為真。
- `x or y`：至少一邊為真就為真。
- `not x`：反轉真假。

字幕中的 `not (x and y)` 會得到 `True`，因為 `x and y` 先得到 `False`，再由 `not` 轉成 `True`。若沒有括號，`not x and y` 表示 `(not x) and y`，是不同運算式。

### Truthiness：條件不只接受 `bool`

Python 會把物件放進真假情境中判斷。常見的 falsy 值包括：

```python
False
None
0
0.0
""
[]
{}
set()
```

非空字串、非空容器及大多數其他物件是 truthy。可以用 `bool()` 明確查看：

```python
print(bool(0))        # False
print(bool(""))       # False
print(bool("False"))  # True，因為它是非空字串
print(bool([0]))      # True，因為它是非空 list
```

### 專家會注意：`and` 與 `or` 不一定回傳 `bool`

`and` 與 `or` 會回傳其中一個原始運算元：

```python
print("" or "訪客")       # 訪客
print("Ada" or "訪客")    # Ada
print(3 and 5)             # 5
print(0 and 5)             # 0
```

規則可以寫成：

- `x and y`：若 `x` 為假，回傳 `x`；否則回傳 `y`。
- `x or y`：若 `x` 為真，回傳 `x`；否則回傳 `y`。
- `not x`：一定回傳布林值。

因此，若介面要求一定得到布林值，可以明確寫 `bool(expression)`。

### 短路求值

`and` 與 `or` 不一定會計算右側：

```python
denominator = 0

safe = denominator != 0 and 10 / denominator > 2
print(safe)  # False，右側除法沒有執行
```

- `and` 左側為假時，結果已確定，不計算右側。
- `or` 左側為真時，結果已確定，不計算右側。

這可用來先檢查前置條件，但不要把過多副作用藏在複雜的邏輯運算式裡。

---

## 三、成員測試：`in` 與 `not in`

字幕所說的「某個數字是否在某個數字裡」不精確。`in` 的右側通常是容器或其他支援成員測試的物件：

```python
number = 3
numbers = [1, 2, 3, 4]

print(number in numbers)      # True
print(8 in numbers)           # False
print(8 not in numbers)       # True
```

不同容器的成員語意不同：

```python
print("py" in "python")                       # True，檢查子字串
print("name" in {"name": "Ada"})             # True，dict 預設檢查鍵
print("Ada" in {"name": "Ada"})              # False，不是檢查值
print("Ada" in {"name": "Ada"}.values())     # True，明確檢查值
```

選擇容器時也要考慮查找方式。需要大量重複成員查找時，`set` 或 `dict` 通常比 list 更適合；但仍要看資料是否需要保留順序或重複元素，不必為一次查找改換資料結構。

```python
allowed_roles = {"admin", "editor", "viewer"}
role = "editor"

print(role in allowed_roles)  # True
```

---

## 四、同一性測試：`is` 與 `is not`

### `==` 比值，`is` 比是否為同一個物件

```python
first = [1, 2]
second = [1, 2]
alias = first

print(first == second)  # True，內容相等
print(first is second)  # False，不是同一個 list
print(first is alias)   # True，參照同一個 list
```

可以用 `id()` 觀察物件 identity：

```python
print(id(first) == id(alias))   # True
print(id(first) == id(second))  # False
```

`id()` 適合教學和除錯，不應拿來代替正常的值比較。

### 字幕中的整數範例不能當成規則

```python
x = 2
y = 2
print(x is y)
```

這行在常見 Python 實作與執行情境中可能顯示 `True`，原因可能涉及物件重用、常數折疊或整數快取；這不是「值相等就一定是同一個物件」的語言規則。不要依賴這個結果：

```python
print(x == y)  # 比較數值時應該這樣寫
```

`is` 最常見且正確的日常用途，是和 `None` 這類 singleton 比較：

```python
result = None

if result is None:
    print("尚無結果")

if result is not None:
    print("已有結果")
```

實務規則：

- 比較值：使用 `==`、`!=`。
- 比較 `None`：使用 `is None`、`is not None`。
- 只有真的在意兩個參照是否指向同一物件時，才使用 `is`。

---

## 五、位元運算：先把整數寫成二進位

假設：

```python
x = 10  # 0b1010
y = 4   # 0b0100
```

`0b` 是二進位整數字面值的前綴，不是位元本身。可以用 `bin()` 查看整數的二進位表示：

```python
print(bin(10))  # 0b1010
print(bin(4))   # 0b100
```

為了逐位對齊，可將 `4` 想成四位的 `0100`。

### AND、OR 與 XOR

```text
  1010  (10)
  0100  ( 4)
```

| 運算 | 符號 | 位元規則 | 二進位結果 | 十進位結果 |
| --- | --- | --- | --- | ---: |
| AND | `&` | 兩個位元都是 1 才是 1 | `0000` | `0` |
| OR | `\|` | 至少一個位元是 1 | `1110` | `14` |
| XOR | `^` | 兩個位元不同才是 1 | `1110` | `14` |

```python
print(10 & 4)  # 0
print(10 | 4)  # 14
print(10 ^ 4)  # 14
```

這個例子中 OR 與 XOR 剛好都是 `14`，因為 `10` 與 `4` 沒有位置同時為 `1`。它們不是相同運算：

```python
print(6 | 3)  # 7：110 | 011 = 111
print(6 ^ 3)  # 5：110 ^ 011 = 101
```

### NOT

位元 NOT 使用 `~`：

```python
print(~10)  # -11
```

對 Python 整數，`~x` 等於 `-(x + 1)`。結果不是把畫面上的四個位元 `1010` 反轉成 `0101`；Python 整數沒有固定的 4 位或 8 位寬度。若需求是固定寬度遮罩，必須明確套用 mask：

```python
mask = 0b1111
print((~10) & mask)  # 5，只保留低 4 位
```

### 左移與右移

```python
print(10 << 2)  # 40
print(10 >> 2)  # 2
```

對非負整數，可以直觀理解為：

```text
1010 << 2  -> 101000  -> 40
1010 >> 2  -> 10      -> 2
```

對 Python 整數：

- `x << n` 等於 `x * 2 ** n`。
- `x >> n` 等於 `x // 2 ** n`。
- 位移量 `n` 必須是非負整數，負數會引發 `ValueError`。

第二條也適用於負整數，因此右移不是對所有數字都能簡化成「砍掉右邊幾位」：

```python
print(-10 >> 2)       # -3
print(-10 // 2 ** 2)  # -3
```

---

## 六、不要混淆邏輯運算與位元運算

| 邏輯運算 | 位元運算 |
| --- | --- |
| `and`、`or`、`not` | `&`、`\|`、`^`、`~` |
| 根據 truthiness 選擇結果 | 對整數的對應位元操作 |
| `and`、`or` 會短路 | 兩側運算元都會求值 |
| 常用於條件與預設值 | 常用於旗標、遮罩、權限與二進位格式 |

```python
print(10 and 4)  # 4
print(10 & 4)    # 0
```

即使 `bool` 也支援部分位元運算，撰寫一般條件時仍優先使用 `and`、`or`、`not`，才能清楚表達意圖並取得短路行為。混合多種運算子時，括號通常比背完整優先順序更安全、更易讀。

---

## 七、字幕內容需要修正或補充的地方

1. **operator 應譯為運算子**：operand 才是運算元。
2. **`and` 與 `or` 不只接受 `True`、`False`**：它們依物件的 truthiness 判斷，並回傳其中一個運算元。
3. **`not` 的範例應加括號**：`not (x and y)` 能清楚表示先做 `and`；`not x and y` 是另一個運算式。
4. **Membership 不是「數字是否在數字裡」**：它測試左側值是否為右側容器的成員。
5. **`dict` 的 `in` 預設檢查鍵**：若要檢查值，要明確使用 `.values()`。
6. **不能用小整數推導 `is` 的一般規則**：整數快取或常數重用是實作細節，不該成為程式正確性的依據。
7. **值相等應使用 `==`**：`is` 是同一性測試，最常用於 `None`。
8. **兩個分別建立且內容相同的 list 通常 `==` 為真、`is` 為假**：這正好說明值與 identity 不同。
9. **OR 與 XOR 在 `10`、`4` 的結果剛好相同**：換成有重疊 `1` 位元的數字，結果便不同。
10. **位元運算還包括 `~`**：字幕漏掉位元 NOT。
11. **右移不宜一律說成砍掉位元**：對 Python 負整數，應以 `x // 2 ** n` 理解。
12. **Python 整數不是固定寬度**：解釋 `~` 與負數位元運算時，不能擅自假設只有 4 位或 8 位。

---

## 八、Python 專家會關注的點

### 1. 運算式回傳的是什麼型別與物件

看到 `and`、`or` 時，不只問真假，也要問最後回傳哪一個運算元。使用 `value or default` 很方便，但若 `0`、`""` 或空容器是合法資料，它們也會被換成預設值，可能造成錯誤。

### 2. 短路是否保護了危險操作

將便宜且安全的檢查放左側，再把可能失敗或昂貴的操作放右側，例如先檢查除數不為零、物件不為 `None`。同時保持條件簡單，避免讀者必須追蹤隱藏副作用。

### 3. 容器的成員語意與資料結構

`in` 對字串、list、set、dict 的意義不同；dict 預設查鍵。若查找頻繁，應評估 `set` 或 `dict`，而不是在大型 list 中一再線性搜尋。

### 4. Identity 絕不是 value equality 的捷徑

物件快取會讓錯誤的 `is` 比較偶爾看似正常，因而特別危險。程式若關心內容就用 `==`；只有 sentinel 或真正的別名判斷才使用 `is`。

### 5. 位元運算需要明確的位寬與遮罩

通訊協定、檔案格式或權限旗標通常規定位寬。Python 整數本身不限固定位數，因此取反、截斷或輸出時要明確套用 mask，不能只看 `bin()` 顯示猜測。

### 6. 可讀性優先於炫技

一般條件使用邏輯運算；只有問題本身確實是位元旗標或遮罩時才使用位元運算。混合比較、邏輯與位元運算時加括號，讓意圖不用靠背誦優先順序才能理解。

---

## 九、我能立即執行的步驟

在專案根目錄啟動 JupyterLab：

```bash
uv run jupyter lab
```

每個實驗先在 Markdown Cell 寫預測，再執行 Code Cell，最後記錄「預測與結果不同的原因」。

### 步驟 1：建立邏輯運算真值表

```python
values = [False, True]

for x in values:
    for y in values:
        print(x, y, x and y, x or y)

for x in values:
    print(x, not x)
```

### 步驟 2：觀察回傳值與短路求值

```python
print("" or "預設名稱")
print("Ada" or "預設名稱")
print(0 and 10)
print(3 and 10)

denominator = 0
print(denominator != 0 and 10 / denominator > 1)
```

逐行寫下結果的值與型別，並解釋為什麼最後一行沒有 `ZeroDivisionError`。

### 步驟 3：比較四種容器的成員測試

```python
print(3 in [1, 2, 3])
print("py" in "python")
print("name" in {"name": "Ada"})
print("Ada" in {"name": "Ada"}.values())
print(9 not in {1, 3, 5, 7})
```

### 步驟 4：用 list 分辨 `==` 與 `is`

```python
first = [1, 2]
second = [1, 2]
alias = first

print(first == second)
print(first is second)
print(first == alias)
print(first is alias)
```

接著執行 `first.append(3)`，預測 `second` 與 `alias` 各自會看到什麼。

### 步驟 5：逐位計算 AND、OR、XOR

```python
x = 10
y = 4

print(f"x     = {x:04b}")
print(f"y     = {y:04b}")
print(f"x & y = {x & y:04b} = {x & y}")
print(f"x | y = {x | y:04b} = {x | y}")
print(f"x ^ y = {x ^ y:04b} = {x ^ y}")
```

把 `x`、`y` 改成 `6`、`3`，觀察 OR 與 XOR 不再相等。

### 步驟 6：驗證位移和乘除法的關係

```python
for x in [10, -10]:
    for n in [0, 1, 2, 3]:
        print(
            x,
            n,
            x << n,
            x * 2 ** n,
            x >> n,
            x // 2 ** n,
        )
```

核對每一列的左移結果與乘法是否相同，右移結果與向下取整除法是否相同。

### 步驟 7：做一個實用權限旗標

```python
READ = 0b001
WRITE = 0b010
EXECUTE = 0b100

permissions = READ | WRITE

can_read = bool(permissions & READ)
can_write = bool(permissions & WRITE)
can_execute = bool(permissions & EXECUTE)

print(can_read, can_write, can_execute)
```

再加入執行權限：

```python
permissions = permissions | EXECUTE
print(f"{permissions:03b}")  # 111
```

移除寫入權限：

```python
permissions = permissions & ~WRITE
print(f"{permissions:03b}")  # 101
```

## 實作檢查清單

- [ ] 寫出 `and`、`or`、`not` 的真值表
- [ ] 找出四個 falsy 值與四個 truthy 值
- [ ] 說明 `and`、`or` 回傳哪個運算元
- [ ] 用短路避免一次除以零
- [ ] 對 list、字串、dict 與 set 各做一次 `in` 測試
- [ ] 說明 dict 的 `in` 預設檢查什麼
- [ ] 用 list 示範 `==` 與 `is` 的差異
- [ ] 使用 `is None` 寫一個條件
- [ ] 手算並執行 `10 & 4`、`10 | 4`、`10 ^ 4`
- [ ] 比較 `6 | 3` 與 `6 ^ 3`
- [ ] 驗證正數與負數的位移規則
- [ ] 完成三種權限旗標的新增、檢查與移除
- [ ] 不看筆記回答下方複習題

---

## 十、複習題

先收起參考答案，從記憶回答：

1. `and`、`or`、`not` 是否都一定回傳 `bool`？
2. `"" or "guest"` 與 `3 and 5` 分別得到什麼？
3. 什麼是短路求值？
4. 為什麼 `bool("False")` 是 `True`？
5. `"name" in {"name": "Ada"}` 與 `"Ada" in {"name": "Ada"}` 分別得到什麼？
6. `==` 與 `is` 的問題有何不同？
7. 為什麼不能用 `x is 2` 比較數值？
8. 比較 `None` 的建議寫法是什麼？
9. `10 & 4`、`10 | 4`、`10 ^ 4` 分別是多少？
10. 為什麼上一題的 OR 與 XOR 結果相同，卻不能視為同一運算？
11. `10 << 2` 與 `10 >> 2` 分別是多少？
12. `~10` 是多少？若只想反轉最低四個位元，應如何處理？
13. `-10 >> 2` 是多少？應用哪個算式理解？
14. `and` 與 `&` 有哪兩個重要差異？
15. 以下程式依序輸出什麼？

```python
first = [1, 2]
second = [1, 2]
alias = first

print(first == second)
print(first is second)
print(first is alias)
```

<details>
<summary>參考答案</summary>

1. 不是。`and` 與 `or` 回傳其中一個原始運算元；`not` 回傳 `bool`。
2. 分別是字串 `"guest"` 與整數 `5`。
3. 當左側已足以決定 `and` 或 `or` 的結果時，Python 不再計算右側。`and` 左側為假時停止；`or` 左側為真時停止。
4. 因為 `"False"` 是包含字元的非空字串；字串內容看起來像布林值，不會改變其 truthiness。
5. 分別是 `True` 與 `False`。dict 的 `in` 預設檢查鍵，不是值。
6. `==` 問兩個物件的值是否相等；`is` 問兩個參照是否指向同一個物件。
7. Python 實作可能重用某些整數物件，讓 `is` 偶爾看似可用，但這不是值相等的規則。比較數值應使用 `x == 2`。
8. 使用 `value is None` 或 `value is not None`。
9. 分別是 `0`、`14`、`14`。
10. `10` 的 `1010` 與 `4` 的 `0100` 沒有共同為 `1` 的位置，所以 OR 與 XOR 在這組輸入碰巧相同。若改用 `6` 與 `3`，OR 是 `7`，XOR 是 `5`。
11. 分別是 `40` 與 `2`。
12. `~10` 是 `-11`。只保留最低四位可用遮罩：`(~10) & 0b1111`，結果為 `5`。
13. 結果是 `-3`；用 `-10 // 2 ** 2` 理解。
14. `and` 根據 truthiness 回傳運算元之一，而且會短路；`&` 對整數逐位運算，而且兩側都會求值。
15. 依序是 `True`、`False`、`True`。前兩個 list 內容相等但不是同一物件；`alias` 與 `first` 參照同一個 list。

</details>

---

## 本節重點

> `and`、`or` 組合真假情境並可能短路；`in` 測成員；`==` 比值，`is` 比同一物件；位元運算則處理整數的二進位位置。先確認問題類型，再選符號。

這些運算會用在輸入驗證、空值處理、權限檢查、條件分支與二進位資料處理。練習時除了記錄結果，也要說出結果的型別、是否短路、比較的是值還是 identity，以及位元寬度是否有明確限制。

## Python 官方參考資料

- [Python Expressions：Boolean operations](https://docs.python.org/3/reference/expressions.html#boolean-operations)
- [Python Expressions：Comparisons、membership 與 identity](https://docs.python.org/3/reference/expressions.html#comparisons)
- [Python Expressions：Binary bitwise operations](https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations)
- [Python Expressions：Shifting operations](https://docs.python.org/3/reference/expressions.html#shifting-operations)
- [Python Standard Type Hierarchy：Integers](https://docs.python.org/3/reference/datamodel.html#numbers-integral)
- [Python Built-in Functions：`bin()`、`bool()` 與 `id()`](https://docs.python.org/3/library/functions.html)
