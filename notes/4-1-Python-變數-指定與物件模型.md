# 4-1 Python 變數、指定與物件模型

## 學習目標

完成這一節後，我應該能夠：

1. 用「名稱綁定到物件」解釋 `a = 9`，而不只把變數想成裝值的盒子。
2. 分辨指定目標、運算子（operator）與運算元（operand）。
3. 使用 `type()`、`id()`、`==` 與 `is` 觀察物件的型別、身分、值與同一性。
4. 理解連鎖指定與多重指定的執行方式。
5. 準確說明 Python 的動態型別：物件有型別，名稱可以改綁定到不同型別的物件。
6. 預測共用可變物件時會發生的別名（aliasing）效果。

---

## 一、變數的精確心智模型

教材將變數說成「用來儲存數值的記憶體」，這適合當入門比喻，但 Python 更精確的模型是：

> 名稱（name）參照物件（object）；指定會建立或改變這個綁定關係。

```python
a = 9
```

可以分成兩件事：

1. Python 求值右側運算式 `9`，取得值為 `9` 的 `int` 物件。
2. 名稱 `a` 被綁定到該物件。

```text
a ──參照──> int 物件 9
```

這也解釋了為什麼同一個名稱之後可以指向別的物件：

```python
a = 9
a = "hello"
```

第二行不是把 `9` 轉換成字串，也不是改變原本整數物件的型別；它是讓 `a` 改為綁定到另一個 `str` 物件。

### 變數本身不是物件

Python 的資料由物件表示，但不應簡化成「每個變數都是物件」。在 `a = 9` 中：

- `a` 是名稱。
- `9` 是 `int` 物件的字面表示。
- 名稱 `a` 參照該物件。

之後學習 `list`、`dict`、函式參數與物件共用時，這個區別會非常重要。

---

## 二、`=` 在這裡是指定語句的語法

```python
total = 3 + 6
```

Python 會先求值右側 `3 + 6`，再讓左側目標 `total` 指向結果 `9`。

教材將 `=` 稱為「運算子」是常見口語，但 Python 語言參考將普通 `=` 這類語法放在「assignment statements」中說明。在初學階段，最重要的是不要把它和相等比較 `==` 混淆：

```python
a = 9          # 指定：讓 a 指向 9
print(a == 9)  # 比較值：True
```

### operator 與 operand

在一般運算式中：

```python
3 + 6
```

- `+` 是運算子（operator）。
- `3` 與 `6` 是運算元（operands）。

在 `total = 3 + 6` 中，`total` 更適合稱為指定目標（assignment target），右側整體是一個運算式。

---

## 三、連鎖指定與多重指定

### 連鎖指定：多個名稱指向同一物件

```python
a = b = c = 1
```

執行方式如下：

1. 右側 `1` 只求值一次。
2. 單一結果物件依序指定給左側的各個目標。
3. `a`、`b`、`c` 最後都參照同一個結果物件。

因此，不要把它理解成教材所說的「先寫入 `c`，再從 `c` 複製給 `b`，最後複製給 `a`」，也不需要背「由右到左」這種過度簡化的口訣。應該記住：

> 右側先求值；結果再指定給左側目標。

### 可變物件會讓共用參照的效果更明顯

```python
a = b = []
a.append("Python")

print(a)  # ['Python']
print(b)  # ['Python']
```

`a` 與 `b` 指向同一個 list。`append()` 改變該 list 後，從兩個名稱都會看到改變。

如果要建立兩個獨立 list，應分開建立：

```python
a = []
b = []

print(a is b)  # False
```

### 多重指定（unpacking）

```python
a, b, c = 1, 2, 3
```

教材字幕中的 `1 2 boom` 應是轉錄錯誤，範例應理解為 `1, 2, 3`。左右數量必須可以正確解包，否則會發生 `ValueError`：

```python
a, b, c = 1, 2  # ValueError
```

右側會先求值，所以可以不借助臨時變數交換兩個綁定：

```python
a = 1
b = 2

a, b = b, a

print(a, b)  # 2 1
```

---

## 四、每個物件都有 identity、type 與 value

在 Python 資料模型中，每個物件都有：

