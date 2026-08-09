# 5-3 Python 布林型別與比較運算

## 學習目標

完成這一節後，我應該能夠：

1. 說明 `bool` 型別只有 `True` 與 `False` 兩個值。
2. 使用比較運算式產生布林結果。
3. 正確寫出 `True`、`False` 與 `!=`。
4. 用 `type()` 與 `bool()` 驗證值及型別。
5. 分辨布林值、真假性（truthiness）與字串 `"True"`、`"False"`。
6. 寫出語意清楚、可以直接交給 `if` 判斷的條件。

---

## 一、`bool` 只表示兩種邏輯狀態

Python 的布林型別名稱是 `bool`，只有兩個值：

```python
True
False
```

它們常用來表示某個命題是否成立，例如：

- 使用者是否已登入。
- 檔案是否存在。
- 成績是否及格。
- 資料是否通過驗證。

可以直接查看值的型別：

```python
print(type(True))   # <class 'bool'>
print(type(False))  # <class 'bool'>
```

`True` 和 `False` 的第一個字母必須大寫，而且兩者都是 Python 關鍵字。小寫的 `true`、`false` 並不是 Python 的布林值：

```python
# print(true)  # NameError：找不到名為 true 的名稱
```

> 教材口語說的是「true、false」，實際 Python 程式碼必須寫成 `True`、`False`。

