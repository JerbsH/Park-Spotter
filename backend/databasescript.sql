-- This script creates the database and tables for the parking application
DROP DATABASE IF EXISTS parking;
CREATE DATABASE parking;
USE parking;

-- Create the table for the parking spots
CREATE TABLE AVAILABLE_SPOTS (
        ID INT PRIMARY KEY AUTO_INCREMENT,
        PARKSPOTS INT,
        HANDICAPSPOTS INT,
        TOTALHANDICAPSPOTS INT,
        TOTALSPOTS INT,
        IMAGE VARCHAR(255)
);
INSERT INTO AVAILABLE_SPOTS (PARKSPOTS, HANDICAPSPOTS, TOTALHANDICAPSPOTS, TOTALSPOTS, IMAGE) VALUES (0, 0, 0, 0, '');

-- Create the table for the push notifications register token
CREATE TABLE DEVICE_TOKEN (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    TOKEN VARCHAR(255) NOT NULL
);
INSERT INTO DEVICE_TOKEN (TOKEN) VALUES ('');