| 面向 | 問題 | 觀察方式 |
| --- | --- | --- |
| identity（身分） | 這是否為同一個物件？ | `id(obj)` 或 `is` |
| type（型別） | 這個物件支援哪些操作？ | `type(obj)` |
| value（值） | 這個物件所表示的資料是什麼？ | 直接求值或 `print(obj)` |

```python
message = "hello"

print(id(message))
print(type(message))  # <class 'str'>
print(message)        # hello
```

`type()` 與 `id()` 查詢的是傳入的物件。當參數是名稱時，Python 會先經由名稱取得物件，並不是在查詢一個獨立存在的「變數型別」。

### `id()` 不應直接定義為記憶體位址

`id(obj)` 回傳一個整數，在該物件的生命期內保持不變，並與同時存在的其他物件區分。

在 CPython 實作中，`id()` 的值就是物件的記憶體位址；但這是實作細節，不是所有 Python 實作都必須遵守的語言保證。而且物件消失後，它的 `id` 數值之後可能被重複利用。

因此，實作程式時不要把 `id()` 當成業務資料的編號，也不要依賴其數值大小或持久性。

---

## 五、值相等不等於同一物件

```python
a = [1, 2]
b = [1, 2]
c = a

print(a == b)  # True：值相等
print(a is b)  # False：不是同一個 list
print(a is c)  # True：是同一個 list
```

- `==` 比較值是否相等。
- `is` 比較兩側是否參照同一個物件。

比較資料內容時通常使用 `==`。`is` 最常見的正確用法是和 `None` 比較：

```python
result = None

if result is None:
    print("還沒有結果")
```

### 不要從字面值的 `id()` 得出過度結論

```python
a = "hello"
b = "hello"

print(id(a) == id(b))
```

在特定一次執行中可能得到 `True`，因為 Python 實作可以共用某些不可變物件，並且編譯器也可能重用常數。這不是程式應依賴的行為。

要測試「兩個名稱明確指向同一物件」，寫成這樣才清楚：

```python
a = "hello"
b = a

print(a is b)  # True
```

教材中「`a = "hello"` 與 `b = "hello"` 的 `id` 一定一樣」不是 Python 語言保證。

---

## 六、Python 是動態型別，但不是隨意自動轉型

```python
variable_a = "hello"
print(type(variable_a))  # <class 'str'>

variable_a = 3.14
print(type(variable_a))  # <class 'float'>
```

更精確的說法是：

- Python 在執行期處理型別。
- 物件有型別，而且物件的型別建立後不會因名稱重新指定而改變。
- 同一個名稱可以在不同時間綁定到不同型別的物件。

不要說 Python 在上例中「把 `variable_a` 自動轉成浮點數」。它只是讓名稱改綁定到一個新的 `float` 物件。

Python 也不會在所有情況下猜測你想要的轉型：

```python
print("9" + 1)  # TypeError
```

必須明確轉型：

```python
print(int("9") + 1)  # 10
```

因此，Python 常被形容為「動態型別且強型別」：名稱可以在執行期間改綁定到不同型別的物件，但不相容的型別不會任意混合運算。

### 型別提示不會改變 Python 的執行模型

現代 Python 可以加入型別提示：

```python
age: int = 20
```

這能幫助閱讀者、IDE 與靜態分析工具，但一般情況下不會在執行時自動強制 `age` 永遠只能綁定 `int`。這是之後寫可維護專案時會再學到的工具。

---

## 七、指定另一個名稱時，發生的是重新綁定

```python
a = "hello"
b = "hello"
c = 5

b = c
```

執行 `b = c` 時：

1. Python 先求值右側名稱 `c`，取得它參照的 `int` 物件 `5`。
2. `b` 改為參照同一個物件。
3. `c` 本身沒有被改變。
4. `b` 原先參照的字串不會被「轉成整數」。

```python
print(b is c)     # True
print(type(b))    # <class 'int'>
print(type(c))    # <class 'int'>
```

如果已經沒有任何參照指向舊物件，該物件之後才可能被 Python 回收；回收時間屬於實作細節，不應寫程式依賴它立即發生。

---

## 教材內容需要修正的地方

