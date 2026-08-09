# 9-1 `while` 迴圈：重複執行、`break` 與 `continue`

## 這堂課在講什麼

迴圈讓電腦能重複執行同一段程式碼。這一節介紹 `while`：只要條件仍是 `True`，程式就會持續執行縮排區塊；每一輪結束後，再回頭檢查一次條件。

本節也會用猜數字、累加 1 到 100 的例子，說明如何用 `break` 離開迴圈，以及用 `continue` 跳過本輪剩下的程式碼。

## 學完要會什麼

完成本節後，我應該能夠：

1. 寫出基本的 `while` 迴圈，並追蹤每一輪的條件與變數變化。
2. 用 `while` 寫出重複輸入直到猜中的程式。
3. 說明 `break` 與 `continue` 分別會讓流程跳到哪裡。
4. 用累加器計算 1 到 100，或只加總其中的偶數。
5. 發現無窮迴圈時，在 Jupyter Notebook 重新啟動 Kernel。

---

## 一、`while` 的基本概念

`while` 後面接一個條件。條件為 `True` 時，執行縮排的程式區塊；區塊執行完後，程式會回到 `while` 再檢查條件。只要條件持續為真，這個過程就會重複。

```python
while 條件:
    條件為 True 時重複執行的程式碼
```

流程可以想成：

```text
檢查條件 → True → 執行程式區塊 → 回到條件
     └──── False ───→ 離開迴圈
```

### 範例：印出 1 到 5

```python
i = 1

while i < 6:
    print(i)
    i += 1
```

輸出：

```text
1
2
3
4
5
```

第一輪先判斷 `1 < 6`，結果為 `True`，所以印出 `1`，再把 `i` 加 1。之後依序檢查 `2 < 6`、`3 < 6`……當 `i` 變成 `6`，`6 < 6` 為 `False`，迴圈結束。

> 在 `while` 中，要確認條件會在適當的時機變成 `False`。上例的 `i += 1` 就是讓迴圈能停止的關鍵。

---

## 二、猜數字：用條件控制迴圈何時結束

以下程式會持續要求使用者猜 1 到 6 的數字，直到猜中 `answer` 為止。

```python
answer = 3
guess = 0

while guess != answer:
    guess = int(input("Please enter a digit from 1 to 6: "))

    if guess > answer:
        print("bigger than the answer")
    elif guess < answer:
        print("smaller than the answer")
    else:
        print("bingo")
```

一開始 `guess` 是 `0`，而 `0 != 3` 為 `True`，因此進入迴圈。若依序輸入 `1`、`4`、`3`，結果會是：

```text
smaller than the answer
bigger than the answer
bingo
```

每次輸入後，程式都會回到 `while guess != answer:` 檢查。輸入 `3` 後，`guess != answer` 變成 `False`，因此印出 `bingo` 後就離開迴圈。

---

## 三、`break`：立刻跳出迴圈

`break` 出現在迴圈內時，程式會立刻離開整個迴圈，不會再執行本輪後面的程式，也不會再進行下一輪。它常和 `if` 搭配，在特定條件發生時停止。

```python
answer = 3

while True:
    guess = int(input("Please enter a digit from 1 to 6: "))

    if guess > answer:
        print("bigger than the answer")
    elif guess < answer:
        print("smaller than the answer")
    else:
        print("bingo")
        break
```

`while True` 的條件永遠為真，所以若沒有 `break`，迴圈會一直執行。這個版本和前面的猜數字程式功能相同：猜到 `3` 時，先印出 `bingo`，再用 `break` 離開迴圈。

### 練習無窮迴圈時的注意事項

初學時很容易不小心寫出跳不出去的無窮迴圈。在 Jupyter Notebook 中，若 cell 長時間顯示 `[*]`，表示 Kernel 仍處於 busy 狀態；課程建議按 **Kernel Restart** 重新啟動 Notebook。

---

## 四、`continue`：跳過本輪剩下的程式碼

`continue` 不會離開整個迴圈。它會直接結束目前這一輪，回到 `while` 的條件處重新判斷；若條件仍為 `True`，才開始下一輪。

```python
while True:
    x = int(input("Please enter a digit from 1 to 6: "))

    if x == 1:
        print("continue statement")
        continue
    else:
        print("enter else block")

    print("still in while loop")
```

輸入 `1` 時，程式印出 `continue statement` 後就回到 `while True`。因此 `print("still in while loop")` 會被跳過。輸入不是 `1` 的數字時，程式會進入 `else`，接著也會印出 `still in while loop`，最後才回到迴圈開頭。

| 語法 | 發生後的流程 |
| --- | --- |
| `break` | 立刻離開整個迴圈 |
| `continue` | 跳過本輪剩下的程式碼，回到 `while` 條件 |

---

## 五、用 `while` 累加 1 到 100

累加時通常需要兩個變數：`i` 用來記錄目前加到哪個數字，`number_sum` 用來保存累積結果。

```python
i = 0
number_sum = 0

while i <= 100:
    number_sum = number_sum + i
    i = i + 1

print(number_sum)
```

這段程式把 `0` 到 `100` 加進 `number_sum`；加上 `0` 不影響結果，所以最後得到的就是 1 加到 100 的總和。

前幾輪的變化如下：

| 輪次 | 加入的 `i` | 累加後的 `number_sum` | 下一輪的 `i` |
| --- | ---: | ---: | ---: |
| 1 | 0 | 0 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 2 | 3 | 3 |

如果看不懂迴圈如何變動，可以在迴圈內印出想觀察的變數：

```python
print(i, number_sum)
```

逐輪查看值的變化，比只看最後答案更容易理解迴圈。

---

## 六、搭配 `continue`：只加總偶數

若要計算 `2 + 4 + 6 + ... + 100`，可以在遇到奇數時先讓 `i` 加 1，再用 `continue` 跳過累加的程式碼。

```python
i = 0
number_sum = 0

while i <= 100:
    if i % 2 == 1:
        i = i + 1
        continue

    number_sum = number_sum + i
    i = i + 1

print(number_sum)
```

當 `i` 是奇數時，例如 `1`，會先變成 `2`，然後直接回到條件判斷，因此不會執行 `number_sum = number_sum + i`。偶數才會被加進 `number_sum`。

> `continue` 前必須先更新 `i`。如果奇數時直接 `continue`，`i` 會一直停在同一個奇數，造成無窮迴圈。

---

## 七、用 `while True` 完成 1 到 100 的累加

同一件事也能寫成無窮迴圈，然後在數字超過範圍時以 `break` 結束：

```python
i = 0
number_sum = 0

while True:
    i = i + 1

    if i > 100:
        break

    number_sum = number_sum + i

print(number_sum)
```

這個版本先把 `i` 加 1；當 `i` 變成 `101` 時，`i > 100` 成立，立刻 `break`，因此只會把 1 到 100 加進 `number_sum`。

---

## 常見誤解／注意事項

- `while` 不是只檢查一次條件；每輪程式區塊結束後都會再檢查一次。
- `while True` 本身不會自動結束，通常要在迴圈內安排 `break`。
- `break` 是離開整個迴圈；`continue` 只是跳過目前這一輪剩下的程式碼。
- 想知道迴圈為什麼結果不如預期時，先在迴圈裡 `print()` 目前的變數值，逐輪觀察。
- 無窮迴圈會讓 Jupyter Notebook 一直顯示 busy；若長時間沒有結束，可重新啟動 Kernel。

## 一句話回顧

`while` 會在條件為 `True` 時重複執行程式區塊；用變數更新或 `break` 安排結束時機，用 `continue` 略過本輪不需要處理的部分。
