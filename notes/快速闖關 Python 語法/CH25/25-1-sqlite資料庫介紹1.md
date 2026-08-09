# 模組 25：SQLite 資料庫介紹（一）

## 這堂課在講什麼

本節先介紹 SQLite，以及後續單元會用到的基本資料庫名詞。模組 25 共有三個小節：

1. SQLite 介紹。
2. SQLite Browser 介紹。
3. SQLite Browser 操作。

## 學完要會什麼

- 知道 SQLite 是 Python 安裝後會一併提供的資料庫。
- 了解 SQLite 是輕量級的關聯式資料庫。
- 辨認資料表中的 `record`、`field` 與 `data value`。

## SQLite 是什麼

SQLite 是一種 Python 內建的資料庫。安裝 Python 後，SQLite 也會一併安裝。

它是一種輕量級的關聯式資料庫。之後可以使用 SQL 與 Python 程式語言和 SQLite 溝通；課程接下來會介紹如何這樣操作。

## 資料庫的基本名詞

資料庫裡可以有多個資料表，資料表看起來像一張張表格。

| 資料表中的部分 | 專有名詞 | 說明 |
| --- | --- | --- |
| 每一列（row） | `record` | 一筆紀錄 |
| 每一欄（column） | `field` | 一個欄位 |
| 表格中的值 | `data value` | 實際儲存的資料值 |

這些列、欄與資料值共同構成一張資料表。

## 注意事項

本節只介紹 SQLite 與資料表的基本概念，尚未示範 SQL、Python 或 SQLite Browser 的實際操作。

## 一句話回顧

SQLite 是 Python 安裝後可使用的輕量級關聯式資料庫；先認識資料表中的 `record`、`field` 和 `data value`，再進一步用 SQL 與 Python 操作它。