1. **變數不是單純保留的記憶體盒子**：在 Python 中，用「名稱綁定到物件」會更準確。
2. **名稱不是物件**：物件才有 identity、type 與 value；名稱用來參照物件。
3. **`int` 才是 Python 型別名稱**：`Integer` 是英文概念名稱，`type(9)` 會顯示 `<class 'int'>`。
4. **`id()` 的語言保證是物件身分**：CPython 實作將其直接對應到記憶體位址，但這不是所有 Python 實作的語言保證。
5. **兩個相同字面值的 `id` 不保證一樣**：`a = "hello"; b = "hello"` 可能因實作優化共用物件，但程式不可依賴此現象。
6. **`a = b = c = 1` 不是連鎖複製**：右側只求值一次，同一結果物件被指定給各目標。
7. **動態型別不是物件自動轉型**：名稱可改綁定到另一型別的物件。
8. **`1 2 boom` 應為字幕錯誤**：多重指定的正常範例是 `a, b, c = 1, 2, 3`。

---

## 實作時要注意的事

1. **心智模型要能解釋可變物件**：「盒子裝值」遇到 list 共用時容易誤導；「名稱參照物件」才能一致解釋。
2. **區分 equality 與 identity**：比較資料內容使用 `==`；比較是否同一物件才使用 `is`。
3. **不依賴實作優化**：字串駐留、整數快取與 CPython 的記憶體佈局都不應成為程式邏輯。
4. **用可變物件測試指定概念**：只用整數與字串容易隱藏共用參照；list 的修改能讓別名效果立即可見。
5. **真實程式應使用有意義的名稱**：教學實驗可以用 `a`、`b` 等短名稱；真實程式應使用 `user_count`、`total_price` 等能表達用途的名稱。
6. **不用 `id()` 作為應用程式識別碼**：需要持久、跨執行的唯一識別碼時，應使用為該需求設計的 ID，而不是 `id()`。
7. **型別錯誤是有用的回饋**：`"9" + 1` 的 `TypeError` 提醒你在程式邊界先進行明確轉型，不要期待 Python 任意猜測。

---

## 接下來可以執行的步驟

### 1. 啟動專案的 JupyterLab

```bash
uv run jupyter lab
```

建立一個 Notebook，下方每個實驗各用一個 Cell。每次都先在 Markdown Cell 寫下預測，再執行核對。

### 2. 觀察重新綁定

```python
value = 9
print(value, type(value), id(value))

value = "hello"
print(value, type(value), id(value))
```

用自己的話解釋：是 `value` 被轉型，還是 `value` 改綁定到新物件？

### 3. 比較 `==` 與 `is`

```python
first = [1, 2]
second = [1, 2]
alias = first

print(first == second)
print(first is second)
print(first == alias)
print(first is alias)
```

執行前先預測四個布林值，再用「值」與「身分」解釋每個結果。

### 4. 觀察可變物件的別名效果

```python
first = []
second = first

second.append("learn")

print(first)
print(second)
print(first is second)
```

接著改成：

```python
first = []
second = []
```

重新預測、執行並比較。

### 5. 測試連鎖指定的風險

```python
a = b = []
a.append(1)

print(a)
print(b)
print(a is b)
```

將第一行改成獨立指定，讓修改 `a` 不影響 `b`。

### 6. 練習解包與交換

```python
left = "L"
right = "R"

left, right = right, left

print(left, right)
```

接著故意讓左右數量不同，讀取 `ValueError` 訊息，確認是「太多值」還是「不夠值」。

### 7. 用小範例模擬實際開發

```python
product_name = "Python 入門課"
unit_price = 600
quantity = 2
total_price = unit_price * quantity

print(product_name)
print(type(unit_price))
print(total_price)
```

把 `unit_price` 改成字串 `"600"`，先預測後續運算的語意，再思考真實程式應在哪個邊界完成轉型。

## 實作檢查清單