參考：[Python 官方文件：Boolean Values](https://docs.python.org/3/library/stdtypes.html#boolean-values)

---

## 二、比較運算式會回答「成立嗎？」

比較運算子把兩邊的值拿來比較。對這一節使用的內建數值而言，結果會是 `True` 或 `False`：

| 運算子 | 意義 | 範例 | 結果 |
| --- | --- | --- | --- |
| `>` | 大於 | `5 > 3` | `True` |
| `<` | 小於 | `5 < 3` | `False` |
| `>=` | 大於等於 | `5 >= 5` | `True` |
| `<=` | 小於等於 | `3 <= 5` | `True` |
| `==` | 等於 | `5 == 3` | `False` |
| `!=` | 不等於 | `5 != 3` | `True` |

教材的三個例子可以完整寫成：

```python
print(5 > 3)   # True
print(5 != 3)  # True
print(5 < 3)   # False
```

`print` 是函式，因此 Python 3 要使用括號。括號內的 `5 > 3` 會先求值成 `True`，接著 `print()` 才把結果顯示出來：

```text
5 > 3  ──比較──>  True  ──交給 print──>  顯示 True
```

比較結果也可以保存起來，讓名稱表達它在程式中的意義：

```python
age = 20
is_adult = age >= 18

print(is_adult)        # True
print(type(is_adult))  # <class 'bool'>
```

`is_adult` 比 `result` 更容易看出這個布林值代表什麼。

參考：[Python 官方文件：Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)

---

## 三、`=` 和 `==` 的差別

`=` 用於指定，`==` 用於比較：

```python
score = 80       # 指定：讓 score 參照 80
is_full = score == 100  # 比較：score 是否等於 100
```

| 寫法 | 用途 | 是否產生比較結果 |
| --- | --- | --- |
| `=` | 把值指定給名稱 | 否 |
| `==` | 比較兩個值是否相等 | 是 |
| `!=` | 比較兩個值是否不相等 | 是 |

若在需要條件的地方誤寫成單一 `=`，Python 通常會直接回報 `SyntaxError`，而不是默默把它當成相等比較。

---

## 四、布林值會成為程式的分岔開關

布林值的主要用途，是控制程式接下來要走哪一條路：

```python
temperature = 31
is_hot = temperature > 30

if is_hot:
    print("今天很熱")
else:
    print("今天不算太熱")
```

也可以把比較運算式直接放進 `if`：

```python
if temperature > 30:
    print("今天很熱")
```

兩種寫法都可以。當條件只使用一次時，直接寫比較式通常較簡潔；當結果會重複使用，或需要一個名稱解釋其含義時，再存成 `is_hot`。

### 多個比較可以串在一起

Python 支援連鎖比較：

```python
age = 20
print(18 <= age < 65)  # True
```

它表達「`age` 至少 18，而且小於 65」。連鎖比較可以避免重複寫出 `age`：

```python
print(age >= 18 and age < 65)  # True
```

---

## 五、`bool()` 可以查看物件的真假性

Python 的條件不只接受 `True` 與 `False`。其他物件也會被判定為 truthy 或 falsy，可以用 `bool()` 查看：

```python
print(bool(0))       # False
print(bool(1))       # True
print(bool(""))      # False
print(bool("Python"))  # True
print(bool([]))      # False
print(bool([0]))     # True
```

常見的 falsy 值包括：

- `False`
- 數值零，例如 `0`、`0.0`
- 空字串 `""`
- 空容器，例如 `[]`、`()`、`{}`
- `None`

其他大多數物件是 truthy。

### 字串內容不是布林值

```python
print(bool("False"))  # True
```

原因是 `"False"` 是一個**非空字串**，不是布林值 `False`。同樣地：

```python
print(type(False))    # <class 'bool'>
print(type("False"))  # <class 'str'>
```

如果資料來自表單、CSV 或環境變數，不能直接用 `bool(text)` 判斷文字是否表示 `True` 或 `False`；必須先定義可接受的文字，再明確轉換。

參考：[Python 官方文件：Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)

---

## 六、使用布林值時的重點

1. **大小寫是語法的一部分。** Python 寫 `True`、`False`，不是 `true`、`false`。
2. **比較的是值時使用 `==`，不要拿 `is` 代替。** `is` 判斷兩個名稱是否參照同一個物件，語意不同。
3. **布林名稱應能表達是非條件。** `is_valid`、`has_permission`、`can_save` 通常比 `flag`、`data` 更清楚。
4. **不要多寫 `== True`。** `if is_valid:` 通常比 `if is_valid == True:` 直接；判斷相反情況可寫 `if not is_valid:`。
5. **`bool` 是 `int` 的子型別。** 因此 `True == 1`、`False == 0` 與 `isinstance(True, int)` 都是 `True`：

   ```python
   print(True == 1)              # True
   print(False == 0)             # True
   print(isinstance(True, int))  # True
   print(True + True)            # 2
   ```

   這是 Python 的相容性設計，不代表程式應把「是否成功」當成一般數量來運算。若要計數，最好明確表達意圖。
6. **真假性不等於型別是 `bool`。** `if [1]:` 會進入分支，但 `[1]` 仍然是 `list`，不是 `bool`。
7. **本節把比較結果簡化為 `bool`。** 一般內建數值比較會得到 `True` 或 `False`；Python 的自訂型別則能改寫比較行為，某些第三方資料型別也可能回傳其他結果物件。
8. **浮點數比較仍要留意近似誤差。** `0.1 + 0.2 == 0.3` 是 `False`；一般計算結果可用 `math.isclose()` 判斷是否足夠接近。

參考：[PEP 8：Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations)

---

## 七、立即練習

在 Notebook 或 Python 檔案中貼上以下程式，但先不要執行。先寫下每一項的預測值與型別：

```python
expressions = [
    5 > 3,
    5 != 3,
    5 < 3,
    3 <= 3,
    1 == True,
    bool(0),
    bool("False"),
]

for value in expressions:
    print(repr(value), type(value).__name__)
```

接著依序完成：

1. **預測：** 不執行程式，先寫下七個結果。
2. **執行：** 實際執行並核對差異。
3. **解釋：** 用自己的話解釋為什麼 `bool("False")` 是 `True`。
4. **應用：** 寫一個 `score` 變數，再建立 `is_passing = score >= 60`。
5. **分岔：** 用 `if is_passing:` 分別印出「及格」或「未及格」。

完成後，再確認比較結果如何交給 `if` 作為條件。

---

## 八、文末小問題解答

教材文末依序比較：

```python
print(5 > 3)
print(5 != 3)
print(5 < 3)
```

輸出是：

```text
True
True
False
```

原因如下：

1. `5 > 3`：5 的確大於 3，所以是 `True`。
2. `5 != 3`：5 的確不等於 3，所以是 `True`。
3. `5 < 3`：5 並不小於 3，所以是 `False`。

這三個結果的型別全部都是 `bool`：

```python
print(type(5 > 3))   # <class 'bool'>
print(type(5 != 3))  # <class 'bool'>
print(type(5 < 3))   # <class 'bool'>
```

---

## 九、複習題

請先不看答案，直接從記憶回答。

1. Python 的兩個布林值應如何拼寫？
2. `5 == 3` 與 `5 != 3` 分別得到什麼結果？
3. `=` 和 `==` 的用途有何不同？
4. `type(5 > 3)` 會得到什麼？
5. 為什麼 `bool("False")` 是 `True`？
6. `True == 1` 的結果是什麼？實務上為什麼仍不應混用布林與數量語意？
7. `if is_ready:` 和 `if is_ready == True:` 通常應優先使用哪一個？
8. 如何用一個比較運算式表示 `age` 介於 18（含）到 65（不含）之間？

<details>
<summary>參考答案</summary>

1. `True` 與 `False`，第一個字母必須大寫。
2. `5 == 3` 是 `False`；`5 != 3` 是 `True`。
3. `=` 用於指定；`==` 用於比較兩個值是否相等。
4. `<class 'bool'>`。
5. 因為 `"False"` 是非空字串；非空字串是 truthy。它不是布林值 `False`。
6. 結果是 `True`，因為 `bool` 是 `int` 的子型別；但「狀態」和「數量」表達不同領域意義，混用會降低可讀性，也容易造成錯誤。
7. 通常使用 `if is_ready:`，語意更直接。
8. `18 <= age < 65`。

</details>

---

## 本節教材補充

| 教材說法 | 更完整的 Python 說法 |
| --- | --- |
| 布林值是 true、false | 程式碼必須寫成 `True`、`False` |
| `print 5 > 3` | Python 3 應寫成 `print(5 > 3)` |
| 比較會產生 true 或 false | 對本節內建數值範例成立；結果是 `bool` 的 `True` 或 `False` |
| 布林型別很單純 | 值只有兩個，但還要分辨 truthiness、字串內容，以及 `bool` 與 `int` 的關係 |

## 延伸閱讀

- [Python 官方文件：Boolean Values](https://docs.python.org/3/library/stdtypes.html#boolean-values)
- [Python 官方文件：Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)
- [Python 官方文件：Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)
- [PEP 8：Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations)

若預測和實際輸出不同，請保留兩者，寫下原本的判斷，並根據差異找出需要重新理解的觀念。
