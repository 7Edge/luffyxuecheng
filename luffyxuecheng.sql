/*
SQLyog Ultimate v12.4.0 (64 bit)
MySQL - 10.1.10-MariaDB : Database - luffyxuecheng
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`luffyxuecheng` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `luffyxuecheng`;

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_group` */

/*Table structure for table `auth_group_permissions` */

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Can add permission',1,'add_permission'),
(2,'Can change permission',1,'change_permission'),
(3,'Can delete permission',1,'delete_permission'),
(4,'Can add group',2,'add_group'),
(5,'Can change group',2,'change_group'),
(6,'Can delete group',2,'delete_group'),
(7,'Can add user',3,'add_user'),
(8,'Can change user',3,'change_user'),
(9,'Can delete user',3,'delete_user'),
(10,'Can add content type',4,'add_contenttype'),
(11,'Can change content type',4,'change_contenttype'),
(12,'Can delete content type',4,'delete_contenttype'),
(13,'Can add session',5,'add_session'),
(14,'Can change session',5,'change_session'),
(15,'Can delete session',5,'delete_session'),
(16,'Can add chapters',6,'add_chapters'),
(17,'Can change chapters',6,'change_chapters'),
(18,'Can delete chapters',6,'delete_chapters'),
(19,'Can add course',7,'add_course'),
(20,'Can change course',7,'change_course'),
(21,'Can delete course',7,'delete_course'),
(22,'Can add course detail',8,'add_coursedetail'),
(23,'Can change course detail',8,'change_coursedetail'),
(24,'Can delete course detail',8,'delete_coursedetail'),
(25,'Can add test2',9,'add_test2'),
(26,'Can change test2',9,'change_test2'),
(27,'Can delete test2',9,'delete_test2'),
(28,'Can add test',10,'add_test'),
(29,'Can change test',10,'change_test'),
(30,'Can delete test',10,'delete_test'),
(31,'Can add log entry',11,'add_logentry'),
(32,'Can change log entry',11,'change_logentry'),
(33,'Can delete log entry',11,'delete_logentry'),
(34,'Can add user token',12,'add_usertoken'),
(35,'Can change user token',12,'change_usertoken'),
(36,'Can delete user token',12,'delete_usertoken'),
(37,'Can add user info',13,'add_userinfo'),
(38,'Can change user info',13,'change_userinfo'),
(39,'Can delete user info',13,'delete_userinfo');

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `auth_user` */

insert  into `auth_user`(`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`) values 
(1,'pbkdf2_sha256$100000$t0YmSHioYMuM$Z1znMXacK7m9IDvt8yGLzv6O42OSF225j/6YPsKJvJU=','2018-12-29 06:11:49.429432',1,'root','','','',1,1,'2018-12-29 06:11:30.038916');

/*Table structure for table `auth_user_groups` */

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user_groups` */

/*Table structure for table `auth_user_user_permissions` */

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user_user_permissions` */

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

/*Data for the table `django_admin_log` */

