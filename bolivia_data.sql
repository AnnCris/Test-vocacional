-- Script SQL para insertar datos de universidades bolivianas
-- Compatible con PostgreSQL
-- Fecha: 2025

-- Limpiar datos existentes (opcional)
-- TRUNCATE TABLE recommendations CASCADE;
-- TRUNCATE TABLE test_answers CASCADE;
-- TRUNCATE TABLE careers CASCADE;
-- TRUNCATE TABLE students CASCADE;
-- TRUNCATE TABLE users CASCADE;
-- TRUNCATE TABLE faculties CASCADE;

-- ========================================
-- INSERTAR USUARIOS DE EJEMPLO
-- ========================================

INSERT INTO users (username, email, password_hash, is_admin, created_at) VALUES
('maria.rodriguez', 'maria.rodriguez@estudiante.bo', 'pbkdf2:sha256:260000$XYZabc123DEFghi$a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', false, NOW()),
('carlos.mamani', 'carlos.mamani@estudiante.bo', 'pbkdf2:sha256:260000$LMNopq456RST$b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3', false, NOW()),
('ana.quispe', 'ana.quispe@estudiante.bo', 'pbkdf2:sha256:260000$UVWxyz789ABC$c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4', false, NOW()),
('diego.vargas', 'diego.vargas@estudiante.bo', 'pbkdf2:sha256:260000$DEFghi012JKL$d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5', false, NOW()),
('lucia.santos', 'lucia.santos@estudiante.bo', 'pbkdf2:sha256:260000$MNOpqr345STU$e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', false, NOW()),
('jorge.flores', 'jorge.flores@estudiante.bo', 'pbkdf2:sha256:260000$VWXyza678BCD$f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7', false, NOW()),
('sofia.choque', 'sofia.choque@estudiante.bo', 'pbkdf2:sha256:260000$EFGhij901KLM$a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8', false, NOW()),
('ricardo.torrez', 'ricardo.torrez@estudiante.bo', 'pbkdf2:sha256:260000$NOPqrs234TUV$b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9', false, NOW());

-- ========================================
-- INSERTAR FACULTADES BOLIVIANAS
-- ========================================

INSERT INTO faculties (name, description) VALUES
-- Universidad Mayor de San Andrés (UMSA) - La Paz
('Facultad de Ingeniería - UMSA', 'Facultad de Ingeniería de la Universidad Mayor de San Andrés, formando ingenieros en diversas especialidades'),
('Facultad de Medicina - UMSA', 'Facultad de Medicina, Enfermería, Nutrición y Tecnología Médica de la UMSA'),
('Facultad de Ciencias Económicas y Financieras - UMSA', 'Facultad de Ciencias Económicas y Financieras de la Universidad Mayor de San Andrés'),
('Facultad de Humanidades y Ciencias de la Educación - UMSA', 'Facultad enfocada en humanidades, educación y ciencias sociales'),
('Facultad de Derecho y Ciencias Políticas - UMSA', 'Facultad de Derecho y Ciencias Políticas de la Universidad Mayor de San Andrés'),
('Facultad de Ciencias Puras y Naturales - UMSA', 'Facultad de Ciencias Puras y Naturales, incluyendo matemáticas, física, química y biología'),
('Facultad de Arquitectura, Artes, Diseño y Urbanismo - UMSA', 'Facultad de Arquitectura, Artes, Diseño y Urbanismo'),
('Facultad de Agronomía - UMSA', 'Facultad de Agronomía de la Universidad Mayor de San Andrés'),

-- Universidad Mayor de San Simón (UMSS) - Cochabamba
('Facultad de Ciencias y Tecnología - UMSS', 'Facultad de Ciencias y Tecnología de la Universidad Mayor de San Simón'),
('Facultad de Medicina - UMSS', 'Facultad de Medicina de la Universidad Mayor de San Simón'),
('Facultad de Ciencias Económicas - UMSS', 'Facultad de Ciencias Económicas de la UMSS'),
('Facultad de Humanidades y Ciencias de la Educación - UMSS', 'Facultad de Humanidades y Ciencias de la Educación de la UMSS'),
('Facultad de Ciencias Jurídicas y Políticas - UMSS', 'Facultad de Ciencias Jurídicas y Políticas de la UMSS'),

-- Universidad Autónoma Gabriel René Moreno (UAGRM) - Santa Cruz
('Facultad de Ingeniería - UAGRM', 'Facultad de Ingeniería de la Universidad Autónoma Gabriel René Moreno'),
('Facultad de Ciencias de la Salud - UAGRM', 'Facultad de Ciencias de la Salud de la UAGRM'),
('Facultad de Ciencias Económicas, Administrativas y Financieras - UAGRM', 'Facultad de Ciencias Económicas, Administrativas y Financieras'),
('Facultad de Humanidades - UAGRM', 'Facultad de Humanidades de la Universidad Autónoma Gabriel René Moreno'),

-- Universidad Técnica de Oruro (UTO)
('Facultad Nacional de Ingeniería - UTO', 'Facultad Nacional de Ingeniería de la Universidad Técnica de Oruro'),
('Facultad de Medicina - UTO', 'Facultad de Medicina de la Universidad Técnica de Oruro'),
('Facultad de Ciencias Económicas, Financieras y Administrativas - UTO', 'Facultad de Ciencias Económicas, Financieras y Administrativas de la UTO'),

-- Universidad Autónoma Tomás Frías (UATF) - Potosí
('Facultad de Ingeniería - UATF', 'Facultad de Ingeniería de la Universidad Autónoma Tomás Frías'),
('Facultad de Medicina - UATF', 'Facultad de Medicina de la Universidad Autónoma Tomás Frías'),

-- Universidad Autónoma del Beni (UAB)
('Facultad de Ciencias Agropecuarias - UAB', 'Facultad de Ciencias Agropecuarias de la Universidad Autónoma del Beni'),
('Facultad de Ciencias de la Salud - UAB', 'Facultad de Ciencias de la Salud de la UAB'),

-- Universidad de Tarija (UAJMS)
('Facultad de Ciencias y Tecnología - UAJMS', 'Facultad de Ciencias y Tecnología de la Universidad Juan Misael Saracho'),
('Facultad de Ciencias de la Salud - UAJMS', 'Facultad de Ciencias de la Salud de la UAJMS');

INSERT INTO faculties (name, description) VALUES
-- Universidad Central (UCB) - La Paz
('Facultad de Ingeniería - UCB', 'Facultad de Ingeniería de la Universidad Católica Boliviana'),
('Facultad de Ciencias de la Salud - UCB', 'Facultad de Ciencias de la Salud UCB'),
('Facultad de Ciencias Empresariales - UCB', 'Facultad de Ciencias Empresariales UCB'),

-- Universidad Privada de Santa Cruz (UPSA)
('Facultad de Ingeniería y Tecnología - UPSA', 'Facultad de Ingeniería y Tecnología UPSA'),
('Facultad de Ciencias Empresariales - UPSA', 'Facultad de Ciencias Empresariales UPSA'),
('Facultad de Derecho - UPSA', 'Facultad de Derecho UPSA'),

-- Universidad Franz Tamayo (UNIFRANZ)
('Facultad de Ingeniería y Tecnología - UNIFRANZ', 'Facultad de Ingeniería y Tecnología UNIFRANZ'),
('Facultad de Ciencias de la Salud - UNIFRANZ', 'Facultad de Ciencias de la Salud UNIFRANZ'),
('Facultad de Ciencias Sociales - UNIFRANZ', 'Facultad de Ciencias Sociales UNIFRANZ'),

