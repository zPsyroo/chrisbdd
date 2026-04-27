-- ============================================
-- Veterinary Clinic Database
-- ============================================
CREATE DATABASE IF NOT EXISTS veterinaria;
USE veterinaria;

CREATE TABLE duenos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    email VARCHAR(100)
);

CREATE TABLE veterinarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    telefono VARCHAR(15)
);

CREATE TABLE animales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(50),
    edad INT,
    dueno_id INT,
    FOREIGN KEY (dueno_id) REFERENCES duenos(id) ON DELETE SET NULL
);

CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    motivo VARCHAR(200),
    animal_id INT,
    veterinario_id INT,
    FOREIGN KEY (animal_id) REFERENCES animales(id) ON DELETE CASCADE,
    FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id) ON DELETE SET NULL
);

CREATE TABLE tratamientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL,
    medicamento VARCHAR(100),
    dosis VARCHAR(100),
    cita_id INT,
    FOREIGN KEY (cita_id) REFERENCES citas(id) ON DELETE CASCADE
);

-- Sample data
INSERT INTO duenos (nombre, telefono, email) VALUES
('Carlos García', '600111222', 'carlos@email.com'),
('María López', '600333444', 'maria@email.com'),
('Juan Martínez', '600555666', 'juan@email.com');

INSERT INTO veterinarios (nombre, especialidad, telefono) VALUES
('Dr. Pérez', 'Cirugía', '600777888'),
('Dra. Ruiz', 'Dermatología', '600999000'),
('Dr. Sánchez', 'Medicina General', '600123456');

INSERT INTO animales (nombre, especie, raza, edad, dueno_id) VALUES
('Rex', 'Perro', 'Labrador', 3, 1),
('Misi', 'Gato', 'Siamés', 5, 2),
('Toby', 'Perro', 'Golden Retriever', 2, 3),
('Luna', 'Gato', 'Persa', 4, 1);

INSERT INTO citas (fecha, motivo, animal_id, veterinario_id) VALUES
('2025-01-10', 'Revisión anual', 1, 1),
('2025-02-15', 'Problema de piel', 2, 2),
('2025-03-20', 'Vacunación', 3, 3);

INSERT INTO tratamientos (descripcion, medicamento, dosis, cita_id) VALUES
('Vacuna antirrábica', 'Rabisin', '1ml', 1),
('Crema para dermatitis', 'Cortiderm', 'Aplicar 2 veces al día', 2),
('Desparasitación', 'Drontal', '1 comprimido', 3);

-- Database users
CREATE USER 'flask_user'@'%' IDENTIFIED BY 'flask1234';
GRANT SELECT, INSERT, UPDATE, DELETE ON veterinaria.* TO 'flask_user'@'%';

CREATE USER 'admin_user'@'%' IDENTIFIED BY 'admin1234';
GRANT ALL PRIVILEGES ON veterinaria.* TO 'admin_user'@'%';

FLUSH PRIVILEGES;
