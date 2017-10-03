SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF  EXISTS `knowledgetree` ;
CREATE SCHEMA `knowledgetree` DEFAULT CHARACTER SET utf8 ;
USE `knowledgetree`;

-- -----------------------------------------------------
-- Table `knowledgetree`.`country`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`country` (
  `id` CHAR(10) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`state`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`state` (
  `id` CHAR(10) NOT NULL ,
  `Country_id` CHAR(10) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`, `Country_id`) ,
  INDEX `fk_State_Country` (`Country_id` ASC) ,
  CONSTRAINT `fk_State_Country`
    FOREIGN KEY (`Country_id` )
    REFERENCES `knowledgetree`.`country` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`city`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`city` (
  `id` CHAR(10) NOT NULL ,
  `State_id` CHAR(10) NOT NULL ,
  `Country_id` CHAR(10) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`, `State_id`, `Country_id`) ,
  INDEX `fk_City_State` (`State_id` ASC, `Country_id` ASC) ,
  CONSTRAINT `fk_City_State`
    FOREIGN KEY (`State_id` , `Country_id` )
    REFERENCES `knowledgetree`.`state` (`id` , `Country_id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`district`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`district` (
  `id` CHAR(10) NOT NULL ,
  `State_id` CHAR(10) NOT NULL ,
  `Country_id` CHAR(10) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`, `State_id`, `Country_id`) ,
  INDEX `fk_District_State` (`State_id` ASC, `Country_id` ASC) ,
  CONSTRAINT `fk_District_State`
    FOREIGN KEY (`State_id` , `Country_id` )
    REFERENCES `knowledgetree`.`state` (`id` , `Country_id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`person`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person` (
  `id` CHAR(20) NOT NULL ,
  `First` CHAR(30) NULL DEFAULT NULL ,
  `Middle` CHAR(30) NULL DEFAULT NULL ,
  `Last` CHAR(30) NULL DEFAULT NULL ,
  `Initials` CHAR(10) NULL DEFAULT NULL ,
  `Nick` CHAR(20) NULL DEFAULT NULL ,
  `Other` CHAR(30) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Persons';


-- -----------------------------------------------------
-- Table `knowledgetree`.`address`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`address` (
  `id` CHAR(20) NOT NULL ,
  `Value` VARCHAR(500) NULL DEFAULT NULL ,
  `HouseNumber` CHAR(30) NULL DEFAULT NULL ,
  `Street` CHAR(30) NULL DEFAULT NULL ,
  `Area` CHAR(30) NULL DEFAULT NULL ,
  `City_id` CHAR(10) NULL DEFAULT NULL ,
  `City_State_id` CHAR(10) NULL DEFAULT NULL ,
  `City_Country_id` CHAR(10) NULL DEFAULT NULL ,
  `District_id` CHAR(10) NULL DEFAULT NULL ,
  `District_State_id` CHAR(10) NULL DEFAULT NULL ,
  `District_Country_id` CHAR(10) NULL DEFAULT NULL ,
  `Person` CHAR(20) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Address_City` (`City_id` ASC, `City_State_id` ASC, `City_Country_id` ASC) ,
  INDEX `fk_Address_District` (`District_id` ASC, `District_State_id` ASC, `District_Country_id` ASC) ,
  INDEX `fk_Address_Person` (`Person` ASC) ,
  CONSTRAINT `fk_Address_City`
    FOREIGN KEY (`City_id` , `City_State_id` , `City_Country_id` )
    REFERENCES `knowledgetree`.`city` (`id` , `State_id` , `Country_id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Address_District`
    FOREIGN KEY (`District_id` , `District_State_id` , `District_Country_id` )
    REFERENCES `knowledgetree`.`district` (`id` , `State_id` , `Country_id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Address_Person`
    FOREIGN KEY (`Person` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`language`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`language` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Langauges for the works, commentaries etc';


-- -----------------------------------------------------
-- Table `knowledgetree`.`affiliation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`affiliation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'An institution that a person is affiliated with';


-- -----------------------------------------------------
-- Table `knowledgetree`.`personlife`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`personlife` (
  `id` CHAR(10) NOT NULL ,
  `Living` BOOLEAN NULL DEFAULT TRUE ,
  `Birth` DATE NULL DEFAULT NULL ,
  `Death` DATE NULL DEFAULT NULL ,
  `Period` CHAR(25) NULL DEFAULT NULL ,
  `History` VARCHAR(255) NULL DEFAULT NULL ,
  `Life` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_PersonLife_Person` (`id` ASC) ,
  CONSTRAINT `fk_PersonLife_Person`
    FOREIGN KEY (`id` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'The life of a person. May be a historical, fictional or even a mytholgical person';


-- -----------------------------------------------------
-- Table `knowledgetree`.`role`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`role` (
  `id` CHAR(20) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'A person can be an Author, Scholar, Reviewer etc';


-- -----------------------------------------------------
-- Table `knowledgetree`.`script`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`script` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Scripts for the works, commentaries etc';


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject` (
  `id` CHAR(20) NOT NULL ,
  `Name` CHAR(30) NOT NULL ,
  `Description` VARCHAR(5000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`work`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(45) NULL DEFAULT NULL ,
  `Description` VARCHAR(5000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_subject_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_subject_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(45) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject_has_work`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject_has_work` (
  `Subject` CHAR(20) NOT NULL ,
  `Work` CHAR(20) NOT NULL ,
  `Relation` CHAR(20) NOT NULL ,
  PRIMARY KEY (`Subject`, `Work`, `Relation`) ,
  INDEX `fk_Subject_has_Work_Subject` (`Subject` ASC) ,
  INDEX `fk_Subject_has_Work_Work` (`Work` ASC) ,
  INDEX `fk_subject_has_work_work_subject_relation` (`Relation` ASC) ,
  CONSTRAINT `fk_Subject_has_Work_Subject`
    FOREIGN KEY (`Subject` )
    REFERENCES `knowledgetree`.`subject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Subject_has_Work_Work`
    FOREIGN KEY (`Work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_subject_has_work_work_subject_relation`
    FOREIGN KEY (`Relation` )
    REFERENCES `knowledgetree`.`work_subject_relation` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject_subject_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject_subject_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject_relatesto_subject`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject_relatesto_subject` (
  `Subject1` CHAR(20) NOT NULL ,
  `Subject2` CHAR(20) NOT NULL ,
  `Relation` CHAR(20) NULL DEFAULT NULL ,
  `Sortorder` SMALLINT NULL COMMENT 'Each subject2 has a sequence in its relation to subject1 (1,2,3). Used for sorting the subtree.' ,
  PRIMARY KEY (`Subject1`, `Subject2`) ,
  INDEX `fk_subject_has_subject_subject` (`Subject1` ASC) ,
  INDEX `fk_subject_has_subject_subject1` (`Subject2` ASC) ,
  INDEX `fk_subject_relatesto_subject_subject_subject_relation` (`Relation` ASC) ,
  CONSTRAINT `fk_subject_has_subject_subject`
    FOREIGN KEY (`Subject1` )
    REFERENCES `knowledgetree`.`subject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_subject_has_subject_subject1`
    FOREIGN KEY (`Subject2` )
    REFERENCES `knowledgetree`.`subject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_subject_relatesto_subject_subject_subject_relation`
    FOREIGN KEY (`Relation` )
    REFERENCES `knowledgetree`.`subject_subject_relation` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`tag`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`tag` (
  `id` VARCHAR(255) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  `BelongsTo` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Tag_Tag` (`BelongsTo` ASC) ,
  CONSTRAINT `fk_Tag_Tag`
    FOREIGN KEY (`BelongsTo` )
    REFERENCES `knowledgetree`.`tag` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Tags are additional metadata. They can be used in search and filter for subjects, works and persons. They can be managed by a Metadata Manager';


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_has_affiliation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_has_affiliation` (
  `person` CHAR(20) NOT NULL ,
  `affiliation` CHAR(20) NOT NULL ,
  PRIMARY KEY (`person`, `affiliation`) ,
  INDEX `fk_person_has_Affiliation_person` (`person` ASC) ,
  INDEX `fk_person_has_Affiliation_Affiliation` (`affiliation` ASC) ,
  CONSTRAINT `fk_person_has_Affiliation_person`
    FOREIGN KEY (`person` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_person_has_Affiliation_Affiliation`
    FOREIGN KEY (`affiliation` )
    REFERENCES `knowledgetree`.`affiliation` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_in_language`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_in_language` (
  `Work` CHAR(20) NOT NULL ,
  `Language` CHAR(20) NOT NULL ,
  `Location` VARCHAR(255) NULL COMMENT 'Physical location URL' ,
  PRIMARY KEY (`Work`, `Language`) ,
  INDEX `fk_work_has_language_work` (`Work` ASC) ,
  INDEX `fk_work_has_language_language` (`Language` ASC) ,
  CONSTRAINT `fk_work_has_language_work`
    FOREIGN KEY (`Work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_work_has_language_language`
    FOREIGN KEY (`Language` )
    REFERENCES `knowledgetree`.`language` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_in_script`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_in_script` (
  `Work` CHAR(20) NOT NULL ,
  `Script` CHAR(20) NOT NULL ,
  `Location` VARCHAR(255) NULL COMMENT 'Physical location URL' ,
  PRIMARY KEY (`Work`, `Script`) ,
  INDEX `fk_work_has_script_work` (`Work` ASC) ,
  INDEX `fk_work_has_script_script` (`Script` ASC) ,
  CONSTRAINT `fk_work_has_script_work`
    FOREIGN KEY (`Work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_work_has_script_script`
    FOREIGN KEY (`Script` )
    REFERENCES `knowledgetree`.`script` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`tagSubject`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`tagSubject` (
  `id` VARCHAR(255) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  `BelongsTo` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_TagSubject_TagSubject` (`BelongsTo` ASC) ,
  CONSTRAINT `fk_TagSubject_TagSubject`
    FOREIGN KEY (`BelongsTo` )
    REFERENCES `knowledgetree`.`tagSubject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Tags are additional metadata. They can be used in search and filter for subjects, works and persons. They can be managed by a Metadata Manager';


-- -----------------------------------------------------
-- Table `knowledgetree`.`tagWork`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`tagWork` (
  `id` VARCHAR(255) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  `BelongsTo` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_TagWork_TagWork` (`BelongsTo` ASC) ,
  CONSTRAINT `fk_TagWork_TagWork`
    FOREIGN KEY (`BelongsTo` )
    REFERENCES `knowledgetree`.`tagWork` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Tags are additional metadata. They can be used in search and filter for subjects, works and persons. They can be managed by a Metadata Manager';


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject_has_tag`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject_has_tag` (
  `subject` CHAR(20) NOT NULL ,
  `tag` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`subject`, `tag`) ,
  INDEX `fk_subject_has_tagSubject_subject` (`subject` ASC) ,
  INDEX `fk_subject_has_tagSubject_tagSubject` (`tag` ASC) ,
  CONSTRAINT `fk_subject_has_tagSubject_subject`
    FOREIGN KEY (`subject` )
    REFERENCES `knowledgetree`.`subject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_subject_has_tagSubject_tagSubject`
    FOREIGN KEY (`tag` )
    REFERENCES `knowledgetree`.`tagSubject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_has_tag`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_has_tag` (
  `work` CHAR(20) NOT NULL ,
  `tag` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`work`, `tag`) ,
  INDEX `fk_work_has_tagWork_work` (`work` ASC) ,
  INDEX `fk_work_has_tagWork_tagWork` (`tag` ASC) ,
  CONSTRAINT `fk_work_has_tagWork_work`
    FOREIGN KEY (`work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_work_has_tagWork_tagWork`
    FOREIGN KEY (`tag` )
    REFERENCES `knowledgetree`.`tagWork` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_has_role`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_has_role` (
  `person` CHAR(20) NOT NULL ,
  `role` CHAR(20) NOT NULL ,
  PRIMARY KEY (`person`, `role`) ,
  INDEX `fk_person_has_role_person` (`person` ASC) ,
  INDEX `fk_person_has_role_role` (`role` ASC) ,
  CONSTRAINT `fk_person_has_role_person`
    FOREIGN KEY (`person` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_person_has_role_role`
    FOREIGN KEY (`role` )
    REFERENCES `knowledgetree`.`role` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_work_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_work_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_relatesto_work`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_relatesto_work` (
  `Work1` CHAR(20) NOT NULL ,
  `Work2` CHAR(20) NOT NULL ,
  `Relation` CHAR(20) NULL ,
  `Sortorder` SMALLINT NULL ,
  PRIMARY KEY (`Work1`, `Work2`) ,
  INDEX `fk_work_has_work_work` (`Work1` ASC) ,
  INDEX `fk_work_has_work_work1` (`Work2` ASC) ,
  INDEX `fk_work_has_work_work_work_relation` (`Relation` ASC) ,
  CONSTRAINT `fk_work_has_work_work`
    FOREIGN KEY (`Work1` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_work_has_work_work1`
    FOREIGN KEY (`Work2` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_work_has_work_work_work_relation`
    FOREIGN KEY (`Relation` )
    REFERENCES `knowledgetree`.`work_work_relation` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_person_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_person_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_relatesto_person`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_relatesto_person` (
  `person1` CHAR(20) NOT NULL ,
  `person2` CHAR(20) NOT NULL ,
  `relation` CHAR(20) NOT NULL ,
  PRIMARY KEY (`person1`, `person2`, `relation`) ,
  INDEX `fk_person_has_person_person` (`person1` ASC) ,
  INDEX `fk_person_has_person_person1` (`person2` ASC) ,
  INDEX `fk_person_relatesto_person_person_person_relation` (`relation` ASC) ,
  CONSTRAINT `fk_person_has_person_person`
    FOREIGN KEY (`person1` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_person_has_person_person1`
    FOREIGN KEY (`person2` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_person_relatesto_person_person_person_relation`
    FOREIGN KEY (`relation` )
    REFERENCES `knowledgetree`.`person_person_relation` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_work_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_work_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(45) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_work_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_work_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(45) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_has_work`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_has_work` (
  `Person` CHAR(20) NOT NULL ,
  `Work` CHAR(20) NOT NULL ,
  `Relation` CHAR(20) NOT NULL ,
  PRIMARY KEY (`Person`, `Work`, `Relation`) ,
  INDEX `fk_person_has_work_person` (`Person` ASC) ,
  INDEX `fk_person_has_work_work` (`Work` ASC) ,
  INDEX `fk_person_has_work_relation` (`Relation` ASC) ,
  CONSTRAINT `fk_person_has_work_person`
    FOREIGN KEY (`Person` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_person_has_work_work`
    FOREIGN KEY (`Work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_person_has_work_relation`
    FOREIGN KEY (`Relation` )
    REFERENCES `knowledgetree`.`person_work_relation` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
