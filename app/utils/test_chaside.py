class TestChaside:
    """
    Implementación del test vocacional CHASIDE para determinar intereses y aptitudes
    basado en el test estándar de 98 preguntas
    """
    
    def __init__(self):
        self.areas = {
            'C': {'name': 'Administrativas y contables', 'interests': [], 'aptitudes': []},
            'H': {'name': 'Humanísticas y ciencias sociales y jurídicas', 'interests': [], 'aptitudes': []},
            'A': {'name': 'Artísticas', 'interests': [], 'aptitudes': []},
            'S': {'name': 'Ciencias de la salud', 'interests': [], 'aptitudes': []},
            'I': {'name': 'Enseñanzas técnicas e ingenierías', 'interests': [], 'aptitudes': []},
            'D': {'name': 'Defensa y seguridad', 'interests': [], 'aptitudes': []},
            'E': {'name': 'Ciencias experimentales', 'interests': [], 'aptitudes': []}
        }
        
        # Mapeo de números de preguntas a áreas para intereses
        self.interest_map = {
            1: 'C', 9: 'H', 3: 'A', 8: 'S', 6: 'I', 5: 'D', 17: 'E',
            12: 'C', 25: 'H', 11: 'A', 16: 'S', 19: 'I', 14: 'D', 32: 'E',
            20: 'C', 34: 'H', 21: 'A', 23: 'S', 27: 'I', 24: 'D', 35: 'E',
            53: 'C', 41: 'H', 28: 'A', 33: 'S', 38: 'I', 31: 'D', 42: 'E',
            64: 'C', 56: 'H', 36: 'A', 44: 'S', 47: 'I', 37: 'D', 49: 'E',
            71: 'C', 67: 'H', 45: 'A', 52: 'S', 54: 'I', 48: 'D', 61: 'E',
            78: 'C', 74: 'H', 50: 'A', 62: 'S', 60: 'I', 58: 'D', 68: 'E',
            85: 'C', 80: 'H', 57: 'A', 70: 'S', 75: 'I', 65: 'D', 77: 'E',
            91: 'C', 89: 'H', 81: 'A', 87: 'S', 83: 'I', 73: 'D', 88: 'E',
            98: 'C', 95: 'H', 96: 'A', 92: 'S', 97: 'I', 84: 'D', 93: 'E'
        }
        
        # Mapeo de números de preguntas a áreas para aptitudes
        self.aptitude_map = {
            2: 'C', 30: 'H', 22: 'A', 4: 'S', 10: 'I', 13: 'D', 7: 'E',
            15: 'C', 63: 'H', 39: 'A', 29: 'S', 26: 'I', 18: 'D', 55: 'E',
            46: 'C', 72: 'H', 76: 'A', 40: 'S', 59: 'I', 43: 'D', 79: 'E',
            51: 'C', 86: 'H', 82: 'A', 69: 'S', 90: 'I', 66: 'D', 94: 'E'
        }
        
        # Inicialización de intereses y aptitudes por área
        self._initialize_test_items()
    
    def _initialize_test_items(self):
        """Inicializa las preguntas del test CHASIDE según la versión estándar"""
        
        # Intereses - Las preguntas reales del test
        self.interests_questions = {
            1: "¿Aceptarías trabajar escribiendo artículos en la sección económica de un diario?",
            2: "¿Te ofrecerías para organizar la despedida de soltero de uno de tus amigos?",
            3: "¿Te gustaría dirigir/crear un proyecto de urbanización en tu provincia?",
            4: "¿A una frustración siempre opones un pensamiento positivo?",
            5: "¿Te dedicarías a socorrer a personas accidentadas o atacadas por asaltantes?",
            6: "¿Cuando eras chico, te interesaba saber cómo estaban construidos tus juguetes?",
            7: "¿Te interesan más los misterios de la naturaleza que los secretos de la tecnología?",
            8: "¿Escuchas atentamente los problemas que te plantean tus amigos?",
            9: "¿Te ofrecerías para explicar a tus compañeros un determinado tema que ellos no entendieron?",
            10: "¿Eres exigente y crítico con tu equipo de trabajo?",
            11: "¿Te atrae armar rompecabezas o puzzles?",
            12: "¿Te gustaría conocer la diferencia entre macroeconomía y microeconomía?",
            13: "¿Usar uniforme te hace sentir distinto, importante?",
            14: "¿Participarías como profesional en un espectáculo de acrobacia aérea?",
            15: "¿Organizas tu dinero de manera que te alcance hasta el próximo cobro?",
            16: "¿Convences fácilmente a otras personas sobre la validez de tus argumentos?",
            17: "¿Te gustaría estar informado sobre los nuevos descubrimientos que se están realizando sobre el origen del Universo?",
            18: "¿Ante una situación de emergencia actúas rápidamente?",
            19: "¿Cuando tienes que resolver un problema matemático, perseveras hasta encontrar la solución?",
            20: "¿Si te convocara tu club preferido para planificar, organizar y dirigir un campo de deportes, aceptarías?",
            21: "¿Eres el que pone un toque de alegría en las fiestas?",
            22: "¿Crees que los detalles son tan importantes como el todo?",
            23: "¿Te sentirías a gusto trabajando en un ámbito hospitalario?",
            24: "¿Te gustaría participar para mantener el orden ante grandes desórdenes y cataclismos?",
            25: "¿Pasarías varias horas leyendo algún libro de tu interés?",
            26: "¿Planificas detalladamente tus trabajos antes de empezar?",
            27: "¿Entablas una relación casi personal con tu ordenador?",
            28: "¿Disfrutas modelando con arcilla?",
            29: "¿Ayudas habitualmente a los no videntes (a quien lo necesite) a cruzar la calle?",
            30: "¿Consideras importante que desde la educación secundaria se fomente la actitud crítica y la participación activa?",
            31: "¿Aceptarías que las mujeres formaran parte de las fuerzas armadas bajo las mismas normas que los hombres?",
            32: "¿Te gustaría crear nuevas técnicas para descubrir las patologías de algunas enfermedades a través del microscopio?",
            33: "¿Participarías en una campaña de prevención contra la enfermedad como el sida?",
            34: "¿Te interesan los temas relacionados al pasado y a la evolución del hombre?",
            35: "¿Te incluirías en un proyecto de investigación de los movimientos sísmicos y sus consecuencias?",
            36: "¿Fuera de los horarios escolares, dedicas algún día de la semana a la realización de actividades corporales?",
            37: "¿Te interesan las actividades de mucha acción y de reacción rápida en situaciones imprevistas y de algún peligro?",
            38: "¿Te ofrecerías para colaborar como voluntario en los gabinetes espaciales de la NASA?",
            39: "¿Te gusta más el trabajo manual que el trabajo intelectual?",
            40: "¿Estarías dispuesto a renunciar a un momento placentero para ofrecer tu servicio como profesional(ayudando)?",
            41: "¿Participarías de una investigación sobre la violencia en el fútbol?",
            42: "¿Te gustaría trabajar en un laboratorio mientras estudias?",
            43: "¿Arriesgarías tu vida para salvar la vida de otro que no conoces?",
            44: "¿Te agradaría hacer un curso de primeros auxilios?",
            45: "¿Tolerarías empezar tantas veces como fuere necesario hasta obtener el logro deseado?",
            46: "¿Distribuyes tu horarios del día adecuadamente para poder hacer todo lo planeado?",
            47: "¿Harías un curso para aprender a fabricar los instrumentos y/o piezas de las máquinas o aparatos con que trabajas?",
            48: "¿Elegirías una profesión en la tuvieras que estar algunos meses alejado de tu familia, por ejemplo el marino?",
            49: "¿Te radicarías en una zona agrícola-ganadera para desarrollar tus actividades como profesional?",
            50: "¿Cuando estás en un grupo trabajando, te entusiasma producir ideas originales y que sean tenidas en cuenta?",
            51: "¿Te resulta fácil coordinar un grupo de trabajo?",
            52: "¿Te resultó interesante el estudio de las ciencias biológicas?",
            53: "¿Si una gran empresa solicita un profesional como gerente de comercialización, te sentirías a gusto desempeñando ese rol?",
            54: "¿Te incluirías en un proyecto nacional de desarrollo de la principal fuente de recursos de tu provincia?",
            55: "¿Tienes interés por saber cuales son las causas que determinan ciertos fenómenos, aunque saberlo no altere tu vida?",
            56: "¿Descubriste algún filósofo o escritor que haya expresado tus mismas ideas con antelación?",
            57: "¿Desearías que te regalen algún instrumento musical para tu cumpleaños?",
            58: "¿Aceptarías colaborar con el cumplimiento de las normas en lugares públicos?",
            59: "¿Crees que tus ideas son importantes, y haces todo lo posible para ponerlas en práctica?",
            60: "¿Cuando se descompone un artefacto en tu casa, te dispones prontamente a repararlo?",
            61: "¿Formarías parte de un equipo de trabajo orientado a la preservación de la flora y la fauna en extinción?",
            62: "¿Leerías revistas relacionadas con los últimos avances científicos y tecnológicos en el área de la salud?",
            63: "¿Preservar las raíces culturales de nuestro país, te parece importante y necesario?",
            64: "¿Te gustaría realizar una investigación que contribuyera a hacer más justa la distribución de la riqueza?",
            65: "¿Te gustaría realizar tareas auxiliares en una nave, como por ejemplo izado y arriado de velas, pintura y conservación del casco, arreglo de averías, conservación de motores, etc.?",
            66: "¿Crees que un país debe poseer la más alta tecnología armamentista, a cualquier precio?",
            67: "¿La libertad y la justicia son valores fundamentales en tu vida?",
            68: "¿Aceptarías hacer una práctica pagadas en una industria de productos alimenticios en el sector de control de calidad?",
            69: "¿Consideras que la salud pública debe ser prioritaria, gratuita y eficiente para todos?",
            70: "¿Te interesaría investigar sobre alguna nueva vacuna?",
            71: "¿En un equipo de trabajo, preferís el rol de coordinador?",
            72: "¿En una discusión entre amigos, te ofreces como mediador?",
            73: "¿Estás de acuerdo con la formación de un cuerpo de soldados profesionales?",
            74: "¿Lucharías por una causa justa hasta las últimas consecuencias?",
            75: "¿Te gustaría investigar científicamente sobre cultivos agrícolas?",
            76: "¿Harías un nuevo diseño de una prenda pasada de moda, ante una reunión?",
            77: "¿Visitarías un observatorio astronómico para conocer en acción el funcionamiento de los aparatos?",
            78: "¿Dirigirías el área de importación y exportación de una empresa?",
            79: "¿Te cohíbes/inhibes –cortas- al entrar a un lugar nuevo con gente desconocida?",
            80: "¿Te gratificaría el trabajar con niños?",
            81: "¿Harías el diseño de un cartel o afiche para una campaña contra el sida?",
            82: "¿Dirigirías un grupo de teatro independiente?",
            83: "¿Enviarías tu curriculum a una empresa automotriz que solicita gerente para su área de producción?",
            84: "¿Participarías en un grupo de defensa internacional dentro de alguna fuerza armada?",
            85: "¿Te costearías tus estudios trabajando en una auditoría –revisión de las cuentas-?",
            86: "¿Eres de los que defiendes causas perdidas?",
            87: "¿Ante una emergencia epidémica participarías en una campaña brindando tu ayuda?",
            88: "¿Sabrías responder que significa ADN o ARN?",
            89: "¿Elegirías una carrera cuyo instrumento de trabajo fuere la utilización de un idioma extranjero?",
            90: "¿Trabajar con objetos, máquinas, te resulta más gratificante que trabajar con personas?",
            91: "¿Te resultaría gratificante ser asesor contable en una empresa reconocida?",
            92: "¿Ante un llamado solidario, te ofrecerías para cuidar a un enfermo?",
            93: "¿Te atrae investigar sobre los misterios del universo, por ejemplo los agujeros negros?",
            94: "¿El trabajo individual te resulta más rápido y efectivo que el trabajo grupal?",
            95: "¿Dedicarías parte de tu tiempo a ayudar a personas con carencias o necesitadas?",
            96: "¿Cuando eliges tu ropa o decoras un ambiente, tienes en cuenta la combinación de los colores, las telas o el estilo de los muebles?",
            97: "¿Te gustaría trabajar como profesional dirigiendo la construcción de una empresa hidroeléctrica?",
            98: "¿Sabes qué es el PIB? Se trata de un concepto económico. ¿Te gusta este tipo de tema?"
        }
    
    def get_questions(self):
        """Devuelve todas las preguntas del test organizadas por número"""
        return self.interests_questions  # Debe ser un diccionario {1: "¿Pregunta 1?", 2: "¿Pregunta 2?", ...}

    def calculate_scores(self, answers):
        """
        Calcula las puntuaciones por área basado en las respuestas
        
        Args:
            answers: Diccionario con las respuestas en formato 
                    {1: True, 2: False, 3: True, ...}
                    donde True = Sí, False = No
        
        Returns:
            Diccionario con las puntuaciones totales por área y separadas por intereses y aptitudes
        """
        scores = {
            'C': {'interests': 0, 'aptitudes': 0, 'total': 0},
            'H': {'interests': 0, 'aptitudes': 0, 'total': 0},
            'A': {'interests': 0, 'aptitudes': 0, 'total': 0},
            'S': {'interests': 0, 'aptitudes': 0, 'total': 0},
            'I': {'interests': 0, 'aptitudes': 0, 'total': 0},
            'D': {'interests': 0, 'aptitudes': 0, 'total': 0},
            'E': {'interests': 0, 'aptitudes': 0, 'total': 0}
        }
        
        # Procesar respuestas para intereses
        for question_id_str, is_yes in answers.items():
            if not is_yes:
                continue
                
            question_id = int(question_id_str)
            
            # Verificar si es una pregunta de interés
            if question_id in self.interest_map:
                area = self.interest_map[question_id]
                scores[area]['interests'] += 1
            
            # Verificar si es una pregunta de aptitud
            elif question_id in self.aptitude_map:
                area = self.aptitude_map[question_id]
                scores[area]['aptitudes'] += 1
        
        # Calcular totales
        for area in scores:
            scores[area]['total'] = scores[area]['interests'] + scores[area]['aptitudes']
        
        return scores
    
    def get_recommended_areas(self, scores, top_n=2):
        """
        Devuelve las áreas más recomendadas basado en las puntuaciones
        
        Args:
            scores: Diccionario con las puntuaciones por área
            top_n: Número de áreas a recomendar
        
        Returns:
            Lista de tuplas (área, puntuación) ordenadas de mayor a menor
        """
        # Ordenar áreas por puntuación total
        sorted_areas = sorted(
            [(area, data['total']) for area, data in scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_areas[:top_n]
    
    def get_area_characteristics(self, area_code):
        """
        Devuelve las características (intereses y aptitudes) asociadas a un área
        
        Args:
            area_code: Código del área (C, H, A, S, I, D, E)
        
        Returns:
            Diccionario con características del área
        """
        area_info = {
            'C': {
                'name': 'Administrativas y contables',
                'interests': ['Organización', 'Supervisión', 'Orden', 'Análisis y síntesis', 'Colaboración', 'Cálculo'],
                'aptitudes': ['Persuasivo', 'Objetivo', 'Práctico', 'Tolerante', 'Responsable', 'Ambicioso']
            },
            'H': {
                'name': 'Humanidades y Ciencias Sociales y Jurídicas',
                'interests': ['Precisión Verbal', 'Organización', 'Relación de hechos', 'Lingüística', 'Orden', 'Justicia'],
                'aptitudes': ['Responsable', 'Justo', 'Conciliador', 'Persuasivo', 'Sagaz', 'Imaginativo']
            },
            'A': {
                'name': 'Artística',
                'interests': ['Estético', 'Armónico', 'Manual', 'Visual', 'Auditivo', 'Sensible'],
                'aptitudes': ['Imaginativo', 'Creativo', 'Detallista', 'Innovador', 'Intuitivo']
            },
            'S': {
                'name': 'Ciencias de la Salud',
                'interests': ['Asistir', 'Investigar', 'Precisión', 'Percepción', 'Análisis', 'Ayudar'],
                'aptitudes': ['Altruista', 'Solidario', 'Paciente', 'Comprensivo', 'Respetuoso', 'Persuasivo']
            },
            'I': {
                'name': 'Enseñanzas Técnicas',
                'interests': ['Cálculo', 'Científico', 'Manual', 'Exactitud', 'Planificar', 'Preciso'],
                'aptitudes': ['Práctico', 'Crítico', 'Analítico', 'Rígido']
            },
            'D': {
                'name': 'Defensa y Seguridad',
                'interests': ['Justicia', 'Equidad', 'Colaboración', 'Espíritu de equipo', 'Liderazgo'],
                'aptitudes': ['Arriesgado', 'Solidario', 'Valiente', 'Agresivo', 'Persuasivo']
            },
            'E': {
                'name': 'Ciencias Experimentales',
                'interests': ['Investigación', 'Orden', 'Organización', 'Análisis y Síntesis', 'Cálculo numérico', 'Clasificar'],
                'aptitudes': ['Metódico', 'Analítico', 'Observador', 'Introvertido', 'Paciente', 'Seguro']
            }
        }
        
        return area_info.get(area_code, {})
    
    def get_careers_by_area(self, area_code):
        """
        Devuelve las carreras recomendadas para un área específica
        
        Args:
            area_code: Código del área (C, H, A, S, I, D, E)
        
        Returns:
            Lista de carreras recomendadas para esa área
        """
        careers_by_area = {
            'C': [
                'Administración de Empresas',
                'Contabilidad',
                'Economía',
                'Marketing',
                'Finanzas',
                'Comercio Internacional',
                'Gestión de Recursos Humanos'
            ],
            'H': [
                'Derecho',
                'Psicología',
                'Sociología',
                'Historia',
                'Filosofía',
                'Antropología',
                'Ciencias Políticas',
                'Trabajo Social',
                'Comunicación Social',
                'Relaciones Internacionales'
            ],
            'A': [
                'Diseño Gráfico',
                'Diseño de Interiores',
                'Arquitectura',
                'Bellas Artes',
                'Música',
                'Teatro',
                'Danza',
                'Cine y Audiovisuales',
                'Diseño de Moda',
                'Fotografía'
            ],
            'S': [
                'Medicina',
                'Enfermería',
                'Odontología',
                'Fisioterapia',
                'Nutrición',
                'Farmacia',
                'Veterinaria',
                'Bioquímica',
                'Terapia Ocupacional',
                'Fonoaudiología'
            ],
            'I': [
                'Ingeniería de Sistemas',
                'Ingeniería Civil',
                'Ingeniería Industrial',
                'Ingeniería Eléctrica',
                'Ingeniería Mecánica',
                'Ingeniería Electrónica',
                'Ingeniería de Software',
                'Arquitectura de Computadores',
                'Robótica',
                'Telecomunicaciones'
            ],
            'D': [
                'Ciencias Militares',
                'Ciencias Policiales',
                'Ciencias Navales',
                'Ciencias Aeronáuticas',
                'Criminología',
                'Seguridad Pública',
                'Gestión de Desastres',
                'Defensa Civil'
            ],
            'E': [
                'Física',
                'Química',
                'Biología',
                'Matemáticas',
                'Geología',
                'Astronomía',
                'Biotecnología',
                'Ciencias Ambientales',
                'Meteorología',
                'Geografía'
            ]
        }
        
        return careers_by_area.get(area_code, [])