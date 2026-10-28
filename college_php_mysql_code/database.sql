-- Database initialization script for Green Building Performance Dashboard
-- For deployment in phpMyAdmin / MySQL Server

CREATE DATABASE IF NOT EXISTS `green_building_dashboard` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `green_building_dashboard`;

-- 1. Table: settings
CREATE TABLE IF NOT EXISTS `settings` (
  `setting_key` varchar(50) NOT NULL,
  `setting_value` varchar(255) NOT NULL,
  PRIMARY KEY (`setting_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `settings` (`setting_key`, `setting_value`) VALUES
('active_mode', 'LIVE')
ON DUPLICATE KEY UPDATE `setting_value`=`setting_value`;

-- 2. Table: sensor_nodes
CREATE TABLE IF NOT EXISTS `sensor_nodes` (
  `node_id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `sensor_type` varchar(50) NOT NULL,
  `threshold` double NOT NULL,
  `calibration_factor` double NOT NULL,
  PRIMARY KEY (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `sensor_nodes` (`node_id`, `name`, `sensor_type`, `threshold`, `calibration_factor`) VALUES
('node_energy', 'Main Office Energy Node', 'PZEM-004T', 3500.0, 1.0),
('node_water', 'Ground Water Supply Line', 'YF-S201', 25.0, 1.0),
('node_climate', 'Server Room Climate', 'DHT11', 28.0, 1.0)
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 3. Table: sensor_readings
CREATE TABLE IF NOT EXISTS `sensor_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_id` varchar(50) NOT NULL,
  `value1` double NOT NULL,
  `value2` double DEFAULT NULL,
  `mode` varchar(10) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `node_id` (`node_id`),
  CONSTRAINT `sensor_readings_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `sensor_nodes` (`node_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 4. Table: alerts
CREATE TABLE IF NOT EXISTS `alerts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_id` varchar(50) NOT NULL,
  `reading_value` double NOT NULL,
  `threshold` double NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `resolved` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `node_id` (`node_id`),
  CONSTRAINT `alerts_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `sensor_nodes` (`node_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 5. Table: users
CREATE TABLE IF NOT EXISTS `users` (
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Insert default admin login (username: admin, password: admin123, SHA256 hashed)
INSERT INTO `users` (`username`, `password_hash`) VALUES
('admin', '240789146302e1b12b55f11e9f45d8b8e010839e4a3c104d49d973cfcb40b5d8')
ON DUPLICATE KEY UPDATE `password_hash`=`password_hash`;
