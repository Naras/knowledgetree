/*
SQLyog Community Edition- MySQL GUI v8.12 
MySQL - 5.5.27 : Database - knowledgetree
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

DROP DATABASE IF EXISTS `knowledgetree`;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`knowledgetree` DEFAULT CHARACTER SET utf8;

USE `knowledgetree`;

/*Table structure for table `language` */

CREATE TABLE `language` (
  `id` char(10) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `UnicodeBlock` mediumint(9) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Langauges for the works, commentaries etc';

/*Data for the table `language` */

insert  into `language`(`id`,`Name`,`UnicodeBlock`) values ('aSSAmi','aSSAmi',21),('bengAli','bengAli',21),('English','English',2),('gujarAthi','gujarAthi',23),('hindi','hindi',20),('kannaDa','KannaDa',27),('kashmIri','kashmIri',185),('malayALam','malayALam',28),('mANipuri','mANipuri',136),('marATHi','marATHi',20),('oDiyA','oDiyA',24),('punjAbi','punJabi',22),('Samskrth','Samskrth',20),('tamiL','tamiL',25),('telugu','telugu',26),('urdu','urdu',19);

/*Table structure for table `script` */

CREATE TABLE `script` (
  `id` char(10) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `UnicodeBlock` mediumint(9) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Scripts for the works, commentaries etc';

/*Data for the table `script` */

insert  into `script`(`id`,`Name`,`UnicodeBlock`) values ('bengAli','bengAli',21),('brAhmi','brAhmi',181),('devanAgari','devanAgari',20),('granTHa','granTHa',NULL),('gujarAthi','gujarAthi',23),('gurmukhi','gurmukhi',22),('kannaDa','kannADa',27),('malayALam','malayALam',28),('oDiyA','oDiyA',24),('shArada','shArada',185),('tamiL','tamiL',25),('telugu','telugu',26);

/*Table structure for table `subject` */

CREATE TABLE `subject` (
  `id` char(10) NOT NULL,
  `Name` char(30) NOT NULL,
  `Description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `subject` */

insert  into `subject`(`id`,`Name`,`Description`) values ('Aitreya','Aitreya','Aitreyopanishad  \"The Microcosm of Man\"'),('AraNyaka','AraNyaka',' \"wilderness texts\" or \"forest treaties\"'),('aum','औं','औं - The Primary Sound'),('AV','aTHarvaNa Veda','aTHarvaNa Veda'),('Ayurveda','Ayurveda','Indian Medical Systems'),('BrahadAraN','BrahadAraNyaka','the big forest treatise'),('BrahmaNa','BrahmaNa','Prose commentaries on Samhitas'),('Chandas','Chandas','Metre'),('Chandogya','Chandogya','Chandogyopanishad \"Song and Sacrifice\"'),('Dhanurveda','Dhanurveda','Archery'),('Gandharvav','Gandharva veda','Sacred Music and Dance'),('Isa','Isa','Isopanishad \"The Inner Ruler\"'),('Jyotisha','Jyotisha','Astronomy/Astrology/Cosmology'),('Kalpa','Kalpa','Ritual'),('Katha','Katha','Kathopanishad \"Death as Teacher\"'),('Kena','Kena','Kenopanishad \"Who moves the world?\"'),('mAndukya','mAndukya','mAndukyopanishad \"Consciousness and its phases\"'),('Mundaka','Mundaka','Mundakopanoishad  \"Two modes of Knowing\"'),('Nirukta','Nirukta','Etymology'),('Poorva','Poorva Mimamsa','Darshana -  Glimpse of Divinity'),('Prasna','Prasna','Prasnopanishad  \"The Breath of Life\"'),('RV','Rk Veda','Rk Veda'),('Samhita','Samhita','Collection of metric texts'),('Samkhya','Samkhya','Darshana -  Glimpse of Divinity'),('ShastrashA','ShastrashAstra','Military Knowledge'),('Shiksha','Shiksha','Phonetics'),('ShilpashAs','Shilpa shAstra',NULL),('Sthapatyav','Sthapatyaveda','Architecture (temples)'),('SV','sAma Veda','sAma Veda'),('TaittirIya','TaittirIya','Taittiriyopanishad  \"From Food to Joy\"'),('Upanishad','Upanishad','Fundamental philosophy'),('Upaveda','Upaveda','Subsidiary vedas \"applied knowledge\"'),('Uttara','Uttara Mimamsa','Darshana -  Glimpse of Divinity'),('Vaishesh','Nyaya Vaisheshika','Darshana'),('Veda','Veda','Veda'),('Vedanga','Vedanga','Angas (limbs) of Vedas'),('Vedantha','Vedantha','Darshana -  \"End of the vedas\" - sum of all knowledge'),('VyAkaraNa','VyAkaraNa','Grammar'),('Yoga','Yoga','Darshana -  Glimpse of Divinity'),('YV','Yajur Veda','Yajur Veda');

/*Table structure for table `subject_has_work` */

CREATE TABLE `subject_has_work` (
  `Subject_id` char(10) NOT NULL,
  `Work_id` char(10) NOT NULL,
  PRIMARY KEY (`Subject_id`,`Work_id`),
  KEY `fk_Subject_has_Work_Subject` (`Subject_id`),
  KEY `fk_Subject_has_Work_Work` (`Work_id`),
  CONSTRAINT `fk_Subject_has_Work_Subject` FOREIGN KEY (`Subject_id`) REFERENCES `subject` (`id`) ON DELETE NO ACTION ON UPDATE  CASCADE,
  CONSTRAINT `fk_Subject_has_Work_Work` FOREIGN KEY (`Work_id`) REFERENCES `work` (`id`) ON DELETE NO ACTION ON UPDATE  CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `subject_has_work` */

insert  into `subject_has_work`(`Subject_id`,`Work_id`) values ('RV','BhagavadGi'),('Samkhya','BhagavadGi'),('Vaishesh','ShriBhashy'),('Veda','BhagavadGi'),('VyAkaraNa','ShriBhashy'),('Yoga','BhagavadGi'),('Yoga','ShriBhashy');

/*Table structure for table `subject_subject_relation` */

CREATE TABLE `subject_subject_relation` (
  `id` char(10) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `subject_subject_relation` */

insert  into `subject_subject_relation`(`id`,`Name`,`Description`) values ('darshana','Darshana','Glimpse of Divinity'),('parentchil','Avayavi','Avayava-Avayavi Bhava (Parent/Child Relation)'),('part','Anga','Anga - Angi Bhava (Part-Whole relation)'),('shruthi','shruthi','Revealed texts - direct perception by Rishis'),('sibling','Common Parent','The two subjects are related by a common parent subject'),('smrithi','smrithi','Remembered texts - Memorized and transmitted by students'),('upa','Upaveda','Subsidiary branches of Vedas'),('upani','Upanishad','Description of Vedas');

/*Table structure for table `subject_relatesto_subject` */

CREATE TABLE `subject_relatesto_subject` (
  `Subject1` char(10) NOT NULL,
  `Subject2` char(10) NOT NULL,
  `Relations_id` char(10) DEFAULT NULL,
  PRIMARY KEY (`Subject1`,`Subject2`),
  KEY `fk_Subject_has_Subject_Subject` (`Subject1`),
  KEY `fk_Subject_has_Subject_Subject1` (`Subject2`),
  KEY `fk_Subject_RelatesTo_Subject_Relations` (`Relations_id`),
  CONSTRAINT `fk_Subject_has_Subject_Subject` FOREIGN KEY (`Subject1`) REFERENCES `subject` (`id`) ON DELETE NO ACTION ON UPDATE  CASCADE,
  CONSTRAINT `fk_Subject_has_Subject_Subject1` FOREIGN KEY (`Subject2`) REFERENCES `subject` (`id`) ON DELETE NO ACTION ON UPDATE  CASCADE,
  CONSTRAINT `fk_Subject_RelatesTo_Subject_Relations` FOREIGN KEY (`Relations_id`) REFERENCES `subject_subject_relation` (`id`) ON DELETE NO ACTION ON UPDATE  CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `subject_relatesto_subject` */

insert  into `subject_relatesto_subject`(`Subject1`,`Subject2`,`Relations_id`) values ('Veda','Poorva','darshana'),('Veda','Samkhya','darshana'),('Veda','Uttara','darshana'),('Veda','Vaishesh','darshana'),('Veda','Vedantha','darshana'),('Veda','Yoga','darshana'),('aum','Veda','parentchil'),('Chandas','BrahmaNa','parentchil'),('Chandas','Samhita','parentchil'),('Upanishad','AranyaKa','parentchil'),('Upanishad','BrahadAraN','parentchil'),('Upanishad','Isa','parentchil'),('Upanishad','Kena','parentchil'),('Upanishad','mAndukya','parentchil'),('Upanishad','Mundaka','parentchil'),('Upanishad','Prasna','parentchil'),('Veda','AV','parentchil'),('Veda','RV','parentchil'),('Veda','SV','parentchil'),('Veda','YV','parentchil'),('Veda','Chandas','part'),('Veda','Jyotisha','part'),('Veda','Kalpa','part'),('Veda','Nirukta','part'),('Veda','Shiksha','part'),('Veda','VyakaraNa','part'),('Veda','Ayurveda','upa'),('Veda','Dhanurveda','upa'),('Veda','Gandharvav','upa'),('Veda','UpaVeda','upa'),('Veda','Upanishad','upani');

/*Table structure for table `work` */

CREATE TABLE `work` (
  `id` char(10) NOT NULL,
  `Title` varchar(45) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `work` */

insert  into `work`(`id`,`Title`,`Description`) values ('BhagavadGi','Bhagavad Geetha','The Song Celestial by Lord KrishNa'),('ShriBhashy','Shree Bhashyam',"Shree rAmAnuja's Comprehensive Treatise on Brahman"),('SiddhataKa','Siddhata Kaumudi','A Kaumudi on Siddhatas :-)'),('VivekChood','Viveka ChoodAmaNi','The Source of Spiritual Wisdom');

/*Table structure for table `work_in_language` */


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_in_language`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_in_language` (
  `work_id` CHAR(10) NOT NULL ,
  `language_id` CHAR(10) NOT NULL ,
  `location` VARCHAR(255) NULL COMMENT 'URL of the document physical location' ,
  PRIMARY KEY (`work_id`, `language_id`) ,
  INDEX `fk_work_has_language_work` (`work_id` ASC) ,
  INDEX `fk_work_has_language_language` (`language_id` ASC) ,
  CONSTRAINT `fk_work_has_language_work`
    FOREIGN KEY (`work_id` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE NO ACTION
    ON UPDATE  CASCADE,
  CONSTRAINT `fk_work_has_language_language`
    FOREIGN KEY (`language_id` )
    REFERENCES `knowledgetree`.`language` (`id` )
    ON DELETE NO ACTION
    ON UPDATE  CASCADE);


/*Data for the table `work_in_language` */

insert  into `work_in_language`(`work_id`,`language_id`) values ('BhagavadGi','English'),('BhagavadGi','kannaDa'),('BhagavadGi','Samskrth'),('ShriBhashy','Samskrth'),('ShriBhashy','tamiL'),('SiddhataKa','Samskrth'),('VivekChood','Samskrth');

-- -----------------------------------------------------
-- Table `knowledgetree`.`work_in_script`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_in_script` (
  `work_id` CHAR(10) NOT NULL ,
  `script_id` CHAR(10) NOT NULL ,
  `location` VARCHAR(255) NULL COMMENT 'URL of the document physical location' ,
  PRIMARY KEY (`work_id`, `script_id`) ,
  INDEX `fk_work_has_script_work` (`work_id` ASC) ,
  INDEX `fk_work_has_script_script` (`script_id` ASC) ,
  CONSTRAINT `fk_work_has_script_work`
    FOREIGN KEY (`work_id` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE NO ACTION
    ON UPDATE  CASCADE,
  CONSTRAINT `fk_work_has_script_script`
    FOREIGN KEY (`script_id` )
    REFERENCES `knowledgetree`.`script` (`id` )
    ON DELETE NO ACTION
    ON UPDATE  CASCADE);

/*Data for the table `work_in_script` */

insert  into `work_in_script`(`work_id`,`script_id`) values ('BhagavadGi','devanAgari'),('BhagavadGi','granTHa'),('BhagavadGi','kannaDa'),('ShriBhashy','devanAgari'),('ShriBhashy','shArada'),('SiddhataKa','devanAgari'),('VivekChood','devanAgari');

/*Table structure for table `work_subject_relation` */

CREATE TABLE `work_subject_relation` (
  `id` char(10) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `work_subject_relation` */

insert  into `work_subject_relation`(`id`,`Name`,`Description`) values ('comcom','Commentary on Commentary','Secondary commentary'),('commentary','Commentary','Commentary on subject'),('compile','Compilation','Compilation of other works'),('original','Original Work','Original Work on subject'),('subcomment','Sub-commentary','Sub-commentary on subject'),('translate','Traslation','Translation of another work'),('treatise','Treatise','Treatise on subject'),('vritthi','Vritthi','ವೃತ್ತಿ ಅಂದರೆ ?');

/*Table structure for table `subject_work_have_relation` */

CREATE TABLE `subject_work_have_relation` (
  `Subject_id` char(10) NOT NULL,
  `Work_id` char(10) NOT NULL,
  `work_subject_relation` char(10) NOT NULL,
  PRIMARY KEY (`Subject_id`,`Work_id`,`work_subject_relation`),
  KEY `fk_subject_work_relation_1` (`Subject_id`,`Work_id`),
  KEY `fk_subject_work_relation_2` (`work_subject_relation`),
  CONSTRAINT `fk_subject_work_relation_1` FOREIGN KEY (`Subject_id`, `Work_id`) REFERENCES `subject_has_work` (`Subject_id`, `Work_id`) ON DELETE NO ACTION ON UPDATE  CASCADE,
  CONSTRAINT `fk_subject_work_relation_2` FOREIGN KEY (`work_subject_relation`) REFERENCES `work_subject_relation` (`id`) ON DELETE NO ACTION ON UPDATE  CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='A subject (like Rg Veda) has a relation with a work (like Bhagavad Geetha) ';

/*Data for the table `subject_work_have_relation` */

insert  into `subject_work_have_relation`(`Subject_id`,`Work_id`,`work_subject_relation`) values ('Vaishesh','ShriBhashy','commentary'),('Yoga','ShriBhashy','commentary'),('Vaishesh','ShriBhashy','treatise'),('VyAkaraNa','ShriBhashy','treatise'),('Yoga','BhagavadGi','treatise');

/*View structure for view view_subject_subject */

CREATE VIEW `view_subject_subject` AS 
select
  `s1`.`id`           AS `sub1Id`,
  `s1`.`Name`         AS `subject1`,
  `s1`.`Description`  AS `subject1Description`,
  `s2`.`id`           AS `sub2Id`,
  `s2`.`Name`         AS `subject2`,
  `s2`.`Description`  AS `subject2Description`,
  `ssr`.`Name`        AS `relation`,
  `ssr`.`Description` AS `relation_description`
from (((`subject` `s1`
     join `subject` `s2`)
    join `subject_relatesto_subject` `srs`)
   join `subject_subject_relation` `ssr`)
where ((`s1`.`id` = `srs`.`Subject1`)
            and (`s2`.`id` = `srs`.`Subject2`)
            and (`srs`.`Relations_id` = `ssr`.`id`));

/*View structure for view view_subject_work */

CREATE VIEW `view_subject_work`
AS
   SELECT `s`.`Name` AS `Subject`,
          `w`.`Title` AS `Work`,
          `wsr`.`Name` AS `Relation`
     FROM ((((`subject` `s` JOIN `work` `w`)
             JOIN `subject_has_work` `sw`)
            JOIN `subject_work_have_relation` `swr`)
           JOIN `work_subject_relation` `wsr`)
    WHERE (    (`s`.`id` = `sw`.`Subject_id`)
           AND (`w`.`id` = `sw`.`Work_id`)
           AND (`swr`.`Subject_id` = `sw`.`Subject_id`)
           AND (`swr`.`Work_id` = `sw`.`Work_id`)
           AND (`swr`.`work_subject_relation` = `wsr`.`id`));
		 
		 

/*View structure for view view_subject_subject */

CREATE VIEW `view_subject_subject` AS 
select
  `s1`.`id`           AS `sub1Id`,
  `s1`.`Name`         AS `subject1`,
  `s1`.`Description`  AS `subject1Description`,
  `s2`.`id`           AS `sub2Id`,
  `s2`.`Name`         AS `subject2`,
  `s2`.`Description`  AS `subject2Description`,
  `ssr`.`Name`        AS `relation`,
  `ssr`.`Description` AS `relation_description`
from (((`subject` `s1`
     join `subject` `s2`)
    join `subject_relatesto_subject` `srs`)
   join `subject_subject_relation` `ssr`)
where ((`s1`.`id` = `srs`.`Subject1`)
            and (`s2`.`id` = `srs`.`Subject2`)
            and (`srs`.`Relations_id` = `ssr`.`id`));

/*View structure for view view_subject_work */

CREATE VIEW `view_subject_work`
AS
   SELECT `s`.`Name` AS `Subject`,
          `w`.`Title` AS `Work`,
          `wsr`.`Name` AS `Relation`
     FROM (((`subject` `s` JOIN `work` `w`)
             JOIN `subject_has_work` `sw`)
           JOIN `work_subject_relation` `wsr`)
    WHERE (    (`s`.`id` = `sw`.`Subject_id`)
           AND (`w`.`id` = `sw`.`Work_id`)
           AND (`sw`.`work_subject_relation` = `wsr`.`id`)
           );

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