-- Universidad Nur
('Facultad de Ingeniería - NUR', 'Facultad de Ingeniería Universidad Nur'),
('Facultad de Medicina - NUR', 'Facultad de Medicina Universidad Nur'),
('Facultad de Ciencias Empresariales - NUR', 'Facultad de Ciencias Empresariales Nur'),

-- Escuela Militar de Ingeniería (EMI)
('Facultad de Ingeniería - EMI', 'Escuela Militar de Ingeniería'),

-- Universidad Adventista de Bolivia (UAB)
('Facultad de Ingeniería y Tecnología - UAB', 'Facultad de Ingeniería UAB'),

-- Instituto Tecnológico Boliviano
('Facultad de Tecnología - ITB', 'Instituto Tecnológico Boliviano');


INSERT INTO aptitudes (name, description, category) VALUES
-- Aptitudes del Área C (Administrativas y Contables)
('Liderazgo', 'Capacidad para dirigir y motivar equipos de trabajo', 'Administrativa'),
('Organización', 'Habilidad para planificar y estructurar actividades', 'Administrativa'),
('Análisis Numérico', 'Facilidad para trabajar con números y cálculos', 'Administrativa'),
('Toma de Decisiones', 'Capacidad para evaluar opciones y decidir efectivamente', 'Administrativa'),
('Negociación', 'Habilidad para llegar a acuerdos beneficiosos', 'Administrativa'),
('Gestión de Recursos', 'Capacidad para administrar recursos humanos y materiales', 'Administrativa'),
('Visión Estratégica', 'Capacidad para planificar a largo plazo', 'Administrativa'),

-- Aptitudes del Área H (Humanísticas y Sociales)
('Comunicación Oral', 'Habilidad para expresarse verbalmente de forma efectiva', 'Humanística'),
('Comunicación Escrita', 'Capacidad para redactar textos claros y coherentes', 'Humanística'),
('Empatía', 'Capacidad para comprender y conectar con otros', 'Humanística'),
('Análisis Social', 'Habilidad para entender fenómenos sociales', 'Humanística'),
('Investigación', 'Capacidad para indagar y descubrir información', 'Humanística'),
('Pensamiento Crítico', 'Habilidad para evaluar y cuestionar ideas', 'Humanística'),
('Mediación', 'Capacidad para resolver conflictos entre personas', 'Humanística'),
('Trabajo Comunitario', 'Habilidad para trabajar con grupos sociales', 'Humanística'),

-- Aptitudes del Área A (Artísticas)
('Creatividad', 'Capacidad para generar ideas originales', 'Artística'),
('Sensibilidad Estética', 'Apreciación y creación de belleza', 'Artística'),
('Expresión Visual', 'Habilidad para comunicar a través de imágenes', 'Artística'),
('Expresión Musical', 'Capacidad para crear y interpretar música', 'Artística'),
('Innovación', 'Habilidad para crear soluciones novedosas', 'Artística'),
('Percepción Espacial', 'Capacidad para visualizar formas y espacios', 'Artística'),
('Coordinación Motora Fina', 'Precisión en movimientos detallados', 'Artística'),

-- Aptitudes del Área S (Ciencias de la Salud)
('Cuidado y Atención', 'Dedicación al bienestar de otros', 'Salud'),
('Resistencia al Estrés', 'Capacidad para manejar situaciones tensas', 'Salud'),
('Observación Clínica', 'Habilidad para detectar síntomas y signos', 'Salud'),
('Destreza Manual', 'Precisión en procedimientos manuales', 'Salud'),
('Compasión', 'Sensibilidad hacia el sufrimiento ajeno', 'Salud'),
('Trabajo en Equipo Médico', 'Colaboración en entornos sanitarios', 'Salud'),
('Ética Profesional', 'Compromiso con principios morales', 'Salud'),

-- Aptitudes del Área I (Ingeniería y Tecnología)
('Razonamiento Lógico', 'Capacidad para seguir secuencias lógicas', 'Técnica'),
('Resolución de Problemas', 'Habilidad para encontrar soluciones técnicas', 'Técnica'),
('Precisión Técnica', 'Exactitud en trabajos técnicos', 'Técnica'),
('Innovación Tecnológica', 'Capacidad para desarrollar nuevas tecnologías', 'Técnica'),
('Análisis Sistemático', 'Habilidad para descomponer sistemas complejos', 'Técnica'),
('Programación', 'Capacidad para crear software', 'Técnica'),
('Diseño Técnico', 'Habilidad para crear planos y diseños', 'Técnica'),

-- Aptitudes del Área D (Defensa y Seguridad)
('Liderazgo Militar', 'Capacidad para dirigir en situaciones críticas', 'Defensa'),
('Resistencia Física', 'Fortaleza para actividades físicamente exigentes', 'Defensa'),
('Disciplina', 'Capacidad para seguir normas y procedimientos', 'Defensa'),
('Trabajo bajo Presión', 'Rendimiento efectivo en situaciones tensas', 'Defensa'),
('Valentía', 'Coraje para enfrentar situaciones peligrosas', 'Defensa'),
('Integridad', 'Compromiso con valores éticos sólidos', 'Defensa'),
('Estrategia', 'Capacidad para planificar operaciones complejas', 'Defensa'),

-- Aptitudes del Área E (Ciencias Exactas y Naturales)
('Razonamiento Matemático', 'Capacidad para resolver problemas matemáticos', 'Científica'),
('Investigación Científica', 'Habilidad para aplicar método científico', 'Científica'),
('Análisis de Datos', 'Capacidad para interpretar información cuantitativa', 'Científica'),
('Experimentación', 'Habilidad para diseñar y ejecutar experimentos', 'Científica'),
('Observación Detallada', 'Capacidad para notar detalles importantes', 'Científica'),
('Pensamiento Abstracto', 'Habilidad para manejar conceptos abstractos', 'Científica'),
('Curiosidad Científica', 'Interés por entender cómo funciona el mundo', 'Científica'),

-- Aptitudes Transversales
('Adaptabilidad', 'Capacidad para ajustarse a cambios', 'Transversal'),
('Autocontrol', 'Capacidad para regular emociones y comportamientos', 'Transversal'),
('Perseverancia', 'Capacidad para persistir ante dificultades', 'Transversal'),
('Responsabilidad', 'Compromiso con obligaciones y tareas', 'Transversal'),
('Tolerancia', 'Respeto hacia la diversidad de ideas y personas', 'Transversal');

-- ========================================
-- INSERTAR CARRERAS BOLIVIANAS
-- ========================================

INSERT INTO careers (name, description, faculty_id, area_c, area_h, area_a, area_s, area_i, area_d, area_e) VALUES

