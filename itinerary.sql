-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 22, 2024 at 07:53 PM
-- Server version: 8.0.37
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `itinerary`
--
CREATE DATABASE IF NOT EXISTS `itinerary` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `itinerary`;
DROP DATABASE itinerary;

-- --------------------------------------------------------

--
-- Table structure for table `activities`
--

DROP TABLE IF EXISTS `activities`;
CREATE TABLE `activities` (
  `activityID` int NOT NULL,
  `activityName` varchar(50) NOT NULL,
  `timeFrom` varchar(10) NOT NULL,
  `timeTo` varchar(10) NOT NULL,
  `address` varchar(50) NOT NULL,
  `activityDescription` varchar(50) NOT NULL,
  `destinationID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `activities`
--

INSERT INTO `activities` (`activityID`, `activityName`, `timeFrom`, `timeTo`, `address`, `activityDescription`, `destinationID`) VALUES
(4, 'test2', '14:29', '15:29', 'test2', '          test2', 4),
(5, 'asdasd', '23:18', '07:18', 'asdasd', '          asdasd', 6),
(7, 'asdasd', '04:58', '13:00', 'asdasdasd', '          asdasdasd', 7),
(8, 'asdasd', '15:37', '14:37', 'asdasdasd', 'not', 7),
(9, 'asdasd', '14:40', '19:41', 'test2', '          asdasdad', 10);

-- --------------------------------------------------------

--
-- Table structure for table `destinations`
--

DROP TABLE IF EXISTS `destinations`;
CREATE TABLE `destinations` (
  `destinationID` int NOT NULL,
  `zipcode` int NOT NULL,
  `destinationName` varchar(50) NOT NULL,
  `cityName` varchar(50) NOT NULL,
  `regionName` varchar(50) NOT NULL,
  `itineraryID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `destinations`
--

INSERT INTO `destinations` (`destinationID`, `zipcode`, `destinationName`, `cityName`, `regionName`, `itineraryID`) VALUES
(2, 4242, 'not mabua pebble beach', 'not surigao city', 'not surigao del norte', 2),
(4, 4242, 'test', 'test', 'test', 5),
(5, 4242, 'test2', 'test2', 'test2', 5),
(6, 4242, 'not mabua pebble beach', 'destination1', 'not surigao del norte', 13),
(7, 2323, '2323', '2323', '2323', 16),
(8, 3, 'asdasd', 'asdasd', 'asdasd', 16),
(9, 2222, 'asdasdasd', 'asdasdasd', 'asdasdasd', 16),
(10, 4242, 'asdasdasd', 'asdasda', 'asdasd', 17);

-- --------------------------------------------------------

--
-- Table structure for table `itineraries`
--

DROP TABLE IF EXISTS `itineraries`;
CREATE TABLE `itineraries` (
  `itineraryID` int NOT NULL,
  `itineraryDay` int DEFAULT '1',
  `itineraryName` varchar(50) NOT NULL,
  `itineraryDescription` varchar(50) NOT NULL,
  `travelID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `itineraries`
--

INSERT INTO `itineraries` (`itineraryID`, `itineraryDay`, `itineraryName`, `itineraryDescription`, `travelID`) VALUES
(2, 2, 'going to iit', '          iit', 18),
(3, 1, 'what', '          asdasdasd', 19),
(5, 1, 'test', '          test', 21),
(6, 3, 'not really', '          asdasda', 18),
(7, 31, '2', '          21', 18),
(8, 2, '2', '          2', 20),
(9, 234, 'asdasdasd23', '          asdasdasd', 20),
(10, 2, '3', '          asdasd', 20),
(11, 3, '2why', '          4we', 20),
(12, 3, 'testprint', '        asdasdas  ', 20),
(13, 2, '232323', '          232323', 24),
(14, 3, '231', '          adaqsdasd', 24),
(15, 4, 'asdasdasd', '          asdasdasdasd', 24),
(16, 2323, '2323', '          232323', 25),
(17, 3, '222', '          222', 25);

-- --------------------------------------------------------

--
-- Table structure for table `travel`
--

DROP TABLE IF EXISTS `travel`;
CREATE TABLE `travel` (
  `travelID` int NOT NULL,
  `accountID` int NOT NULL,
  `travelName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `days` int NOT NULL,
  `travelDescription` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `travel`
--

INSERT INTO `travel` (`travelID`, `accountID`, `travelName`, `startDate`, `endDate`, `days`, `travelDescription`) VALUES
(18, 10, 'name has changed2', '2024-05-22', '2024-05-25', 3, 'long'),
(19, 10, 'IIT TRIP 2', '2024-05-23', '2024-05-25', 2, 'not going'),
(20, 11, 'admin2', '2024-05-21', '2024-05-23', 2, '          asdasd'),
(21, 10, 'test', '2024-05-21', '2024-05-22', 1, '          test'),
(22, 13, 'im jsta nother', '2024-05-29', '2024-05-30', 1, '          asdasdasdasd'),
(23, 11, '2-day manila trip', '2024-05-23', '2024-05-24', 1, '          asdasdasd'),
(24, 14, 'going to manila', '2024-05-23', '2024-05-23', 0, '          asdasdasd'),
(25, 15, '2-day manila trip', '2024-05-23', '2024-05-24', 1, '          asdasd');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `accountID` int NOT NULL,
  `firstName` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `Dyear` int NOT NULL,
  `month` int NOT NULL,
  `day` int NOT NULL,
  `sex` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`accountID`, `firstName`, `lastName`, `Dyear`, `month`, `day`, `sex`, `email`, `password`) VALUES
(10, 'admin1', 'admin1', 2020, 11, 11, 'Male', 'admin1@admin1.admin1', 'admin1admin1'),
(11, 'admin2', 'admin2', 2222, 22, 22, 'Male', 'admin2@admin2.com', 'admin2admin2'),
(12, 'asdasdasd', 'garbanzos', 2222, 22, 22, 'Male', 'louisantondy@gmail.com', 'dark123'),
(13, 'shodz', 'caliso', 1111, 11, 11, 'Male', 'shodz@caliso.com', 'shodzshodz'),
(14, 'earl', 'ruelo', 1111, 11, 11, 'Female', 'earl@ruelo.com', 'earl111'),
(15, 'test', 'test', 1111, 11, 11, 'Male', 'test@test.com', 'testtest');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activities`
--
ALTER TABLE `activities`
  ADD PRIMARY KEY (`activityID`),
  ADD KEY `destinationID` (`destinationID`);

--
-- Indexes for table `destinations`
--
ALTER TABLE `destinations`
  ADD PRIMARY KEY (`destinationID`),
  ADD KEY `itineraryID` (`itineraryID`);

--
-- Indexes for table `itineraries`
--
ALTER TABLE `itineraries`
  ADD PRIMARY KEY (`itineraryID`),
  ADD KEY `travelID` (`travelID`);

--
-- Indexes for table `travel`
--
ALTER TABLE `travel`
  ADD PRIMARY KEY (`travelID`),
  ADD KEY `accountID` (`accountID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`accountID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activities`
--
ALTER TABLE `activities`
  MODIFY `activityID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `destinations`
--
ALTER TABLE `destinations`
  MODIFY `destinationID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `itineraries`
--
ALTER TABLE `itineraries`
  MODIFY `itineraryID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `travel`
--
ALTER TABLE `travel`
  MODIFY `travelID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `accountID` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activities`
--
ALTER TABLE `activities`
  ADD CONSTRAINT `destinationID` FOREIGN KEY (`destinationID`) REFERENCES `destinations` (`destinationID`);

--
-- Constraints for table `destinations`
--
ALTER TABLE `destinations`
  ADD CONSTRAINT `itineraryID` FOREIGN KEY (`itineraryID`) REFERENCES `itineraries` (`itineraryID`);

--
-- Constraints for table `itineraries`
--
ALTER TABLE `itineraries`
  ADD CONSTRAINT `travelID` FOREIGN KEY (`travelID`) REFERENCES `travel` (`travelID`);

--
-- Constraints for table `travel`
--
ALTER TABLE `travel`
  ADD CONSTRAINT `accountID` FOREIGN KEY (`accountID`) REFERENCES `users` (`accountID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
