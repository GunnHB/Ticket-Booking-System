
CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(50) NOT NULL,
	email VARCHAR(100) NOT NULL UNIQUE
	);

CREATE TABLE IF NOT EXISTS games (
	id INT AUTO_INCREMENT PRIMARY KEY,
	home_team VARCHAR(50) NOT NULL,
	away_team VARCHAR(50) NOT NULL,
	game_date DATETIME NOT NULL,
	total_seats INT DEFAULT 100,
	available_seats INT DEFAULT 100
	);

CREATE TABLE IF NOT EXISTS tickets (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT,
	game_id INT,
	seat_number VARCHAR(10) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (game_id) REFERENCES games(id)
	);

INSERT INTO games (home_team, away_team, game_date)
VALUES ('LG Twins', 'Doosan Bears', '2026-06-01 18:30:00');
