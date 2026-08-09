# 8-5 字元分類：用 `ord()` 與 `if` / `elif` / `else` 判斷字元類型

## 這堂課在講什麼

Practice 2 要求輸入一個字元，判斷它屬於下列哪一類：

- 英文大寫字母：輸出 `Uppercase character`
- 英文小寫字母：輸出 `Lowercase character`
- 數字：輸出 `digit`
- 以上皆非：輸出 `special character`

這題利用 ASCII 編碼的數值區間分類，再用 `if` / `elif` / `else` 做四選一的判斷。

## 學完要會什麼

完成這一節後，應該能夠：

1. 說明 ASCII 編碼如何替字元對應一個數字。
2. 用 `ord()` 取得輸入字元的 ASCII 碼。
3. 用數值區間判斷英文字母、數字與特殊字元。
4. 用 `if` / `elif` / `else` 確保四種結果中一定會執行其中一種。

## 重點整理

### ASCII 編碼與 `ord()`

ASCII 編碼會為鍵盤上的字元對應一個數字。例如：

| 字元類型 | ASCII 碼範圍 |
| --- | --- |
| 空白 | `32` |
| 數字 `0` 到 `9` | `48` 到 `57` |
| 大寫 `A` 到 `Z` | `65` 到 `90` |
| 小寫 `a` 到 `z` | `97` 到 `122` |

`ord()` 可以把輸入的字元轉成它對應的 ASCII 碼：

```python
ch = input()
code = ord(ch)
```

輸入的 `ch` 會交給 `ord()`，結果存入 `code`，後續便可用數值範圍判斷字元類型。

### 用區間判斷字元類型

判斷時依序檢查：大寫字母、小寫字母、數字；都不符合時，交由 `else` 判定為特殊字元。

```python
ch = input()
code = ord(ch)

if ord("A") <= code <= ord("Z"):
    print("Uppercase character")
elif ord("a") <= code <= ord("z"):
    print("Lowercase character")
elif ord("0") <= code <= ord("9"):
    print("digit")
else:
    print("special character")
```

`if` / `elif` / `elif` / `else` 是同一條決策鏈。程式會依序檢查條件，找到第一個成立的分支後就執行；若前三個條件都不成立，最後一定會進入 `else`。因此，四種分類中必定有一種結果。

## 範例與操作

若輸入 `G`，`ord("G")` 落在大寫字母的區間，輸出：

```text
Uppercase character
```

若輸入 `m`，會輸出：

```text
Lowercase character
```

若輸入 `7`，會輸出：

```text
digit
```

其他不在三個區間內的字元，則輸出：

```text
special character
```

### 實務上也可以直接比較字元

這一題使用 `ord()` 的目的，是理解字元背後有對應的編碼數值，以及如何用數值區間做分類。若需求明確是判斷 ASCII 的英文大小寫字母與數字，實務上通常可直接比較字元區間，少一個 `code` 變數，也更容易閱讀：

```python
ch = input()

if "A" <= ch <= "Z":
    print("Uppercase character")
elif "a" <= ch <= "z":
    print("Lowercase character")
elif "0" <= ch <= "9":
    print("digit")
else:
    print("special character")
```

這和前面的 `ord()` 寫法結果相同；Python 會依字元的編碼順序進行比較。對這種固定三種分類的題目而言，兩種寫法每次最多做固定次數的判斷，時間複雜度都是 `O(1)`，不需要為了效能特別優化。

`ch.isupper()`、`ch.islower()`、`ch.isdigit()` 也能用來分類，但它們依 Unicode 的規則判斷。例如，某些非 ASCII 的文字或數字也可能被視為大寫、小寫或數字。題目若指定 ASCII，使用 `"A" <= ch <= "Z"`、`"a" <= ch <= "z"`、`"0" <= ch <= "9"` 會更符合需求。

## 注意事項

- 這題的輸入前提是一個字元，逐字稿沒有示範多個字元時的處理方式。
- 大寫英文字母的 ASCII 範圍是 `A` 到 `Z`，也就是 `65` 到 `90`。程式判斷時要用完整的 `A`–`Z` 區間。

## 一句話回顧

先用 `ord()` 把字元轉為 ASCII 碼，再用 `if` / `elif` / `else` 比對所在區間，就能將它分類為大寫字母、小寫字母、數字或特殊字元。
