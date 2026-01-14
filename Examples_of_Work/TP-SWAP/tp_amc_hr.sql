-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 19, 2024 at 04:21 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tp_amc_hr`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_log`
--

CREATE TABLE `activity_log` (
  `log_id` int(11) NOT NULL,
  `action` text NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_log`
--

INSERT INTO `activity_log` (`log_id`, `action`, `time`) VALUES
(271, '1 cleared the logs.', '2024-01-19 15:49:47'),
(272, '22 applied for leave.', '2024-01-19 15:50:47'),
(273, '22 applied for leave.', '2024-01-19 15:51:37'),
(274, '22 applied for leave.', '2024-01-19 15:55:12'),
(275, '22 applied for leave.', '2024-01-19 15:55:56'),
(276, '22 applied for leave.', '2024-01-19 15:56:08'),
(277, '22 applied for MC.', '2024-01-19 15:57:23'),
(278, 'Personal information of 22 was updated.', '2024-01-19 15:58:38'),
(279, '22\'s password was changed', '2024-01-19 16:01:27'),
(280, '22 reset the account status and password of 22.', '2024-01-19 16:01:42'),
(281, '22 deleted employee 25.', '2024-01-19 16:01:48'),
(282, '22 updated employee information of 29', '2024-01-19 16:16:58'),
(283, '22 updated employee information of 29', '2024-01-19 16:17:08'),
(284, 'Personal information of 29 was updated.', '2024-01-19 16:17:50');

-- --------------------------------------------------------

--
-- Table structure for table `employee_information`
--

CREATE TABLE `employee_information` (
  `employee_id` int(11) NOT NULL,
  `name` text NOT NULL,
  `department` text NOT NULL,
  `contact` text NOT NULL,
  `email` text NOT NULL,
  `bank_account` text NOT NULL,
  `birthday` text NOT NULL,
  `salary` text NOT NULL,
  `leave_days_taken` int(2) NOT NULL DEFAULT 0,
  `mc_days_taken` int(2) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_information`
--

INSERT INTO `employee_information` (`employee_id`, `name`, `department`, `contact`, `email`, `bank_account`, `birthday`, `salary`, `leave_days_taken`, `mc_days_taken`) VALUES
(1, 'boss', 'BOSS', 'QU2ZvBIhuvwxkQ6pYXznf2d1T25VU2RENk9CamI2WTFLYTJLTXc9PQ==', 'TQzRJHZaiXFkJtEYhZg4uldsb1pSRGQzcHBZekVNUm9Jc1k0dk5xRFdIb2VJTHlzeGxxRFFJRG13bXc9', 'zp8dqR5NENxaRzlcoHUT8jRLejJEZHZzcVlraW53T0tlZUh3d1E9PQ==', '2f0e9/XrY8QbF4f2poSWu2YyU1JiaDNwL0lwUG1zMytaS01LSmc9PQ==', '0GARPa0WOJ7Am8bFJzUmIHpwV0tJZVlaaWkyenc0aUJ2RXNUb0E9PQ==', 0, 0),
(22, 'gideono', 'HR', 'BJHAgeghL/Jl7oUd3Y9M7lFhbDBVUnJMdy8rUkx6Nklsd0xFK1E9PQ==', 'qpR7fmbBCzblrPXF/ue6P2FqWk1LcVUyM1lINTUzelJ2YXdBRHRCeGt6Q1J3YWZxdlRjbHBSS2RLL2M9', '+ramz2llxJXaeMaWKTelbWpCczR3bWhVaGsrUHlabG5KWnhmVVE9PQ==', 'AlqR0ZH0BLcvsN+AUyrcVFBIRWxwREphdkp6YkVreW9kcWQ4Y3c9PQ==', '5Qdt3HucSkYjxGi/5dzA9jd6VFQyTDZvTEdMQVVaZUZvcWRudFE9PQ==', 0, 0),
(29, 'eeeeee', 'IT', 'kWLBrph/gTSSaVcE4y3aby9ldHFQSmRrTTNmR201Wkh0NndSN0E9PQ==', 'yt/IhaCFee3Vq4b8ObnW8TdhdHVIQ2h1eTJWemJRMk9IU2M0WW8yOXpiSXdLQTBHamZmRU04OVFTSWc9', 'CFOwdwic1UEd73H/gdxiDk4xMEo4TXdacUkyelNqWVdyOGNyMnc9PQ==', 'dD9DrMtQ9zVUGzDdhh02rXlXMFlQejVldnZ0bDNhTkNUYWF4Tnc9PQ==', '1ZcK4Wr1xYRiWZMfvyvlDVdnQzlYcmtsblRuY3UrRVc2RHd6M2c9PQ==', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `leave_application`
--

CREATE TABLE `leave_application` (
  `leave_id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `reason` text NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` varchar(8) NOT NULL DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leave_application`
--

INSERT INTO `leave_application` (`leave_id`, `employee_id`, `reason`, `start_date`, `end_date`, `status`) VALUES
(19, 22, '020222', '2024-01-19', '2024-01-21', 'pending'),
(20, 22, 'dddddd', '2024-01-19', '2024-01-26', 'pending'),
(21, 22, 'rffff fff', '2024-01-19', '2024-01-27', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `mc_application`
--

CREATE TABLE `mc_application` (
  `mc_id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `mc_picture` longblob NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` varchar(8) NOT NULL DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_accounts`
--

CREATE TABLE `user_accounts` (
  `user_id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `user_account_level` int(1) NOT NULL DEFAULT 1,
  `password` text NOT NULL DEFAULT 'K+1EqObWZ8Xr/tVv5mlIXEFKUEtoenBCRXcwQ0JxNG9MVDJoUW1OZkdiS3YzbFZDT3RYZmthZG9lakhaN0Y4dXNFeG9GNmVRN2RZY200VzRBZjkrc09qb1c5TEVCRW1CaHlVaTBPcXZCWFNuYUpIaHJUbXdrQVltV0ZVPQ==',
  `account_status` varchar(10) NOT NULL DEFAULT 'logged out',
  `password_failed_attempts` int(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_accounts`
--

INSERT INTO `user_accounts` (`user_id`, `employee_id`, `user_account_level`, `password`, `account_status`, `password_failed_attempts`) VALUES
(1, 1, 3, 'K+1EqObWZ8Xr/tVv5mlIXEFKUEtoenBCRXcwQ0JxNG9MVDJoUW1OZkdiS3YzbFZDT3RYZmthZG9lakhaN0Y4dXNFeG9GNmVRN2RZY200VzRBZjkrc09qb1c5TEVCRW1CaHlVaTBPcXZCWFNuYUpIaHJUbXdrQVltV0ZVPQ==', 'logged out', 0),
(23, 22, 2, 'K+1EqObWZ8Xr/tVv5mlIXEFKUEtoenBCRXcwQ0JxNG9MVDJoUW1OZkdiS3YzbFZDT3RYZmthZG9lakhaN0Y4dXNFeG9GNmVRN2RZY200VzRBZjkrc09qb1c5TEVCRW1CaHlVaTBPcXZCWFNuYUpIaHJUbXdrQVltV0ZVPQ==', 'logged out', 0),
(30, 29, 1, 'K+1EqObWZ8Xr/tVv5mlIXEFKUEtoenBCRXcwQ0JxNG9MVDJoUW1OZkdiS3YzbFZDT3RYZmthZG9lakhaN0Y4dXNFeG9GNmVRN2RZY200VzRBZjkrc09qb1c5TEVCRW1CaHlVaTBPcXZCWFNuYUpIaHJUbXdrQVltV0ZVPQ==', 'logged out', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_log`
--
ALTER TABLE `activity_log`
  ADD PRIMARY KEY (`log_id`);

--
-- Indexes for table `employee_information`
--
ALTER TABLE `employee_information`
  ADD PRIMARY KEY (`employee_id`);

--
-- Indexes for table `leave_application`
--
ALTER TABLE `leave_application`
  ADD PRIMARY KEY (`leave_id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Indexes for table `mc_application`
--
ALTER TABLE `mc_application`
  ADD PRIMARY KEY (`mc_id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Indexes for table `user_accounts`
--
ALTER TABLE `user_accounts`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `employee_id` (`employee_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_log`
--
ALTER TABLE `activity_log`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=285;

--
-- AUTO_INCREMENT for table `employee_information`
--
ALTER TABLE `employee_information`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `leave_application`
--
ALTER TABLE `leave_application`
  MODIFY `leave_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `mc_application`
--
ALTER TABLE `mc_application`
  MODIFY `mc_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `user_accounts`
--
ALTER TABLE `user_accounts`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `leave_application`
--
ALTER TABLE `leave_application`
  ADD CONSTRAINT `leave_application_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee_information` (`employee_id`) ON DELETE CASCADE;

--
-- Constraints for table `mc_application`
--
ALTER TABLE `mc_application`
  ADD CONSTRAINT `mc_application_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee_information` (`employee_id`) ON DELETE CASCADE;

--
-- Constraints for table `user_accounts`
--
ALTER TABLE `user_accounts`
  ADD CONSTRAINT `user_accounts_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee_information` (`employee_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
