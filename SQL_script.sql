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

INSERT INTO `genre` (`genre_id`, `genre_name`) VALUES 
('G001', 'Action'),
('G002', 'Drama'),
('G003', 'Sci-Fi'),
('G004', 'Comedy');

INSERT INTO `studio` (`studio_id`, `studio_name`, `founded_year`, `headquarters`) VALUES 
('S001', 'Warner Bros.', 1923, 'Burbank'),
('S002', 'Paramount Pictures', 1912, 'Hollywood'),
('S003', 'Marvel Studios', 1993, 'Burbank');

INSERT INTO `movie` (`movie_id`, `movie_name`, `release_year`, `genre_id`, `studio_id`) VALUES 
('M001', 'The Dark Knight', 2008, 'G001', 'S001'),
('M002', 'Inception', 2010, 'G003', 'S001'),
('M003', 'The Shawshank Redemption', 1994, 'G002', 'S002'),
('M004', 'Pulp Fiction', 1994, 'G002', 'S002'),
('M005', 'The Matrix', 1999, 'G003', 'S001'),
('M006', 'Forrest Gump', 1994, 'G002', 'S002'),
('M007', 'The Avengers', 2012, 'G001', 'S003'),
('M008', 'Jurassic Park', 1993, 'G003', 'S002'),
('M009', 'The Godfather', 1972, 'G002', 'S002'),
('M010', 'Black Panther', 2018, 'G001', 'S003');

# ('M011', 'La La Land', 2016, 'G004', 'S001');

SELECT 
	m.movie_id,
    m.movie_name,
    m.release_year,
    g.genre_name,
    s.studio_name
FROM 
    movie m
JOIN 
    genre g ON m.genre_id = g.genre_id
JOIN 
    studio s ON m.studio_id = s.studio_id
ORDER BY 
    m.movie_id;
    genre_id;
    
SELECT * FROM studio;

SELECT 
	m.movie_id,
    m.movie_name,
    m.release_year,
    g.genre_name,
    s.studio_name
FROM 
    movie m
JOIN 
    genre g ON m.genre_id = g.genre_id
JOIN 
    studio s ON m.studio_id = s.studio_id
ORDER BY 
    m.movie_id;genre_id;
    
    
SELECT 
    m.movie_id,
    m.movie_name,
    m.release_year,
    g.genre_id, 
    g.genre_name,
    s.studio_name,
    s.studio_id,
    s.founded_year,
    s.headquarters
FROM 
    movie m
JOIN 
    genre g ON m.genre_id = g.genre_id
JOIN 
    studio s ON m.studio_id = s.studio_id
WHERE 
    m.movie_id = 'M001' 
ORDER BY 
    m.movie_id;