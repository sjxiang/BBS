

# 临时设置, 中文
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_database = utf8mb4;
SET character_set_results = utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;
SET collation_database = utf8mb4_unicode_ci;
SET collation_server = utf8mb4_unicode_ci;

# 创建数据库
CREATE DATABASE IF NOT EXISTS `bbs_api_development`;

# 切换数据库
USE `bbs_api`;

INSERT INTO `users` (`nickname`, `password`, `email`, `avatar`, `is_admin`, `create_at`, `update_at`) 
VALUES ();


-- 创建帖子
INSERT INTO `posts` (`title`, `content`, `user_id`, `is_draft`, `create_at`, `update_at`) 
VALUES ();

-- 发帖
UPDATE `posts` SET `is_draft` = 0 WHERE `id` = 1;

-- 删帖
DELETE FROM `posts` WHERE `id` = 5;


-- 最新帖子 (按照 created_at 从晚到早排序, 即降序)
SELECT * FROM `posts` WHERE `id` > 0 ORDER BY `created_at` DESC;


INSERT INTO `settings` (`name`, `icp`, `copyright`) VALUES ('bbs论坛', '苏ICP备123456789号', '© 2023 bbs论坛 版权所有');

DROP TABLE `categories`;
DROP TABLE `chapters`;
DROP TABLE `courses`;
DROP TABLE `likes`;
DROP TABLE `posts`;
DROP TABLE `settings`;
DROP TABLE `users`;

