# 8-4 認識主鍵 (Primary Key)

## 這堂課在講什麼

說明關聯式資料庫中主鍵（Primary Key，PK）的定義與約束特性，包括「唯一性」與「不可為空值」兩大限制、單一主鍵與複合主鍵的差別，以及當欄位眾多時，如何依序從超級鍵（Super Key）、候選鍵（Candidate Key）篩選出主鍵（Primary Key）與次要鍵（Alternate Key）。

---

## 學完要會什麼

1. 說明主鍵的兩大限制：唯一性（值不重複）與不可為空值（NOT NULL）。
2. 理解主鍵約束（Constraint）的運作，以及寫入重複值或空值時資料庫的報錯機制。
3. 區分單一欄位主鍵與多欄位組成的複合主鍵（Composite Key）。
4. 依「唯一性（Super Key）→ 最小性（Candidate Key）→ 最適性（PK / Alternate Key）」的順序挑選主鍵。

---

## 重點整理

### 1. 主鍵（Primary Key）的定義與約束特性

- **基本定義**：英文為 Primary Key，簡稱 PK。主鍵是用來唯一識別資料表中每一筆紀錄的欄位。
- **約束機制（Constraint）**：主鍵是加在欄位上的資料庫限制。設定為主鍵後，資料庫會強制檢查：
  - **唯一性（Uniqueness）**：欄位內的值不能重複，每筆紀錄都必須獨一無二。
  - **不可為空值（NOT NULL）**：主鍵欄位不能為 NULL，否則無法識別。
- **重複寫入時的行為**：
  - 第一筆資料寫入 `978986000001` 成功。
  - 第二筆資料若再次寫入相同的 `978986000001`，資料庫會直接拒絕寫入並回傳錯誤（如 `Duplicate entry '...' for key 'PRIMARY'`）。
- **配置原則**：
  - 一張資料表最多只能設定一個主鍵。
  - 語法上允許不設主鍵，但資料庫管理系統通常會發出警示，強烈建議每張表都要建立主鍵。

---

### 2. 單一主鍵 vs 複合主鍵

| 類型 | 定義 | 適用場景 | 範例 |
| :--- | :--- | :--- | :--- |
| **單一欄位主鍵** | 單靠一個欄位就能滿足唯一性。 | 多數有天然唯一識別碼或自增編號的資料表。 | 書籍表的 `isbn`、出版社表的 `publisher_id`、會員表的 `user_id` |
| **複合主鍵<br>(Composite Key)** | 單一欄位無法獨立識別，需組合兩個以上欄位才能達到唯一。 | 多對多關聯的中介表、歷史記錄表、明細表。 | 選課表的 `(student_id, course_id)`、訂單明細表的 `(order_id, item_seq)` |

---

### 3. 主鍵挑選的三層篩選流程

當資料表欄位較多時，可依三步驟篩選合適的主鍵：

```text
【所有欄位集合】
       │
       ▼  篩選 1：找出所有具備「唯一性」的欄位或組合
【超級鍵 Super Key】（單一或多欄位組合）
       │
       ▼  篩選 2：去除冗餘欄位，只保留具備「最小性」者
【候選鍵 Candidate Key】（候選清單）
       │
       ▼  篩選 3：依業務需求選出最適欄位
   ┌───┴────────────────────────┐
   ▼                            ▼
【主鍵 Primary Key (PK)】   【次要鍵 / 替代鍵 Alternate Key】
 (最終選定作為主鍵)           (未被選為 PK 的候選鍵，可設為 UNIQUE)
```

#### 第一步：找出超級鍵（Super Key）：滿足唯一性
- **定義**：只要該欄位（或欄位組合）能唯一區分出每一列資料，就是 Super Key。
- **範例**：
  - `isbn`（單一欄位，值不重複）→ 是 Super Key
  - `書籍編號`（自訂編號，值不重複）→ 是 Super Key
  - `isbn + 書籍編號`（組合鍵，值不重複）→ 是 Super Key
  - `isbn + 書名`（組合鍵，值不重複）→ 是 Super Key

#### 第二步：篩出候選鍵（Candidate Key）：滿足唯一性與最小性
- **定義**：在 Super Key 中去除多餘欄位，只留下無法再刪減任何欄位的最小子集。
- **範例比較**：
  - `isbn`：只有 1 個欄位，具最小性 → 是 Candidate Key
  - `書籍編號`：只有 1 個欄位，具最小性 → 是 Candidate Key
  - `isbn + 書籍編號`：拿掉 `書籍編號` 後 `isbn` 依然具唯一性，代表有冗餘欄位，不符合最小性 → 淘汰

