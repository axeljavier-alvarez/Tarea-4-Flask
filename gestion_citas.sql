-- GESTION DE CITAS MEDICAS
-- AXEL JAVIER GUADALUPE ALVAREZ FELIPE

create database gestion_citas_medicas;
use gestion_citas_medicas;


CREATE TABLE Pacientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    fecha_nacimiento DATE,
    telefono VARCHAR(15),
    email VARCHAR(100)
);

CREATE TABLE Medicos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    especialidad VARCHAR(100),
    telefono VARCHAR(15),
    email VARCHAR(100)
);

CREATE TABLE Citas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    paciente_id INT,
    medico_id INT,
    fecha_cita DATETIME,
    estado VARCHAR(20) CHECK (estado IN ('programada', 'cancelada', 'completada')),
    FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
    FOREIGN KEY (medico_id) REFERENCES Medicos(id)
);

CREATE TABLE Historial_Medico (
    id INT IDENTITY(1,1) PRIMARY KEY,
    paciente_id INT,
    fecha DATE,
    descripcion TEXT,
    FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
);


INSERT INTO Pacientes (nombre, apellido, fecha_nacimiento, telefono, email) VALUES
('Juan', 'Pérez', '1985-06-15', '555-1234', 'juan.perez@example.com'),
('María', 'Gómez', '1990-03-22', '555-5678', 'maria.gomez@example.com'),
('Carlos', 'López', '1978-11-30', '555-9876', 'carlos.lopez@example.com');

INSERT INTO Medicos (nombre, apellido, especialidad, telefono, email) VALUES
('Dr. Ana', 'Martínez', 'Pediatría', '555-1122', 'ana.martinez@example.com'),
('Dr. Luis', 'Fernández', 'Cardiología', '555-3344', 'luis.fernandez@example.com'),
('Dra. Sara', 'Hernández', 'Dermatología', '555-5566', 'sara.hernandez@example.com');


INSERT INTO Citas (paciente_id, medico_id, fecha_cita, estado) VALUES
(1, 1, '2025-04-10 10:00:00', 'programada'),
(2, 2, '2025-04-11 14:30:00', 'programada'),
(3, 3, '2025-04-12 09:00:00', 'programada');

INSERT INTO Historial_Medico (paciente_id, fecha, descripcion) VALUES
(1, '2025-03-01', 'Revisión anual, todo en orden.'),
(2, '2025-03-15', 'Consulta por alergias, se recomienda tratamiento.'),
(3, '2025-03-20', 'Control de presión arterial, se ajusta medicación.');