-- CARRERAS DE INGENIERÍA (Facultades estatales y privadas)
('Ingeniería Eléctrica', 'Sistemas de energía eléctrica y electrónica', 1, 0.3, 0.1, 0.2, 0.1, 0.9, 0.2, 0.8),
('Ingeniería Electrónica', 'Sistemas electrónicos y telecomunicaciones', 1, 0.3, 0.1, 0.3, 0.1, 0.9, 0.2, 0.8),
('Ingeniería Mecánica', 'Diseño y mantenimiento de sistemas mecánicos', 1, 0.4, 0.1, 0.3, 0.1, 0.9, 0.2, 0.7),
('Ingeniería Química', 'Procesos químicos industriales', 1, 0.3, 0.1, 0.2, 0.3, 0.8, 0.1, 0.9),
('Ingeniería Petrolera', 'Exploración y extracción de hidrocarburos', 1, 0.4, 0.2, 0.2, 0.2, 0.8, 0.3, 0.8),
('Ingeniería de Alimentos', 'Procesamiento y conservación de alimentos', 1, 0.4, 0.2, 0.2, 0.4, 0.7, 0.1, 0.8),
('Ingeniería Ambiental', 'Protección del medio ambiente', 1, 0.4, 0.4, 0.3, 0.3, 0.7, 0.2, 0.8),

-- Ingenierías Especializadas
('Ingeniería Biomédica', 'Aplicación de ingeniería en medicina', 25, 0.3, 0.2, 0.3, 0.7, 0.8, 0.1, 0.7),
('Ingeniería en Telecomunicaciones', 'Sistemas de comunicación', 25, 0.3, 0.2, 0.3, 0.1, 0.9, 0.2, 0.8),
('Ingeniería de Software', 'Desarrollo de aplicaciones y software', 25, 0.4, 0.2, 0.4, 0.1, 0.9, 0.1, 0.7),
('Ingeniería en Redes y Comunicaciones', 'Infraestructura de redes', 25, 0.3, 0.2, 0.2, 0.1, 0.9, 0.3, 0.8),
('Ingeniería Mecatrónica', 'Integración de mecánica, electrónica e informática', 25, 0.3, 0.1, 0.4, 0.1, 0.9, 0.2, 0.8),
('Ingeniería Aeronáutica', 'Diseño y construcción de aeronaves', 37, 0.3, 0.1, 0.3, 0.1, 0.9, 0.4, 0.8),
('Ingeniería Naval', 'Construcción naval y sistemas marítimos', 37, 0.4, 0.2, 0.3, 0.1, 0.8, 0.5, 0.7),
('Ingeniería de Minas', 'Extracción y procesamiento de minerales', 1, 0.4, 0.2, 0.2, 0.2, 0.8, 0.3, 0.8),
('Ingeniería Metalúrgica', 'Procesamiento de metales', 1, 0.3, 0.1, 0.2, 0.2, 0.8, 0.2, 0.9),
('Ingeniería Topográfica', 'Medición y representación del terreno', 1, 0.4, 0.2, 0.3, 0.1, 0.7, 0.2, 0.7),

-- CARRERAS DE MEDICINA Y SALUD
('Odontología', 'Salud bucodental', 2, 0.4, 0.3, 0.4, 0.8, 0.3, 0.2, 0.5),
('Bioquímica y Farmacia', 'Análisis bioquímicos y medicamentos', 2, 0.3, 0.2, 0.2, 0.7, 0.4, 0.1, 0.9),
('Nutrición y Dietética', 'Alimentación y salud nutricional', 2, 0.4, 0.4, 0.2, 0.8, 0.2, 0.1, 0.6),
('Fisioterapia y Kinesiología', 'Rehabilitación física', 2, 0.3, 0.4, 0.3, 0.8, 0.3, 0.2, 0.5),
('Fonoaudiología', 'Trastornos de la comunicación', 2, 0.3, 0.6, 0.4, 0.7, 0.2, 0.1, 0.3),
('Tecnología Médica', 'Equipos médicos y diagnóstico', 26, 0.4, 0.3, 0.3, 0.8, 0.6, 0.2, 0.6),
('Psicología Clínica', 'Tratamiento de trastornos mentales', 26, 0.3, 0.8, 0.4, 0.7, 0.2, 0.2, 0.3),
('Terapia Ocupacional', 'Rehabilitación ocupacional', 26, 0.3, 0.5, 0.5, 0.8, 0.3, 0.2, 0.3),

-- Especialidades Médicas
('Radiología e Imagenología', 'Diagnóstico por imágenes', 26, 0.3, 0.3, 0.3, 0.8, 0.5, 0.1, 0.6),
('Laboratorio Clínico', 'Análisis clínicos', 26, 0.3, 0.2, 0.2, 0.7, 0.3, 0.1, 0.8),
('Optometría', 'Salud visual', 26, 0.3, 0.3, 0.3, 0.8, 0.4, 0.1, 0.5),
('Medicina Veterinaria', 'Salud animal', 8, 0.4, 0.3, 0.2, 0.8, 0.3, 0.2, 0.6),

-- CARRERAS ECONÓMICAS Y ADMINISTRATIVAS
('Economía', 'Análisis económico', 3, 0.8, 0.5, 0.2, 0.1, 0.3, 0.3, 0.5),
('Ingeniería Comercial', 'Gestión comercial y negocios', 3, 0.8, 0.4, 0.3, 0.1, 0.4, 0.2, 0.3),
('Marketing', 'Mercadotecnia y publicidad', 3, 0.8, 0.5, 0.6, 0.1, 0.3, 0.2, 0.2),
('Turismo', 'Gestión turística', 3, 0.7, 0.6, 0.5, 0.2, 0.2, 0.2, 0.2),
('Administración Pública', 'Gestión del sector público', 27, 0.8, 0.6, 0.2, 0.2, 0.2, 0.5, 0.3),
('Comercio Internacional', 'Negocios internacionales', 27, 0.8, 0.5, 0.3, 0.1, 0.3, 0.2, 0.3),
('Finanzas', 'Gestión financiera', 27, 0.9, 0.3, 0.2, 0.1, 0.3, 0.2, 0.4),
('Recursos Humanos', 'Gestión del talento humano', 27, 0.7, 0.7, 0.3, 0.2, 0.2, 0.2, 0.2),

-- Especialidades Empresariales
('Administración Hotelera', 'Gestión de hoteles y servicios', 27, 0.7, 0.6, 0.4, 0.2, 0.2, 0.2, 0.2),
('Gastronomía', 'Arte culinario y gestión gastronómica', 27, 0.5, 0.4, 0.7, 0.3, 0.2, 0.1, 0.4),
('Gestión Ambiental', 'Administración de recursos naturales', 27, 0.6, 0.5, 0.3, 0.3, 0.4, 0.2, 0.7),
('Administración Deportiva', 'Gestión de organizaciones deportivas', 27, 0.7, 0.5, 0.3, 0.3, 0.2, 0.3, 0.2),

-- CARRERAS DE HUMANIDADES Y EDUCACIÓN
('Trabajo Social', 'Intervención social', 4, 0.4, 0.9, 0.3, 0.5, 0.2, 0.4, 0.2),
('Ciencias de la Educación', 'Pedagogía y educación', 4, 0.4, 0.9, 0.4, 0.3, 0.2, 0.3, 0.3),
('Historia', 'Estudio del pasado', 4, 0.3, 0.9, 0.4, 0.1, 0.1, 0.3, 0.3),
('Filosofía', 'Reflexión filosófica', 4, 0.2, 0.9, 0.4, 0.1, 0.1, 0.2, 0.3),
('Lingüística e Idiomas', 'Estudio de las lenguas', 4, 0.3, 0.9, 0.4, 0.1, 0.2, 0.2, 0.2),
('Antropología', 'Estudio del ser humano', 4, 0.3, 0.9, 0.4, 0.3, 0.1, 0.2, 0.4),
('Sociología', 'Estudio de la sociedad', 4, 0.4, 0.9, 0.3, 0.3, 0.1, 0.3, 0.3),
('Arqueología', 'Estudio de culturas pasadas', 4, 0.3, 0.8, 0.5, 0.2, 0.2, 0.2, 0.6),

