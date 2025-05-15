CREATE SCHEMA `movie_manager`;
USE `movie_manager`;

CREATE TABLE IF NOT EXISTS `genre` (
    `genre_id` VARCHAR(45) NOT NULL,
    `genre_name` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`genre_id`)
);

CREATE TABLE IF NOT EXISTS `studio` (
    `studio_id` VARCHAR(45) NOT NULL,
    `studio_name` VARCHAR(100) NOT NULL,
    `founded_year` YEAR,
    PRIMARY KEY (`studio_id`)
);

CREATE TABLE IF NOT EXISTS `movie` (
    `movie_id` VARCHAR(15) NOT NULL,
    `movie_name` VARCHAR(100) NOT NULL,
    `release_year` YEAR,
    `genre_id` VARCHAR(45) NOT NULL,
    `studio_id` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`movie_id`),
    FOREIGN KEY (`genre_id`) REFERENCES `genre`(`genre_id`),
    FOREIGN KEY (`studio_id`) REFERENCES `studio`(`studio_id`)
);