#### 第三步：決定主鍵（PK）與次要鍵（Alternate Key）
- **主鍵（Primary Key）**：從候選鍵中選出最合適、最常查詢的欄位作為主鍵。
- **次要鍵／替代鍵（Alternate Key）**：未被選為 PK 的其他候選鍵。
- **範例結果**：
  - 若選 `書籍編號` 作為 Primary Key，則 `isbn` 為 Alternate Key。
  - 若選 `isbn` 作為 Primary Key，則 `書籍編號` 為 Alternate Key。
  - 實務上常將 Alternate Key 設定為 `UNIQUE` 約束，確保不重複並輔助查詢。

---

## 範例與操作

### 1. 單一主鍵資料表宣告

```sql
-- 以 isbn 作為單一主鍵
CREATE TABLE books (
    isbn VARCHAR(13) PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    price INT UNSIGNED NOT NULL,
    author VARCHAR(100)
);
```

### 2. 測試主鍵唯一性限制（重複寫入報錯）

```sql
-- 1. 成功寫入第一筆資料
INSERT INTO books (isbn, title, price, author)
VALUES ('978986000001', 'Head First Java', 680, 'Sierra');

-- 2. 嘗試寫入相同主鍵值
INSERT INTO books (isbn, title, price, author)
VALUES ('978986000001', 'Learning Python', 750, 'Lutz');

-- 資料庫回傳錯誤：
-- ERROR 1062 (23000): Duplicate entry '978986000001' for key 'books.PRIMARY'
```

### 3. 複合主鍵資料表宣告

```sql
-- 學生選課表：以 (student_id, course_id) 組成複合主鍵
CREATE TABLE course_enrollments (
    student_id VARCHAR(10) NOT NULL,
    course_id VARCHAR(10) NOT NULL,
    enroll_date DATE NOT NULL,
    grade INT,
    CONSTRAINT pk_enrollments PRIMARY KEY (student_id, course_id)
);
```

### 4. 主鍵與次要鍵（UNIQUE）搭配宣告

```sql
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY, -- 選定為 Primary Key
    sku_code VARCHAR(30) NOT NULL UNIQUE,      -- 次要鍵（Alternate Key），設為 UNIQUE
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

---

## 常見誤解／注意事項

1. **誤解：一張表可以設定多個主鍵。**
   - **說明**：一張表只能有一個主鍵。若有多個欄位需保持唯一，只能選一個當主鍵，其餘設為 `UNIQUE` 約束；若是多個欄位合在一起識別，那是「一個複合主鍵」，並非多個主鍵。
2. **誤解：只要欄位值不會重複（Super Key）就能直接當主鍵。**
   - **說明**：Super Key 可能包含多餘欄位。必須先滿足最小性篩出候選鍵，再從中擇優選出，以降低索引開銷與複雜度。
3. **誤解：主鍵可以允許部分資料為 NULL。**
   - **說明**：主鍵不允許 NULL。在 SQL 中定義為 `PRIMARY KEY` 的欄位會自動包含 `NOT NULL` 約束。
4. **誤解：沒有天然唯一欄位時就不設主鍵。**
   - **說明**：若業務欄位無法保證唯一或過長，標準做法是加入代理鍵（Surrogate Key），如自動遞增整數 `id INT AUTO_INCREMENT` 或 UUID 作為系統主鍵。

---

## 重點速記

| 概念名詞 | 英文術語 | 必備條件 | 角色與用途 |
| :--- | :--- | :--- | :--- |
| **超級鍵** | Super Key | 唯一性 | 能唯一識別資料列的任何欄位或組合。 |
| **候選鍵** | Candidate Key | 唯一性 ＋ 最小性 | 超級鍵中去除冗餘欄位後的最小集合。 |
| **主鍵** | Primary Key (PK) | 唯一性 ＋ 最小性 ＋ NOT NULL | 從候選鍵中選出的唯一代表，每張表最多一個。 |
| **次要鍵** | Alternate Key | 唯一性 ＋ 最小性 | 未被選為主鍵的其他候選鍵，通常設為 `UNIQUE`。 |
| **複合主鍵** | Composite Key | 多欄位組合 ＋ 唯一性 | 單一欄位無法唯一識別時，組合多個欄位作為主鍵。 |
