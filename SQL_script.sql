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
    `headquarters` VARCHAR(100),
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

-- 1. Insert genres
INSERT INTO `genre` (`genre_id`, `genre_name`) VALUES 
('G001', 'Action'),
('G002', 'Drama'),
('G003', 'Sci-Fi');

-- 2. Insert studios
INSERT INTO `studio` (`studio_id`, `studio_name`, `founded_year`, `headquarters`) VALUES 
('S001', 'Warner Bros.', 1923, 'Burbank, California'),
('S002', 'Paramount Pictures', 1912, 'Hollywood, California'),
('S003', 'Marvel Studios', 1993, 'Burbank, California');

-- 3. Insert movies
INSERT INTO `movie` (`movie_id`, `movie_name`, `release_year`, `duration_minutes`, `description`, `genre_id`, `studio_id`) VALUES 
('M001', 'The Dark Knight', 2008, 152, 'Batman faces the Joker in Gotham City', 'G001', 'S001'),
('M002', 'Inception', 2010, 148, 'Dream-sharing technology heist', 'G003', 'S001'),
('M003', 'The Shawshank Redemption', 1994, 142, 'Two imprisoned men bond over the years', 'G002', 'S002');
