-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema ncga
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ncga
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ncga` DEFAULT CHARACTER SET utf8mb4 ;
USE `ncga` ;

-- -----------------------------------------------------
-- Table `ncga`.`bills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`bills` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `bill_id` VARCHAR(8) NOT NULL,
  `session` YEAR NOT NULL,
  `date_filed` DATE NULL,
  `title` VARCHAR(250) NULL DEFAULT NULL,
  `link` VARCHAR(150) NULL,
  `page_scraped` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1487
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `ncga`.`camp_doc_lu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`camp_doc_lu` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `committee` VARCHAR(128) NOT NULL,
  `report_year` YEAR NOT NULL,
  `report_type` ENUM('24-Hour Electioneering Communications', '48-Hour', 'Annual', 'Audit Letter', 'Campaign Reporter', 'Candidate Designation of Committee Funds', 'Candidate Specific Communications', 'Certification of Inactive Status', 'Certification of Incorporated Political Committee', 'Certification of Return to Active Status', 'Certification of Threshold', 'Certification of Treasurer', 'Certification to Close Committee', 'Contribution from a Business Account Statement', 'Correspondence Returned Undeliverable or Unclaimed', 'Declaration of Intent', 'Deferred Notice', 'District Attorney Letter', 'Electioneering Communications Report', 'Federal Mid Year', 'Federal Year End', 'Final', 'First Quarter', 'Forgiven Loan Statement', 'Fourth Quarter', 'Independent Expenditure Political Committee Certification', 'Independent Expenditure Report', 'Independent Expenditure for Registered Committees', 'Independent Expenditure for non-Committees', 'Interim', 'Judicial Qualifying Contributions Report', 'Loan Proceeds Statement', 'Mid Year Semi-Annual', 'Miscellaneous Correspondence', 'Monthly', 'Municipal Voter-Owned Election Qualifying Contributions', 'Non-Compliance Letter', 'Non-Participating Candidate', 'Notice of Candidacy', 'Notice of Termination of Active Status', 'Notification of Change to Reporting Schedule', 'Organizational', 'Other', 'Paid Penalty Assessment or Forfeiture', 'Penalty Appeal', 'Penalty Appeal Decision', 'Penalty Assessment', 'Penalty Assessment Letter', 'Penalty Resolution Agreement Executed', 'Penalty Resolution Agreement Proposal', 'Penalty Waiver Letter', 'Political Party Executive Committee Exempt Sales Plan', 'Post General', 'Post Primary', 'Pre-Election', 'Pre-Primary', 'Pre-Referendum', 'Pre-Runoff', 'Rescind Letter', 'Second Quarter', 'Signed Penalty Waiver Agreement', 'Special', 'Statement of Organization', 'Supplemental Final', 'Ten-day', 'Third Quarter', 'Thirty-day', 'Thirty-five-day', 'Twelve-day', 'Voter-Owned Election Qualifying Contributions', 'Weekly', 'Year End Semi-Annual', 'Penalty Assessment - 30 Days Aged') NULL DEFAULT NULL,
  `amend` TINYINT(1) NULL DEFAULT NULL,
  `rec_date` DATE NULL DEFAULT NULL,
  `start_date` DATE NULL DEFAULT NULL,
  `end_date` DATE NULL DEFAULT NULL,
  `image_link` VARCHAR(128) NOT NULL,
  `data_link` VARCHAR(384) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 35051
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `ncga`.`members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`members` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(100) NULL,
  `ref_name` VARCHAR(45) NULL,
  `chamber` ENUM('H', 'S', 'O') NOT NULL,
  `userid` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ncga`.`bill_sponsor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`bill_sponsor` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `bill_id` INT NOT NULL,
  `member_id` INT NOT NULL,
  `stype` VARCHAR(20) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_bill_sponsor_bill`
    FOREIGN KEY (`bill_id`)
    REFERENCES `ncga`.`bills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bill_sponsor_sponsor`
    FOREIGN KEY (`member_id`)
    REFERENCES `ncga`.`members` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_bill_sponsor_bill_idx` ON `ncga`.`bill_sponsor` (`bill_id` ASC);

CREATE INDEX `fk_bill_sponsor_member_idx` ON `ncga`.`bill_sponsor` (`member_id` ASC);


-- -----------------------------------------------------
-- Table `ncga`.`bill_editions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`bill_editions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `bill_id` INT NOT NULL,
  `edition` VARCHAR(45) NOT NULL,
  `link` VARCHAR(300) NOT NULL,
  `page_scraped` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_bill_editions_bill`
    FOREIGN KEY (`bill_id`)
    REFERENCES `ncga`.`bills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_bill_editions_billid_idx` ON `ncga`.`bill_editions` (`bill_id` ASC);


-- -----------------------------------------------------
-- Table `ncga`.`keywords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`keywords` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `keyword` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ncga`.`bill_keywords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`bill_keywords` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `bill_id` INT NOT NULL,
  `keyword_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_bill_keywords_bill`
    FOREIGN KEY (`bill_id`)
    REFERENCES `ncga`.`bills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bill_keywords_keyword`
    FOREIGN KEY (`keyword_id`)
    REFERENCES `ncga`.`keywords` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_bill_keywords_bill_idx` ON `ncga`.`bill_keywords` (`bill_id` ASC);

CREATE INDEX `fk_bill_keywords_keyword_idx` ON `ncga`.`bill_keywords` (`keyword_id` ASC);


-- -----------------------------------------------------
-- Table `ncga`.`counties`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`counties` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ncga`.`statutes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`statutes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `statute` VARCHAR(45) NOT NULL,
  `stype` ENUM('Chapter', 'Section', 'NA') NULL DEFAULT 'NA',
  `link` VARCHAR(200) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ncga`.`bill_county`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`bill_county` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `bill_id` INT NOT NULL,
  `county_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_bill_county_bill`
    FOREIGN KEY (`bill_id`)
    REFERENCES `ncga`.`bills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bill_county_county`
    FOREIGN KEY (`county_id`)
    REFERENCES `ncga`.`counties` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_bill_county_bill_idx` ON `ncga`.`bill_county` (`bill_id` ASC);

CREATE INDEX `fk_bill_county_county_idx` ON `ncga`.`bill_county` (`county_id` ASC);


-- -----------------------------------------------------
-- Table `ncga`.`bill_statute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncga`.`bill_statute` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `bill_id` INT NOT NULL,
  `statute_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_bill_statute_bill`
    FOREIGN KEY (`bill_id`)
    REFERENCES `ncga`.`bills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bill_statute_statute`
    FOREIGN KEY (`statute_id`)
    REFERENCES `ncga`.`statutes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_bill_statute_bill_idx` ON `ncga`.`bill_statute` (`bill_id` ASC);

CREATE INDEX `fk_bill_statute_statute_idx` ON `ncga`.`bill_statute` (`statute_id` ASC);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
