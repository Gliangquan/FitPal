/*
 Navicat Premium Dump SQL

 Source Server         : localhost-mysql
 Source Server Type    : MySQL
 Source Server Version : 80042 (8.0.42)
 Source Host           : localhost:3306
 Source Schema         : fit

 Target Server Type    : MySQL
 Target Server Version : 80042 (8.0.42)
 File Encoding         : 65001

 Date: 02/03/2026 20:25:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin_audit_log
-- ----------------------------
DROP TABLE IF EXISTS `admin_audit_log`;
CREATE TABLE `admin_audit_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `admin_user_id` bigint NOT NULL,
  `biz_type` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `biz_id` bigint NOT NULL,
  `action` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `remark` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_admin_audit` (`biz_type`,`biz_id`),
  KEY `fk_audit_admin` (`admin_user_id`),
  CONSTRAINT `fk_audit_admin` FOREIGN KEY (`admin_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员审核日志';

-- ----------------------------
-- Records of admin_audit_log
-- ----------------------------
BEGIN;
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (1, 1, 'community_post', 1, 'add', '后台操作记录#1，用于联调与审计测试。', '2026-02-24 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (2, 2, 'recommendation_content', 2, 'update', '后台操作记录#2，用于联调与审计测试。', '2026-02-25 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (3, 1, 'coach_profile', 3, 'delete', '后台操作记录#3，用于联调与审计测试。', '2026-02-26 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (4, 2, 'personalized_plan', 4, 'publish', '后台操作记录#4，用于联调与审计测试。', '2026-02-27 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (5, 1, 'content', 5, 'reject', '后台操作记录#5，用于联调与审计测试。', '2026-02-28 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (6, 2, 'points_rule', 6, 'approve', '后台操作记录#6，用于联调与审计测试。', '2026-03-01 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (7, 1, 'community_post', 7, 'hide', '后台操作记录#7，用于联调与审计测试。', '2026-03-02 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (8, 2, 'recommendation_content', 8, 'reset', '后台操作记录#8，用于联调与审计测试。', '2026-03-03 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (9, 1, 'coach_profile', 9, 'add', '后台操作记录#9，用于联调与审计测试。', '2026-03-04 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (10, 2, 'personalized_plan', 10, 'update', '后台操作记录#10，用于联调与审计测试。', '2026-03-05 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (11, 1, 'content', 11, 'delete', '后台操作记录#11，用于联调与审计测试。', '2026-03-06 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (12, 2, 'points_rule', 12, 'publish', '后台操作记录#12，用于联调与审计测试。', '2026-03-07 08:30:00');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (13, 1, 'community_post', 11, 'publish', '', '2026-03-02 19:54:56');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (14, 1, 'community_post', 9, 'publish', '', '2026-03-02 19:54:57');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (15, 1, 'community_post', 11, 'reject', '内容不符合社区规范', '2026-03-02 19:55:01');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (16, 1, 'community_post', 11, 'publish', '', '2026-03-02 20:16:32');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (17, 1, 'community_post', 11, 'publish', '', '2026-03-02 20:16:32');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (18, 1, 'community_post', 11, 'publish', '', '2026-03-02 20:16:34');
INSERT INTO `admin_audit_log` (`id`, `admin_user_id`, `biz_type`, `biz_id`, `action`, `remark`, `create_time`) VALUES (19, 1, 'community_post', 11, 'publish', '', '2026-03-02 20:16:34');
COMMIT;

-- ----------------------------
-- Table structure for coach_consultation
-- ----------------------------
DROP TABLE IF EXISTS `coach_consultation`;
CREATE TABLE `coach_consultation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `coach_user_id` bigint DEFAULT NULL,
  `question` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `reply` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending' COMMENT 'pending/replied/closed',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `reply_time` datetime DEFAULT NULL,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_consult_user` (`user_id`,`create_time`),
  KEY `idx_consult_coach` (`coach_user_id`,`status`),
  CONSTRAINT `fk_consult_coach` FOREIGN KEY (`coach_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_consult_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='在线咨询记录';

-- ----------------------------
-- Records of coach_consultation
-- ----------------------------
BEGIN;
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (1, 5, 3, '第1次咨询：晚餐后总想加餐，如何控制饥饿感？', '已接单，正在评估近7日饮食记录。', 'pending', '2026-02-18 08:30:00', '2026-02-18 11:30:00', '2026-02-18 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (2, 6, 4, '第2次咨询：晚餐后总想加餐，如何控制饥饿感？', '建议提高晚餐蛋白和蔬菜体积，睡前补充无糖酸奶。', 'replied', '2026-02-19 08:30:00', '2026-02-19 11:30:00', '2026-02-19 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (3, 7, 5, '第3次咨询：晚餐后总想加餐，如何控制饥饿感？', '建议提高晚餐蛋白和蔬菜体积，睡前补充无糖酸奶。', 'closed', '2026-02-20 08:30:00', '2026-02-20 11:30:00', '2026-02-20 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (4, 8, 3, '第4次咨询：晚餐后总想加餐，如何控制饥饿感？', '已接单，正在评估近7日饮食记录。', 'pending', '2026-02-21 08:30:00', '2026-02-21 11:30:00', '2026-02-21 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (5, 9, 4, '第5次咨询：晚餐后总想加餐，如何控制饥饿感？', '建议提高晚餐蛋白和蔬菜体积，睡前补充无糖酸奶。', 'replied', '2026-02-22 08:30:00', '2026-02-22 11:30:00', '2026-02-22 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (6, 10, 5, '第6次咨询：晚餐后总想加餐，如何控制饥饿感？', '建议提高晚餐蛋白和蔬菜体积，睡前补充无糖酸奶。', 'closed', '2026-02-23 08:30:00', '2026-02-23 11:30:00', '2026-02-23 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (7, 11, 3, '第7次咨询：晚餐后总想加餐，如何控制饥饿感？', '已接单，正在评估近7日饮食记录。', 'pending', '2026-02-24 08:30:00', '2026-02-24 11:30:00', '2026-02-24 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (8, 12, 4, '第8次咨询：晚餐后总想加餐，如何控制饥饿感？', '建议提高晚餐蛋白和蔬菜体积，睡前补充无糖酸奶。', 'replied', '2026-02-25 08:30:00', '2026-02-25 11:30:00', '2026-02-25 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (9, 5, 5, '第9次咨询：晚餐后总想加餐，如何控制饥饿感？', '建议提高晚餐蛋白和蔬菜体积，睡前补充无糖酸奶。', 'closed', '2026-02-26 08:30:00', '2026-02-26 11:30:00', '2026-02-26 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (10, 6, 3, '第10次咨询：晚餐后总想加餐，如何控制饥饿感？', '已接单，正在评估近7日饮食记录。', 'pending', '2026-02-27 08:30:00', '2026-02-27 11:30:00', '2026-02-27 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (11, 7, 4, '第11次咨询：晚餐后总想加餐，如何控制饥饿感？', '建议提高晚餐蛋白和蔬菜体积，睡前补充无糖酸奶。', 'replied', '2026-02-28 08:30:00', '2026-02-28 11:30:00', '2026-02-28 12:30:00', 1);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (12, 8, 5, '第12次咨询：晚餐后总想加餐，如何控制饥饿感？', '建议提高晚餐蛋白和蔬菜体积，睡前补充无糖酸奶。', 'closed', '2026-03-01 08:30:00', '2026-03-01 11:30:00', '2026-03-01 12:30:00', 0);
INSERT INTO `coach_consultation` (`id`, `user_id`, `coach_user_id`, `question`, `reply`, `status`, `create_time`, `reply_time`, `update_time`, `is_delete`) VALUES (13, 1, 3, 'hi', NULL, 'pending', '2026-03-02 20:05:21', NULL, '2026-03-02 20:05:21', 0);
COMMIT;

-- ----------------------------
-- Table structure for coach_profile
-- ----------------------------
DROP TABLE IF EXISTS `coach_profile`;
CREATE TABLE `coach_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `real_name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `certificate_type` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `certificate_no` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `specialties` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `introduction` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending' COMMENT 'pending/approved/rejected',
  `passed_time` datetime DEFAULT NULL,
  `reject_reason` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `fk_coach_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教练认证信息';

-- ----------------------------
-- Records of coach_profile
-- ----------------------------
BEGIN;
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (1, 3, '陈教练', '运动营养师', 'CERT-FIT-202601', '饮食管理', '从业3年，擅长制定可执行的周计划与复盘策略。', 'approved', '2026-02-17 08:30:00', '资质通过', '2026-02-17 08:30:00', '2026-02-17 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (2, 4, '吴教练', '体重管理师', 'CERT-FIT-202602', '产后恢复', '从业4年，擅长制定可执行的周计划与复盘策略。', 'pending', '2026-02-18 08:30:00', '待平台终审', '2026-02-18 08:30:00', '2026-02-18 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (3, 5, '马教练', '国职健身教练', 'CERT-FIT-202603', '体态矫正', '从业5年，擅长制定可执行的周计划与复盘策略。', 'rejected', '2026-02-19 08:30:00', '材料完整性不足，需补充继续教育证明', '2026-02-19 08:30:00', '2026-02-19 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (4, 6, '王晨曦', '运动营养师', 'CERT-FIT-202604', '减脂塑形', '从业6年，擅长制定可执行的周计划与复盘策略。', 'approved', '2026-02-20 08:30:00', '资质通过', '2026-02-20 08:30:00', '2026-02-20 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (5, 7, '李雨桐', '体重管理师', 'CERT-FIT-202605', '饮食管理', '从业7年，擅长制定可执行的周计划与复盘策略。', 'pending', '2026-02-21 08:30:00', '待平台终审', '2026-02-21 08:30:00', '2026-02-21 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (6, 8, '赵明远', '国职健身教练', 'CERT-FIT-202606', '产后恢复', '从业8年，擅长制定可执行的周计划与复盘策略。', 'rejected', '2026-02-22 08:30:00', '材料完整性不足，需补充继续教育证明', '2026-02-22 08:30:00', '2026-02-22 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (7, 9, '刘佳宁', '运动营养师', 'CERT-FIT-202607', '体态矫正', '从业9年，擅长制定可执行的周计划与复盘策略。', 'approved', '2026-02-23 08:30:00', '资质通过', '2026-02-23 08:30:00', '2026-02-23 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (8, 10, '孙子涵', '体重管理师', 'CERT-FIT-202608', '减脂塑形', '从业10年，擅长制定可执行的周计划与复盘策略。', 'pending', '2026-02-24 08:30:00', '待平台终审', '2026-02-24 08:30:00', '2026-02-24 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (9, 11, '何悦', '国职健身教练', 'CERT-FIT-202609', '饮食管理', '从业11年，擅长制定可执行的周计划与复盘策略。', 'rejected', '2026-02-25 08:30:00', '材料完整性不足，需补充继续教育证明', '2026-02-25 08:30:00', '2026-02-25 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (10, 12, '徐浩然', '运动营养师', 'CERT-FIT-202610', '产后恢复', '从业12年，擅长制定可执行的周计划与复盘策略。', 'approved', '2026-02-26 08:30:00', '资质通过', '2026-02-26 08:30:00', '2026-02-26 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (11, 13, '钱依琳', '体重管理师', 'CERT-FIT-202611', '体态矫正', '从业13年，擅长制定可执行的周计划与复盘策略。', 'pending', '2026-02-27 08:30:00', '待平台终审', '2026-02-27 08:30:00', '2026-02-27 10:30:00', 0);
INSERT INTO `coach_profile` (`id`, `user_id`, `real_name`, `certificate_type`, `certificate_no`, `specialties`, `introduction`, `status`, `passed_time`, `reject_reason`, `create_time`, `update_time`, `is_delete`) VALUES (12, 14, '丁一鸣', '国职健身教练', 'CERT-FIT-202612', '减脂塑形', '从业14年，擅长制定可执行的周计划与复盘策略。', 'rejected', '2026-02-28 08:30:00', '材料完整性不足，需补充继续教育证明', '2026-02-28 08:30:00', '2026-02-28 10:30:00', 1);
COMMIT;

-- ----------------------------
-- Table structure for coach_review
-- ----------------------------
DROP TABLE IF EXISTS `coach_review`;
CREATE TABLE `coach_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `coach_user_id` bigint NOT NULL,
  `rating` int NOT NULL,
  `content` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_coach_review_user` (`user_id`,`create_time`),
  KEY `idx_coach_review_coach` (`coach_user_id`,`create_time`),
  CONSTRAINT `fk_coach_review_coach` FOREIGN KEY (`coach_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_coach_review_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of coach_review
-- ----------------------------
BEGIN;
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (1, 5, 3, 2, '第1次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-19 08:30:00', '2026-02-19 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (2, 6, 4, 3, '第2次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-20 08:30:00', '2026-02-20 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (3, 7, 5, 4, '第3次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-21 08:30:00', '2026-02-21 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (4, 8, 3, 5, '第4次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-22 08:30:00', '2026-02-22 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (5, 9, 4, 1, '第5次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-23 08:30:00', '2026-02-23 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (6, 10, 5, 2, '第6次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-24 08:30:00', '2026-02-24 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (7, 11, 3, 3, '第7次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-25 08:30:00', '2026-02-25 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (8, 12, 4, 4, '第8次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-26 08:30:00', '2026-02-26 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (9, 5, 5, 5, '第9次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-27 08:30:00', '2026-02-27 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (10, 6, 3, 1, '第10次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-02-28 08:30:00', '2026-02-28 09:30:00', 1);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (11, 7, 4, 2, '第11次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-03-01 08:30:00', '2026-03-01 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (12, 8, 5, 3, '第12次评价：建议可执行、反馈及时，体重管理更有方向。', '2026-03-02 08:30:00', '2026-03-02 09:30:00', 0);
INSERT INTO `coach_review` (`id`, `user_id`, `coach_user_id`, `rating`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (13, 1, 3, 5, 'hi', '2026-03-02 20:05:30', '2026-03-02 20:05:30', 0);
COMMIT;

-- ----------------------------
-- Table structure for community_comment
-- ----------------------------
DROP TABLE IF EXISTS `community_comment`;
CREATE TABLE `community_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `content` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_comment_post_time` (`post_id`,`create_time`),
  KEY `idx_comment_user_time` (`user_id`,`create_time`),
  CONSTRAINT `fk_comment_post` FOREIGN KEY (`post_id`) REFERENCES `community_post` (`id`),
  CONSTRAINT `fk_comment_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of community_comment
-- ----------------------------
BEGIN;
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (1, 1, 7, '评论1：你这个方法很实用，我也准备按周复盘饮食。', '2026-02-22 08:30:00', '2026-02-22 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (2, 2, 8, '评论2：你这个方法很实用，我也准备按周复盘饮食。', '2026-02-23 08:30:00', '2026-02-23 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (3, 3, 9, '评论3：你这个方法很实用，我也准备按周复盘饮食。', '2026-02-24 08:30:00', '2026-02-24 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (4, 4, 10, '评论4：你这个方法很实用，我也准备按周复盘饮食。', '2026-02-25 08:30:00', '2026-02-25 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (5, 5, 11, '评论5：你这个方法很实用，我也准备按周复盘饮食。', '2026-02-26 08:30:00', '2026-02-26 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (6, 6, 12, '评论6：你这个方法很实用，我也准备按周复盘饮食。', '2026-02-27 08:30:00', '2026-02-27 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (7, 7, 1, '评论7：你这个方法很实用，我也准备按周复盘饮食。', '2026-02-28 08:30:00', '2026-02-28 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (8, 8, 2, '评论8：你这个方法很实用，我也准备按周复盘饮食。', '2026-03-01 08:30:00', '2026-03-01 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (9, 9, 3, '评论9：你这个方法很实用，我也准备按周复盘饮食。', '2026-03-02 08:30:00', '2026-03-02 09:30:00', 1);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (10, 10, 4, '评论10：你这个方法很实用，我也准备按周复盘饮食。', '2026-03-03 08:30:00', '2026-03-03 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (11, 11, 5, '评论11：你这个方法很实用，我也准备按周复盘饮食。', '2026-03-04 08:30:00', '2026-03-04 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (12, 12, 6, '评论12：你这个方法很实用，我也准备按周复盘饮食。', '2026-03-05 08:30:00', '2026-03-05 09:30:00', 0);
INSERT INTO `community_comment` (`id`, `post_id`, `user_id`, `content`, `create_time`, `update_time`, `is_delete`) VALUES (13, 1, 1, 'hi', '2026-03-02 20:05:09', '2026-03-02 20:05:09', 0);
COMMIT;

-- ----------------------------
-- Table structure for community_post
-- ----------------------------
DROP TABLE IF EXISTS `community_post`;
CREATE TABLE `community_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '社区分类',
  `image_urls` text COLLATE utf8mb4_unicode_ci,
  `like_count` int NOT NULL DEFAULT '0',
  `comment_count` int NOT NULL DEFAULT '0',
  `view_count` int NOT NULL DEFAULT '0',
  `status` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'published',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_post_user_time` (`user_id`,`create_time`),
  KEY `idx_post_category_status` (`category`,`status`,`create_time`),
  CONSTRAINT `fk_post_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社区动态';

-- ----------------------------
-- Records of community_post
-- ----------------------------
BEGIN;
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (1, 5, '减脂打卡日记第1天', '今天完成1000步，控糖晚餐，体重趋势继续向下。', 'diet', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 19, 6, 148, 'published', '2026-02-20 08:30:00', '2026-03-02 20:05:09', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (2, 6, '减脂打卡日记第2天', '今天完成2000步，控糖晚餐，体重趋势继续向下。', 'workout', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 21, 6, 174, 'hidden', '2026-02-21 08:30:00', '2026-03-02 20:01:14', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (3, 7, '减脂打卡日记第3天', '今天完成3000步，控糖晚餐，体重趋势继续向下。', 'mindset', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 24, 7, 201, 'rejected', '2026-02-22 08:30:00', '2026-03-02 20:01:14', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (4, 8, '减脂打卡日记第4天', '今天完成4000步，控糖晚餐，体重趋势继续向下。', 'weight-loss', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 27, 8, 229, 'published', '2026-02-23 08:30:00', '2026-03-02 20:01:14', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (5, 9, '减脂打卡日记第5天', '今天完成5000步，控糖晚餐，体重趋势继续向下。', 'diet', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 30, 9, 255, 'hidden', '2026-02-24 08:30:00', '2026-03-02 20:01:14', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (6, 10, '减脂打卡日记第6天', '今天完成6000步，控糖晚餐，体重趋势继续向下。', 'workout', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 33, 10, 282, 'rejected', '2026-02-25 08:30:00', '2026-03-02 20:01:14', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (7, 11, '减脂打卡日记第7天', '今天完成7000步，控糖晚餐，体重趋势继续向下。', 'mindset', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 36, 11, 311, 'published', '2026-02-26 08:30:00', '2026-03-02 20:01:18', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (8, 12, '减脂打卡日记第8天', '今天完成8000步，控糖晚餐，体重趋势继续向下。', 'weight-loss', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 39, 12, 336, 'hidden', '2026-02-27 08:30:00', '2026-03-02 20:01:14', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (9, 5, '减脂打卡日记第9天', '今天完成9000步，控糖晚餐，体重趋势继续向下。', 'diet', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 42, 13, 363, 'published', '2026-02-28 08:30:00', '2026-03-02 20:01:14', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (10, 6, '减脂打卡日记第10天', '今天完成10000步，控糖晚餐，体重趋势继续向下。', 'workout', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 45, 14, 390, 'published', '2026-03-01 08:30:00', '2026-03-02 20:01:14', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (11, 7, '减脂打卡日记第11天', '今天完成11000步，控糖晚餐，体重趋势继续向下。', 'mindset', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 48, 15, 417, 'published', '2026-03-02 08:30:00', '2026-03-02 20:16:34', 0);
INSERT INTO `community_post` (`id`, `user_id`, `title`, `content`, `category`, `image_urls`, `like_count`, `comment_count`, `view_count`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (12, 8, '减脂打卡日记第12天', '今天完成12000步，控糖晚餐，体重趋势继续向下。', 'weight-loss', '[\"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\", \"/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg\"]', 51, 16, 444, 'rejected', '2026-03-03 08:30:00', '2026-03-02 20:01:14', 1);
COMMIT;

-- ----------------------------
-- Table structure for community_post_like
-- ----------------------------
DROP TABLE IF EXISTS `community_post_like`;
CREATE TABLE `community_post_like` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_post_user` (`post_id`,`user_id`),
  KEY `idx_like_user_time` (`user_id`,`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_post_like
-- ----------------------------
BEGIN;
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (1, 1, 6, '2026-02-21 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (2, 2, 7, '2026-02-22 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (3, 3, 8, '2026-02-23 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (4, 4, 9, '2026-02-24 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (5, 5, 10, '2026-02-25 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (6, 6, 11, '2026-02-26 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (7, 7, 12, '2026-02-27 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (8, 8, 1, '2026-02-28 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (9, 9, 2, '2026-03-01 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (10, 10, 3, '2026-03-02 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (11, 11, 4, '2026-03-03 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (12, 12, 5, '2026-03-04 08:30:00');
INSERT INTO `community_post_like` (`id`, `post_id`, `user_id`, `create_time`) VALUES (13, 1, 1, '2026-03-02 20:05:05');
COMMIT;

-- ----------------------------
-- Table structure for content
-- ----------------------------
DROP TABLE IF EXISTS `content`;
CREATE TABLE `content` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `content_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '内容类型：article/video/recipe/exercise',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '内容标题',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '内容描述',
  `content` longtext COLLATE utf8mb4_unicode_ci COMMENT '内容详情',
  `target_audience` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '目标用户：all/beginner/intermediate/advanced',
  `tags` json DEFAULT NULL COMMENT '标签（JSON格式）',
  `cover_image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '封面图片',
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'draft' COMMENT '发布状态：draft/published/archived',
  `recommend_score` int DEFAULT '0' COMMENT '推荐指数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` int DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  KEY `idx_content_type` (`content_type`),
  KEY `idx_status` (`status`),
  KEY `idx_target_audience` (`target_audience`),
  FULLTEXT KEY `ft_title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='内容表';

-- ----------------------------
-- Records of content
-- ----------------------------
BEGIN;
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (1, 'article', '运营内容库文章1', '内容1用于后台运营测试，包含真实训练与饮食建议。', '内容正文1：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'office', '[\"减脂\", \"营养\", \"专题1\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'draft', 61, '2026-02-10 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (2, 'video', '运营内容库文章2', '内容2用于后台运营测试，包含真实训练与饮食建议。', '内容正文2：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'advanced', '[\"减脂\", \"营养\", \"专题2\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', 62, '2026-02-11 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (3, 'article', '运营内容库文章3', '内容3用于后台运营测试，包含真实训练与饮食建议。', '内容正文3：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'newbie', '[\"减脂\", \"营养\", \"专题3\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'archived', 63, '2026-02-12 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (4, 'video', '运营内容库文章4', '内容4用于后台运营测试，包含真实训练与饮食建议。', '内容正文4：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'office', '[\"减脂\", \"营养\", \"专题4\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'draft', 64, '2026-02-13 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (5, 'article', '运营内容库文章5', '内容5用于后台运营测试，包含真实训练与饮食建议。', '内容正文5：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'advanced', '[\"减脂\", \"营养\", \"专题5\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', 65, '2026-02-14 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (6, 'video', '运营内容库文章6', '内容6用于后台运营测试，包含真实训练与饮食建议。', '内容正文6：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'newbie', '[\"减脂\", \"营养\", \"专题6\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'archived', 66, '2026-02-15 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (7, 'article', '运营内容库文章7', '内容7用于后台运营测试，包含真实训练与饮食建议。', '内容正文7：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'office', '[\"减脂\", \"营养\", \"专题7\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'draft', 67, '2026-02-16 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (8, 'video', '运营内容库文章8', '内容8用于后台运营测试，包含真实训练与饮食建议。', '内容正文8：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'advanced', '[\"减脂\", \"营养\", \"专题8\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', 68, '2026-02-17 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (9, 'article', '运营内容库文章9', '内容9用于后台运营测试，包含真实训练与饮食建议。', '内容正文9：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'newbie', '[\"减脂\", \"营养\", \"专题9\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'archived', 69, '2026-02-18 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (10, 'video', '运营内容库文章10', '内容10用于后台运营测试，包含真实训练与饮食建议。', '内容正文10：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'office', '[\"减脂\", \"营养\", \"专题10\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'draft', 70, '2026-02-19 08:30:00', '2026-03-02 20:00:09', 1);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (11, 'article', '运营内容库文章11', '内容11用于后台运营测试，包含真实训练与饮食建议。', '内容正文11：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'advanced', '[\"减脂\", \"营养\", \"专题11\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', 71, '2026-02-20 08:30:00', '2026-03-02 20:00:09', 0);
INSERT INTO `content` (`id`, `content_type`, `title`, `description`, `content`, `target_audience`, `tags`, `cover_image`, `status`, `recommend_score`, `created_at`, `updated_at`, `is_delete`) VALUES (12, 'video', '运营内容库文章12', '内容12用于后台运营测试，包含真实训练与饮食建议。', '内容正文12：建议每周跟踪体脂变化，并结合力量训练提升基础代谢。', 'newbie', '[\"减脂\", \"营养\", \"专题12\"]', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'archived', 72, '2026-02-21 08:30:00', '2026-03-02 20:00:09', 0);
COMMIT;

-- ----------------------------
-- Table structure for health_record
-- ----------------------------
DROP TABLE IF EXISTS `health_record`;
CREATE TABLE `health_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `record_date` date NOT NULL,
  `weight_kg` decimal(5,2) DEFAULT NULL,
  `body_fat_rate` decimal(5,2) DEFAULT NULL,
  `calorie_intake` int DEFAULT NULL,
  `calorie_burn` int DEFAULT NULL,
  `sleep_hours` decimal(4,1) DEFAULT NULL,
  `note` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_health_user_date` (`user_id`,`record_date`),
  CONSTRAINT `fk_health_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='健康数据记录';

-- ----------------------------
-- Records of health_record
-- ----------------------------
BEGIN;
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (1, 5, '2026-02-02', 74.10, 28.25, 1575, 320, 6.9, '午餐蛋白质充足，完成核心训练', '2026-02-04 08:30:00', '2026-02-04 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (2, 6, '2026-02-03', 73.70, 28.00, 1600, 340, 7.3, '补水达标，情绪稳定', '2026-02-05 08:30:00', '2026-02-05 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (3, 7, '2026-02-04', 73.30, 27.75, 1625, 360, 7.7, '晚餐减少油炸，睡眠改善', '2026-02-06 08:30:00', '2026-02-06 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (4, 8, '2026-02-05', 72.90, 27.50, 1650, 380, 6.5, '早餐控制主食，晚间快走45分钟', '2026-02-07 08:30:00', '2026-02-07 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (5, 9, '2026-02-06', 72.50, 27.25, 1675, 400, 6.9, '午餐蛋白质充足，完成核心训练', '2026-02-08 08:30:00', '2026-02-08 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (6, 10, '2026-02-07', 72.10, 27.00, 1700, 420, 7.3, '补水达标，情绪稳定', '2026-02-09 08:30:00', '2026-02-09 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (7, 11, '2026-02-08', 71.70, 26.75, 1725, 440, 7.7, '晚餐减少油炸，睡眠改善', '2026-02-10 08:30:00', '2026-02-10 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (8, 12, '2026-02-09', 71.30, 26.50, 1750, 460, 6.5, '早餐控制主食，晚间快走45分钟', '2026-02-11 08:30:00', '2026-02-11 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (9, 5, '2026-02-10', 70.90, 26.25, 1775, 480, 6.9, '午餐蛋白质充足，完成核心训练', '2026-02-12 08:30:00', '2026-02-12 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (10, 6, '2026-02-11', 70.50, 26.00, 1800, 500, 7.3, '补水达标，情绪稳定', '2026-02-13 08:30:00', '2026-02-13 09:30:00', 1);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (11, 7, '2026-02-12', 70.10, 25.75, 1825, 520, 7.7, '晚餐减少油炸，睡眠改善', '2026-02-14 08:30:00', '2026-02-14 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (12, 8, '2026-02-13', 69.70, 25.50, 1850, 540, 6.5, '早餐控制主食，晚间快走45分钟', '2026-02-15 08:30:00', '2026-02-15 09:30:00', 0);
INSERT INTO `health_record` (`id`, `user_id`, `record_date`, `weight_kg`, `body_fat_rate`, `calorie_intake`, `calorie_burn`, `sleep_hours`, `note`, `create_time`, `update_time`, `is_delete`) VALUES (13, 1, '2026-03-02', 68.50, 23.40, 1650, 420, 7.5, '还好', '2026-03-02 20:02:26', '2026-03-02 20:02:26', 0);
COMMIT;

-- ----------------------------
-- Table structure for personalized_plan
-- ----------------------------
DROP TABLE IF EXISTS `personalized_plan`;
CREATE TABLE `personalized_plan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `questionnaire_id` bigint DEFAULT NULL,
  `plan_type` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'fat_loss',
  `bmr` decimal(8,2) DEFAULT NULL,
  `daily_calorie_target` int DEFAULT NULL,
  `diet_suggestion` text COLLATE utf8mb4_unicode_ci,
  `workout_suggestion` text COLLATE utf8mb4_unicode_ci,
  `season_tips` text COLLATE utf8mb4_unicode_ci,
  `source` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'mifflin-st-jeor',
  `effective_from` date DEFAULT NULL,
  `effective_to` date DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_plan_user_time` (`user_id`,`create_time`),
  KEY `fk_plan_questionnaire` (`questionnaire_id`),
  CONSTRAINT `fk_plan_questionnaire` FOREIGN KEY (`questionnaire_id`) REFERENCES `user_questionnaire` (`id`),
  CONSTRAINT `fk_plan_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='个性化减脂方案';

-- ----------------------------
-- Records of personalized_plan
-- ----------------------------
BEGIN;
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (1, 3, 1, 'recomposition', 1342.50, 1485, '第1周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第1周建议保持23点前入睡。', 'admin-manual', '2026-02-05', '2026-03-07', '2026-02-05 08:30:00', '2026-02-05 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (2, 4, 2, 'maintenance', 1365.00, 1520, '第2周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第2周建议保持23点前入睡。', 'coach-optimize', '2026-02-06', '2026-03-08', '2026-02-06 08:30:00', '2026-02-06 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (3, 5, 3, 'fat_loss', 1387.50, 1555, '第3周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第3周建议保持23点前入睡。', 'mifflin-st-jeor', '2026-02-07', '2026-03-09', '2026-02-07 08:30:00', '2026-02-07 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (4, 6, 4, 'recomposition', 1410.00, 1590, '第4周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第4周建议保持23点前入睡。', 'admin-manual', '2026-02-08', '2026-03-10', '2026-02-08 08:30:00', '2026-02-08 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (5, 7, 5, 'maintenance', 1432.50, 1625, '第5周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第5周建议保持23点前入睡。', 'coach-optimize', '2026-02-09', '2026-03-11', '2026-02-09 08:30:00', '2026-02-09 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (6, 8, 6, 'fat_loss', 1455.00, 1660, '第6周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第6周建议保持23点前入睡。', 'mifflin-st-jeor', '2026-02-10', '2026-03-12', '2026-02-10 08:30:00', '2026-02-10 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (7, 9, 7, 'recomposition', 1477.50, 1695, '第7周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第7周建议保持23点前入睡。', 'admin-manual', '2026-02-11', '2026-03-13', '2026-02-11 08:30:00', '2026-02-11 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (8, 10, 8, 'maintenance', 1500.00, 1730, '第8周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第8周建议保持23点前入睡。', 'coach-optimize', '2026-02-12', '2026-03-14', '2026-02-12 08:30:00', '2026-02-12 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (9, 11, 9, 'fat_loss', 1522.50, 1765, '第9周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第9周建议保持23点前入睡。', 'mifflin-st-jeor', '2026-02-13', '2026-03-15', '2026-02-13 08:30:00', '2026-02-13 10:30:00', 1);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (10, 12, 10, 'recomposition', 1545.00, 1800, '第10周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第10周建议保持23点前入睡。', 'admin-manual', '2026-02-14', '2026-03-16', '2026-02-14 08:30:00', '2026-02-14 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (11, 13, 11, 'maintenance', 1567.50, 1835, '第11周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第11周建议保持23点前入睡。', 'coach-optimize', '2026-02-15', '2026-03-17', '2026-02-15 08:30:00', '2026-02-15 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (12, 14, 12, 'fat_loss', 1590.00, 1870, '第12周采用三餐两加餐，主食粗细搭配，蛋白优先。', '每周4次训练：2次有氧+2次力量，单次40~60分钟。', '注意体重波动与水盐平衡，第12周建议保持23点前入睡。', 'mifflin-st-jeor', '2026-02-16', '2026-03-18', '2026-02-16 08:30:00', '2026-02-16 10:30:00', 0);
INSERT INTO `personalized_plan` (`id`, `user_id`, `questionnaire_id`, `plan_type`, `bmr`, `daily_calorie_target`, `diet_suggestion`, `workout_suggestion`, `season_tips`, `source`, `effective_from`, `effective_to`, `create_time`, `update_time`, `is_delete`) VALUES (13, 1, 13, 'fat_loss', 1595.00, 1200, '每日热量控制在1200kcal；优先高蛋白、低GI碳水，避免含糖饮料。', '每周4-5次中等强度运动，结合有氧与力量训练。 当前建议强度：medium。', '夏至专题：代谢友好减脂：午后适量日照，夜间减少蓝光刺激', 'mifflin-st-jeor', '2026-03-02', '2026-05-01', '2026-03-02 20:04:47', '2026-03-02 20:04:47', 0);
COMMIT;

-- ----------------------------
-- Table structure for point_badge
-- ----------------------------
DROP TABLE IF EXISTS `point_badge`;
CREATE TABLE `point_badge` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `badge_code` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `badge_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `badge_desc` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `icon_url` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `required_point` int NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '1',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `badge_code` (`badge_code`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of point_badge
-- ----------------------------
BEGIN;
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (1, 'BADGE_001', '健康勋章1', '累计达到40积分，达成阶段性目标。', '/static/icon_fit/badge_1.png', 40, 1, '2026-02-12 08:30:00', '2026-02-12 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (2, 'BADGE_002', '健康勋章2', '累计达到80积分，达成阶段性目标。', '/static/icon_fit/badge_2.png', 80, 1, '2026-02-13 08:30:00', '2026-02-13 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (3, 'BADGE_003', '健康勋章3', '累计达到120积分，达成阶段性目标。', '/static/icon_fit/badge_3.png', 120, 1, '2026-02-14 08:30:00', '2026-02-14 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (4, 'BADGE_004', '健康勋章4', '累计达到160积分，达成阶段性目标。', '/static/icon_fit/badge_4.png', 160, 1, '2026-02-15 08:30:00', '2026-02-15 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (5, 'BADGE_005', '健康勋章5', '累计达到200积分，达成阶段性目标。', '/static/icon_fit/badge_5.png', 200, 0, '2026-02-16 08:30:00', '2026-02-16 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (6, 'BADGE_006', '健康勋章6', '累计达到240积分，达成阶段性目标。', '/static/icon_fit/badge_6.png', 240, 1, '2026-02-17 08:30:00', '2026-02-17 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (7, 'BADGE_007', '健康勋章7', '累计达到280积分，达成阶段性目标。', '/static/icon_fit/badge_7.png', 280, 1, '2026-02-18 08:30:00', '2026-02-18 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (8, 'BADGE_008', '健康勋章8', '累计达到320积分，达成阶段性目标。', '/static/icon_fit/badge_8.png', 320, 1, '2026-02-19 08:30:00', '2026-02-19 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (9, 'BADGE_009', '健康勋章9', '累计达到360积分，达成阶段性目标。', '/static/icon_fit/badge_9.png', 360, 1, '2026-02-20 08:30:00', '2026-02-20 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (10, 'BADGE_010', '健康勋章10', '累计达到400积分，达成阶段性目标。', '/static/icon_fit/badge_10.png', 400, 0, '2026-02-21 08:30:00', '2026-02-21 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (11, 'BADGE_011', '健康勋章11', '累计达到440积分，达成阶段性目标。', '/static/icon_fit/badge_11.png', 440, 1, '2026-02-22 08:30:00', '2026-02-22 09:30:00', 0);
INSERT INTO `point_badge` (`id`, `badge_code`, `badge_name`, `badge_desc`, `icon_url`, `required_point`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (12, 'BADGE_012', '健康勋章12', '累计达到480积分，达成阶段性目标。', '/static/icon_fit/badge_12.png', 480, 1, '2026-02-23 08:30:00', '2026-02-23 09:30:00', 1);
COMMIT;

-- ----------------------------
-- Table structure for points_rule
-- ----------------------------
DROP TABLE IF EXISTS `points_rule`;
CREATE TABLE `points_rule` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `rule_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '规则名称',
  `rule_description` text COLLATE utf8mb4_unicode_ci COMMENT '规则描述',
  `points` int NOT NULL DEFAULT '0' COMMENT '积分数量',
  `rule_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '规则类型：task/achievement/social/other',
  `enabled` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` int DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  KEY `idx_rule_type` (`rule_type`),
  KEY `idx_enabled` (`enabled`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='积分规则表';

-- ----------------------------
-- Records of points_rule
-- ----------------------------
BEGIN;
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (1, '积分规则1', '规则1：完成指定健康任务即可获得积分。', 5, 'checkin', 1, '2026-02-11 08:30:00', '2026-02-11 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (2, '积分规则2', '规则2：完成指定健康任务即可获得积分。', 10, 'community', 1, '2026-02-12 08:30:00', '2026-02-12 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (3, '积分规则3', '规则3：完成指定健康任务即可获得积分。', 15, 'health', 1, '2026-02-13 08:30:00', '2026-02-13 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (4, '积分规则4', '规则4：完成指定健康任务即可获得积分。', 20, 'coach', 0, '2026-02-14 08:30:00', '2026-02-14 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (5, '积分规则5', '规则5：完成指定健康任务即可获得积分。', 25, 'checkin', 1, '2026-02-15 08:30:00', '2026-02-15 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (6, '积分规则6', '规则6：完成指定健康任务即可获得积分。', 30, 'community', 1, '2026-02-16 08:30:00', '2026-02-16 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (7, '积分规则7', '规则7：完成指定健康任务即可获得积分。', 35, 'health', 1, '2026-02-17 08:30:00', '2026-02-17 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (8, '积分规则8', '规则8：完成指定健康任务即可获得积分。', 40, 'coach', 0, '2026-02-18 08:30:00', '2026-02-18 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (9, '积分规则9', '规则9：完成指定健康任务即可获得积分。', 45, 'checkin', 1, '2026-02-19 08:30:00', '2026-02-19 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (10, '积分规则10', '规则10：完成指定健康任务即可获得积分。', 50, 'community', 1, '2026-02-20 08:30:00', '2026-02-20 09:30:00', 0);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (11, '积分规则11', '规则11：完成指定健康任务即可获得积分。', 55, 'health', 1, '2026-02-21 08:30:00', '2026-02-21 09:30:00', 1);
INSERT INTO `points_rule` (`id`, `rule_name`, `rule_description`, `points`, `rule_type`, `enabled`, `created_at`, `updated_at`, `is_delete`) VALUES (12, '积分规则12', '规则12：完成指定健康任务即可获得积分。', 60, 'coach', 0, '2026-02-22 08:30:00', '2026-02-22 09:30:00', 0);
COMMIT;

-- ----------------------------
-- Table structure for recommendation_content
-- ----------------------------
DROP TABLE IF EXISTS `recommendation_content`;
CREATE TABLE `recommendation_content` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'article/video',
  `stage_tag` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `body_tag` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `summary` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content_url` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content_body` text COLLATE utf8mb4_unicode_ci,
  `tags` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `publish_status` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'published',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_recommend_stage` (`stage_tag`,`publish_status`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='个性化推荐内容';

-- ----------------------------
-- Records of recommendation_content
-- ----------------------------
BEGIN;
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (1, '减脂知识专题第1期', 'article', 'middle', 'hip', '第1期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/1', '完整内容1：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '体态,核心,步行', 'draft', '2026-02-09 08:30:00', '2026-02-09 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (2, '减脂知识专题第2期', 'article', 'late', 'overall', '第2期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/2', '完整内容2：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '睡眠,恢复,代谢', 'pending', '2026-02-10 08:30:00', '2026-02-10 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (3, '减脂知识专题第3期', 'video', 'early', 'abdomen', '第3期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/3', '完整内容3：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '减脂,饮食,训练', 'published', '2026-02-11 08:30:00', '2026-02-11 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (4, '减脂知识专题第4期', 'article', 'middle', 'hip', '第4期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/4', '完整内容4：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '体态,核心,步行', 'rejected', '2026-02-12 08:30:00', '2026-02-12 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (5, '减脂知识专题第5期', 'article', 'late', 'overall', '第5期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/5', '完整内容5：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '睡眠,恢复,代谢', 'draft', '2026-02-13 08:30:00', '2026-02-13 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (6, '减脂知识专题第6期', 'video', 'early', 'abdomen', '第6期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/6', '完整内容6：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '减脂,饮食,训练', 'pending', '2026-02-14 08:30:00', '2026-02-14 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (7, '减脂知识专题第7期', 'article', 'middle', 'hip', '第7期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/7', '完整内容7：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '体态,核心,步行', 'published', '2026-02-15 08:30:00', '2026-02-15 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (8, '减脂知识专题第8期', 'article', 'late', 'overall', '第8期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/8', '完整内容8：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '睡眠,恢复,代谢', 'rejected', '2026-02-16 08:30:00', '2026-02-16 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (9, '减脂知识专题第9期', 'video', 'early', 'abdomen', '第9期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/9', '完整内容9：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '减脂,饮食,训练', 'draft', '2026-02-17 08:30:00', '2026-02-17 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (10, '减脂知识专题第10期', 'article', 'middle', 'hip', '第10期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/10', '完整内容10：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '体态,核心,步行', 'pending', '2026-02-18 08:30:00', '2026-02-18 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (11, '减脂知识专题第11期', 'article', 'late', 'overall', '第11期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/11', '完整内容11：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '睡眠,恢复,代谢', 'published', '2026-02-19 08:30:00', '2026-02-19 09:30:00', 0);
INSERT INTO `recommendation_content` (`id`, `title`, `content_type`, `stage_tag`, `body_tag`, `summary`, `content_url`, `content_body`, `tags`, `publish_status`, `create_time`, `update_time`, `is_delete`) VALUES (12, '减脂知识专题第12期', 'video', 'early', 'abdomen', '第12期聚焦饮食结构、训练安排和行为习惯。', 'https://fitpal-content.example.com/reco/12', '完整内容12：围绕热量缺口、蛋白质摄入、训练恢复进行系统说明。', '减脂,饮食,训练', 'rejected', '2026-02-20 08:30:00', '2026-02-20 09:30:00', 1);
COMMIT;

-- ----------------------------
-- Table structure for solar_term
-- ----------------------------
DROP TABLE IF EXISTS `solar_term`;
CREATE TABLE `solar_term` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `solar_term_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '节气名称',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '专题标题',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '专题描述',
  `day1_recipe` text COLLATE utf8mb4_unicode_ci COMMENT '第一天食谱',
  `day2_recipe` text COLLATE utf8mb4_unicode_ci COMMENT '第二天食谱',
  `day3_recipe` text COLLATE utf8mb4_unicode_ci COMMENT '第三天食谱',
  `exercise_guide` text COLLATE utf8mb4_unicode_ci COMMENT '运动指南',
  `lifestyle_advice` text COLLATE utf8mb4_unicode_ci COMMENT '起居建议',
  `health_knowledge` text COLLATE utf8mb4_unicode_ci COMMENT '养生知识',
  `cover_image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '封面图片',
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'draft' COMMENT '发布状态：draft/published',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` int DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  KEY `idx_solar_term_name` (`solar_term_name`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='节气专题表';

-- ----------------------------
-- Records of solar_term
-- ----------------------------
BEGIN;
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (1, '立春', '立春轻体养护计划', '立春阶段重点在于调整饮食节律与稳态运动。', '立春第1天：燕麦鸡胸能量碗', '立春第2天：番茄牛肉藜麦饭', '立春第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '立春时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', '2026-02-06 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (2, '雨水', '雨水轻体养护计划', '雨水阶段重点在于调整饮食节律与稳态运动。', '雨水第1天：燕麦鸡胸能量碗', '雨水第2天：番茄牛肉藜麦饭', '雨水第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '雨水时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', '2026-02-07 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (3, '惊蛰', '惊蛰轻体养护计划', '惊蛰阶段重点在于调整饮食节律与稳态运动。', '惊蛰第1天：燕麦鸡胸能量碗', '惊蛰第2天：番茄牛肉藜麦饭', '惊蛰第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '惊蛰时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'draft', '2026-02-08 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (4, '春分', '春分轻体养护计划', '春分阶段重点在于调整饮食节律与稳态运动。', '春分第1天：燕麦鸡胸能量碗', '春分第2天：番茄牛肉藜麦饭', '春分第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '春分时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', '2026-02-09 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (5, '清明', '清明轻体养护计划', '清明阶段重点在于调整饮食节律与稳态运动。', '清明第1天：燕麦鸡胸能量碗', '清明第2天：番茄牛肉藜麦饭', '清明第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '清明时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', '2026-02-10 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (6, '谷雨', '谷雨轻体养护计划', '谷雨阶段重点在于调整饮食节律与稳态运动。', '谷雨第1天：燕麦鸡胸能量碗', '谷雨第2天：番茄牛肉藜麦饭', '谷雨第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '谷雨时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'draft', '2026-02-11 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (7, '立夏', '立夏轻体养护计划', '立夏阶段重点在于调整饮食节律与稳态运动。', '立夏第1天：燕麦鸡胸能量碗', '立夏第2天：番茄牛肉藜麦饭', '立夏第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '立夏时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', '2026-02-12 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (8, '小满', '小满轻体养护计划', '小满阶段重点在于调整饮食节律与稳态运动。', '小满第1天：燕麦鸡胸能量碗', '小满第2天：番茄牛肉藜麦饭', '小满第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '小满时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', '2026-02-13 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (9, '芒种', '芒种轻体养护计划', '芒种阶段重点在于调整饮食节律与稳态运动。', '芒种第1天：燕麦鸡胸能量碗', '芒种第2天：番茄牛肉藜麦饭', '芒种第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '芒种时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'draft', '2026-02-14 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (10, '夏至', '夏至轻体养护计划', '夏至阶段重点在于调整饮食节律与稳态运动。', '夏至第1天：燕麦鸡胸能量碗', '夏至第2天：番茄牛肉藜麦饭', '夏至第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '夏至时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', '2026-02-15 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (11, '小暑', '小暑轻体养护计划', '小暑阶段重点在于调整饮食节律与稳态运动。', '小暑第1天：燕麦鸡胸能量碗', '小暑第2天：番茄牛肉藜麦饭', '小暑第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '小暑时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'published', '2026-02-16 08:30:00', '2026-03-02 20:20:52', 0);
INSERT INTO `solar_term` (`id`, `solar_term_name`, `title`, `description`, `day1_recipe`, `day2_recipe`, `day3_recipe`, `exercise_guide`, `lifestyle_advice`, `health_knowledge`, `cover_image`, `status`, `created_at`, `updated_at`, `is_delete`) VALUES (12, '大暑', '大暑轻体养护计划', '大暑阶段重点在于调整饮食节律与稳态运动。', '大暑第1天：燕麦鸡胸能量碗', '大暑第2天：番茄牛肉藜麦饭', '大暑第3天：西兰花虾仁全麦意面', '30分钟快走 + 20分钟力量循环', '保持规律作息，降低夜间高盐摄入', '大暑时节注意补水与电解质平衡，避免情绪性进食。', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', 'draft', '2026-02-17 08:30:00', '2026-03-02 20:20:52', 1);
COMMIT;

-- ----------------------------
-- Table structure for solar_term_topic
-- ----------------------------
DROP TABLE IF EXISTS `solar_term_topic`;
CREATE TABLE `solar_term_topic` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `term_name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `recipe_text` text COLLATE utf8mb4_unicode_ci,
  `sport_guide` text COLLATE utf8mb4_unicode_ci,
  `routine_advice` text COLLATE utf8mb4_unicode_ci,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'published',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='节气减脂专题';

-- ----------------------------
-- Records of solar_term_topic
-- ----------------------------
BEGIN;
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (1, '立春', '立春专题：代谢友好减脂', '立春推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-06', '2026-02-20', 'published', '2026-02-07 08:30:00', '2026-02-07 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (2, '雨水', '雨水专题：代谢友好减脂', '雨水推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-07', '2026-02-21', 'published', '2026-02-08 08:30:00', '2026-02-08 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (3, '惊蛰', '惊蛰专题：代谢友好减脂', '惊蛰推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-08', '2026-02-22', 'published', '2026-02-09 08:30:00', '2026-02-09 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (4, '春分', '春分专题：代谢友好减脂', '春分推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-09', '2026-02-23', 'draft', '2026-02-10 08:30:00', '2026-02-10 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (5, '清明', '清明专题：代谢友好减脂', '清明推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-10', '2026-02-24', 'published', '2026-02-11 08:30:00', '2026-02-11 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (6, '谷雨', '谷雨专题：代谢友好减脂', '谷雨推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-11', '2026-02-25', 'published', '2026-02-12 08:30:00', '2026-02-12 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (7, '立夏', '立夏专题：代谢友好减脂', '立夏推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-12', '2026-02-26', 'published', '2026-02-13 08:30:00', '2026-02-13 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (8, '小满', '小满专题：代谢友好减脂', '小满推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-13', '2026-02-27', 'draft', '2026-02-14 08:30:00', '2026-02-14 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (9, '芒种', '芒种专题：代谢友好减脂', '芒种推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-14', '2026-02-28', 'published', '2026-02-15 08:30:00', '2026-02-15 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (10, '夏至', '夏至专题：代谢友好减脂', '夏至推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-15', '2026-03-01', 'published', '2026-02-16 08:30:00', '2026-02-16 09:30:00', 0);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (11, '小暑', '小暑专题：代谢友好减脂', '小暑推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-16', '2026-03-02', 'published', '2026-02-17 08:30:00', '2026-02-17 09:30:00', 1);
INSERT INTO `solar_term_topic` (`id`, `term_name`, `title`, `recipe_text`, `sport_guide`, `routine_advice`, `start_date`, `end_date`, `status`, `create_time`, `update_time`, `is_delete`) VALUES (12, '大暑', '大暑专题：代谢友好减脂', '大暑推荐食谱：高纤主食+优质蛋白+深色蔬菜。', '低冲击有氧结合核心稳定训练', '午后适量日照，夜间减少蓝光刺激', '2026-02-17', '2026-03-03', 'draft', '2026-02-18 08:30:00', '2026-02-18 09:30:00', 0);
COMMIT;

-- ----------------------------
-- Table structure for solar_term_topic_link
-- ----------------------------
DROP TABLE IF EXISTS `solar_term_topic_link`;
CREATE TABLE `solar_term_topic_link` (
  `solar_term_id` bigint NOT NULL,
  `topic_id` bigint NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`solar_term_id`),
  KEY `idx_topic_id` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of solar_term_topic_link
-- ----------------------------
BEGIN;
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (1, 1, '2026-02-08 08:30:00', '2026-02-08 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (2, 2, '2026-02-09 08:30:00', '2026-02-09 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (3, 3, '2026-02-10 08:30:00', '2026-02-10 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (4, 4, '2026-02-11 08:30:00', '2026-02-11 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (5, 5, '2026-02-12 08:30:00', '2026-02-12 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (6, 6, '2026-02-13 08:30:00', '2026-02-13 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (7, 7, '2026-02-14 08:30:00', '2026-02-14 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (8, 8, '2026-02-15 08:30:00', '2026-02-15 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (9, 9, '2026-02-16 08:30:00', '2026-02-16 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (10, 10, '2026-02-17 08:30:00', '2026-02-17 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (11, 11, '2026-02-18 08:30:00', '2026-02-18 09:30:00');
INSERT INTO `solar_term_topic_link` (`solar_term_id`, `topic_id`, `create_time`, `update_time`) VALUES (12, 12, '2026-02-19 08:30:00', '2026-02-19 09:30:00');
COMMIT;

-- ----------------------------
-- Table structure for system_setting
-- ----------------------------
DROP TABLE IF EXISTS `system_setting`;
CREATE TABLE `system_setting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `setting_group` varchar(64) NOT NULL,
  `setting_json` json NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_group` (`setting_group`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_setting
-- ----------------------------
BEGIN;
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (1, 'basic', '{\"version\": \"1.0.0\", \"siteName\": \"FitPal\", \"maintenance\": false}', '2026-02-23 08:30:00', '2026-02-23 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (2, 'security', '{\"loginCaptcha\": true, \"passwordMinLength\": 8, \"sessionTimeoutMinutes\": 120}', '2026-02-24 08:30:00', '2026-02-24 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (3, 'points', '{\"checkinPoints\": 10, \"contentLikePoints\": 5, \"postContentPoints\": 30}', '2026-02-25 08:30:00', '2026-02-25 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (4, 'notification', '{\"smsEnabled\": false, \"emailEnabled\": true, \"weeklyReport\": true}', '2026-02-26 08:30:00', '2026-02-26 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (5, 'community', '{\"postAuditMode\": \"manual\", \"defaultCategory\": \"weight-loss\", \"maxContentLength\": 5000}', '2026-02-27 08:30:00', '2026-02-27 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (6, 'storage', '{\"provider\": \"minio\", \"bucketPost\": \"fitpal-community-post\", \"bucketAvatar\": \"fitpal-user-avatar\"}', '2026-02-28 08:30:00', '2026-02-28 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (7, 'mail', '{\"enabled\": false, \"smtpServer\": \"smtp.example.com\", \"senderEmail\": \"noreply@fitpal.com\"}', '2026-03-01 08:30:00', '2026-03-01 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (8, 'privacy', '{\"retentionDays\": 30, \"profileVisibleDefault\": true, \"healthDataVisibleDefault\": false}', '2026-03-02 08:30:00', '2026-03-02 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (9, 'coach', '{\"autoAssign\": true, \"coachEnabled\": true, \"responseHours\": 24}', '2026-03-03 08:30:00', '2026-03-03 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (10, 'analytics', '{\"retentionDays\": 365, \"analyticsEnabled\": true, \"dashboardRefreshSec\": 60}', '2026-03-04 08:30:00', '2026-03-04 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (11, 'agreement', '{\"version\": \"2026.03\", \"termsUrl\": \"https://fitpal.com/terms\", \"privacyUrl\": \"https://fitpal.com/privacy\"}', '2026-03-05 08:30:00', '2026-03-05 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (12, 'feature_toggle', '{\"communityEnabled\": true, \"solarTermEnabled\": true, \"registrationEnabled\": true}', '2026-03-06 08:30:00', '2026-03-06 09:30:00');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (13, 'review', '{\"maxImageCount\": 9, \"sensitiveWords\": \"违禁词1\\n违禁词2\\n违禁词3\", \"maxContentLength\": 5000, \"autoApproveThreshold\": 80, \"autoReviewSensitiveWords\": true}', '2026-03-02 19:55:23', '2026-03-02 19:55:23');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (14, 'features', '{\"coachEnabled\": true, \"pointsEnabled\": true, \"analyticsEnabled\": true, \"communityEnabled\": true, \"solarTermEnabled\": true, \"registrationEnabled\": true}', '2026-03-02 19:55:23', '2026-03-02 19:55:23');
INSERT INTO `system_setting` (`id`, `setting_group`, `setting_json`, `create_time`, `update_time`) VALUES (15, 'email', '{\"enabled\": false, \"smtpPort\": 587, \"smtpServer\": \"smtp.gmail.com\", \"senderEmail\": \"noreply@fitpal.com\", \"senderPassword\": \"\"}', '2026-03-02 19:55:23', '2026-03-02 19:55:23');
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `user_account` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号',
  `user_password` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `user_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '昵称',
  `user_avatar` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像',
  `user_profile` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '简介',
  `user_role` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'user' COMMENT '角色:user/coach/admin/ban',
  `user_phone` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号',
  `user_email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `union_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '微信unionId',
  `mp_open_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '小程序openId',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态:1启用 0禁用',
  `create_by` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_by` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_account` (`user_account`),
  UNIQUE KEY `user_phone` (`user_phone`),
  UNIQUE KEY `user_email` (`user_email`),
  UNIQUE KEY `union_id` (`union_id`),
  UNIQUE KEY `mp_open_id` (`mp_open_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (1, 'admin', '1269d023eff6b95104c6673e64167c80', '梁管理员', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '梁管理员，关注科学减脂与长期健康管理。', 'admin', '13800000001', 'admin_liang@fitpal.com', 'union_fit_0001', 'openid_fit_0001', 1, 'seed-script', '2026-02-01 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (2, 'admin_zhou', '1269d023eff6b95104c6673e64167c80', '周运营', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '周运营，关注科学减脂与长期健康管理。', 'admin', '13800000002', 'admin_zhou@fitpal.com', 'union_fit_0002', 'openid_fit_0002', 1, 'seed-script', '2026-02-02 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (3, 'coach_chen', '1269d023eff6b95104c6673e64167c80', '陈教练', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '陈教练，关注科学减脂与长期健康管理。', 'coach', '13800000003', 'coach_chen@fitpal.com', 'union_fit_0003', 'openid_fit_0003', 1, 'seed-script', '2026-02-03 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (4, 'coach_wu', '1269d023eff6b95104c6673e64167c80', '吴教练', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '吴教练，关注科学减脂与长期健康管理。', 'coach', '13800000004', 'coach_wu@fitpal.com', 'union_fit_0004', 'openid_fit_0004', 1, 'seed-script', '2026-02-04 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (5, 'coach_ma', '1269d023eff6b95104c6673e64167c80', '马教练', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '马教练，关注科学减脂与长期健康管理。', 'coach', '13800000005', 'coach_ma@fitpal.com', 'union_fit_0005', 'openid_fit_0005', 1, 'seed-script', '2026-02-05 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (6, 'user_wang', '1269d023eff6b95104c6673e64167c80', '王晨曦', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '王晨曦，关注科学减脂与长期健康管理。', 'user', '13800000006', 'user_wang@fitpal.com', 'union_fit_0006', 'openid_fit_0006', 1, 'seed-script', '2026-02-06 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (7, 'user_li', '1269d023eff6b95104c6673e64167c80', '李雨桐', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '李雨桐，关注科学减脂与长期健康管理。', 'user', '13800000007', 'user_li@fitpal.com', 'union_fit_0007', 'openid_fit_0007', 1, 'seed-script', '2026-02-07 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (8, 'user_zhao', '1269d023eff6b95104c6673e64167c80', '赵明远', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '赵明远，关注科学减脂与长期健康管理。', 'user', '13800000008', 'user_zhao@fitpal.com', 'union_fit_0008', 'openid_fit_0008', 1, 'seed-script', '2026-02-08 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (9, 'user_liu', '1269d023eff6b95104c6673e64167c80', '刘佳宁', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '刘佳宁，关注科学减脂与长期健康管理。', 'user', '13800000009', 'user_liu@fitpal.com', 'union_fit_0009', 'openid_fit_0009', 1, 'seed-script', '2026-02-09 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (10, 'user_sun', '1269d023eff6b95104c6673e64167c80', '孙子涵', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '孙子涵，关注科学减脂与长期健康管理。', 'user', '13800000010', 'user_sun@fitpal.com', 'union_fit_0010', 'openid_fit_0010', 1, 'seed-script', '2026-02-10 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (11, 'user_he', '1269d023eff6b95104c6673e64167c80', '何悦', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '何悦，关注科学减脂与长期健康管理。', 'user', '13800000011', 'user_he@fitpal.com', 'union_fit_0011', 'openid_fit_0011', 1, 'seed-script', '2026-02-11 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (12, 'user_xu', '1269d023eff6b95104c6673e64167c80', '徐浩然', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '徐浩然，关注科学减脂与长期健康管理。', 'user', '13800000012', 'user_xu@fitpal.com', 'union_fit_0012', 'openid_fit_0012', 1, 'seed-script', '2026-02-12 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (13, 'user_qian', '1269d023eff6b95104c6673e64167c80', '钱依琳', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '钱依琳，关注科学减脂与长期健康管理。', 'user', '13800000013', 'user_qian@fitpal.com', 'union_fit_0013', 'openid_fit_0013', 1, 'seed-script', '2026-02-13 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (14, 'user_ding', '1269d023eff6b95104c6673e64167c80', '丁一鸣', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '丁一鸣，关注科学减脂与长期健康管理。', 'ban', '13800000014', 'user_ding@fitpal.com', 'union_fit_0014', 'openid_fit_0014', 1, 'seed-script', '2026-02-14 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (15, 'user_yang', '1269d023eff6b95104c6673e64167c80', '杨梦琪', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '杨梦琪，关注科学减脂与长期健康管理。', 'user', '13800000015', 'user_yang@fitpal.com', 'union_fit_0015', 'openid_fit_0015', 0, 'seed-script', '2026-02-15 08:30:00', 'seed-script', '2026-03-02 20:09:34', 0);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (16, 'user_hu', '1269d023eff6b95104c6673e64167c80', '胡景天', '/api/file/preview/user_avatar/1/nwifo4K2-img1.jpg', '胡景天，关注科学减脂与长期健康管理。', 'user', '13800000016', 'user_hu@fitpal.com', 'union_fit_0016', 'openid_fit_0016', 1, 'seed-script', '2026-02-16 08:30:00', 'seed-script', '2026-03-02 20:09:34', 1);
INSERT INTO `user` (`id`, `user_account`, `user_password`, `user_name`, `user_avatar`, `user_profile`, `user_role`, `user_phone`, `user_email`, `union_id`, `mp_open_id`, `status`, `create_by`, `create_time`, `update_by`, `update_time`, `is_delete`) VALUES (17, 'demo', '1269d023eff6b95104c6673e64167c80', NULL, NULL, NULL, 'user', '13777777777', NULL, NULL, NULL, 1, NULL, '2026-03-02 20:09:26', NULL, '2026-03-02 20:09:34', 0);
COMMIT;

-- ----------------------------
-- Table structure for user_badge
-- ----------------------------
DROP TABLE IF EXISTS `user_badge`;
CREATE TABLE `user_badge` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `badge_id` bigint NOT NULL,
  `cost_point` int NOT NULL DEFAULT '0',
  `source` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'exchange',
  `obtain_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_user_badge` (`user_id`,`badge_id`),
  KEY `idx_user_badge_user_time` (`user_id`,`obtain_time`),
  KEY `fk_user_badge_badge` (`badge_id`),
  CONSTRAINT `fk_user_badge_badge` FOREIGN KEY (`badge_id`) REFERENCES `point_badge` (`id`),
  CONSTRAINT `fk_user_badge_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_badge
-- ----------------------------
BEGIN;
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (1, 3, 1, 40, 'task_reward', '2026-02-13 08:30:00', '2026-02-13 08:30:00', '2026-02-13 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (2, 4, 2, 80, 'admin_grant', '2026-02-14 08:30:00', '2026-02-14 08:30:00', '2026-02-14 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (3, 5, 3, 120, 'exchange', '2026-02-15 08:30:00', '2026-02-15 08:30:00', '2026-02-15 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (4, 6, 4, 160, 'task_reward', '2026-02-16 08:30:00', '2026-02-16 08:30:00', '2026-02-16 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (5, 7, 5, 200, 'admin_grant', '2026-02-17 08:30:00', '2026-02-17 08:30:00', '2026-02-17 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (6, 8, 6, 240, 'exchange', '2026-02-18 08:30:00', '2026-02-18 08:30:00', '2026-02-18 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (7, 9, 7, 280, 'task_reward', '2026-02-19 08:30:00', '2026-02-19 08:30:00', '2026-02-19 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (8, 10, 8, 320, 'admin_grant', '2026-02-20 08:30:00', '2026-02-20 08:30:00', '2026-02-20 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (9, 11, 9, 360, 'exchange', '2026-02-21 08:30:00', '2026-02-21 08:30:00', '2026-02-21 09:30:00', 1);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (10, 12, 10, 400, 'task_reward', '2026-02-22 08:30:00', '2026-02-22 08:30:00', '2026-02-22 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (11, 13, 11, 440, 'admin_grant', '2026-02-23 08:30:00', '2026-02-23 08:30:00', '2026-02-23 09:30:00', 0);
INSERT INTO `user_badge` (`id`, `user_id`, `badge_id`, `cost_point`, `source`, `obtain_time`, `create_time`, `update_time`, `is_delete`) VALUES (12, 14, 12, 480, 'exchange', '2026-02-24 08:30:00', '2026-02-24 08:30:00', '2026-02-24 09:30:00', 0);
COMMIT;

-- ----------------------------
-- Table structure for user_point_account
-- ----------------------------
DROP TABLE IF EXISTS `user_point_account`;
CREATE TABLE `user_point_account` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `total_point` int NOT NULL DEFAULT '0',
  `available_point` int NOT NULL DEFAULT '0',
  `level_name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '青铜',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `fk_point_account_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户积分账户';

-- ----------------------------
-- Records of user_point_account
-- ----------------------------
BEGIN;
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (1, 3, 175, 175, '青铜', '2026-02-14 08:30:00', '2026-02-14 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (2, 4, 230, 230, '白银', '2026-02-15 08:30:00', '2026-02-15 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (3, 5, 290, 270, '白银', '2026-02-16 08:30:00', '2026-03-02 20:05:05');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (4, 6, 340, 340, '铂金', '2026-02-17 08:30:00', '2026-02-17 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (5, 7, 395, 395, '青铜', '2026-02-18 08:30:00', '2026-02-18 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (6, 8, 450, 430, '白银', '2026-02-19 08:30:00', '2026-02-19 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (7, 9, 505, 505, '黄金', '2026-02-20 08:30:00', '2026-02-20 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (8, 10, 560, 560, '铂金', '2026-02-21 08:30:00', '2026-02-21 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (9, 11, 615, 595, '青铜', '2026-02-22 08:30:00', '2026-02-22 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (10, 12, 670, 670, '白银', '2026-02-23 08:30:00', '2026-02-23 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (11, 13, 725, 725, '黄金', '2026-02-24 08:30:00', '2026-02-24 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (12, 14, 780, 760, '铂金', '2026-02-25 08:30:00', '2026-02-25 09:30:00');
INSERT INTO `user_point_account` (`id`, `user_id`, `total_point`, `available_point`, `level_name`, `create_time`, `update_time`) VALUES (13, 1, 113, 113, '白银', '2026-03-02 19:57:45', '2026-03-02 20:05:09');
COMMIT;

-- ----------------------------
-- Table structure for user_point_log
-- ----------------------------
DROP TABLE IF EXISTS `user_point_log`;
CREATE TABLE `user_point_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `task_code` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `task_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `point_change` int NOT NULL,
  `biz_date` date DEFAULT NULL,
  `remark` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_point_log_user_date` (`user_id`,`biz_date`),
  CONSTRAINT `fk_point_log_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='积分变更记录';

-- ----------------------------
-- Records of user_point_log
-- ----------------------------
BEGIN;
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (1, 3, 'DAILY_CHECKIN', '每日打卡', 11, '2026-02-12', '系统发放积分，批次1', '2026-02-15 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (2, 4, 'COMMUNITY_POST', '发布社区内容', 32, '2026-02-13', '系统发放积分，批次2', '2026-02-16 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (3, 5, 'COMMUNITY_COMMENT', '社区评论', 5, '2026-02-14', '系统发放积分，批次3', '2026-02-17 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (4, 6, 'HEALTH_RECORD', '健康记录', 19, '2026-02-15', '系统发放积分，批次4', '2026-02-18 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (5, 7, 'DAILY_CHECKIN', '每日打卡', 15, '2026-02-16', '系统发放积分，批次5', '2026-02-19 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (6, 8, 'COMMUNITY_POST', '发布社区内容', 36, '2026-02-17', '系统发放积分，批次6', '2026-02-20 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (7, 9, 'COMMUNITY_COMMENT', '社区评论', 9, '2026-02-18', '系统发放积分，批次7', '2026-02-21 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (8, 10, 'HEALTH_RECORD', '健康记录', 23, '2026-02-19', '系统发放积分，批次8', '2026-02-22 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (9, 11, 'DAILY_CHECKIN', '每日打卡', 19, '2026-02-20', '系统发放积分，批次9', '2026-02-23 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (10, 12, 'COMMUNITY_POST', '发布社区内容', 40, '2026-02-21', '系统发放积分，批次10', '2026-02-24 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (11, 13, 'COMMUNITY_COMMENT', '社区评论', 13, '2026-02-22', '系统发放积分，批次11', '2026-02-25 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (12, 14, 'HEALTH_RECORD', '健康记录', 27, '2026-02-23', '系统发放积分，批次12', '2026-02-26 08:30:00');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (13, 1, 'DAILY_CHECKIN', '每日打卡', 10, '2026-03-02', '完成每日健康打卡', '2026-03-02 19:57:45');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (14, 1, 'ASSESSMENT_COMPLETE', '完成减脂评估', 100, '2026-03-02', '完成问卷评估', '2026-03-02 20:04:47');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (15, 1, 'COMMUNITY_LIKE', '社区点赞', 1, '2026-03-02', '点赞社区帖子', '2026-03-02 20:05:05');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (16, 5, 'POST_LIKED', '内容被赞', 5, '2026-03-02', '社区帖子#1获得点赞', '2026-03-02 20:05:05');
INSERT INTO `user_point_log` (`id`, `user_id`, `task_code`, `task_name`, `point_change`, `biz_date`, `remark`, `create_time`) VALUES (17, 1, 'COMMUNITY_COMMENT', '社区评论', 2, '2026-03-02', '评论社区帖子', '2026-03-02 20:05:09');
COMMIT;

-- ----------------------------
-- Table structure for user_points
-- ----------------------------
DROP TABLE IF EXISTS `user_points`;
CREATE TABLE `user_points` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `user_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户名',
  `total_points` int NOT NULL DEFAULT '0' COMMENT '总积分',
  `medal_count` int NOT NULL DEFAULT '0' COMMENT '勋章数',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` int DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_id` (`user_id`),
  KEY `idx_total_points` (`total_points`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户积分表';

-- ----------------------------
-- Records of user_points
-- ----------------------------
BEGIN;
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (1, 3, '陈教练', 225, 2, '2026-02-16 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (2, 4, '吴教练', 270, 3, '2026-02-17 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (3, 5, '马教练', 315, 4, '2026-02-18 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (4, 6, '王晨曦', 360, 1, '2026-02-19 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (5, 7, '李雨桐', 405, 2, '2026-02-20 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (6, 8, '赵明远', 450, 3, '2026-02-21 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (7, 9, '刘佳宁', 495, 4, '2026-02-22 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (8, 10, '孙子涵', 540, 1, '2026-02-23 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (9, 11, '何悦', 585, 2, '2026-02-24 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (10, 12, '徐浩然', 630, 3, '2026-02-25 08:30:00', 1);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (11, 13, '钱依琳', 675, 4, '2026-02-26 08:30:00', 0);
INSERT INTO `user_points` (`id`, `user_id`, `user_name`, `total_points`, `medal_count`, `updated_at`, `is_delete`) VALUES (12, 14, '丁一鸣', 720, 1, '2026-02-27 08:30:00', 0);
COMMIT;

-- ----------------------------
-- Table structure for user_questionnaire
-- ----------------------------
DROP TABLE IF EXISTS `user_questionnaire`;
CREATE TABLE `user_questionnaire` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `height_cm` decimal(5,2) DEFAULT NULL,
  `current_weight_kg` decimal(5,2) DEFAULT NULL,
  `target_weight_kg` decimal(5,2) DEFAULT NULL,
  `goal_cycle_days` int DEFAULT NULL,
  `diet_preference` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sport_preference` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `intensity` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `health_condition` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `answer_json` text COLLATE utf8mb4_unicode_ci,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_questionnaire_user` (`user_id`),
  CONSTRAINT `fk_questionnaire_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='兴趣与健康问卷';

-- ----------------------------
-- Records of user_questionnaire
-- ----------------------------
BEGIN;
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (1, 3, 23, 'male', 159.00, 77.00, 70.00, 65, '控糖饮食', '力量训练', 'medium', '轻度脂肪肝', '{\"mealRegularity\": 4, \"exerciseDays\": 3, \"waterIntakeMl\": 1880}', '2026-02-03 08:30:00', '2026-02-03 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (2, 4, 24, 'female', 160.00, 76.00, 68.00, 70, '地中海饮食', '游泳', 'high', '久坐腰背紧张', '{\"mealRegularity\": 5, \"exerciseDays\": 4, \"waterIntakeMl\": 1960}', '2026-02-04 08:30:00', '2026-02-04 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (3, 5, 25, 'male', 161.00, 75.00, 66.00, 75, '轻断食', '瑜伽', 'low', '轻微高尿酸', '{\"mealRegularity\": 3, \"exerciseDays\": 5, \"waterIntakeMl\": 2040}', '2026-02-05 08:30:00', '2026-02-05 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (4, 6, 26, 'female', 162.00, 74.00, 68.00, 80, '低脂高蛋白', '慢跑', 'medium', '无慢病', '{\"mealRegularity\": 4, \"exerciseDays\": 2, \"waterIntakeMl\": 2120}', '2026-02-06 08:30:00', '2026-02-06 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (5, 7, 27, 'male', 163.00, 73.00, 66.00, 85, '控糖饮食', '力量训练', 'high', '轻度脂肪肝', '{\"mealRegularity\": 5, \"exerciseDays\": 3, \"waterIntakeMl\": 2200}', '2026-02-07 08:30:00', '2026-02-07 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (6, 8, 28, 'female', 164.00, 72.00, 64.00, 90, '地中海饮食', '游泳', 'low', '久坐腰背紧张', '{\"mealRegularity\": 3, \"exerciseDays\": 4, \"waterIntakeMl\": 2280}', '2026-02-08 08:30:00', '2026-02-08 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (7, 9, 29, 'male', 165.00, 71.00, 62.00, 95, '轻断食', '瑜伽', 'medium', '轻微高尿酸', '{\"mealRegularity\": 4, \"exerciseDays\": 5, \"waterIntakeMl\": 2360}', '2026-02-09 08:30:00', '2026-02-09 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (8, 10, 30, 'female', 166.00, 70.00, 64.00, 100, '低脂高蛋白', '慢跑', 'high', '无慢病', '{\"mealRegularity\": 5, \"exerciseDays\": 2, \"waterIntakeMl\": 2440}', '2026-02-10 08:30:00', '2026-02-10 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (9, 11, 31, 'male', 167.00, 69.00, 62.00, 105, '控糖饮食', '力量训练', 'low', '轻度脂肪肝', '{\"mealRegularity\": 3, \"exerciseDays\": 3, \"waterIntakeMl\": 2520}', '2026-02-11 08:30:00', '2026-02-11 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (10, 12, 32, 'female', 168.00, 68.00, 60.00, 110, '地中海饮食', '游泳', 'medium', '久坐腰背紧张', '{\"mealRegularity\": 4, \"exerciseDays\": 4, \"waterIntakeMl\": 2600}', '2026-02-12 08:30:00', '2026-02-12 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (11, 13, 33, 'male', 169.00, 67.00, 58.00, 115, '轻断食', '瑜伽', 'high', '轻微高尿酸', '{\"mealRegularity\": 5, \"exerciseDays\": 5, \"waterIntakeMl\": 2680}', '2026-02-13 08:30:00', '2026-02-13 10:30:00', 0);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (12, 14, 22, 'female', 170.00, 66.00, 60.00, 120, '低脂高蛋白', '慢跑', 'low', '无慢病', '{\"mealRegularity\": 3, \"exerciseDays\": 2, \"waterIntakeMl\": 2760}', '2026-02-14 08:30:00', '2026-02-14 10:30:00', 1);
INSERT INTO `user_questionnaire` (`id`, `user_id`, `age`, `gender`, `height_cm`, `current_weight_kg`, `target_weight_kg`, `goal_cycle_days`, `diet_preference`, `sport_preference`, `intensity`, `health_condition`, `answer_json`, `create_time`, `update_time`, `is_delete`) VALUES (13, 1, 28, 'male', 168.00, 68.00, 60.00, 60, NULL, NULL, 'medium', NULL, NULL, '2026-03-02 20:04:47', '2026-03-02 20:04:47', 0);
COMMIT;

-- ----------------------------
-- Table structure for user_settings
-- ----------------------------
DROP TABLE IF EXISTS `user_settings`;
CREATE TABLE `user_settings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `checkin_reminder_enabled` tinyint NOT NULL DEFAULT '1' COMMENT '打卡提醒',
  `community_notification_enabled` tinyint NOT NULL DEFAULT '1' COMMENT '社区互动提醒',
  `weekly_report_notification_enabled` tinyint NOT NULL DEFAULT '1' COMMENT '周报提醒',
  `coach_reply_notification_enabled` tinyint NOT NULL DEFAULT '1' COMMENT '教练回复提醒',
  `health_data_visible` tinyint NOT NULL DEFAULT '0' COMMENT '健康数据是否公开',
  `profile_visible` tinyint NOT NULL DEFAULT '1' COMMENT '个人资料是否公开',
  `consultation_data_retention_days` int NOT NULL DEFAULT '30' COMMENT '咨询记录保留天数',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `idx_user_settings_user` (`user_id`),
  CONSTRAINT `fk_user_settings_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户设置';

-- ----------------------------
-- Records of user_settings
-- ----------------------------
BEGIN;
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (1, 1, 1, 1, 1, 1, 1, 1, 31, '2026-02-02 08:30:00', '2026-02-02 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (2, 2, 1, 1, 1, 0, 0, 1, 32, '2026-02-03 08:30:00', '2026-02-03 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (3, 3, 0, 1, 1, 1, 0, 1, 33, '2026-02-04 08:30:00', '2026-02-04 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (4, 4, 1, 0, 1, 0, 1, 0, 34, '2026-02-05 08:30:00', '2026-02-05 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (5, 5, 1, 1, 0, 1, 0, 1, 35, '2026-02-06 08:30:00', '2026-02-06 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (6, 6, 0, 1, 1, 0, 0, 1, 36, '2026-02-07 08:30:00', '2026-02-07 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (7, 7, 1, 1, 1, 1, 1, 1, 37, '2026-02-08 08:30:00', '2026-02-08 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (8, 8, 1, 0, 1, 0, 0, 0, 38, '2026-02-09 08:30:00', '2026-02-09 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (9, 9, 0, 1, 1, 1, 0, 1, 39, '2026-02-10 08:30:00', '2026-02-10 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (10, 10, 1, 1, 0, 0, 1, 1, 40, '2026-02-11 08:30:00', '2026-02-11 09:30:00', 0);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (11, 11, 1, 1, 1, 1, 0, 1, 41, '2026-02-12 08:30:00', '2026-02-12 09:30:00', 1);
INSERT INTO `user_settings` (`id`, `user_id`, `checkin_reminder_enabled`, `community_notification_enabled`, `weekly_report_notification_enabled`, `coach_reply_notification_enabled`, `health_data_visible`, `profile_visible`, `consultation_data_retention_days`, `create_time`, `update_time`, `is_delete`) VALUES (12, 12, 0, 0, 1, 0, 0, 0, 42, '2026-02-13 08:30:00', '2026-02-13 09:30:00', 0);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
