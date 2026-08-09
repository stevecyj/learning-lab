# 模組 25：SQLite Browser 基本操作

## 這堂課在講什麼

本節示範如何使用 SQLite Browser 開啟既有資料庫、查看資料表結構與資料內容，並認識介面中可用來插入資料的功能。

## 學完要會什麼

- 在 SQLite Browser 新建資料庫，或開啟既有的 `.db` 資料庫檔。
- 從 `Database Structure` 查看資料表及其欄位。
- 從 `Browse Data` 查看資料表中的資料。
- 知道可透過 SQLite Browser 的內建介面插入資料。

## 開啟或新建資料庫

開啟 SQLite Browser 後，可以在左上角選擇兩種方式：

- **新建資料庫**：建立一個新的資料庫來練習。
- **打開資料庫**：開啟已經存在的資料庫檔案，例如先前建立的 `.db` 檔。

若要使用既有資料庫，找到課程資料夾中的資料庫檔後開啟即可。

## 查看資料庫結構

開啟資料庫後，切換到 `Database Structure` 分頁，可以查看資料庫裡有哪些資料表。

課程示範的資料庫中有一個 `students` 資料表。展開資料表後，可以看到它包含三個欄位：

- `id`
- `name`
- `gender`

## 查看資料表資料

切換到 `Browse Data` 分頁後，可以選擇資料庫中的資料表，查看欄位與目前的資料列。

以 `students` 為例，畫面會顯示 `id`、`name`、`gender` 三個欄位。示範中的資料表雖然已建立欄位，但目前沒有任何資料。

## 插入資料

SQLite Browser 內建可在介面中新增資料的方式。需要插入資料時，可以使用這些功能，直接把資料加入資料表，再回到 `Browse Data` 觀察結果。

## 注意事項

- `Database Structure` 用來查看資料表與欄位結構。
- `Browse Data` 用來查看資料表中實際儲存的資料。
- 資料表有欄位不代表一定已有資料列；例如示範中的 `students` 表目前是空的。

## 一句話回顧

SQLite Browser 可以開啟 `.db` 檔，透過 `Database Structure` 查看表格結構，並在 `Browse Data` 查看或新增資料。
