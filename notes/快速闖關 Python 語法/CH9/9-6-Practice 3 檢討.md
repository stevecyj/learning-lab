# 9-6 Practice 3：檢討

## 這堂課在講什麼

本節檢討四個練習：用巢狀迴圈印出直角三角形、手動加總串列中的數字、找出串列最大值，以及移除串列中的重複元素。

## 學完要會什麼

- 用外層與內層迴圈控制每一列要印出的字元數。
- 用累積變數逐一加總 `list` 中的數字。
- 先假設第一個元素最大，再逐一比較並更新最大值。
- 利用 `set` 判斷元素是否重複，或直接用型別轉換去除重複值。

## 重點整理

### 第一題：用巢狀迴圈印出直角三角形

題目要印出往右的直角三角形。外層迴圈控制列數，內層迴圈控制同一列要印出的 `*`；只有當 `j <= i` 時才印出星號。

```python
for i in range(1, 4):
    for j in range(1, 4):
        if j <= i:
            print("*", end="")
    print()
```

輸出結果：

```text
*
**
***
```

`print("*", end="")` 讓星號留在同一行；內層迴圈結束後的 `print()` 才負責換行。

也可以直接讓內層迴圈依照目前的 `i` 執行：

```python
for i in range(1, 4):
    for j in range(i):
        print("*", end="")
    print()
```

兩種寫法會得到相同結果。

### 第二題：加總 list 中的所有數字

先把加總結果 `sum_number` 設成 `0`，再逐一取出 `my_list` 的元素。每跑一圈，就把目前的元素加進累積結果。

```python
my_list = [1, 2, 3, 4, 5]
sum_number = 0

for x in my_list:
    sum_number += x

print(sum_number)
```

`sum_number += x` 等同於 `sum_number = sum_number + x`。迴圈結束後，`sum_number` 就是所有元素的總和。

Python 也提供內建的 `sum()` 函數：

```python
sum_number = sum(my_list)
```

不過這題的重點是理解累積加總的過程；`sum()` 底層的做法和逐一把元素加進結果的概念相近。

### 第三題：找出 list 中的最大值

先把第一個元素暫時當成最大值，接著逐一比較串列中的元素。只要目前元素比 `max_number` 大，就立刻更新 `max_number`。

```python
my_list = [3, 8, 2, 10, 5]
max_number = my_list[0]

for x in my_list:
    if x > max_number:
        max_number = x

print(max_number)
```

這個做法假設 `my_list` 至少有一個元素，因為一開始要用 `my_list[0]` 作為比較基準。

Python 也有對應的內建函數：

```python
max_number = max(my_list)
```

先理解手動比較的原理，再使用 `max()`，會更清楚它替我們省下了哪些步驟。

### 第四題：移除 list 中的重複元素

可以準備一個空的 `set` 來記錄已經看過的元素，以及一個空的 `list` 來保存不重複的結果。走訪 `my_list` 時，只有在元素還不在 `seen` 中，才把它加入 `set` 和結果串列。

```python
my_list = [1, 2, 2, 3, 1, 4]
seen = set()
unique_list = []

for x in my_list:
    if x not in seen:
        seen.add(x)
        unique_list.append(x)

print(unique_list)
```

`set` 不會保留重複元素，因此也能用較短的寫法：先把 `list` 轉成 `set`，再轉回 `list`。

```python
unique_list = list(set(my_list))
```

## 常見誤解／注意事項

- 印圖形時，`end=""` 決定星號是否留在同一列；少了它，每個星號都會自動換行。
- 加總的累積變數要從 `0` 開始；找最大值則從第一個元素開始當基準。
- 找最大值時，只在目前元素更大時才更新 `max_number`。
- 用 `set` 去除重複值後，若還需要 `list` 型別，要再用 `list()` 轉回來。

## 一句話回顧

這四題都靠逐一走訪資料：依條件印出字元、累積數字、更新目前最大值，或只保留第一次出現的元素。
