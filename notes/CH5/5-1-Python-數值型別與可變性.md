# 5-1 Python 數值型別與可變性

## 學習目標

完成這一節後，我應該能夠：

1. 分辨 Python 的 `int`、`float` 與 `complex`。
2. 使用十進位、二進位、八進位與十六進位整數字面值。
3. 正確解讀浮點數的科學記號，例如 `18.3e9`。
4. 使用 `j` 寫出虛部，並知道結果物件的型別是 `complex`。
5. 用 `type()` 驗證數值物件的型別。
6. 從「物件能否原地改變」理解 mutable 與 immutable。

---

## 一、先建立 Python 內建型別地圖

這一章先介紹數值型別，後續章節再討論其他容器型別：

| 類別 | 常見內建型別 | 說明 |
| --- | --- | --- |
| 數值 | `int`、`float`、`complex` | 整數、浮點數、複數 |
| 布林 | `bool` | `True`、`False`；它也是 `int` 的子型別 |
| 序列 | `str`、`tuple`、`list`、`range` | 依順序保存或呈現資料 |
| 集合 | `set`、`frozenset` | 保存不重複元素 |
| 映射 | `dict` | 以鍵對應值 |

教材把 `set` 與 `dict` 合稱為「雜湊型別」，這不是 Python 官方型別分類。它們的實作與使用確實和 hash 有關，但官方文件分別稱為 set type 與 mapping type。