- [ ] 用自己的話說明「名稱綁定到物件」
- [ ] 分辨 `=`、`==` 與 `is`
- [ ] 觀察同一名稱重新指定後的 `type()` 與 `id()`
- [ ] 預測並執行 list 別名實驗
- [ ] 比較 `a = b = []` 與 `a = []; b = []`
- [ ] 使用多重指定交換兩個名稱
- [ ] 故意觸發一次解包 `ValueError`
- [ ] 解釋為什麼 `id()` 不適合當永久識別碼
- [ ] 不看筆記回答下方複習題

---

## 複習題

先關掉參考答案，從記憶回答：

1. `a = 9` 用「名稱與物件」的模型應如何解釋？
2. 在 `3 + 6` 中，哪些是 operand，哪個是 operator？
3. `=` 與 `==` 的用途有何不同？
4. `a = b = c = 1` 是否表示將 `1` 先複製到 `c`，再逐步複製到 `b` 與 `a`？
5. `a, b, c = 1, 2` 會發生什麼？為什麼？
6. 物件的 identity、type 與 value 分別代表什麼？
7. `id()` 是否在所有 Python 實作中都保證回傳記憶體位址？
8. 物件消失後，它用過的 `id` 數值是否永遠不會出現第二次？
9. `==` 與 `is` 分別在比較什麼？
10. 為什麼 `a = "hello"` 與 `b = "hello"` 即使某次執行得到同一 `id`，程式也不應依賴它？
11. 如果 `a = b = []`，執行 `a.append(1)` 後，`b` 是什麼？為什麼？
12. 為什麼將同一名稱先綁定到 `str`，後來綁定到 `float`，不應說成原本物件被轉型？
13. 為什麼說 Python 的動態型別不等於「所有型別都會自動轉換」？
14. 以下四行的結果依序是什麼？

```python
a = [1, 2]
b = [1, 2]
c = a

print(a == b)
print(a is b)
print(a == c)
print(a is c)
```

<details>
<summary>參考答案</summary>

1. Python 先求值右側 `9`，取得一個值為 `9` 的 `int` 物件，再讓名稱 `a` 綁定到該物件。
2. `3` 與 `6` 是 operands；`+` 是 operator。
3. `=` 用於指定，讓左側目標綁定右側求值結果；`==` 用於比較兩側的值是否相等。
4. 否。右側 `1` 只求值一次，同一結果物件再指定給各個左側目標；不是經由 `c` 與 `b` 進行連鎖複製。
5. 會引發 `ValueError`，因為右側只有兩個值，無法解包給左側三個目標。
6. identity 區分是否為同一物件；type 決定物件支援的操作與可能值；value 是物件所表示的資料。
7. 否。`id()` 保證的是物件生命期內的身分整數；它對應記憶體位址是 CPython 的實作細節。
8. 否。只要兩個物件的生命期沒有重疊，數值就可能被重複使用。
9. `==` 比較值是否相等；`is` 比較是否為同一個物件。
10. Python 實作可以重用某些不可變物件，編譯器也可能共用常數；這是可變動的實作與優化行為，不是語言保證。
11. `b` 也會顯示 `[1]`，因為 `a` 與 `b` 參照同一個 list，`append()` 改變了該 list。
12. 因為前後是兩個不同物件。原本 `str` 物件沒有改變型別；名稱只是改為參照一個 `float` 物件。
13. Python 不會為所有不相容運算自動猜測轉型；例如 `"9" + 1` 會發生 `TypeError`，需要明確寫成 `int("9") + 1`。
14. 依序是 `True`、`False`、`True`、`True`。`a` 與 `b` 是值相等的不同 list；`c = a` 讓 `c` 與 `a` 參照同一個 list。

</details>

---

## 本節重點

> 右側先求值，左側名稱再綁定到結果物件。物件有 identity、type 與 value；名稱可以重新綁定。`==` 比值，`is` 比同一性。

掌握這個模型後，之後學 list、dict、函式參數與物件導向程式時，就能預測「透過一個名稱修改物件後，為什麼另一個名稱也可能看到變化」。

## Python 官方參考資料

- [Python Data Model：Objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)
- [Python Execution Model：Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)
- [Python Simple Statements：Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)
- [Python Expressions：Evaluation order](https://docs.python.org/3/reference/expressions.html#evaluation-order)
- [Python Built-in Functions：`id()` 與 `type()`](https://docs.python.org/3/library/functions.html)
