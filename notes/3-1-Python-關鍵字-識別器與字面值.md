# 3-1 Python 關鍵字、識別器與字面值

## 這一節要學會什麼

完成這一節後，我應該能夠：

1. 分辨 keyword、identifier 與 literal。
2. 判斷名稱的字元格式是否符合 Python 規則。
3. 檢查名稱是否撞到 Python 關鍵字。
4. 使用清楚且一致的命名方式表達程式意圖。
5. 看懂常見的字串、數字與布林值寫法。
6. 不靠猜測，直接用 Python 工具驗證名稱。

---

## 一、三個最底層的概念

### Keyword：Python 保留的關鍵字

關鍵字在 Python 語法中有特殊用途，不能當作一般變數、函式或類別名稱。

```python
if
for
class
return
True
False
```

關鍵字大小寫有別：

```python
import keyword

print(keyword.iskeyword("if"))  # True
print(keyword.iskeyword("IF"))  # False
```

`IF` 雖然不是關鍵字，但不代表它是好名稱。名稱還要讓人看得懂用途，並符合團隊的命名慣例。

### Identifier：程式中的名稱

Identifier 是用來辨認物件的名稱，例如：

```python
user_name = "Steve"


def calculate_total():
    pass


class UserAccount:
    pass
```

其中 `user_name`、`calculate_total` 與 `UserAccount` 都是 identifier。

初學時可以先記住：

- 可以使用英文字母、數字與底線。
- 不能以數字開頭。
- 不能包含減號、空白等不合法符號。
- 不能使用 Python 關鍵字。
- Python 大小寫有別。

```python
user_name    # 格式合法
_result      # 格式合法
user2        # 格式合法
99user       # 格式不合法：數字開頭
user-name    # 格式不合法：減號會被當成運算子
for          # 格式合法，但它是關鍵字
```

Python 實際上也支援 Unicode identifier，因此下面的名稱在技術上可以成立：

```python
使用者名稱 = "Steve"
價格 = 100
```

不過本課程先使用英文名稱，以便配合 Python 生態系、文件、搜尋與常見團隊慣例。

### Literal：直接寫在程式碼中的值

Literal 是某些內建型別之固定值的程式碼表示法。

```python
30          # 十進位整數
3.14        # 浮點數
"Steve"     # 字串
0b11001     # 二進位整數
0o31        # 八進位整數
0x19        # 十六進位整數
```

在下面的指定敘述中：

```python
age = 30
```

- `age` 是 identifier。
- `=` 是指定運算子。
- `30` 是 integer literal。

`True` 與 `False` 是 `bool` 型別的兩個固定值。初學教材常把它們稱為布林字面值；更精確地說，它們也是不能重新指定的 Python 關鍵字與內建常數。

---

## 二、合法名稱要做兩層檢查

### 第一層：字元格式是否合法

字串方法 `isidentifier()` 只檢查字元排列是否符合 identifier 格式：

```python
print("abc".isidentifier())        # True
print("99a".isidentifier())        # False
print("_abc".isidentifier())       # True
print("user-name".isidentifier())  # False
print("for".isidentifier())        # True
```

`"for".isidentifier()` 得到 `True` 並不是 Python 的缺陷。它只代表 `for` 的字元排列符合 identifier 格式。

### 第二層：是不是關鍵字

```python
import keyword

print(keyword.iskeyword("for"))        # True
print(keyword.iskeyword("user_name"))  # False
```

因此，一般名稱檢查可以寫成：

```python
import keyword


def is_valid_python_name(name: str) -> bool:
    return name.isidentifier() and not keyword.iskeyword(name)
```

測試：

```python
names = [
    "abc",
    "99a",
    "_abc",
    "user_name",
    "user-name",
    "for",
    "if",
]

for name in names:
    print(name, is_valid_python_name(name))
```

預期結果：

```text
abc True
99a False
_abc True
user_name True
user-name False
for False
if False
```

這個函式足以處理本節的一般命名練習，但 `True` 不代表名稱一定清楚，也不保證它能在所有語法位置中使用。像 `__debug__` 就是不能重新指定的特殊內建常數。

---

## 三、查詢目前直譯器的關鍵字

不必死背整份清單。需要時直接查詢目前執行中的 Python：

```python
import keyword

print(keyword.kwlist)
```

正確屬性名稱是：

```python
keyword.kwlist
```

不是：

```python
keyword.keywordlist
```

Python 3.11 另外有 soft keyword。它們只在特定語法情境中扮演關鍵字：

```python
print(keyword.softkwlist)
print(keyword.issoftkeyword("match"))
```

例如 `match` 與 `case` 和結構化模式比對有關。現階段先知道它們與一般保留關鍵字不同，不必提前深入語法。

---

## 四、合法不等於清楚

下面的名稱都可能合法，但無法清楚表達用途：

```python
a = 30
x1 = 500
data = True
```

較清楚的寫法是：

```python
user_age = 30
order_total = 500
is_active = True
```

依照 PEP 8 的常見慣例：

| 對象 | 慣例 | 範例 |
| --- | --- | --- |
| 變數 | `snake_case` | `user_name` |
| 函式 | `snake_case` | `calculate_total` |
| 類別 | `CapWords` | `UserAccount` |
| 常數 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |

若名稱剛好與關鍵字衝突，PEP 8 建議在尾端加一個底線：

```python
class_ = "beginner"
```

這通常比故意縮寫或拼錯名稱更容易理解。

命名時依序問：

```text
1. 字元格式是否合法？
2. 是否撞到 Python 關鍵字？
3. 名稱能否準確表達用途？
4. 是否符合一致的命名慣例？
```

