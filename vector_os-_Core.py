import numpy as np

class SistemaVectorialOS:
    def __init__(self):
        # Creamos una matriz virtual de nodos (nuestra mini-galaxia de datos)
        # Cada nodo tiene una coordenada X, Y, Z fija
        self.espacio_nodos = {
            "Nodo_Alpha": np.array([1.0, 0.0, 3.5]),
            "Nodo_Beta":  np.array([0.0, 2.2, 1.1]),
            "Nodo_Gamma": np.array([4.0, 4.0, 0.0]),
            "Nodo_Delta": np.array([2.5, 1.0, 5.0])
        }
        
        # Asignamos valores del diccionario de idiomas a cada nodo (Indexación)
        self.diccionario_nodos = {
            "Nodo_Alpha": {"ES": "Origen", "EN": "Origin", "VAL": 0.1},
            "Nodo_Beta":  {"ES": "Mente",  "EN": "Mind",   "VAL": 0.2},
            "Nodo_Gamma": {"ES": "Matriz", "EN": "Matrix", "VAL": 0.3},
            "Nodo_Delta": {"ES": "Retorno", "EN": "Return", "VAL": 0.4}
        }

    def recuperar_por_trayectoria(self, nodo_inicio, nodo_fin):
        """
        En lugar de leer un archivo pesado de la memoria RAM, 
        el OS calcula el vector de trayectoria entre dos nodos para extraer el dato.
        """
        coord_inicio = self.espacio_nodos[nodo_inicio]
        coord_fin = self.espacio_nodos[nodo_fin]
        
        # Operación geométrica: Cálculo del vector resultante
        vector_trayectoria = coord_fin - coord_inicio
        magnitud = np.linalg.norm(vector_trayectoria)
        
        # El OS interpreta la geometría para reconstruir la información
        datos_origen = self.diccionario_nodos[nodo_inicio]["ES"]
        datos_destino = self.diccionario_nodos[nodo_fin]["ES"]
        
        print(f"--- Operación de OS Vectorial ---")
        print(f"Trayectoria calculada: {vector_trayectoria}")
        print(f"Magnitud del vector (Carga de datos): {magnitud:.4f}")
        print(f"Concepto decodificado en tiempo de vuelo: '{datos_origen}' enlazado con '{datos_destino}'")
        print(f"Memoria RAM física utilizada para almacenar texto: 0 bytes (Cálculo puro)\n")
        
        return vector_trayectoria

# --- EJECUCIÓN DE LA PRUEBA DE CONCEPTO ---
if __name__ == "__main__":
    # Inicializamos el prototipo del Sistema Operativo Vectorial
    vOS = SistemaVectorialOS()
    
    # Simulamos una instrucción de sistema: Unir el vector Origen con el vector Retorno
    # Esto emula cómo regresaste usando tus circunstancias raíz
    vOS.recuperar_por_trayectoria("Nodo_Alpha", "Nodo_Delta")
    
    # Otra instrucción: Enlazar Mente y Matriz
    vOS.recuperar_por_trayectoria("Nodo_Beta", "Nodo_Gamma")