-- Especialidades en Educación
('Educación Inicial', 'Educación de primera infancia', 4, 0.4, 0.8, 0.6, 0.4, 0.1, 0.2, 0.2),
('Educación Primaria', 'Enseñanza primaria', 4, 0.4, 0.9, 0.5, 0.3, 0.2, 0.2, 0.3),
('Educación Secundaria', 'Enseñanza secundaria', 4, 0.4, 0.9, 0.4, 0.2, 0.3, 0.2, 0.4),
('Educación Especial', 'Educación inclusiva', 4, 0.3, 0.8, 0.4, 0.6, 0.2, 0.2, 0.2),
('Educación Física', 'Enseñanza deportiva', 4, 0.4, 0.6, 0.4, 0.4, 0.2, 0.3, 0.3),

-- CARRERAS DE DERECHO Y CIENCIAS POLÍTICAS
('Ciencias Políticas', 'Sistemas políticos', 5, 0.5, 0.8, 0.3, 0.2, 0.2, 0.6, 0.4),
('Relaciones Internacionales', 'Diplomacia y política exterior', 29, 0.6, 0.8, 0.3, 0.2, 0.2, 0.4, 0.3),
('Criminología', 'Estudio del crimen', 29, 0.4, 0.7, 0.2, 0.3, 0.3, 0.7, 0.4),

-- CARRERAS DE CIENCIAS PURAS Y NATURALES
('Matemáticas', 'Ciencias matemáticas', 6, 0.2, 0.2, 0.2, 0.1, 0.6, 0.1, 0.9),
('Física', 'Estudio de la materia y energía', 6, 0.2, 0.2, 0.2, 0.2, 0.5, 0.1, 0.9),
('Ciencias de la Computación', 'Computación teórica', 6, 0.3, 0.2, 0.3, 0.1, 0.9, 0.1, 0.8),
('Estadística', 'Análisis de datos', 6, 0.5, 0.3, 0.2, 0.2, 0.6, 0.2, 0.8),
('Geología', 'Estudio de la Tierra', 6, 0.3, 0.3, 0.3, 0.2, 0.4, 0.2, 0.8),
('Geografía', 'Estudio del espacio geográfico', 6, 0.4, 0.6, 0.4, 0.2, 0.3, 0.2, 0.6),

-- CARRERAS DE ARQUITECTURA Y ARTES
('Artes Plásticas', 'Expresión artística visual', 7, 0.2, 0.5, 0.9, 0.1, 0.2, 0.1, 0.2),
('Música', 'Arte musical', 7, 0.2, 0.4, 0.9, 0.1, 0.2, 0.1, 0.2),
('Diseño Industrial', 'Diseño de productos', 7, 0.5, 0.3, 0.8, 0.1, 0.6, 0.1, 0.4),
('Diseño de Interiores', 'Diseño de espacios interiores', 7, 0.5, 0.4, 0.8, 0.1, 0.4, 0.1, 0.3),
('Artes Escénicas', 'Teatro y actuación', 7, 0.3, 0.6, 0.9, 0.2, 0.1, 0.2, 0.1),
('Cinematografía', 'Arte cinematográfico', 7, 0.4, 0.5, 0.8, 0.1, 0.4, 0.1, 0.2),

-- CARRERAS DE AGRONOMÍA Y CIENCIAS AGROPECUARIAS
('Medicina Veterinaria y Zootecnia', 'Salud animal y producción', 8, 0.4, 0.3, 0.2, 0.8, 0.3, 0.2, 0.6),
('Ingeniería Forestal', 'Manejo de bosques', 8, 0.4, 0.4, 0.3, 0.4, 0.5, 0.2, 0.8),
('Ingeniería en Biotecnología', 'Biotecnología aplicada', 8, 0.3, 0.2, 0.2, 0.5, 0.6, 0.1, 0.9),
('Zootecnia', 'Producción animal', 8, 0.5, 0.3, 0.2, 0.6, 0.4, 0.2, 0.6),

-- CARRERAS TECNOLÓGICAS ESPECIALIZADAS
('Tecnología en Sistemas', 'Desarrollo tecnológico', 39, 0.4, 0.2, 0.3, 0.1, 0.8, 0.2, 0.7),
('Tecnología Electrónica', 'Sistemas electrónicos', 39, 0.3, 0.1, 0.3, 0.1, 0.8, 0.2, 0.7),
('Tecnología Mecánica', 'Sistemas mecánicos', 39, 0.4, 0.1, 0.3, 0.1, 0.8, 0.2, 0.6),
('Tecnología en Redes', 'Administración de redes', 39, 0.3, 0.2, 0.2, 0.1, 0.8, 0.3, 0.7),

-- CARRERAS DE CIENCIAS MILITARES Y DEFENSA
('Ciencias Militares', 'Formación militar', 37, 0.4, 0.4, 0.2, 0.2, 0.3, 0.9, 0.3),
('Ingeniería Militar', 'Ingeniería aplicada a defensa', 37, 0.3, 0.2, 0.3, 0.1, 0.8, 0.8, 0.6),

-- CARRERAS EMERGENTES Y ESPECIALIZADAS
('Seguridad Industrial', 'Prevención de riesgos laborales', 30, 0.6, 0.4, 0.3, 0.3, 0.5, 0.4, 0.5),
('Gestión de la Calidad', 'Control y aseguramiento de calidad', 30, 0.7, 0.3, 0.2, 0.2, 0.4, 0.3, 0.5),
('Energías Renovables', 'Tecnologías energéticas sostenibles', 30, 0.4, 0.3, 0.3, 0.2, 0.7, 0.2, 0.8),
('Biotecnología', 'Aplicación de organismos vivos', 32, 0.3, 0.2, 0.2, 0.6, 0.6, 0.1, 0.9),
('Nanotecnología', 'Tecnología a escala nanométrica', 32, 0.2, 0.1, 0.3, 0.3, 0.8, 0.1, 0.9),
('Robótica', 'Diseño y construcción de robots', 32, 0.3, 0.1, 0.4, 0.1, 0.9, 0.2, 0.8),
('Inteligencia Artificial', 'Sistemas inteligentes', 32, 0.3, 0.2, 0.3, 0.1, 0.9, 0.1, 0.8),
('Ciberseguridad', 'Seguridad informática', 32, 0.4, 0.2, 0.2, 0.1, 0.8, 0.6, 0.7);

-- Ingeniería de Sistemas
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(1, 29), (1, 30), (1, 34), (1, 35), (1, 40), (1, 47), (1, 49);

-- Medicina
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(21, 22), (21, 23), (21, 24), (21, 25), (21, 26), (21, 27), (21, 28), (21, 49);

-- Administración de Empresas
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(35, 1), (35, 2), (35, 3), (35, 4), (35, 5), (35, 6), (35, 7), (35, 48);

-- Psicología
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(51, 8), (51, 9), (51, 10), (51, 11), (51, 12), (51, 13), (51, 14), (51, 15);

-- Arquitectura
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(79, 16), (17, 18), (79, 19), (79, 20), (79, 21), (79, 34), (79, 46);