---

## 五、值的表示必須精確

### 相同整數的不同進位表示

```python
decimal_number = 25
binary_number = 0b11001
octal_number = 0o31
hexadecimal_number = 0x19

print(decimal_number)
print(binary_number)
print(octal_number)
print(hexadecimal_number)
```

輸出都是：

```text
25
25
25
25
```

四種寫法產生相同的整數值，只是原始碼中的表示方式不同。

### 字串中的跳脫序列

換行字元寫成反斜線加小寫 `n`：

```python
message = "第一行\n第二行"
print(message)
```

輸出：

```text
第一行
第二行
```

`"\n"` 與 `"/n"` 不同：

- `\n` 是換行字元。
- `/n` 是普通斜線與字母 `n`。

### 大小寫不能混用

```python
is_active = True
is_deleted = False
```

下面的 `true` 只是一般 identifier；若之前沒有定義，使用時會發生 `NameError`：

```python
is_active = true
```

---

## 六、Notebook 操作練習

### 練習一：查詢與判斷關鍵字

```python
import keyword

print(keyword.kwlist)
print(keyword.iskeyword("if"))
print(keyword.iskeyword("IF"))
print(keyword.iskeyword("for"))
print(keyword.iskeyword("user_name"))
```

### 練習二：比較兩層名稱檢查

```python
import keyword

names = ["abc", "99a", "_abc", "user-name", "for"]

for name in names:
    print(
        name,
        "格式：",
        name.isidentifier(),
        "關鍵字：",
        keyword.iskeyword(name),
    )
```

先預測每列結果，再執行 Cell。預測錯誤的地方，才是最值得記錄的部分。

### 練習三：建立可重用的檢查函式

```python
import keyword


def is_valid_python_name(name: str) -> bool:
    return name.isidentifier() and not keyword.iskeyword(name)
```

自行加入五個名稱測試，其中至少包含：

- 一個清楚且合法的名稱。
- 一個數字開頭的名稱。
- 一個 Python 關鍵字。
- 一個包含減號的名稱。
- 一個格式合法但用途不清楚的名稱。

### 練習四：比較不同表示方式

```python
age = 30
binary_number = 0b11001
octal_number = 0o31
hexadecimal_number = 0x19
user_name = "Steve"
message = "第一行\n第二行"
is_active = True

print(age)
print(binary_number)
print(octal_number)
print(hexadecimal_number)
print(user_name)
print(message)
print(is_active)
```

完成後執行一次 Restart Kernel and Run All Cells，確認練習不依賴 Notebook 的舊狀態。

---

## 七、我可以立刻採取的實作清單

- [ ] 使用 `keyword.kwlist` 查看目前 Python 的關鍵字
- [ ] 比較 `"for".isidentifier()` 與 `keyword.iskeyword("for")`
- [ ] 完成 `is_valid_python_name()` 函式
- [ ] 為合法、非法與用途不清楚的名稱各寫一個測試
- [ ] 比較 `0b11001`、`0o31` 與 `0x19` 的輸出
- [ ] 親自比較 `"\n"` 與 `"/n"`
- [ ] 不看筆記回答下方複習題

---

## 八、複習題

先從記憶回答：

1. Keyword、identifier 與 literal 各是什麼？
2. 為什麼 `"for".isidentifier()` 會得到 `True`？
3. 如何判斷一個字串是否為一般可用的 Python 名稱？
4. 合法名稱為什麼不一定是好名稱？
5. `True` 與 `true` 有什麼差別？
6. `0b11001`、`0o31` 與 `0x19` 的共同點是什麼？
7. `"\n"` 與 `"/n"` 有什麼差別？

<details>
<summary>參考答案</summary>

1. Keyword 是 Python 保留字；identifier 是程式中的名稱；literal 是直接寫在原始碼中的固定值表示法。
2. 因為 `isidentifier()` 只檢查字元格式，不檢查關鍵字。
3. 使用 `name.isidentifier() and not keyword.iskeyword(name)` 進行本節的一般檢查。
4. 名稱即使語法合法，仍可能無法表達資料或行為的用途。
5. `True` 是 Python 關鍵字與布林常數；`true` 是一般名稱，未定義時會發生 `NameError`。
6. 它們都是整數 `25` 的不同進位表示法。
7. `\n` 是換行字元；`/n` 是兩個普通字元。

</details>

---

## 九、總結

這一節最重要的習慣是：

> 命名先確認格式合法，再確認沒有撞到關鍵字，最後確認名稱能清楚表達用途。

最常用的檢查方式是：

```python
name.isidentifier() and not keyword.iskeyword(name)
```

但工具只能檢查語法條件，不能替我判斷名稱是否清楚。專業程式碼同時需要：

1. 合法的名稱。
2. 準確的值表示。
3. 一致的命名慣例。
4. 可由工具驗證的判斷方式。

若練習結果與預期不同，可以直接把名稱、程式碼與實際輸出貼給教學助理詢問。

## 官方參考資料

- [Python 3.11：Identifiers and keywords](https://docs.python.org/3.11/reference/lexical_analysis.html#identifiers)
- [Python 3.11：Literals](https://docs.python.org/3.11/reference/lexical_analysis.html#literals)
- [Python 3.11：`keyword` 模組](https://docs.python.org/3.11/library/keyword.html)
- [Python 3.11：Built-in Constants](https://docs.python.org/3.11/library/constants.html)
- [PEP 8：Naming Conventions](https://peps.python.org/pep-0008/#naming-conventions)
