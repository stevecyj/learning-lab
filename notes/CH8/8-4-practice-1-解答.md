# Practice 1 解答：變數交換與條件判斷

## 這堂課在講什麼

本節檢討 Practice 1 的三題：交換兩個變數的值、判斷輸入字元是否為母音，以及依分數判定等第。重點在於將輸入轉成合適的型別，再用條件判斷處理不同情況。

## 學完要會什麼

- 用暫存變數交換兩個變數的值。
- 用 `in` 或多個 `or` 條件判斷字元是否為母音。
- 將 `input()` 的結果轉成整數，依分數區間設定等第。

## 重點整理

### 1. 用暫存變數交換 `a` 和 `b`

假設 `a = 5`、`b = 3`，目標是讓 `a` 變成 `3`、`b` 變成 `5`。直接把 `b` 指派給 `a`，原本 `a` 的值會消失，因此要先用暫存變數保存它。

```python
temp = a  # 先保存 a 原本的值
a = b     # 將 b 的值放入 a
b = temp  # 將原本的 a 放入 b
```

這題和 `if...else` 沒有直接關係，主要是練習變數指派的順序。

### 2. 判斷字元是否為母音

母音（vowel）是 `a`、`e`、`i`、`o`、`u`。輸入一個字元後，若它是母音就印出 `True`，否則印出 `False`。

可以先把所有母音放進串列，再用 `in` 判斷：

```python
character = input("請輸入一個字元：")
vowels = ["a", "e", "i", "o", "u"]

if character not in vowels:
    print(False)
else:
    print(True)
```

也可以逐一比較：

```python
character = input("請輸入一個字元：")

if character == "a" or character == "e" or character == "i" or character == "o" or character == "u":
    print(True)
else:
    print(False)
```

兩種寫法都能完成題目；程式沒有唯一寫法，功能正確即可。

### 3. 依分數判定等第

先輸入分數，並將 `input()` 得到的文字轉成整數。接著依分數區間設定 `rank`：

- `0` 到 `60`：`C`
- `60` 到 `90`：`B`
- `90` 到 `100`：`A`

概念上可先設定 `rank`，再確認它不是 `None` 後輸出結果：

```python
score = int(input("請輸入一個整數："))
rank = None

if 0 <= score <= 60:
    rank = "C"
elif 60 <= score <= 90:
    rank = "B"
elif 90 <= score <= 100:
    rank = "A"

if rank is not None:
    print("score is", rank)
```

## 範例與操作

1. 輸入母音 `a`，程式應印出 `True`。
2. 輸入非母音字元，程式應印出 `False`。
3. 輸入一個 `0` 到 `100` 的整數，依條件設定並輸出對應的 `rank`。

## 常見誤解／注意事項

- `input()` 的回傳值是文字；分數要拿來比較前，需用 `int()` 轉成整數。
- 變數交換時，不能先覆寫掉仍需要的原始值；先用 `temp` 保存即可避免這個問題。
- 講解中的分數區間在 `60` 與 `90` 有重疊。這段 `if...elif` 會由上到下判斷，因此 `60` 會先符合 `C`，`90` 會先符合 `B`。

## 一句話回顧

Practice 1 練習用暫存變數處理值交換，並用條件判斷完成母音辨識與分數等第判定。
