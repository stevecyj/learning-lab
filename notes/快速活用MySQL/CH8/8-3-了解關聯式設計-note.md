# 8-3 了解關聯式設計

## 核心內容

關聯式資料庫將不同實體拆分到各自獨立的資料表，再用外來鍵（Foreign Key）建立關聯，藉此消除單一大表格（Flat Table）帶來的資料重複與維護問題。

### 1. 單一大表格的三大問題

若把書籍資訊（ISBN、書名、定價、作者）與出版社資訊（名稱、聯絡人、電話、地址）全塞進同一張表，會出現三個問題：

- **浪費儲存空間**：多本書籍屬於同一出版社時，出版社名稱、電話、地址每次都要重複寫入。資料量一大，儲存空間就會被重複內容佔滿。
- **輸入錯誤率增加**：每次新增書籍都要重打一次出版社資訊，容易因錯字或格式不一致產生衝突。
- **維護困難（更新異常）**：出版社更換電話或聯絡人時，必須找出所有包含該出版社的書籍逐一修改。資料一旦分散在數萬筆紀錄中，容易漏改，造成同一出版社在不同列有不同資料。

### 2. 關聯式設計：拆分實體並以鍵值連結

把單一大表格拆成兩張主題明確的資料表：

1. **書籍表（`books`）**：存放書籍本身屬性（`isbn`、`title`、`price`、`author`），並加上關聯欄位 `publisher_id`。
2. **出版社表（`publishers`）**：以 `publisher_id` 作為主鍵（Primary Key），統一存放出版社資料（`publisher_name`、`contact_name`、`phone`、`address`）。

```text
【未拆分前：單一大表格】
+---------------+---------------------+-------+-----------+----------------+--------------+-------------------+
| isbn          | title               | price | author    | publisher_name | contact_name | phone             |
+---------------+---------------------+-------+-----------+----------------+--------------+-------------------+
| 978986000001  | Head First Java     |   680 | Sierra    | O'Reilly       | John         | 02-12345678       |
| 978986000002  | Learning Python     |   750 | Lutz      | O'Reilly       | John         | 02-12345678       |
| 978986000003  | Fluent Python       |   880 | Ramalho   | O'Reilly       | John         | 02-12345678       |
+---------------+---------------------+-------+-----------+----------------+--------------+-------------------+
(出版社資訊重複儲存 3 次)

【拆分後：關聯式設計】
[books 表]                                      [publishers 表]
+---------------+---------------------+-------+--------------+       +--------------+----------------+--------------+-------------------+
| isbn          | title               | price | publisher_id | ----> | publisher_id | publisher_name | contact_name | phone             |
+---------------+---------------------+-------+--------------+  FK   +--------------+----------------+--------------+-------------------+
| 978986000001  | Head First Java     |   680 | P001         |       | P001         | O'Reilly       | John         | 02-12345678       |
| 978986000002  | Learning Python     |   750 | P001         |       +--------------+----------------+--------------+-------------------+
| 978986000003  | Fluent Python       |   880 | P001         |       (出版社資訊僅存 1 次)
+---------------+---------------------+-------+--------------+
```

### 3. 關聯欄位的作用

- **維持資料關聯**：書籍表拿掉出版社詳細資料後，只要保留 `publisher_id`，就能在需要聯絡出版社（如補貨）時向 `publishers` 表查詢。
- **單點維護**：出版社聯絡人或電話異動時，只要更新 `publishers` 表中的該筆紀錄，所有透過 `publisher_id` 關聯的書籍查詢都會自動得到最新結果。
- **不能刪除關鍵關聯欄位**：拆分表格時必須留下 `publisher_id` 作為對應依據；若缺少這個欄位，兩張表就失去連結，無法還原完整資訊。

---

## 開發上可採取的行動步驟

1. **劃分業務實體**：檢視資料欄位，依主題區分實體（如書籍、出版社、會員、訂單），一張表只負責一個實體。
2. **抽取重複欄位並建立主表**：把重複出現的屬性抽成獨立資料表，並為新表指定唯一的主鍵（如 `publisher_id`）。
3. **在子表建立外來鍵**：在多方資料表（如書籍）加入外來鍵欄位，對應到主表的主鍵，並確認兩邊欄位的型別與長度一致。
4. **透過 JOIN 查詢重組資料**：業務端需要跨實體完整資訊時，使用 SQL `JOIN` 語法透過關聯欄位組合查詢。

---

## 我可以立刻採取的實作清單

- [ ] **建立主表與子表 Schema**：建立 `publishers` 與 `books` 兩張表並設定外來鍵限制。
  ```sql
  -- 1. 建立出版社表（主表）
  CREATE TABLE publishers (
      publisher_id VARCHAR(10) PRIMARY KEY,
      publisher_name VARCHAR(100) NOT NULL,
      contact_name VARCHAR(50),
      phone VARCHAR(20),
      address VARCHAR(200)
  );

  -- 2. 建立書籍表（子表，包含外來鍵欄位）
  CREATE TABLE books (
      isbn VARCHAR(13) PRIMARY KEY,
      title VARCHAR(150) NOT NULL,
      price INT UNSIGNED NOT NULL,
      author VARCHAR(100),
      publisher_id VARCHAR(10),
      CONSTRAINT fk_books_publishers
          FOREIGN KEY (publisher_id)
          REFERENCES publishers (publisher_id)
  );
  ```
- [ ] **新增測試資料**：
  ```sql
  -- 先建立出版社資料
  INSERT INTO publishers (publisher_id, publisher_name, contact_name, phone, address)
  VALUES ('P001', 'O''Reilly Media', 'John Doe', '02-12345678', '台北市信義區信義路五段7號');

  -- 再建立參照該出版社的多本書籍
  INSERT INTO books (isbn, title, price, author, publisher_id)
  VALUES 
      ('978986000001', 'Head First Java', 680, 'Kathy Sierra', 'P001'),
      ('978986000002', 'Learning Python', 750, 'Mark Lutz', 'P001');
  ```
- [ ] **執行 JOIN 跨表查詢**：
  ```sql
  SELECT 
      b.isbn,
      b.title,
      b.price,
      b.author,
      p.publisher_name,
      p.contact_name,
      p.phone
  FROM books b
  INNER JOIN publishers p ON b.publisher_id = p.publisher_id;
  ```
- [ ] **測試單點更新**：
  ```sql
  -- 更新出版社資訊
  UPDATE publishers 
  SET contact_name = 'Jane Smith', phone = '02-87654321' 
  WHERE publisher_id = 'P001';

  -- 再次執行 JOIN 查詢，確認所有關聯書籍取得最新聯絡資訊
  SELECT b.title, p.publisher_name, p.contact_name, p.phone
  FROM books b
  INNER JOIN publishers p ON b.publisher_id = p.publisher_id;
  ```

---

## 總結

關聯式設計的本質是「拆分實體、集中儲存、靠鍵值連結」。把資料拆到各自的表格能避免重複儲存與輸入錯誤；透過外來鍵關聯，則讓資料異動時只要改一處就能全域同步。
