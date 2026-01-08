CREATE TABLE IF NOT EXISTS shapes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    shape ENUM('circle', 'triangle', 'square') NOT NULL,
    color ENUM('red', 'green', 'blue', 'yellow', 'black') NOT NULL,
    timestamp DATETIME NOT NULL
);