-- Derecho
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(67, 8), (67, 9), (67, 13), (67, 14), (67, 37), (67, 38), (67, 48);

-- Ingeniería Civil
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(2, 29), (2, 30), (2, 31), (2, 34), (2, 35), (2, 46), (2, 49);

-- Comunicación Social
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(52, 8), (52, 9), (52, 11), (52, 13), (52, 16), (52, 20), (52, 46);

-- Diseño Gráfico
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(80, 16), (80, 17), (80, 18), (80, 20), (80, 21), (80, 46), (80, 49);

-- Matemáticas
INSERT INTO career_aptitude (career_id, aptitude_id) VALUES
(71, 41), (71, 42), (71, 43), (71, 45), (71, 47), (71, 49), (71, 50);


INSERT INTO users (username, email, password_hash, is_admin, created_at) VALUES
-- Estudiantes de La Paz
('maria.condori', 'maria.condori@estudiante.bo', 'pbkdf2:sha256:260000$Salt1$hash1', false, NOW()),
('carlos.quispe', 'carlos.quispe@estudiante.bo', 'pbkdf2:sha256:260000$Salt2$hash2', false, NOW()),
('ana.mamani', 'ana.mamani@estudiante.bo', 'pbkdf2:sha256:260000$Salt3$hash3', false, NOW()),
('jose.laura', 'jose.laura@estudiante.bo', 'pbkdf2:sha256:260000$Salt4$hash4', false, NOW()),
('lucia.choque', 'lucia.choque@estudiante.bo', 'pbkdf2:sha256:260000$Salt5$hash5', false, NOW()),

-- Estudiantes de Cochabamba
('sofia.morales', 'sofia.morales@estudiante.bo', 'pbkdf2:sha256:260000$Salt7$hash7', false, NOW()),
('andres.flores', 'andres.flores@estudiante.bo', 'pbkdf2:sha256:260000$Salt8$hash8', false, NOW()),
('valeria.rojas', 'valeria.rojas@estudiante.bo', 'pbkdf2:sha256:260000$Salt9$hash9', false, NOW()),
('gabriel.castro', 'gabriel.castro@estudiante.bo', 'pbkdf2:sha256:260000$Salt10$hash10', false, NOW()),

-- Estudiantes de Santa Cruz
('daniela.mendez', 'daniela.mendez@estudiante.bo', 'pbkdf2:sha256:260000$Salt11$hash11', false, NOW()),
('ricardo.paz', 'ricardo.paz@estudiante.bo', 'pbkdf2:sha256:260000$Salt12$hash12', false, NOW()),
('fernanda.silva', 'fernanda.silva@estudiante.bo', 'pbkdf2:sha256:260000$Salt13$hash13', false, NOW()),
('alejandro.herrera', 'alejandro.herrera@estudiante.bo', 'pbkdf2:sha256:260000$Salt14$hash14', false, NOW()),
('camila.torres', 'camila.torres@estudiante.bo', 'pbkdf2:sha256:260000$Salt15$hash15', false, NOW()),

-- Estudiantes de otros departamentos
('juan.santos', 'juan.santos@estudiante.bo', 'pbkdf2:sha256:260000$Salt16$hash16', false, NOW()),
('paola.gutierrez', 'paola.gutierrez@estudiante.bo', 'pbkdf2:sha256:260000$Salt17$hash17', false, NOW()),
('rodrigo.vega', 'rodrigo.vega@estudiante.bo', 'pbkdf2:sha256:260000$Salt18$hash18', false, NOW()),
('natalia.cruz', 'natalia.cruz@estudiante.bo', 'pbkdf2:sha256:260000$Salt19$hash19', false, NOW()),
('mateo.jimenez', 'mateo.jimenez@estudiante.bo', 'pbkdf2:sha256:260000$Salt20$hash20', false, NOW()),

-- Estudiantes adicionales con nombres típicos bolivianos
('esperanza.apaza', 'esperanza.apaza@estudiante.bo', 'pbkdf2:sha256:260000$Salt21$hash21', false, NOW()),
('willian.calle', 'willian.calle@estudiante.bo', 'pbkdf2:sha256:260000$Salt22$hash22', false, NOW()),
('yolanda.nina', 'yolanda.nina@estudiante.bo', 'pbkdf2:sha256:260000$Salt23$hash23', false, NOW()),
('edwin.copa', 'edwin.copa@estudiante.bo', 'pbkdf2:sha256:260000$Salt24$hash24', false, NOW()),
('roxana.limachi', 'roxana.limachi@estudiante.bo', 'pbkdf2:sha256:260000$Salt25$hash25', false, NOW()),

('marco.huanca', 'marco.huanca@estudiante.bo', 'pbkdf2:sha256:260000$Salt26$hash26', false, NOW()),
('carla.chambi', 'carla.chambi@estudiante.bo', 'pbkdf2:sha256:260000$Salt27$hash27', false, NOW()),
('sergio.colque', 'sergio.colque@estudiante.bo', 'pbkdf2:sha256:260000$Salt28$hash28', false, NOW()),
('andrea.tintaya', 'andrea.tintaya@estudiante.bo', 'pbkdf2:sha256:260000$Salt29$hash29', false, NOW()),
('rolando.ayala', 'rolando.ayala@estudiante.bo', 'pbkdf2:sha256:260000$Salt30$hash30', false, NOW());


-- ========================================
-- INSERTAR ESTUDIANTES DE EJEMPLO
-- ========================================


INSERT INTO students (user_id, first_name, last_name, birth_date, grade, school, 
                     matematicas_score, fisica_score, quimica_score, biologia_score,
                     lenguaje_score, ingles_score, ciencias_sociales_score, filosofia_score,
                     valores_score, artes_plasticas_score, educacion_musical_score, educacion_fisica_score, created_at) VALUES

(2, 'María José', 'Rodríguez Paz', '2006-03-20', '6to de secundaria', 'Unidad Educativa San Calixto',
 92, 89, 91, 85, 88, 82, 86, 84, 87, 75, 70, 78, NOW()),

(3, 'Carlos Eduardo', 'Mamani Quispe', '2005-11-08', '6to de secundaria', 'Colegio Nacional Ayacucho',
 88, 85, 83, 80, 82, 78, 85, 80, 88, 70, 65, 85, NOW()),

(4, 'Ana Sofía', 'Quispe Condori', '2006-07-12', '6to de secundaria', 'Unidad Educativa Sagrado Corazón',
 78, 75, 77, 88, 92, 85, 89, 87, 91, 88, 85, 80, NOW()),

(5, 'Diego Alejandro', 'Vargas Morales', '2005-09-25', '6to de secundaria', 'Colegio La Salle',
 95, 92, 94, 82, 85, 80, 83, 78, 82, 72, 68, 88, NOW()),

(6, 'Lucía Fernanda', 'Santos Gutiérrez', '2006-01-30', '6to de secundaria', 'Unidad Educativa Franz Tamayo',
 80, 78, 76, 85, 90, 88, 92, 89, 88, 92, 90, 82, NOW()),

(7, 'Jorge Luis', 'Flores Zenteno', '2005-05-18', '6to de secundaria', 'Colegio Nacional Junín',
 82, 85, 80, 75, 88, 82, 90, 85, 87, 78, 75, 90, NOW()),

