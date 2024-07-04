SET NAMES utf8mb4;
-- 暂时关闭外键检查，以便在创建或修改表时不受外键约束的限制  
SET FOREIGN_KEY_CHECKS = 0;




-- 创建课程表（course）   
-- 如果已经存在名为'course'的表，则先删除它  
DROP TABLE IF EXISTS `course`;  
-- 创建一个新的表'course'  
CREATE TABLE `course`  (  
  `Cno` char(4) NOT NULL,            -- 课程编号，最多4个字符，不允许为空  
  `Cname` char(40) NOT NULL,         -- 课程名称，最多40个字符，不允许为空  
  `Cpno` char(4) DEFAULT NULL,       -- 先修课程编号，最多4个字符，允许为空  
  `Ccredict` smallint DEFAULT NULL,  -- 学分要求，允许为空  
  -- 设置课程编号为主键，并使用B树索引  
  PRIMARY KEY (`Cno`) USING BTREE,  
  -- 为先修课程编号创建索引  
  INDEX `Cpno`(`Cpno` ASC) USING BTREE,  
  -- 设置外键约束，先修课程编号（Cpno）必须引用本表（course）中的课程编号（Cno）  
  CONSTRAINT `Cpno` FOREIGN KEY (`Cpno`) REFERENCES `course` (`Cno`) ON DELETE RESTRICT ON UPDATE RESTRICT  
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;  


-- 插入课程信息

INSERT INTO `course` VALUES ('1', '崩坏现象基础理论', '1', 4);
INSERT INTO `course` VALUES ('2', '战术分析与团队协作', '1', 2);
INSERT INTO `course` VALUES ('3', '女武神战斗技巧入门', '2', 4);
INSERT INTO `course` VALUES ('4', '量子物理与武器科技', '2', 3);
INSERT INTO `course` VALUES ('5', '崩坏兽生态与对策', '3', 4);
INSERT INTO `course` VALUES ('6', '高级女武神进阶技巧', '3', 2);
INSERT INTO `course` VALUES ('7', '提瓦特高等元素论', '4', 4);




-- 创建学生表（student）  
-- 如果已经存在名为'student'的表，则先删除它  
DROP TABLE IF EXISTS `student`;  
-- 创建一个新的表'student'  
CREATE TABLE `student`  (  
  `Sno` char(9) NOT NULL,         -- 学生编号，最多9个字符，不允许为空  
  `Sname` char(20) DEFAULT NULL,  -- 学生姓名，最多20个字符，允许为空  
  `Ssex` char(2) DEFAULT NULL,    -- 学生性别，最多2个字符，允许为空  
  `Sage` int(20) DEFAULT NULL,    -- 学生年龄，最多20个字符，允许为空  
  `Sdept` char(20) DEFAULT NULL,  -- 学生所在系，最多20个字符，允许为空  
  -- 设置学生编号为主键，并使用B树索引  
  PRIMARY KEY (`Sno`) USING BTREE,  
  -- 为学生姓名创建唯一索引  
  UNIQUE INDEX `Sname`(`Sname` ASC) USING BTREE  
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;  


-- 插入学生信息INSERT INTO `student` VALUES ('20040219', '符华', '女', 54000, 'Gloves');
INSERT INTO `student` VALUES ('20040413', '雷电芽衣', '女', 20, 'TaiKnife');
INSERT INTO `student` VALUES ('20041207', '琪亚娜·卡斯兰娜', '女', 20, 'TwinGuns');
INSERT INTO `student` VALUES ('20060403', '李素裳', '女', 18, 'Gloves');
INSERT INTO `student` VALUES ('20060818', '布洛妮娅·扎伊切克', '女', 18, 'HeavyArtillery');




CREATE TABLE `sc`  (    
  `Sno` char(9) NOT NULL,     
  `Cno` char(4) NOT NULL,    
  `Grade` smallint DEFAULT NULL,    
  PRIMARY KEY (`Sno`, `Cno`) USING BTREE,    
  INDEX `Cno_idx`(`Cno` ASC) USING BTREE,    
  CONSTRAINT `FK_sc_course` FOREIGN KEY (`Cno`) REFERENCES `course` (`Cno`) ON DELETE RESTRICT ON UPDATE RESTRICT,    
  CONSTRAINT `FK_sc_student` FOREIGN KEY (`Sno`) REFERENCES `student` (`Sno`) ON DELETE RESTRICT ON UPDATE RESTRICT   
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- 插入选课信息，其中包括了学生已选课程的成绩

INSERT INTO `sc` VALUES ('20040219', '2', 95);
INSERT INTO `sc` VALUES ('20040413', '3', 92);
INSERT INTO `sc` VALUES ('20041207', '1', 60);
INSERT INTO `sc` VALUES ('20041207', '2', 52);
INSERT INTO `sc` VALUES ('20041207', '3', NULL);
INSERT INTO `sc` VALUES ('20060818', '3', 100);




-- 创建用户信息表（user_info）   
-- 如果已经存在名为'user_info'的表，则先删除它  
DROP TABLE IF EXISTS `user_info`;  
-- 创建一个新的表'user_info'  
CREATE TABLE `user_info`  (  
  `username` varchar(20) NOT NULL,  -- 用户名，不允许为空  
  `password` varchar(32) DEFAULT NULL,  -- 密码，允许为空  
  `role` text DEFAULT NULL,         -- 用户角色，允许为空  
  -- 设置用户名为主键，并使用B树索引  
  PRIMARY KEY (`username`) USING BTREE  
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;  

-- 插入用户信息，有admin和user两种用户角色

INSERT INTO `user_info` VALUES ('20040219', '0219', 'user');
INSERT INTO `user_info` VALUES ('20040413', '0413', 'user');
INSERT INTO `user_info` VALUES ('20041207', '1207', 'user');
INSERT INTO `user_info` VALUES ('20060818', '0818', 'user');
INSERT INTO `user_info` VALUES ('Theresa', '0328', 'admin');


-- 重新开启外键检查
SET FOREIGN_KEY_CHECKS = 1;