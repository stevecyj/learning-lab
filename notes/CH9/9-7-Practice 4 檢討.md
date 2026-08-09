# 9-7 Practice 4：檢討

## 這堂課在講什麼

本節檢討三題練習：判斷大於 `1` 的整數是否為質數、將字串轉成小寫後統計每個字元出現的頻率，以及找出 `list` 中最長的英文單字。

## 學完要會什麼

- 用旗標變數記錄一個數目前是否仍可能是質數。
- 用 `%` 檢查數字是否可被整除，並在找到因數後用 `break` 結束迴圈。
- 用字典累積字元出現的次數。
- 先把第一個元素當成目前最長的單字，再逐一比較並更新結果。

## 重點整理

### 第一題：判斷質數

題目會輸入一個大於 `1` 的整數 `number`。先假設它是質數，將 `is_prime` 設為 `1`；若找到任何能整除它的數，就把 `is_prime` 改成 `0`。

以 `101` 為例，檢查 `2` 到 `101 // 2`，也就是 `2` 到 `50` 之間是否有數能整除 `101`。若都沒有，`101` 就是質數。

```python
number = int(input("請輸入大於 1 的整數："))
is_prime = 1

for i in range(2, number // 2 + 1):
    if number % i == 0:
        is_prime = 0
        break

if is_prime == 0:
    print("this is not a prime number")
else:
    print("this is a prime number")
```

`number % i == 0` 代表 `number` 可以被 `i` 整除，所以它不是質數。找到一個因數就已經足夠判定，因此可立刻用 `break` 離開迴圈。

### 第二題：統計字串的字元頻率

先把輸入字串用 `.lower()` 轉成小寫，再準備一個空字典。逐一走訪字串中的每個字元：若字元已經在字典裡，就把對應的次數加 `1`；否則新增這個字元，並將次數設為 `1`。

```python
text = input("請輸入字串：").lower()
char_count = {}

for char in text:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1

print(char_count)
```

例如字串 `hello I am Isaac.Nice to meet you` 轉成小寫後，`I` 和 `i` 都會以小寫 `i` 統計。這個做法會統計字串中的每個字元，包括空白與標點符號。

### 第三題：找出 list 中最長的英文單字

做法和找出串列最大值相同：先把 `my_list` 的第一個元素 `isaac` 假設為目前最長的單字，接著逐一比較其他元素的長度。只要目前單字比較長，就覆寫 `max_long_word`。

```python
my_list = ["isaac", "amy", "christtina", "tom"]
max_long_word = my_list[0]

for word in my_list:
    if len(word) > len(max_long_word):
        max_long_word = word

print(max_long_word)
```

迴圈跑完後，`max_long_word` 會是 `christtina`，因為它的字元數最多。

## 常見誤解／注意事項

- 題目已限定輸入數字大於 `1`。判斷質數時，只要找到一個可整除的數，就可以判定它不是質數。
- `range()` 不包含停止位置；若要檢查到 `number // 2`，停止位置要再加 `1`。
- 字元頻率統計先做 `.lower()`，才會把大小寫不同、但字母相同的字元算在一起。
- 第一個單字用來當比較基準，所以 `my_list` 必須至少有一個元素。

## 一句話回顧

這三題都用迴圈逐一走訪資料：找到因數就改變質數旗標、遇到字元就更新字典次數、看到更長的單字就更新目前結果。
