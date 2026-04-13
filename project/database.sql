CREATE DATABASE traffic_db;

USE traffic_db;

CREATE TABLE predictionn (
    id INT AUTO_INCREMENT PRIMARY KEY,
    time INT,
    day INT,
    weather INT,
    result VARCHAR(20)
);