(8, 'Sofía Alejandra', 'Choque Huanca', '2006-12-03', '5to de secundaria', 'Unidad Educativa Mariscal Braun',
 75, 72, 70, 82, 85, 80, 83, 80, 85, 95, 92, 78, NOW()),

(9, 'Ricardo Antonio', 'Torrez Silva', '2005-08-14', '6to de secundaria', 'Colegio Nacional Bolívar',
 90, 88, 85, 78, 82, 78, 88, 85, 80, 75, 70, 92, NOW());

INSERT INTO students (user_id, first_name, last_name, birth_date, grade, school, 
                     matematicas_score, fisica_score, quimica_score, biologia_score,
                     lenguaje_score, ingles_score, ciencias_sociales_score, filosofia_score,
                     valores_score, artes_plasticas_score, educacion_musical_score, educacion_fisica_score, created_at) VALUES

-- Estudiantes de La Paz (IDs 10-14)
(10, 'María Elena', 'Condori Mamani', '2005-06-15', '6to de secundaria', 'Colegio Nacional Simón Bolívar - La Paz',
 88, 85, 87, 82, 90, 78, 86, 83, 89, 75, 72, 80, NOW()),

(11, 'Carlos Alberto', 'Quispe Laura', '2005-08-22', '6to de secundaria', 'Unidad Educativa Sagrado Corazón - La Paz',
 92, 89, 88, 79, 83, 81, 85, 80, 84, 70, 68, 85, NOW()),

(12, 'Ana Patricia', 'Mamani Choque', '2006-02-10', '6to de secundaria', 'Colegio San Calixto - La Paz',
 79, 76, 78, 88, 92, 89, 91, 88, 90, 85, 82, 78, NOW()),

(13, 'José Luis', 'Laura Apaza', '2005-11-05', '6to de secundaria', 'Unidad Educativa La Salle - La Paz',
 85, 88, 83, 80, 87, 85, 89, 86, 88, 78, 75, 82, NOW()),

(14, 'Lucía Fernanda', 'Choque Huanca', '2006-04-18', '5to de secundaria', 'Colegio Nacional Ayacucho - La Paz',
 77, 74, 72, 85, 88, 86, 90, 87, 89, 92, 89, 79, NOW()),

-- Estudiantes de Cochabamba (IDs 15-19)
(15, 'Diego Alejandro', 'Vargas Morales', '2005-09-30', '6to de secundaria', 'Colegio San Agustín - Cochabamba',
 94, 91, 90, 78, 82, 79, 81, 78, 80, 72, 70, 88, NOW()),

(16, 'Sofía Alejandra', 'Morales Castro', '2006-01-12', '6to de secundaria', 'Unidad Educativa Adventista - Cochabamba',
 81, 78, 80, 84, 89, 87, 88, 85, 87, 88, 85, 81, NOW()),

(17, 'Andrés Fernando', 'Flores Zenteno', '2005-07-25', '6to de secundaria', 'Colegio Nacional Simón Bolívar - Cochabamba',
 83, 86, 84, 81, 85, 82, 87, 83, 85, 76, 73, 89, NOW()),

(18, 'Valeria Nicole', 'Rojas Gutiérrez', '2006-03-08', '5to de secundaria', 'Unidad Educativa La Salle - Cochabamba',
 78, 75, 77, 87, 91, 88, 89, 86, 88, 90, 87, 80, NOW()),

(19, 'Gabriel Rodrigo', 'Castro Silva', '2005-12-14', '6to de secundaria', 'Colegio Técnico Humanístico - Cochabamba',
 86, 89, 87, 82, 84, 81, 83, 80, 82, 75, 72, 87, NOW()),

-- Estudiantes de Santa Cruz (IDs 20-24)
(20, 'Daniela Paola', 'Méndez Torres', '2006-05-20', '6to de secundaria', 'Colegio Nacional Florida - Santa Cruz',
 80, 77, 79, 86, 90, 92, 88, 85, 87, 83, 80, 82, NOW()),

(21, 'Ricardo Antonio', 'Paz Herrera', '2005-10-03', '6to de secundaria', 'Unidad Educativa Cristo Rey - Santa Cruz',
 91, 88, 85, 79, 81, 78, 80, 77, 79, 73, 71, 90, NOW()),

(22, 'Fernanda Isabel', 'Silva Vargas', '2006-08-17', '6to de secundaria', 'Colegio San José - Santa Cruz',
 76, 73, 75, 84, 88, 90, 92, 89, 91, 86, 83, 78, NOW()),

(23, 'Alejandro José', 'Herrera Mendoza', '2005-04-11', '6to de secundaria', 'Unidad Educativa Alemana - Santa Cruz',
 89, 92, 90, 80, 83, 85, 82, 79, 81, 74, 72, 86, NOW()),

(24, 'Camila Andrea', 'Torres Rojas', '2006-06-29', '5to de secundaria', 'Colegio Experimental España - Santa Cruz',
 82, 79, 81, 83, 87, 89, 85, 82, 84, 89, 86, 83, NOW()),

-- Estudiantes de otros departamentos (IDs 25-29)
(25, 'Juan Carlos', 'Santos Limachi', '2005-09-12', '6to de secundaria', 'Colegio Nacional Bolívar - Oruro',
 85, 88, 86, 81, 84, 80, 83, 81, 83, 76, 74, 88, NOW()),

(26, 'Paola Vanessa', 'Gutiérrez Nina', '2006-02-28', '6to de secundaria', 'Unidad Educativa Sagrado Corazón - Potosí',
 79, 76, 78, 85, 89, 87, 90, 87, 89, 84, 81, 79, NOW()),

(27, 'Rodrigo Andrés', 'Vega Colque', '2005-11-20', '6to de secundaria', 'Colegio Nacional Pichincha - Tarija',
 87, 84, 82, 78, 82, 79, 85, 82, 84, 77, 75, 89, NOW()),

(28, 'Natalia Cristina', 'Cruz Tintaya', '2006-04-05', '5to de secundaria', 'Unidad Educativa Franz Tamayo - Beni',
 81, 78, 80, 88, 91, 89, 87, 84, 86, 85, 82, 80, NOW()),

(29, 'Mateo Sebastián', 'Jiménez Ayala', '2005-07-18', '6to de secundaria', 'Colegio Nacional Adolfo Ballivián - Pando',
 84, 87, 85, 82, 85, 83, 84, 81, 83, 78, 76, 87, NOW()),

-- Estudiantes adicionales (IDs 30-39)
(30, 'Esperanza del Carmen', 'Apaza Chambi', '2006-01-25', '6to de secundaria', 'Unidad Educativa Warisata - La Paz',
 76, 73, 75, 86, 90, 88, 91, 88, 90, 87, 84, 78, NOW()),

(31, 'Willian Roberto', 'Calle Huanca', '2005-08-14', '6to de secundaria', 'Colegio Nacional Gualberto Villarroel - La Paz',
 90, 93, 91, 80, 82, 79, 81, 78, 80, 72, 70, 89, NOW()),

(32, 'Yolanda Mercedes', 'Nina Copa', '2006-03-30', '5to de secundaria', 'Unidad Educativa 6 de Junio - El Alto',
 78, 75, 77, 84, 87, 85, 89, 86, 88, 90, 87, 79, NOW()),

(33, 'Edwin Marcelo', 'Copa Limachi', '2005-10-22', '6to de secundaria', 'Colegio Nacional México - El Alto',
 88, 91, 89, 81, 83, 80, 82, 79, 81, 74, 72, 88, NOW()),

