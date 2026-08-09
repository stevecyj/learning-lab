# 7-5 Practice 2：Heron 公式、串列切片與字典新增

## 學習目標

完成這一節後，我應該能夠：

1. 讀取三個邊長，並用 Heron 公式計算三角形面積。
2. 使用 `** 0.5` 或 `math.sqrt()` 計算平方根。
3. 用 `list[start:stop]` 擷取串列的一部分。
4. 用 `del` 刪除串列中的單一元素或一段元素。
5. 用 `dictionary[key] = value` 新增或更新字典的鍵值對。

---

## 一、用 Heron 公式計算三角形面積

已知三角形的三個邊長 `a`、`b`、`c`，先計算半周長 `s`：

```text
s = (a + b + c) / 2
```

再套用 Heron 公式：

```text
面積 = √(s × (s - a) × (s - b) × (s - c))
```

### 基本寫法

`input()` 回傳的是字串，因此要先轉成數字。這裡使用 `float()`，讓程式也能接受 `3.5` 之類的邊長：

```python
a = float(input("請輸入第一個邊長："))
b = float(input("請輸入第二個邊長："))
c = float(input("請輸入第三個邊長："))

s = (a + b + c) / 2
area = (s * (s - a) * (s - b) * (s - c)) ** 0.5

print(f"三角形面積：{area}")
```

在 Python 中，`**` 是次方運算子。平方根等於 `0.5` 次方，所以：

```python
number ** 0.5
```

也可以改用 `math.sqrt()`，直接表達「計算平方根」：

```python
import math

area = math.sqrt(s * (s - a) * (s - b) * (s - c))
```

