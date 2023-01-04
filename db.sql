-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema wishlist
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `wishlist` ;

-- -----------------------------------------------------
-- Schema wishlist
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `wishlist` DEFAULT CHARACTER SET utf8 ;
USE `wishlist` ;

-- -----------------------------------------------------
-- Table `wishlist`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `wishlist`.`wishlists`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist`.`wishlists` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(400) NOT NULL,
  `text` TEXT NULL,
  `privacy` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  `creator_id` INT NOT NULL,
  `creator_id` BLOB,
  PRIMARY KEY (`id`, `creator_id`),
    FOREIGN KEY (`creator_id`)
    REFERENCES `wishlist`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `wishlist`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(400) NOT NULL,
  `text` TEXT NULL,
  `url` VARCHAR(255) NOT NULL,
  `price` INT NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `creator_id` INT NOT NULL,
  PRIMARY KEY (`id`, `creator_id`),
    FOREIGN KEY (`creator_id`)
    REFERENCES `wishlist`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `wishlist`.`wishlist_likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist`.`wishlist_likes` (
  `user_id` INT NOT NULL,
  `wishlist_id` INT NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`)
    REFERENCES `wishlist`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`wishlist_id`)
    REFERENCES `wishlist`.`wishlists` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `wishlist`.`wishlist_products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist`.`wishlist_products` (
  `wishlist_id` INT NOT NULL,
  `wcreator_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `id` INT ZEROFILL NOT NULL,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`wishlist_id` , `wcreator_id`)
    REFERENCES `wishlist`.`wishlists` (`id` , `creator_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`product_id`)
    REFERENCES `wishlist`.`products` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `wishlist`.`product_likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wishlist`.`product_likes` (
  `user_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `creator_id` INT NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`)
    REFERENCES `wishlist`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`product_id` , `creator_id`)
    REFERENCES `wishlist`.`products` (`id` , `creator_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `wishlist`.`participants`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wishlist`.`participants` (
  `participant_id` INT NOT NULL,
  `wishlists_id` INT NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY  (`id`),
    FOREIGN KEY (`participant_id`)
    REFERENCES `wishlist`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`wishlists_id`)
    REFERENCES `wishlist`.`wishlists` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