insert  into `django_admin_log`(`id`,`action_time`,`object_id`,`object_repr`,`action_flag`,`change_message`,`content_type_id`,`user_id`) values 
(1,'2018-12-29 06:14:41.655197','3','Python全栈',1,'[{\"added\": {}}]',7,1),
(2,'2018-12-29 06:15:00.689474','4','Linux云计算',1,'[{\"added\": {}}]',7,1),
(3,'2018-12-29 06:15:15.858327','5','Python周末',1,'[{\"added\": {}}]',7,1),
(4,'2018-12-29 06:15:56.919160','1','Python全栈',1,'[{\"added\": {}}]',8,1),
(5,'2018-12-29 06:16:21.792826','2','Python周末',1,'[{\"added\": {}}]',8,1),
(6,'2018-12-29 06:16:36.361158','3','Linux云计算',1,'[{\"added\": {}}]',8,1),
(7,'2018-12-29 06:22:34.784357','1','Python基础',1,'[{\"added\": {}}]',6,1),
(8,'2018-12-29 06:22:45.596542','2','Python网络',1,'[{\"added\": {}}]',6,1),
(9,'2018-12-29 06:22:57.776423','3','Python数据库',1,'[{\"added\": {}}]',6,1),
(10,'2018-12-29 06:23:10.717804','4','Python并发',1,'[{\"added\": {}}]',6,1),
(11,'2018-12-29 06:23:34.941477','5','Python文件操作',1,'[{\"added\": {}}]',6,1),
(12,'2018-12-29 06:23:47.335102','6','Python语法基础',1,'[{\"added\": {}}]',6,1),
(13,'2018-12-29 06:23:56.959179','7','Python进阶',1,'[{\"added\": {}}]',6,1),
(14,'2018-12-29 06:24:04.282673','8','Python进阶',1,'[{\"added\": {}}]',6,1),
(15,'2018-12-29 06:24:21.806273','9','Python并发网络编程',1,'[{\"added\": {}}]',6,1),
(16,'2018-12-29 06:24:32.718560','10','Linux安装',1,'[{\"added\": {}}]',6,1),
(17,'2018-12-29 06:24:46.719384','11','Linux常用命令',1,'[{\"added\": {}}]',6,1),
(18,'2018-12-29 06:24:55.932715','12','Linux数据库',1,'[{\"added\": {}}]',6,1),
(19,'2018-12-29 06:25:03.622358','13','Docker',1,'[{\"added\": {}}]',6,1),
(20,'2018-12-29 06:25:11.934137','14','Zabbix',1,'[{\"added\": {}}]',6,1),
(21,'2019-01-08 08:38:07.709690','1','alex',1,'[{\"added\": {}}]',13,1),
(22,'2019-01-08 08:38:15.255091','2','egon',1,'[{\"added\": {}}]',13,1);

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values 
(11,'admin','logentry'),
(2,'auth','group'),
(1,'auth','permission'),
(3,'auth','user'),
(4,'contenttypes','contenttype'),
(6,'luffyapi','chapters'),
(7,'luffyapi','course'),
(8,'luffyapi','coursedetail'),
(10,'luffyapi','test'),
(9,'luffyapi','test2'),
(13,'luffyapi','userinfo'),
(12,'luffyapi','usertoken'),
(5,'sessions','session');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values 
(2,'contenttypes','0001_initial','2018-12-29 03:11:04.040935'),
(3,'contenttypes','0002_remove_content_type_name','2018-12-29 03:11:05.044276'),
(4,'auth','0001_initial','2018-12-29 03:11:14.112125'),
(5,'auth','0002_alter_permission_name_max_length','2018-12-29 03:11:15.231688'),
(6,'auth','0003_alter_user_email_max_length','2018-12-29 03:11:16.636828'),
(7,'auth','0004_alter_user_username_opts','2018-12-29 03:11:16.691799'),
(8,'auth','0005_alter_user_last_login_null','2018-12-29 03:11:17.195298'),
(9,'auth','0006_require_contenttypes_0002','2018-12-29 03:11:17.238268'),
(10,'auth','0007_alter_validators_add_error_messages','2018-12-29 03:11:17.305226'),
(11,'auth','0008_alter_user_username_max_length','2018-12-29 03:11:18.105033'),
(12,'auth','0009_alter_user_last_name_max_length','2018-12-29 03:11:18.864640'),
(13,'sessions','0001_initial','2018-12-29 03:11:19.902424'),
(17,'luffyapi','0001_initial','2018-12-29 05:15:19.695647'),
(18,'luffyapi','0002_test_test2','2018-12-29 05:15:21.345917'),
(19,'luffyapi','0003_auto_20181229_1303','2018-12-29 05:15:25.411375'),
(20,'admin','0001_initial','2018-12-29 06:12:22.036885'),
(21,'admin','0002_logentry_remove_auto_add','2018-12-29 06:12:22.089853'),
(22,'luffyapi','0004_chapters_course','2018-12-29 06:21:17.084106'),
(23,'luffyapi','0005_userinfo_usertoken','2019-01-08 08:34:18.613198');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values 
('4rkb4wsrltvz7seo93n20m7rmk8hhfix','MTJkNDM1NDk4NDg0ZTZmMWI2ZjgwMjJkMTQwNTZjYWE4ZWQ0YTdjYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNWYxNGQxMTg0YjQwYTdiZWNlZTcxZGQxM2JmMzEyZGNjMTVkZjYwIn0=','2019-01-12 06:11:49.709259');

/*Table structure for table `luffyapi_chapters` */

DROP TABLE IF EXISTS `luffyapi_chapters`;