(34, 'Roxana Elizabeth', 'Limachi Choque', '2006-05-15', '6to de secundaria', 'Unidad Educativa Eduardo Avaroa - Oruro',
 80, 77, 79, 85, 88, 86, 87, 84, 86, 86, 83, 81, NOW()),

(35, 'Marco Antonio', 'Huanca Mamani', '2005-12-08', '6to de secundaria', 'Colegio Nacional Camacho - Potosí',
 86, 89, 87, 79, 81, 78, 83, 80, 82, 75, 73, 87, NOW()),

(36, 'Carla Verónica', 'Chambi Quispe', '2006-06-18', '5to de secundaria', 'Unidad Educativa San Luis - Tarija',
 77, 74, 76, 87, 90, 88, 89, 86, 88, 88, 85, 78, NOW()),

(37, 'Sergio Daniel', 'Colque Laura', '2005-09-03', '6to de secundaria', 'Colegio Nacional Eliodoro Camacho - Beni',
 84, 87, 85, 82, 84, 81, 84, 81, 83, 76, 74, 86, NOW()),

(38, 'Andrea Soledad', 'Tintaya Vargas', '2006-02-14', '6to de secundaria', 'Unidad Educativa Nuestra Señora de Fátima - Pando',
 81, 78, 80, 84, 87, 89, 86, 83, 85, 84, 81, 82, NOW());


-- ========================================
-- INSERTAR TEST ANSWERS DE EJEMPLO
-- ========================================

INSERT INTO test_answers (student_id, test_date, score_c, score_h, score_a, score_s, score_i, score_d, score_e, answers_json) VALUES

