# 5-2 Python 複數與虛數字面值

## 學習目標

完成這一節後，我應該能夠：

1. 分清楚實數、純虛數與複數。
2. 使用 `j` 寫出 Python 的虛數字面值。
3. 解讀 `a + bj`，並用 `.real`、`.imag` 取得實部與虛部。
4. 使用 `abs()` 計算複數的大小。
5. 知道何時要使用 `cmath`，而不是 `math`。

---

## 一、先修正教材中的數學分類

教材說「最外層是一個虛數的空間」以及「虛數是所有數字的最外層」，這兩句並不精確。較正確的包含關係是：

```text
自然數 ⊂ 整數 ⊂ 有理數 ⊂ 實數 ⊂ 複數
```

其中：

- 無理數是實數的一部分，例如 `√2` 與 `π`，不是比實數更外層的集合。
- 複數可寫成 `a + bi`，其中 `a`、`b` 都是實數。
- 當 `b = 0` 時，複數就是實數，因此實數可以視為複數的一部分。
- 當 `a = 0` 且 `b != 0` 時，稱為純虛數，例如 `3i`。
- 數學使用 `i` 表示虛數單位，並定義 `i² = -1`；Python 改用 `j`。

### 複數平面

複數 `a + bi` 可以看成平面上的一個點 `(a, b)`：

- 實部 `a` 是 X 座標，落在水平的實軸上。
- 虛部係數 `b` 是 Y 座標，落在垂直的虛軸上。

例如 `5 + 3i` 對應 `(5, 3)`，也就是沿著實軸走 `5`，再沿著虛軸走 `3`：

```text
             虛軸
               ↑
             3 │          ● 5 + 3i
               │
───────────────┼──────────────→ 實軸
               0          5
```

純實數和純虛數都只是複數平面上的特殊位置：

```text
5  = 5 + 0i  ↔ (5, 0)，位於實軸上
3i = 0 + 3i  ↔ (0, 3)，位於虛軸上
```

「實數集合加上純虛數集合」只會得到兩條軸，還會漏掉 `5 + 3i` 這類同時具有實部與虛部的點。複數包含整個平面，所以最外層應稱為「複數」。

> 教材勘誤：「虛數是根號負一」也不夠精確。`√-1` 指的是虛數單位 `i`；一般純虛數是 `bi`，一般複數則是 `a + bi`。

---

## 二、Python 如何表示虛部？

Python 把 `j` 或 `J` 緊接在數值後方，表示虛部：

```python
z = 5 + 3j

print(z)        # (5+3j)
print(type(z))  # <class 'complex'>
```

這裡的 `5` 是實部，`3` 是虛部係數。Python 的內建型別名稱是 `complex`，沒有名為 `imaginary` 的內建數值型別。

### 三個教材範例

| 寫法 | 數學意義 | 實部 | 虛部 | Python 型別 |
| --- | --- | ---: | ---: | --- |
| `5 + 3j` | `5 + 3i` | `5.0` | `3.0` | `complex` |
| `5.j` | `0 + 5i` | `0.0` | `5.0` | `complex` |
| `-3.89j` | `0 - 3.89i` | `-0.0` | `-3.89` | `complex` |

`5.j` 是合法語法，但日常程式通常寫成較容易閱讀的 `5j`。

```python
print(5.j == 5j)  # True
```

`j` 必須緊接在數值後面：

```python
valid = 3j
# invalid = 3 j  # SyntaxError
```

