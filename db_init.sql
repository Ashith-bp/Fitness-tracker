-- Schema for Fitness Tracker
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  age SMALLINT,
  weight_kg DECIMAL(5,2),
  height_cm DECIMAL(5,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workouts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  exercise VARCHAR(255) NOT NULL,
  duration_minutes INT DEFAULT 0,
  calories_burned INT DEFAULT 0,
  workout_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS meals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  meal_name VARCHAR(255) NOT NULL,
  calories INT DEFAULT 0,
  protein_g DECIMAL(6,2) DEFAULT 0,
  carbs_g DECIMAL(6,2) DEFAULT 0,
  fats_g DECIMAL(6,2) DEFAULT 0,
  meal_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS weight_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  weight_kg DECIMAL(5,2) NOT NULL,
  recorded_at DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- sample data
INSERT INTO users (name,email,age,weight_kg,height_cm) VALUES ('Alice','alice@example.com',28,65.5,170),( 'Bob','bob@example.com',32,82.0,180);
INSERT INTO workouts (user_id,exercise,duration_minutes,calories_burned,workout_date) VALUES (1,'Running',30,300,'2025-09-20'),(1,'Yoga',45,180,'2025-09-21'),(2,'Cycling',60,600,'2025-09-21');
INSERT INTO meals (user_id,meal_name,calories,protein_g,carbs_g,fats_g,meal_date) VALUES (1,'Breakfast - Oats',350,12.0,50.0,8.0,'2025-09-21'),(1,'Lunch - Salad',400,10.0,30.0,18.0,'2025-09-21'),(2,'Dinner - Pasta',800,20.0,120.0,15.0,'2025-09-21');
INSERT INTO weight_history (user_id,weight_kg,recorded_at) VALUES (1,66.0,'2025-09-15'),(1,65.5,'2025-09-21'),(2,83.0,'2025-09-20');