參考：[Python 官方文件：Built-in Types](https://docs.python.org/3/library/stdtypes.html)

---

## 二、mutable 與 immutable

判斷 mutable 與 immutable 時，要看物件建立後能否原地修改：

> 一個物件建立後，它本身能不能被原地修改？

### Immutable：物件本身不可變

`int`、`float`、`complex`、`bool`、`str` 與 `tuple` 都是常見的不可變型別。

```python
score = 10
score = score + 5
```

第二行沒有把原本的整數 `10` 改造成 `15`。Python 先算出新的整數物件 `15`，再讓名稱 `score` 改為參照它：

```text
執行前：score ──> 10
執行後：score ──> 15
```

因此，「名稱可以重新指定」和「物件是否可變」是兩件不同的事。

### Mutable：物件可以原地改變

`list`、`dict` 與 `set` 是常見的可變型別：

```python
numbers = [1, 2]
numbers.append(3)

print(numbers)  # [1, 2, 3]
```

`append()` 修改的是原本那個 list。這件事在多個名稱共用同一物件時尤其重要：

```python
first = [1, 2]
second = first
first.append(3)

print(second)  # [1, 2, 3]
```

### `tuple` 有一個容易混淆的細節

`tuple` 本身不可變，不能替換其中的參照；但它可以包含可變物件，而該物件仍然可以改變：

```python
record = ([1, 2], "Python")
record[0].append(3)

print(record)  # ([1, 2, 3], 'Python')
```

所以「tuple 不可變」不等於「它所能連到的所有資料都永遠不變」。

---

## 三、整數 `int`

一般十進位整數可直接書寫：

```python
positive = 22
zero = 0
negative = -3

print(type(positive))  # <class 'int'>
```

Python 的內建整數沒有固定的 32 位元或 64 位元上限；只要記憶體允許，就可以表示很大的整數。

### 同一個整數值可以用不同進位書寫

| 進位 | 前綴 | 範例 | 十進位值 |
| --- | --- | --- | ---: |
| 十進位 | 無 | `171` | 171 |
| 二進位 | `0b` | `0b10101011` | 171 |
| 八進位 | `0o` | `0o253` | 171 |
| 十六進位 | `0x` | `0xAB` | 171 |

```python
binary_number = 0b10101011

print(binary_number)        # 171
print(type(binary_number))  # <class 'int'>
```

這些只是不同的「寫法」；產生的物件仍然都是 `int`。如果想把整數轉成其他進位的字串表示，可使用：

```python
number = 171

print(bin(number))  # 0b10101011
print(oct(number))  # 0o253
print(hex(number))  # 0xab
```

> 教材勘誤：`0b10101011` 的十進位值是 `171`，不是 `175`。

### 負號不是整數字面值的一部分

從 Python 語法的角度看，`-3` 是負號運算子 `-` 作用於整數字面值 `3` 的結果。這個語法細節會影響某些運算的優先順序：

```python
print(-3 ** 2)    # -9，先算 3 ** 2，再套用負號
print((-3) ** 2)  # 9
```

---

## 四、浮點數 `float`

含小數點或十進位指數記號的數值通常會產生 `float`：

```python
a = 0.0
b = 22.5
c = -3.1
d = 10.
e = 1e3

for value in (a, b, c, d, e):
    print(value, type(value))
```

`10.` 與 `1e3` 即使沒有顯示小數部分，型別仍然是 `float`。

### 科學記號使用 `e` 或 `E`

```python
large = 18.3e9
small = 3.14e-4
```

解讀方式是：

```text
18.3e9  = 18.3 × 10⁹
3.14e-4 = 3.14 × 10⁻⁴
```

`e` 後方的正負整數是 10 的指數，而不是英文字母 `e` 的次方。

> 教材字幕把 `e` 辨識成數字 `1`，這是轉錄錯誤。若原範例要表示 `3.1232 × 10³`，Python 應寫成 `3.1232e3`，結果是 `3123.2`；單寫 `3.1232` 沒有乘上 `10³`。

### 浮點數通常是近似值

多數 Python 實作以二進位浮點數表示 `float`，所以某些十進位小數無法被精確保存：

```python
print(0.1 + 0.2)       # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False
```

這個結果來自二進位浮點表示的限制。比較計算結果時，可以使用 `math.isclose()`：

```python
import math

print(math.isclose(0.1 + 0.2, 0.3))  # True
```

金額等需要明確十進位規則的資料，不應想當然地用 `float`；之後可學習標準函式庫的 `decimal.Decimal`。

---

## 五、複數 `complex` 與虛部 `j`

數學常用 `i` 表示虛數單位，Python 使用 `j`：

```python
z = 1 + 2j

print(z)         # (1+2j)
print(type(z))   # <class 'complex'>
print(z.real)    # 1.0
print(z.imag)    # 2.0
```

先區分兩個概念：

- `2j` 是虛數字面值，會產生實部為 `0.0` 的 `complex` 物件。
- `1 + 2j` 是由實數部分與虛數部分相加形成的複數運算式。
- Python 的內建型別名稱是 `complex`，不是 `imaginary`。

```python
print(type(2j))      # <class 'complex'>
print(type(1 + 2j))  # <class 'complex'>
```

一般實數數學函式使用 `math`；處理複數時通常使用 `cmath`。

---

## 六、用 `type()` 做最小驗證

先預測每個結果，再執行：

```python
a = 5
b = 3.1
c = 3e2
d = 1 + 2j
e = 0b10101011

for name, value in (
    ("a", a),
    ("b", b),
    ("c", c),
    ("d", d),
    ("e", e),
):
    print(name, value, type(value))
```

預期結果：

| 名稱 | 顯示的值 | 型別 | 判斷理由 |
| --- | ---: | --- | --- |
| `a` | `5` | `int` | 十進位整數 |
| `b` | `3.1` | `float` | 含小數點 |
| `c` | `300.0` | `float` | 使用 `e` 指數記號 |
| `d` | `(1+2j)` | `complex` | 含 `j` 虛部 |
| `e` | `171` | `int` | 二進位整數字面值 |

`type()` 接收物件並回傳該物件的型別。型別屬於物件，不屬於名稱。

---

## 七、容易混淆的重點

1. **區分字面值、運算式與型別。** `2j` 是虛數字面值，`1 + 2j` 是運算式，兩者求值後都是 `complex` 物件。
2. **進位前綴只改變原始碼寫法。** `171`、`0b10101011`、`0o253` 與 `0xAB` 的值相等，型別也都是 `int`。
3. **科學記號的符號是 `e` 或 `E`。** `3.1232e3` 才代表 `3.1232 × 10³`。
4. **`float` 是近似表示。** 不直接以 `==` 判斷一般浮點計算結果是否「足夠接近」。
5. **可變性是物件的特性。** 名稱重新綁定不代表不可變物件被修改。
6. **`bool` 與整數有繼承關係。** `isinstance(True, int)` 是 `True`，但程式仍應讓布林條件與一般數量維持清楚語意。
7. **分類要精確。** `dict` 是映射型別，`set` 是集合型別；「底層使用 hash」不等於它們屬於同一個官方類別。

---

## 八、立即練習：先預測，再執行

不要先跑程式。先在紙上寫下每一行的「值」與「型別」：

```python
values = [
    42,
    0x2A,
    4.2e1,
    42 + 0j,
    -2 ** 2,
]

for value in values:
    print(repr(value), type(value).__name__)
```

再回答：

1. 前四個物件的值是否相等？
2. 前四個物件的型別是否相同？
3. 最後一項為什麼是 `-4`，不是 `4`？

<details>
<summary>參考答案</summary>

輸出重點如下：

```text
42 int
42 int
42.0 float
(42+0j) complex
-4 int
```

1. 前四個物件在數值比較上相等：`42 == 42.0 == 42 + 0j` 為 `True`。
2. 型別不同：依序是 `int`、`int`、`float`、`complex`。
3. 次方 `**` 的優先順序高於前置負號，所以 `-2 ** 2` 等同 `-(2 ** 2)`。若要平方負二，應寫 `(-2) ** 2`。

</details>

---

## 九、複習題

請先不看答案，直接從記憶回答。

1. mutable 與 immutable 的判斷標準是什麼？
2. `0b`、`0o`、`0x` 分別代表什麼進位？
3. `0b10101011` 的十進位值是多少？型別是什麼？
4. `18.3e9` 應如何解讀？
5. `2j` 與 `1 + 2j` 的型別各是什麼？
6. 為什麼 `0.1 + 0.2 == 0.3` 可能是 `False`？
7. `score = score + 1` 是否修改了原本的整數物件？
8. 為什麼不宜把 `set` 與 `dict` 都叫做「雜湊型別」？

<details>
<summary>參考答案</summary>

1. 看同一個物件建立後，是否能被原地修改；不是看名稱能否重新指定。
2. `0b` 是二進位、`0o` 是八進位、`0x` 是十六進位。
3. 十進位值是 `171`，型別是 `int`。
4. `18.3 × 10⁹`，而且它是 `float`。
5. 兩者都是 `complex`；`2j` 的實部是零，`1 + 2j` 同時有實部與虛部。
6. 因為多數十進位小數無法用有限的二進位浮點數精確表示，運算會帶有微小近似誤差。
7. 不會。整數不可變；運算建立新的整數結果，再讓 `score` 改為參照它。
8. Python 官方將 `set` 分為集合型別、`dict` 分為映射型別。兩者雖都利用 hash，公開語意與操作仍不同。

</details>

---

## 本節教材勘誤總結

| 教材內容 | 正確說法 |
| --- | --- |
| `set`、`dictionary` 是雜湊型別 | 官方分類分別是集合型別與映射型別 |
| 虛數的型別 | Python 內建型別是複數 `complex`；`j` 標記虛部 |
| 英文字母「1」後面表示次方 | 那是 `e` 或 `E`，代表乘以 10 的某次方 |
| 單寫 `3.1232` 是乘以 `10³` | 應寫成 `3.1232e3` |
| `0b10101011` 印出 `175` | 正確結果是 `171` |

## 延伸閱讀

- [Python 官方文件：Numeric literals](https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals)
- [Python 官方文件：Numeric Types — `int`, `float`, `complex`](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)
- [Python 官方教學：Floating-Point Arithmetic](https://docs.python.org/3/tutorial/floatingpoint.html)

有題目無法解釋時，請把預測與實際輸出一起交給老師，再根據差異找出理解錯誤的地方。