參考：[Python 3.11 官方文件：Imaginary literals](https://docs.python.org/3.11/reference/lexical_analysis.html#imaginary-literals)

---

## 三、`5 + 3j` 其實是運算式

這裡要區分字面值與運算式：

- `3j` 是虛數字面值，求值後得到實部為零的 `complex` 物件。
- `5 + 3j` 不是單一的複數字面值，而是 `5`、`+`、`3j` 組成的運算式。
- 這個加法的結果是 `(5+3j)`，型別是 `complex`。

```python
imaginary_part = 3j
complex_number = 5 + imaginary_part

print(type(imaginary_part))  # <class 'complex'>
print(type(complex_number))  # <class 'complex'>
```

也可以使用 `complex()` 建立同樣的物件：

```python
z1 = 5 + 3j
z2 = complex(5, 3)

print(z1 == z2)  # True
```

如果資料來自字串，空白規則不同：

```python
print(complex("5+3j"))  # (5+3j)

# complex("5 + 3j")
# ValueError：字串內部不能在數字、正負號與 j 之間加空白
```

參考：[Python 3.11 官方文件：`complex()`](https://docs.python.org/3.11/library/functions.html#complex)

---

## 四、讀取實部、虛部與大小

`complex` 物件提供 `.real` 與 `.imag`：

```python
z = 5 + 3j

print(z.real)  # 5.0
print(z.imag)  # 3.0
```

兩者都是 `float`：

```python
print(type(z.real))  # <class 'float'>
print(type(z.imag))  # <class 'float'>
```

沿用前面的座標看法，`abs()` 計算的是點 `(a, b)` 到原點的距離，也就是複數的絕對值或模：

```python
z = 3 + 4j

print(abs(z))  # 5.0
```

因為：

```text
|3 + 4j| = √(3² + 4²) = 5
```

共軛複數則可使用 `.conjugate()`：

```python
z = 1 + 2j

print(z.conjugate())  # (1-2j)
```

參考：[Python 3.11 官方文件：Numeric Types](https://docs.python.org/3.11/library/stdtypes.html#numeric-types-int-float-complex)

---

## 五、運算與常見限制

複數支援一般的加、減、乘、除與次方：

```python
first = 1 + 2j
second = 3 - 4j

print(first + second)  # (4-2j)
print(first * second)  # (11+2j)
```

但是複數沒有一般數線上的大小順序，所以不能使用 `<`、`>`、`<=`、`>=`：

```python
# print((1 + 2j) < (2 + 3j))
# TypeError: '<' not supported between instances of 'complex' and 'complex'
```

若要比較兩個複數離原點的距離，可以比較 `abs()` 的結果：

```python
first = 1 + 2j
second = 2 + 3j

print(abs(first) < abs(second))  # True
```

這段程式比較的是兩個 `float` 距離，沒有替複數建立自然順序。

---

## 六、`math` 與 `cmath` 的邊界

一般實數運算使用 `math`；輸入或結果可能是複數時，使用 `cmath`：

```python
import cmath

result = cmath.sqrt(-1)

print(result)        # 1j
print(type(result))  # <class 'complex'>
```

相對地，`math.sqrt(-1)` 會產生 `ValueError`，因為 `math.sqrt()` 的定義域是實數範圍。

`cmath` 還提供複數的相位、極座標、指數、對數與三角函式。可以按問題的數值範圍選擇模組：

```text
實數問題 → math
複數問題 → cmath
```

參考：[Python 3.11 官方文件：`cmath`](https://docs.python.org/3.11/library/cmath.html)

---

## 七、使用複數時的重點

1. **術語要準確。** 最外層是複數集合；虛數不是所有數字的總稱。
2. **區分語法與物件。** `3j` 是虛數字面值；`5 + 3j` 是運算式；兩者求值後都是 `complex` 物件。
3. **不要把 `j` 當變數。** 它是數值字面值的後綴，而且必須緊貼數值。
4. **實部與虛部以浮點數保存。** `.real` 與 `.imag` 都是 `float`，因此也要留意浮點近似誤差。
5. **比較前先說清楚比較標準。** 複數不能直接排序；若要比較模，應明確使用 `abs()`。
6. **依定義域選模組。** 實數數學用 `math`，複數數學用 `cmath`。
7. **先確認問題是否需要複數。** 複數常見於訊號處理、電機、控制、波動與科學計算；一般金額、計數或表格資料通常不該為了「型別更大」而轉成 `complex`。

---

## 八、立即練習

在 Notebook 建立一個新 Cell，先預測每一行的輸出，再執行核對：

```python
import cmath

values = [
    5 + 3j,
    5.j,
    -3.89j,
    complex(2, -1),
    cmath.sqrt(-9),
]

for value in values:
    print(
        "值:", value,
        "型別:", type(value).__name__,
        "實部:", value.real,
        "虛部:", value.imag,
        "大小:", abs(value),
    )
```

執行後，選其中一個結果，用自己的話說明：

1. 它是由哪一種語法建立的？
2. 實部與虛部分別是多少？
3. `abs()` 在複數平面上代表什麼？

請按「先預測、再執行、最後解釋」的順序完成練習，並核對預測與實際輸出的差異。

---

## 九、文末問題解答

字幕文末列出的 `5 + 3j`、`5.j`、`-3.89j` 都會得到 `complex` 物件，但它們不完全是同一種語法：

- `5 + 3j` 是由實數部分與虛數部分相加的運算式，結果為 `(5+3j)`。
- `5.j` 是虛數字面值，等同於 `5j`，結果的實部是 `0.0`、虛部是 `5.0`。
- `-3.89j` 表示負的純虛數，結果的實部是零、虛部是 `-3.89`。

驗證方式：

```python
for value in (5 + 3j, 5.j, -3.89j):
    print(value, type(value), value.real, value.imag)
```

可以更精確地說：

> 這些運算式求值後都會得到 Python 的 `complex` 物件；其中 `5j` 與 `-3.89j` 是純虛數，`5 + 3j` 則是實部和虛部都不為零的複數。

---

## 十、複習題

請先不看答案，直接從記憶回答。

1. 為什麼「虛數是所有數字的最外層」不正確？
2. Python 為什麼寫 `j`，而不是數學常見的 `i`？
3. `3j` 與 `5 + 3j` 在語法上有什麼差別？
4. `complex(5, 3)` 會建立什麼值？
5. 如何取得複數 `z` 的實部與虛部？
6. `abs(3 + 4j)` 的結果是多少？它代表什麼？
7. 為什麼不能直接比較 `(1 + 2j) < (2 + 3j)`？
8. `math.sqrt(-1)` 與 `cmath.sqrt(-1)` 的結果有何不同？

<details>
<summary>參考答案</summary>

1. 包含所有實數並再向外擴展的是複數集合；純虛數只是複數的一部分。
2. 這是 Python 的語法設計；`j` 也常見於電機工程，用來避免和電流符號混淆。
3. `3j` 是虛數字面值；`5 + 3j` 是由整數字面值、加號與虛數字面值組成的運算式。
4. `(5+3j)`，型別是 `complex`。
5. 使用 `z.real` 與 `z.imag`。
6. `5.0`；代表複數平面上的點 `(3, 4)` 到原點的距離。
7. 複數沒有一般數線上的自然大小順序。若問題要比較模，可以改成比較 `abs()` 的結果。
8. `math.sqrt(-1)` 產生 `ValueError`；`cmath.sqrt(-1)` 回傳 `1j`。

</details>

---

## 本節教材勘誤總結

| 教材內容 | 正確說法 |
| --- | --- |
| 無理數是比實數更大的空間 | 無理數是實數的一部分 |
| 最外層是虛數空間 | 實數包含於複數；純虛數只是複數的一部分 |
| 虛數就是根號負一 | `√-1` 是虛數單位；一般純虛數為 `bi` |
| `5 + 3j`、`5.j`、`-3.89j` 都是一種虛數型別 | 三者都得到 `complex`；只有實部為零者是純虛數 |

## 延伸閱讀

- [Python 3.11 官方文件：Imaginary literals](https://docs.python.org/3.11/reference/lexical_analysis.html#imaginary-literals)
- [Python 3.11 官方文件：Numeric Types — `int`, `float`, `complex`](https://docs.python.org/3.11/library/stdtypes.html#numeric-types-int-float-complex)
- [Python 3.11 官方文件：`complex()`](https://docs.python.org/3.11/library/functions.html#complex)
- [Python 3.11 官方文件：`cmath`](https://docs.python.org/3.11/library/cmath.html)

有題目無法解釋時，請把預測與實際輸出一起交給老師，再根據差異找出理解錯誤的地方。
