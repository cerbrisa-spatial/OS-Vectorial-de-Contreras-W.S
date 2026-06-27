#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vectorial OS (vOS) - MVP del Núcleo Matemático v2.2
Arquitecto y Autor: Wilbert Contreras Borda
Licencia: LICENCIA DE INVESTIGACIÓN PROPIETARIA WILBERT CONTRERAS v2.0
Estatus: Patente Pendiente / Simulación Completa con Resiliencia Galáctica
"""

import math
import json
import os

class NodoOctree:
    """Implementación del Octree Espacial de Resolución Variable para el vOS."""
    def __init__(self, centro, tamano, nivel=0, max_nivel=3):
        self.centro = centro  # (x, y, z)
        self.tamano = tamano
        self.nivel = nivel
        self.max_nivel = max_nivel
        self.es_hoja = True
        self.hijos = None
        self.datos_nodos = {}  # ID_Nodo -> Información del Nodo

    def subdividir(self):
        """Divide el cuadrante actual en 8 sub-octantes hijos."""
        self.es_hoja = False
        self.hijos = []
        medio_tamano = self.tamano / 2.0
        offsets = [
            (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
            (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)
        ]
        for dx, dy, dz in offsets:
            c_x = self.centro[0] + dx * (medio_tamano / 2.0)
            c_y = self.centro[1] + dy * (medio_tamano / 2.0)
            c_z = self.centro[2] + dz * (medio_tamano / 2.0)
            self.hijos.append(NodoOctree((c_x, c_y, c_z), medio_tamano, self.nivel + 1, self.max_nivel))

        # Migrar los datos del nodo padre a los hijos correspondientes
        for n_id, n_info in self.datos_nodos.items():
            self.insertar_en_hijos(n_id, n_info)
        self.datos_nodos.clear()

    def insertar_en_hijos(self, nodo_id, nodo_info):
        pos = nodo_info['coords']
        for hijo in self.hijos:
            hs = hijo.tamano / 2.0
            # Verificar si las coordenadas caen dentro de los límites del cubo hijo
            if (hijo.centro[0] - hs <= pos[0] <= hijo.centro[0] + hs and
                hijo.centro[1] - hs <= pos[1] <= hijo.centro[1] + hs and
                hijo.centro[2] - hs <= pos[2] <= hijo.centro[2] + hs):
                hijo.insertar(nodo_id, nodo_info)
                return

    def insertar(self, nodo_id, nodo_info):
        """Inserta un nodo en la estructura con resolución variable bajo demanda."""
        if self.es_hoja:
            self.datos_nodos[nodo_id] = nodo_info
            # Si la densidad de nodos en este cuadrante supera el umbral, se subdivide
            if len(self.datos_nodos) > 2 and self.nivel < self.max_nivel:
                self.subdividir()
        else:
            self.insertar_en_hijos(nodo_id, nodo_info)

    def buscar_nodo(self, coords):
        """Busca el nodo correspondiente a un conjunto de coordenadas 3D."""
        if self.es_hoja:
            for n_id, n_info in self.datos_nodos.items():
                if n_info['coords'] == coords:
                    return n_id, n_info
            return None, None
        else:
            medio_tamano = self.tamano / 2.0
            for hijo in self.hijos:
                if (hijo.centro[0] - medio_tamano <= coords[0] <= hijo.centro[0] + medio_tamano and
                    hijo.centro[1] - medio_tamano <= coords[1] <= hijo.centro[1] + medio_tamano and
                    hijo.centro[2] - medio_tamano <= coords[2] <= hijo.centro[2] + medio_tamano):
                    return hijo.buscar_nodo(coords)
            return None, None


class NúcleoVectorialOS:
    def __init__(self, ruta_checkpoint="vos_core.vcf"):
        self.ruta_checkpoint = ruta_checkpoint
        # Inicializar la raíz del Octree Espacial (Centro en 16000, Tamaño de cubo 32000)
        self.raiz_espacial = NodoOctree((16000.0, 16000.0, 16000.0), 32000.0)
        
        # Constantes nativas del Operador del Eje Z
        self.K_x, self.K_y, self.K_z = 10000, 5000, 20000
        self.theta = 0.1402  # Ángulo de fase armónica basado en la frecuencia local
        self.R_nivel = 40    # Multiplicador de escala de bus de datos
        
        self.cargar_o_inicializar_nodos()

    def cargar_o_inicializar_nodos(self):
        """Carga el punto de restauración (.vcf) o reconstruye la matriz desde la Vía Láctea (ROM)."""
        if os.path.exists(self.ruta_checkpoint):
            try:
                print(f"[vOS] Checkpoint detectado: Cargando {self.ruta_checkpoint}...")
                with open(self.ruta_checkpoint, 'r') as f:
                    datos_checkpoint = json.load(f)
                    self.theta = datos_checkpoint.get("theta", self.theta)
                    for n_id, n_info in datos_checkpoint.get("nodos", {}).items():
                        self.raiz_espacial.insertar(n_id, n_info)
            except (json.JSONDecodeError, KeyError, IOError):
                print("[¡ALERTA vOS!] Archivo de configuración dañado o corrupto.")
                self.reconstruir_desde_mapa_base_galactico()
        else:
            print("[vOS] Archivo de configuración ausente (Primer Arranque / Instalación Limpia).")
            self.reconstruir_desde_mapa_base_galactico()

    def reconstruir_desde_mapa_base_galactico(self):
        """Protocolo de Resiliencia: Carga la matriz inmutable de la Vía Láctea desde la ROM (Ring -3)."""
        print("[vOS - Firmware Ring -3] Cargando Mapa Base Inmutable de la Vía Láctea desde la ROM...")
        
        # Simulación de la estructura de densidad galáctica (Bulbo Central y Brazos Espirales)
        nodos_galacticos = {
            "0x0001": {"coords": [16000.0, 16000.0, 16000.0], "val": "BULBO_CENTRAL_CORE", "slots": {"Alfa": None, "Beta": None}},
            "0x0002": {"code": "Brazo_Orion", "coords": [10000.0, 64.0, 10000.0], "val": "SISTEMA_ARCHIVOS", "slots": {"Alfa": None, "Beta": None}},
            "0x0003": {"code": "Brazo_Sagitario", "coords": [22000.0, 128.0, 25000.0], "val": "INTERCEPTOR_BUS", "slots": {"Alfa": None, "Beta": None}}
        }
        
        for n_id, n_info in nodos_galacticos.items():
            self.raiz_espacial.insertar(n_id, n_info)
        print("[vOS] Espacio proyectivo restablecido con éxito. Sistema operativo en línea en modo seguro.")

    def guardar_checkpoint(self):
        """Subsistema de Persistencia (vOS Checkpoint): Snapshot del estado geométrico."""
        print(f"[vOS] Ejecutando volcado geométrico compacto en '{self.ruta_checkpoint}'...")
        
        todos_los_nodos = {}
        def extraer(nodo_actual):
            if nodo_actual.es_hoja:
                todos_los_nodos.update(nodo_actual.datos_nodos)
            else:
                for hijo in nodo_actual.hijos:
                    extraer(hijo)
                    
        extraer(self.raiz_espacial)
        datos_checkpoint = {
            "theta": self.theta,
            "nodos": todos_los_nodos
        }
        with open(self.ruta_checkpoint, 'w') as f:
            json.dump(datos_checkpoint, f, indent=4)
        print("[vOS] Checkpoint sincronizado con la NVRAM virtual exitosamente.")

    def operador_eje_z(self, D_L):
        """Intercepta una dirección binaria lineal y la traduce a Coordenadas 3D."""
        # Aplicación de la matriz de proyección armónica
        comp_x = (D_L % self.K_x) * math.cos(self.theta) - (D_L % self.K_y) * math.sin(self.theta)
        comp_y = (D_L % self.K_x) * math.sin(self.theta) + (D_L % self.K_y) * math.cos(self.theta)
        comp_z = (D_L % self.K_z) * self.R_nivel
        
        return [abs(round(comp_x, 4)), abs(round(comp_y, 4)), abs(round(comp_z, 4))]

    def calcular_trayectoria(self, coord_A, coord_B):
        """Calcula el vector de trayectoria y su magnitud en tiempo de vuelo."""
        dx = coord_B[0] - coord_A[0]
        dy = coord_B[1] - coord_A[1]
        dz = coord_B[2] - coord_A[2]
        
        magnitud = math.sqrt(dx**2 + dy**2 + dz**2)
        return {"vector": [dx, dy, dz], "magnitude": round(magnitud, 4)}

    def arbitrar_colision(self, nodo_info, proceso_id, vector_t):
        """Protocolo Híbrido de Colisiones: Canales de fase y desempate por Magnitud Vectorial."""
        # 1. Intentar asignar a un slot armónico libre
        for slot_id, ocupante in nodo_info["slots"].items():
            if ocupante is None or ocupante == proceso_id:
                nodo_info["slots"][slot_id] = proceso_id
                return f"Acceso concedido en Canal de Fase [{slot_id}]"
        
        # 2. Si hay saturación, desempate por la Magnitud Absoluta del Vector (||T||)
        print(f"[Arbitraje] ¡Colisión de Bus! Canales llenos. Evaluando prioridad por Magnitud Vectorial...")
        mag_actual = vector_t["magnitude"]
        mag_competidora = 5000.0  # Umbral de simulación para el MVP
        
        if mag_actual > mag_competidora:
            nodo_info["slots"]["Alfa"] = proceso_id
            return "Desplazamiento exitoso: El proceso actual tomó el Canal [Alfa] por Mayor Magnitud."
        else:
            return "Acceso denegado: Magnitud insuficiente. Trayectoria desviada al siguiente ciclo."


# ==========================================
# Sección de Validación y Pruebas del Core
# ==========================================
if __name__ == "__main__":
    print("--- INICIALIZANDO MVP DEL NÚCLEO VECTORIAL OS ---")
    
    # Simulación de arranque 1: Forzar reconstrucción borrando o ignorando un vcf corrupto
    print("\n=== PRUEBA 1: ARRANQUE CON FALLO DE CHECKPOINT ===")
    vos_fail = NúcleoVectorialOS(ruta_checkpoint="corrupto_invalido.vcf")
    
    # Simulación de arranque 2: Inicialización estándar o recuperación
    print("\n=== PRUEBA 2: FLUJO DE TRABAJO ESTÁNDAR ===")
    vos = NúcleoVectorialOS()

    # 1. Intercepción y Proyección con el Operador del Eje Z
    direccion_ram = 7458921
    coords_proyectadas = vos.operador_eje_z(direccion_ram)
    print(f"\n[1] Intercepción de RAM: Dirección {direccion_ram} -> Proyección 3D: {coords_proyectadas}")

    # 2. Cálculo de Trayectoria
    coordenadas_alfa = [10000.0, 64.0, 10000.0]
    trayectoria = vos.calcular_trayectoria(coords_proyectadas, coordenadas_alfa)
    print(f"[2] Vector de Trayectoria resultante T: {trayectoria['vector']}")
    print(f"    Magnitud Absoluta (Densidad de Datos): {trayectoria['magnitude']}")

    # 3. Escalabilidad Dinámica mediante el Octree
    print("\n[3] Inyectando flujos analíticos para forzar subdivisión del Octree...")
    vos.raiz_espacial.insertar("0x0004", {"coords": [10000.0, 65.0, 10000.0], "val": "CORE_IA", "slots": {"Alfa": None, "Beta": None}})
    vos.raiz_espacial.insertar("0x0005", {"coords": [10000.0, 66.0, 10000.0], "val": "NODO_RED", "slots": {"Alfa": None, "Beta": None}})
    
    # Búsqueda estructurada en el árbol
    n_id, n_info = vos.raiz_espacial.buscar_nodo([10000.0, 64.0, 10000.0])
    print(f"    Resolución variable -> Nodo localizado: {n_id} ({n_info['val'] if n_info else 'No registrado'})")

    # 4. Prueba del Protocolo Arbitral ante Colisiones concurrentes
    if n_info:
        print("\n[4] Ejecutando estrés de concurrencia en Canales de Fase...")
        print(f"    Petición 1: {vos.arbitrar_colision(n_info, 'Proceso_IA_Primario', trayectoria)}")
        print(f"    Petición 2: {vos.arbitrar_colision(n_info, 'Proceso_Kernel_Huesped', trayectoria)}")
        # Forzar saturación total de slots
        n_info["slots"]["Beta"] = "Carga_Estática_Bloqueante"
        print(f"    Petición 3 (Saturado): {vos.arbitrar_colision(n_info, 'Proceso_Híper_Crítico', trayectoria)}")

    # 5. Persistencia del Sistema (vOS Checkpoint)
    print("")
    vos.guardar_checkpoint()
    print("\n--- SIMULACIÓN DEL NÚCLEO FINALIZADA CORRECTAMENTE ---")
