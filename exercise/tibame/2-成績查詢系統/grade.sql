-- 伺服器層：查看 CREATE DATABASE 沒有指定字元集時會繼承的預設值。
  SHOW VARIABLES LIKE 'character_set_server';

  -- 伺服器層：查看 CREATE DATABASE 沒有指定排序規則時會繼承的預設值。
  SHOW VARIABLES LIKE 'collation_server';

  -- 資料庫層：確認 mydatabase 實際保存的預設字元集與排序規則。
  -- 如果資料庫早已存在，CREATE DATABASE IF NOT EXISTS 不會更新原設定，
  -- 因此要用這行查看目前真正生效的設定。
  SHOW CREATE DATABASE mydatabase;

  -- 資料表層：確認 students 實際使用的字元集與排序規則。
  -- 資料表明確指定的設定會覆蓋資料庫預設值。
  SHOW CREATE TABLE mydatabase.students;

--
GRANT SELECT, INSERT, UPDATE, DELETE
    ON mydatabase.*
    TO 'grade_app'@'%';

--
show grants for 'grade_app'@'%';

--
select USER, HOST
from mysql.user;

-- 建立 students table
USE mydatabase;

CREATE TABLE IF NOT EXISTS students (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    student_no VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    gender_code CHAR(1) NULL,
    chinese TINYINT UNSIGNED NOT NULL,
    english TINYINT UNSIGNED NOT NULL,
    math TINYINT UNSIGNED NOT NULL,
    social_science TINYINT UNSIGNED NOT NULL,
    science TINYINT UNSIGNED NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_students PRIMARY KEY (id),
    CONSTRAINT uq_students_student_no UNIQUE (student_no),
    CONSTRAINT chk_students_gender_code
        CHECK (gender_code IS NULL OR gender_code IN ('M', 'F')),
    CONSTRAINT chk_students_chinese
        CHECK (chinese BETWEEN 0 AND 100),
    CONSTRAINT chk_students_english
        CHECK (english BETWEEN 0 AND 100),
    CONSTRAINT chk_students_math
        CHECK (math BETWEEN 0 AND 100),
    CONSTRAINT chk_students_social_science
        CHECK (social_science BETWEEN 0 AND 100),
    CONSTRAINT chk_students_science
        CHECK (science BETWEEN 0 AND 100)
) ENGINE = InnoDB
  DEFAULT CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- 建完 students 後驗證
show create table students;
describe students;

select user();