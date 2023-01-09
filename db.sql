-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema wishlist
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `wishlist2` ;

-- -----------------------------------------------------
-- Schema wishlist
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `wishlist2` DEFAULT CHARACTER SET utf8 ;
USE `wishlist2` ;

-- -----------------------------------------------------
-- Table `wishlist2`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist2`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `wishlist2`.`wishlists`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist2`.`wishlists` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(400) NOT NULL,
  `text` TEXT NULL,
  `privacy` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  `creator_id` INT NOT NULL,
  `img_url` VARCHAR(255),
  PRIMARY KEY (`id`),
    FOREIGN KEY (`creator_id`)
    REFERENCES `wishlist2`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `wishlist2`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist2`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(400) NOT NULL,
  `link` VARCHAR(400) NULL,
  `img_url` TEXT NOT NULL,
  `price` INT NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `creator_id` INT NOT NULL,
  `brand` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`, `creator_id`),
    FOREIGN KEY (`creator_id`)
    REFERENCES `wishlist2`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `wishlist2`.`wishlist_products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist2`.`wishlist_products` (
  `wishlist_id` INT NOT NULL,
  `wcreator_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `id` INT AUTO_INCREMENT NOT NULL,
  `status` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`wishlist_id` , `wcreator_id`)
    REFERENCES `wishlist2`.`wishlists` (`id` , `creator_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`product_id`)
    REFERENCES `wishlist2`.`products` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `wishlist2`.`participants`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wishlist2`.`participants` (
  `participant_id` INT NOT NULL,
  `wishlists_id` INT NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY  (`id`),
    FOREIGN KEY (`participant_id`)
    REFERENCES `wishlist2`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`wishlists_id`)
    REFERENCES `wishlist2`.`wishlists` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

  -- -----------------------------------------------------
-- Table `wishlist2`.`participant_purchases`
-- -----------------------------------------------------

  CREATE TABLE IF NOT EXISTS `participant_purchases` (
  `participant_id` int NOT NULL,
  `product_id` int NOT NULL,
  `wishlist_id` int NOT NULL,
  PRIMARY KEY (`participant_id`,`product_id`,`wishlist_id`),
    FOREIGN KEY (`participant_id`)
    REFERENCES `wishlist2`. `participants` (`participant_id`) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
    FOREIGN KEY (`product_id`) 
    REFERENCES `wishlist2`. `wishlist_products` (`product_id`) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
    FOREIGN KEY (`wishlist_id`) 
    REFERENCES `wishlist2`. `wishlists` (`id`) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

