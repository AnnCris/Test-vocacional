import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

class ChartGenerator:
    """
    Clase para generar gráficos y visualizaciones para los resultados del test
    """
    
    @staticmethod
    def generate_radar_chart(scores, max_value=10):
        """
        Genera un gráfico de radar para los puntajes CHASIDE
        
        Args:
            scores: Diccionario con los puntajes por área
            max_value: Valor máximo para normalizar (por defecto 10)
            
        Returns:
            str: Imagen en formato base64
        """
        # Configurar matplotlib
        plt.figure(figsize=(8, 8))
        
        # Categorías del radar (áreas CHASIDE)
        categories = ['Administrativas (C)', 'Humanísticas (H)', 'Artísticas (A)', 
                    'Salud (S)', 'Ingenierías (I)', 'Defensa (D)', 'Científicas (E)']
        
        # Convertir puntuaciones a una lista en el mismo orden
        values = [
            scores.get('C', 0),
            scores.get('H', 0),
            scores.get('A', 0),
            scores.get('S', 0),
            scores.get('I', 0),
            scores.get('D', 0),
            scores.get('E', 0)
        ]
        
        # Número de variables
        N = len(categories)
        
        # Ángulos para cada eje (dividir la circunferencia)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Cerrar el círculo
        
        # Valores para cada eje
        values_normalized = [v / max_value for v in values]  # Normalizar de 0 a 1
        values_normalized += values_normalized[:1]  # Cerrar el círculo
        
        # Crear el trazado
        ax = plt.subplot(111, polar=True)
        
        # Dibujar el polígono y los puntos
        ax.plot(angles, values_normalized, 'o-', linewidth=2, color='#0d6efd')
        ax.fill(angles, values_normalized, alpha=0.25, color='#0d6efd')
        
        # Definir límites del gráfico
        ax.set_ylim(0, 1)
        
        # Etiquetar los ejes
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        
        # Etiquetas para los valores de los ejes
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels([f"{int(x * max_value)}" for x in [0.2, 0.4, 0.6, 0.8, 1.0]])
        
        # Título
        plt.title('Perfil de Intereses y Aptitudes', size=15, y=1.1)
        
        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        
        # Convertir imagen a base64
        image_png = buffer.getvalue()
        buffer.close()
        
        encoded = base64.b64encode(image_png).decode('utf-8')
        return f"data:image/png;base64,{encoded}"
    
    @staticmethod
    def generate_bar_chart(career_scores, top_n=5):
        """
        Genera un gráfico de barras para las carreras recomendadas
        
        Args:
            career_scores: Lista de tuplas (nombre_carrera, puntuación)
            top_n: Número de carreras a mostrar (por defecto 5)
            
        Returns:
            str: Imagen en formato base64
        """
        # Filtrar top N carreras
        top_careers = sorted(career_scores, key=lambda x: x[1], reverse=True)[:top_n]
        
        # Extraer nombres y puntuaciones
        names = [career[0] for career in top_careers]
        scores = [career[1] * 100 for career in top_careers]  # Convertir a porcentaje
        
        # Crear gráfico
        plt.figure(figsize=(10, 6))
        
        # Colores degradados
        colors = plt.cm.Blues(np.linspace(0.6, 1.0, len(names)))
        
        # Crear barras horizontales
        bars = plt.barh(names, scores, color=colors)
        
        # Añadir etiquetas con valores
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f"{width:.1f}%", ha='left', va='center')
        
        # Configurar ejes
        plt.xlabel('Compatibilidad (%)')
        plt.ylabel('Carreras')
        plt.title('Carreras Recomendadas')
        
        # Ajustar límites
        plt.xlim(0, 105)  # Dar espacio para las etiquetas
        
        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        
        # Convertir imagen a base64
        image_png = buffer.getvalue()
        buffer.close()
        
        encoded = base64.b64encode(image_png).decode('utf-8')
        return f"data:image/png;base64,{encoded}"