CREATE TABLE `luffyapi_chapters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `luffyapi_chapters_course_id_1a34ca87_fk_luffyapi_course_id` (`course_id`),
  CONSTRAINT `luffyapi_chapters_course_id_1a34ca87_fk_luffyapi_course_id` FOREIGN KEY (`course_id`) REFERENCES `luffyapi_course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_chapters` */

insert  into `luffyapi_chapters`(`id`,`title`,`course_id`) values 
(1,'Python基础',3),
(2,'Python网络',3),
(3,'Python数据库',3),
(4,'Python并发',3),
(5,'Python文件操作',3),
(6,'Python语法基础',5),
(7,'Python进阶',3),
(8,'Python进阶',5),
(9,'Python并发网络编程',5),
(10,'Linux安装',4),
(11,'Linux常用命令',4),
(12,'Linux数据库',4),
(13,'Docker',4),
(14,'Zabbix',4);

/*Table structure for table `luffyapi_course` */

DROP TABLE IF EXISTS `luffyapi_course`;

CREATE TABLE `luffyapi_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `image` varchar(32) NOT NULL,
  `level` smallint(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_course` */

insert  into `luffyapi_course`(`id`,`title`,`image`,`level`) values 
(3,'Python全栈','luffyapi/images/01.png',1),
(4,'Linux云计算','luffyapi/images/02.png',2),
(5,'Python周末','luffyapi/images/03.png',3);

/*Table structure for table `luffyapi_coursedetail` */

DROP TABLE IF EXISTS `luffyapi_coursedetail`;

CREATE TABLE `luffyapi_coursedetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `why` varchar(32) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id` (`course_id`),
  CONSTRAINT `luffyapi_coursedetail_course_id_69d83b91_fk_luffyapi_course_id` FOREIGN KEY (`course_id`) REFERENCES `luffyapi_course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_coursedetail` */

insert  into `luffyapi_coursedetail`(`id`,`why`,`course_id`) values 
(1,'想做程序员！',3),
(2,'吃饭睡觉打豆豆',5),
(3,'云就是未来',4);

/*Table structure for table `luffyapi_coursedetail_recommend_courses` */

DROP TABLE IF EXISTS `luffyapi_coursedetail_recommend_courses`;

CREATE TABLE `luffyapi_coursedetail_recommend_courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coursedetail_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `luffyapi_coursedetail_re_coursedetail_id_course_i_152ccaa2_uniq` (`coursedetail_id`,`course_id`),
  KEY `luffyapi_coursedetai_course_id_ba53ff75_fk_luffyapi_` (`course_id`),
  CONSTRAINT `luffyapi_coursedetai_course_id_ba53ff75_fk_luffyapi_` FOREIGN KEY (`course_id`) REFERENCES `luffyapi_course` (`id`),
  CONSTRAINT `luffyapi_coursedetai_coursedetail_id_3f35c4c1_fk_luffyapi_` FOREIGN KEY (`coursedetail_id`) REFERENCES `luffyapi_coursedetail` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_coursedetail_recommend_courses` */

insert  into `luffyapi_coursedetail_recommend_courses`(`id`,`coursedetail_id`,`course_id`) values 
(1,1,4),
(2,2,3),
(3,2,4),
(4,3,3),
(5,3,5);

/*Table structure for table `luffyapi_test` */

DROP TABLE IF EXISTS `luffyapi_test`;

CREATE TABLE `luffyapi_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(22) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_test` */

/*Table structure for table `luffyapi_test2` */

DROP TABLE IF EXISTS `luffyapi_test2`;

CREATE TABLE `luffyapi_test2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_test2` */

/*Table structure for table `luffyapi_test2_test` */

DROP TABLE IF EXISTS `luffyapi_test2_test`;

CREATE TABLE `luffyapi_test2_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test2_id` int(11) NOT NULL,
  `test_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `luffyapi_test2_test_test2_id_test_id_5173bcf0_uniq` (`test2_id`,`test_id`),
  KEY `luffyapi_test2_test_test_id_e17e3d7a_fk_luffyapi_test_id` (`test_id`),
  CONSTRAINT `luffyapi_test2_test_test2_id_68302509_fk_luffyapi_test2_id` FOREIGN KEY (`test2_id`) REFERENCES `luffyapi_test2` (`id`),
  CONSTRAINT `luffyapi_test2_test_test_id_e17e3d7a_fk_luffyapi_test_id` FOREIGN KEY (`test_id`) REFERENCES `luffyapi_test` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_test2_test` */

/*Table structure for table `luffyapi_userinfo` */

DROP TABLE IF EXISTS `luffyapi_userinfo`;

CREATE TABLE `luffyapi_userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(64) NOT NULL,
  `pwd` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_userinfo` */

insert  into `luffyapi_userinfo`(`id`,`user`,`pwd`) values 
(1,'alex','123456'),
(2,'egon','123456');

/*Table structure for table `luffyapi_usertoken` */

DROP TABLE IF EXISTS `luffyapi_usertoken`;

CREATE TABLE `luffyapi_usertoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(128) NOT NULL,
  `expired` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `luffyapi_usertoken_user_id_dc7819b1_fk_luffyapi_userinfo_id` FOREIGN KEY (`user_id`) REFERENCES `luffyapi_userinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `luffyapi_usertoken` */

insert  into `luffyapi_usertoken`(`id`,`token`,`expired`,`user_id`) values 
(1,'43cf89b3-4153-4c64-a7d7-38da7eeff919','2019-01-10 09:27:04.752135',2),
(2,'11f44d39-3ad0-4ed9-a43f-1d3bd2fe1eac','2019-01-10 09:28:04.974485',1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