參考：[Python 官方文件：`math.sqrt()`](https://docs.python.org/3/library/math.html#math.sqrt)

### 先確認三邊能構成三角形

三角形任意兩邊之和必須大於第三邊。若輸入 `1`、`2`、`10`，Heron 公式根號內會變成負數。此時 `** 0.5` 會得到複數，`math.sqrt()` 則會拋出 `ValueError`。

實際計算前，先檢查三個邊長：

```python
import math

a = float(input("請輸入第一個邊長："))
b = float(input("請輸入第二個邊長："))
c = float(input("請輸入第三個邊長："))

if a <= 0 or b <= 0 or c <= 0:
    print("邊長必須大於 0")
elif a + b <= c or a + c <= b or b + c <= a:
    print("這三個邊長無法構成三角形")
else:
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    print(f"三角形面積：{area:.2f}")
```

若輸入 `3`、`4`、`5`，半周長是 `6`，面積是 `6.00`。

---

## 二、串列切片遵守「起點包含、終點不包含」

以這個串列為例：

```python
my_list = ["a", "p", "p", "l", "e"]
```

元素和索引的對應如下：

| 元素次序 | 第 1 個 | 第 2 個 | 第 3 個 | 第 4 個 | 第 5 個 |
| --- | --- | --- | --- | --- | --- |
| 索引 index | `0` | `1` | `2` | `3` | `4` |
| 元素 | `"a"` | `"p"` | `"p"` | `"l"` | `"e"` |

切片的基本語法是：

```python
my_list[start:stop]
```

- `start` 指定開始索引，結果包含這個位置。
- `stop` 指定停止索引，結果不包含這個位置。
- 省略 `start` 表示從頭開始。
- 省略 `stop` 表示取到最後。

### 常見範例

```python
print(my_list[2:5])  # ['p', 'l', 'e']，第 3 到第 5 個元素
print(my_list[:3])   # ['a', 'p', 'p']，前 3 個元素
print(my_list[1:])   # ['p', 'p', 'l', 'e']，第 2 個元素到最後
print(my_list[:])    # ['a', 'p', 'p', 'l', 'e']，全部元素的淺層複本
```

> 逐字稿將「從頭到第三個元素」寫成 `my_list[:4]`，但 `[:4]` 會取得前四個元素。若要取得前三個元素，正確寫法是 `my_list[:3]`。

切片範圍和 `range(start, stop)` 一樣，都是左含右不含。

參考：[Python 官方教學：字串與串列切片](https://docs.python.org/3/tutorial/introduction.html#lists)

---

## 三、用 `del` 刪除串列元素

`del` 可以依索引刪除一個元素，也可以搭配切片一次刪除多個元素。它會直接修改原串列，不會回傳被刪除的內容。

### 刪除單一元素

```python
letters = ["p", "r", "o", "g", "r", "a", "m"]

del letters[2]

print(letters)  # ['p', 'r', 'g', 'r', 'a', 'm']
```

索引 `2` 是第三個元素，所以被刪除的是 `"o"`。

### 刪除一段元素

```python
letters = ["p", "r", "o", "g", "r", "a", "m"]

del letters[1:6]

print(letters)  # ['p', 'm']
```

`del letters[1:6]` 會刪除索引 `1` 到 `5`，不包含索引 `6`。刪除後，原本後方的元素會向前補位。

> 逐字稿提到刪除 `index 1` 到 `index 5` 後只剩 `p` 和 `m`。若原串列是 `list("program")`，對應的切片應是 `[1:6]`；寫成 `[1:5]` 還會留下 `"a"`。

其他常見寫法：

```python
del letters[:]  # 刪除全部元素，但保留這個串列物件
```

需要取回被刪除的單一元素時，可以改用 `pop(index)`。

參考：[Python 官方教學：`del` statement](https://docs.python.org/3/tutorial/datastructures.html#the-del-statement)

---

## 四、用鍵指定值，新增或更新字典

假設原本有一個字典：

```python
d = {
    0: 10,
    1: 20,
}
```

將值指定給尚不存在的鍵，就會新增一組鍵值對：

```python
d[2] = 30

print(d)  # {0: 10, 1: 20, 2: 30}
```

語法可以讀成：把值 `30` 存到字典 `d` 的鍵 `2`。

鍵已經存在時，同一種語法會更新原值；字典不會保留重複的鍵：

```python
d[2] = 99

print(d)  # {0: 10, 1: 20, 2: 99}
```

也可以用 `update()` 加入鍵值對：

```python
d.update({2: 30})
```

新增或更新一組資料時，直接寫 `d[2] = 30`。一次處理多組資料時，再使用 `update()`。

參考：[Python 官方教學：Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

---

## 五、快速複習

| 目的 | 寫法 | 關鍵觀念 |
| --- | --- | --- |
| 計算半周長 | `s = (a + b + c) / 2` | `/` 的結果是浮點數 |
| 計算平方根 | `x ** 0.5` | 等同於 x 的二分之一次方 |
| 取第 3～5 個元素 | `items[2:5]` | 元素次序要減 1 才是索引 |
| 取前三個元素 | `items[:3]` | 終點 `3` 不包含在內 |
| 取第二個到最後 | `items[1:]` | 省略終點代表到最後 |
| 複製整個串列 | `items[:]` | 產生新的淺層複本 |
| 刪除第三個元素 | `del items[2]` | `del` 直接修改原串列 |
| 刪除索引 1～5 | `del items[1:6]` | 終點索引 `6` 不包含在內 |
| 新增字典資料 | `d[2] = 30` | 鍵不存在時新增 |
| 更新字典資料 | `d[2] = 99` | 鍵存在時覆蓋原值 |

## 自我檢查

先不要執行程式，試著從記憶回答：

1. `list("python")[1:4]` 會得到什麼？
2. 若要刪除串列最後兩個元素，可以怎麼寫？
3. `scores["Amy"] = 90` 在什麼情況下是新增？什麼情況下是更新？
4. 邊長 `2`、`3`、`6` 能不能套用 Heron 公式計算一般三角形面積？為什麼？

<details>
<summary>查看答案</summary>

1. `["y", "t", "h"]`。
2. `del items[-2:]`。
3. 字典沒有 `"Amy"` 這個鍵時是新增；已經有這個鍵時是更新。
4. 不能，因為 `2 + 3 <= 6`，不符合任意兩邊之和大於第三邊的條件。

</details>