-- Tests para estudiantes 10-19
(10, NOW() - INTERVAL '1 day', 6, 8, 5, 7, 4, 3, 6, '{"1": false, "2": true, "3": true, "4": true, "5": false, "6": false, "7": true}'),
(11, NOW() - INTERVAL '2 days', 9, 4, 3, 2, 8, 5, 7, '{"1": true, "2": true, "3": false, "4": false, "5": true, "6": true, "7": true}'),
(12, NOW() - INTERVAL '3 days', 4, 9, 7, 6, 2, 3, 4, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(13, NOW() - INTERVAL '4 days', 7, 7, 4, 5, 6, 4, 5, '{"1": true, "2": false, "3": true, "4": true, "5": true, "6": false, "7": true}'),
(14, NOW() - INTERVAL '5 days', 3, 8, 9, 4, 2, 2, 3, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(15, NOW() - INTERVAL '6 days', 8, 3, 2, 3, 9, 6, 8, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),
(16, NOW() - INTERVAL '7 days', 5, 6, 8, 7, 3, 2, 4, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(17, NOW() - INTERVAL '8 days', 6, 5, 4, 4, 7, 8, 6, '{"1": false, "2": true, "3": true, "4": true, "5": true, "6": false, "7": true}'),
(18, NOW() - INTERVAL '9 days', 4, 7, 8, 6, 3, 2, 5, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(19, NOW() - INTERVAL '10 days', 7, 4, 3, 3, 8, 6, 7, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),

-- Tests para estudiantes 20-29
(20, NOW() - INTERVAL '11 days', 5, 8, 6, 5, 3, 3, 4, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(21, NOW() - INTERVAL '12 days', 8, 3, 2, 2, 9, 7, 8, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),
(22, NOW() - INTERVAL '13 days', 4, 9, 7, 5, 2, 3, 3, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(23, NOW() - INTERVAL '14 days', 6, 4, 3, 3, 8, 5, 9, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),
(24, NOW() - INTERVAL '15 days', 5, 7, 8, 6, 3, 2, 4, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(25, NOW() - INTERVAL '16 days', 7, 5, 4, 4, 7, 6, 6, '{"1": false, "2": true, "3": true, "4": true, "5": true, "6": false, "7": true}'),
(26, NOW() - INTERVAL '17 days', 4, 8, 7, 6, 2, 3, 4, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(27, NOW() - INTERVAL '18 days', 6, 4, 3, 3, 8, 7, 7, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),
(28, NOW() - INTERVAL '19 days', 5, 7, 6, 8, 3, 2, 5, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(29, NOW() - INTERVAL '20 days', 7, 4, 3, 4, 7, 6, 7, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),

-- Tests para estudiantes 30-39
(30, NOW() - INTERVAL '21 days', 3, 9, 8, 6, 2, 2, 3, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(31, NOW() - INTERVAL '22 days', 8, 3, 2, 2, 9, 6, 9, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),
(32, NOW() - INTERVAL '23 days', 4, 8, 9, 5, 2, 2, 3, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(33, NOW() - INTERVAL '24 days', 7, 4, 3, 3, 8, 5, 8, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),
(34, NOW() - INTERVAL '25 days', 5, 7, 8, 7, 3, 2, 4, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(35, NOW() - INTERVAL '26 days', 6, 4, 3, 3, 8, 6, 7, '{"1": true, "2": false, "3": false, "4": false, "5": true, "6": true, "7": true}'),
(36, NOW() - INTERVAL '27 days', 4, 8, 8, 6, 2, 3, 4, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}'),
(37, NOW() - INTERVAL '28 days', 6, 5, 4, 4, 7, 6, 6, '{"1": false, "2": true, "3": true, "4": true, "5": true, "6": false, "7": true}'),
(38, NOW() - INTERVAL '29 days', 5, 7, 7, 6, 3, 3, 4, '{"1": false, "2": false, "3": true, "4": true, "5": false, "6": false, "7": false}');

-- ========================================
-- INSERTAR RECOMENDACIONES DE EJEMPLO
-- ========================================

INSERT INTO recommendations (student_id, career_id, score, rank, explanation, model_used, created_at) VALUES

-- Recomendaciones para María José (Estudiante 2) - Perfil orientado a Medicina
(2, 10, 0.92, 1, '{"career_name": "Medicina", "compatibility_score": 92, "main_areas": ["Ciencias de la salud"], "reason": "Excelente compatibilidad con ciencias de la salud y rendimiento académico sobresaliente"}', 'rule_based', NOW()),
(2, 13, 0.85, 2, '{"career_name": "Bioquímica y Farmacia", "compatibility_score": 85, "main_areas": ["Ciencias de la salud", "Ciencias exactas"], "reason": "Muy buena compatibilidad con ciencias de la salud y química"}', 'rule_based', NOW()),
(2, 15, 0.78, 3, '{"career_name": "Nutrición y Dietética", "compatibility_score": 78, "main_areas": ["Ciencias de la salud"], "reason": "Buena compatibilidad con el área de salud"}', 'rule_based', NOW()),

-- Recomendaciones para Carlos (Estudiante 3) - Perfil orientado a Ingeniería
(3, 1, 0.89, 1, '{"career_name": "Ingeniería de Sistemas", "compatibility_score": 89, "main_areas": ["Ingeniería", "Ciencias exactas"], "reason": "Excelente perfil para ingeniería de sistemas con fuertes habilidades técnicas"}', 'rule_based', NOW()),
(3, 3, 0.82, 2, '{"career_name": "Ingeniería Industrial", "compatibility_score": 82, "main_areas": ["Ingeniería", "Administrativas"], "reason": "Muy buena compatibilidad con ingeniería e intereses administrativos"}', 'rule_based', NOW()),
(3, 5, 0.75, 3, '{"career_name": "Ingeniería Electrónica", "compatibility_score": 75, "main_areas": ["Ingeniería"], "reason": "Buena compatibilidad con el área de ingeniería"}', 'rule_based', NOW()),

-- Recomendaciones para Ana Sofía (Estudiante 4) - Perfil orientado a Humanidades
(4, 23, 0.88, 1, '{"career_name": "Psicología", "compatibility_score": 88, "main_areas": ["Humanísticas", "Ciencias de la salud"], "reason": "Excelente compatibilidad con humanidades y aptitudes para el trabajo con personas"}', 'rule_based', NOW()),
(4, 24, 0.82, 2, '{"career_name": "Comunicación Social", "compatibility_score": 82, "main_areas": ["Humanísticas", "Artísticas"], "reason": "Muy buena compatibilidad con comunicación y expresión"}', 'rule_based', NOW()),
(4, 25, 0.79, 3, '{"career_name": "Trabajo Social", "compatibility_score": 79, "main_areas": ["Humanísticas"], "reason": "Buena compatibilidad con el trabajo social y comunitario"}', 'rule_based', NOW()),

-- Recomendaciones para Diego (Estudiante 5) - Perfil orientado a Ciencias Exactas/Ingeniería
(5, 4, 0.91, 1, '{"career_name": "Ingeniería Eléctrica", "compatibility_score": 91, "main_areas": ["Ingeniería", "Ciencias exactas"], "reason": "Excelente perfil para ingeniería eléctrica con sobresalientes calificaciones en matemáticas y física"}', 'rule_based', NOW()),
(5, 31, 0.87, 2, '{"career_name": "Física", "compatibility_score": 87, "main_areas": ["Ciencias exactas"], "reason": "Muy buena compatibilidad con ciencias exactas y física"}', 'rule_based', NOW()),
(5, 30, 0.84, 3, '{"career_name": "Matemáticas", "compatibility_score": 84, "main_areas": ["Ciencias exactas"], "reason": "Excelente desempeño en matemáticas"}', 'rule_based', NOW()),

-- Recomendaciones para Lucía (Estudiante 6) - Perfil orientado a Artes/Humanidades
(6, 35, 0.90, 1, '{"career_name": "Diseño Gráfico", "compatibility_score": 90, "main_areas": ["Artísticas"], "reason": "Excelente compatibilidad con artes visuales y diseño"}', 'rule_based', NOW()),
(6, 34, 0.85, 2, '{"career_name": "Arquitectura", "compatibility_score": 85, "main_areas": ["Artísticas", "Ingeniería"], "reason": "Muy buena compatibilidad combinando arte y técnica"}', 'rule_based', NOW()),
(6, 36, 0.82, 3, '{"career_name": "Artes Plásticas", "compatibility_score": 82, "main_areas": ["Artísticas"], "reason": "Excelente aptitud artística"}', 'rule_based', NOW()),

-- Recomendaciones para Jorge (Estudiante 7) - Perfil orientado a Defensa/Humanidades
(7, 29, 0.83, 1, '{"career_name": "Derecho", "compatibility_score": 83, "main_areas": ["Humanísticas", "Defensa"], "reason": "Buena compatibilidad con ciencias jurídicas y justicia"}', 'rule_based', NOW()),
(7, 30, 0.78, 2, '{"career_name": "Ciencias Políticas", "compatibility_score": 78, "main_areas": ["Humanísticas", "Defensa"], "reason": "Buena compatibilidad con ciencias políticas"}', 'rule_based', NOW()),
(7, 45, 0.75, 3, '{"career_name": "Administración Pública", "compatibility_score": 75, "main_areas": ["Administrativas", "Humanísticas"], "reason": "Buena compatibilidad con administración pública"}', 'rule_based', NOW()),

-- Recomendaciones para Sofía (Estudiante 8) - Perfil orientado a Artes
(8, 37, 0.94, 1, '{"career_name": "Música", "compatibility_score": 94, "main_areas": ["Artísticas"], "reason": "Excelente compatibilidad con educación musical y artes"}', 'rule_based', NOW()),
(8, 36, 0.88, 2, '{"career_name": "Artes Plásticas", "compatibility_score": 88, "main_areas": ["Artísticas"], "reason": "Muy buena compatibilidad con artes visuales"}', 'rule_based', NOW()),
(8, 35, 0.85, 3, '{"career_name": "Diseño Gráfico", "compatibility_score": 85, "main_areas": ["Artísticas"], "reason": "Buena compatibilidad con diseño y comunicación visual"}', 'rule_based', NOW()),

-- Recomendaciones para Ricardo (Estudiante 9) - Perfil orientado a Ingeniería/Defensa
(9, 2, 0.86, 1, '{"career_name": "Ingeniería Civil", "compatibility_score": 86, "main_areas": ["Ingeniería"], "reason": "Buena compatibilidad con ingeniería civil y construcción"}', 'rule_based', NOW()),
(9, 6, 0.82, 2, '{"career_name": "Ingeniería Mecánica", "compatibility_score": 82, "main_areas": ["Ingeniería"], "reason": "Buena compatibilidad con ingeniería mecánica"}', 'rule_based', NOW()),
(9, 38, 0.78, 3, '{"career_name": "Ingeniería Agronómica", "compatibility_score": 78, "main_areas": ["Ingeniería", "Ciencias exactas"], "reason": "Buena compatibilidad con ingeniería agronómica"}', 'rule_based', NOW());

-- ========================================
-- CREAR ÍNDICES PARA MEJOR RENDIMIENTO
-- ========================================

CREATE INDEX IF NOT EXISTS idx_students_user_id ON students(user_id);
CREATE INDEX IF NOT EXISTS idx_careers_faculty_id ON careers(faculty_id);
CREATE INDEX IF NOT EXISTS idx_test_answers_student_id ON test_answers(student_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_student_id ON recommendations(student_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_career_id ON recommendations(career_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_score ON recommendations(score DESC);

-- ========================================
-- VERIFICAR DATOS INSERTADOS
-- ========================================

-- Verificar conteos
SELECT 'Usuarios' as tabla, COUNT(*) as total FROM users
UNION ALL
SELECT 'Estudiantes' as tabla, COUNT(*) as total FROM students
UNION ALL
SELECT 'Facultades' as tabla, COUNT(*) as total FROM faculties
UNION ALL
SELECT 'Carreras' as tabla, COUNT(*) as total FROM careers
UNION ALL
SELECT 'Test Answers' as tabla, COUNT(*) as total FROM test_answers
UNION ALL
SELECT 'Recomendaciones' as tabla, COUNT(*) as total FROM recommendations;

-- ========================================
-- CONSULTAS DE EJEMPLO
-- ========================================

-- Ver carreras por facultad
-- SELECT f.name as facultad, COUNT(c.id) as num_carreras
-- FROM faculties f
-- LEFT JOIN careers c ON f.id = c.faculty_id
-- GROUP BY f.id, f.name
-- ORDER BY num_carreras DESC;

-- Ver estudiantes con sus recomendaciones principales
-- SELECT s.first_name, s.last_name, c.name as carrera_recomendada, r.score
-- FROM students s
-- JOIN recommendations r ON s.id = r.student_id AND r.rank = 1
-- JOIN careers c ON r.career_id = c.id
-- ORDER BY r.score DESC;