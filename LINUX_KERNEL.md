# Módulo de Kernel: vOS Linux Native Memory Subsystem (LKM)
**Subsistema de Memoria Vectorial Nativo para Arquitecturas Linux** **Autor:** Wilbert Contreras Borda  
**Estatus:** Patent-Pending / Especificación de Inyección en el Kernel MM

---

## 1. Arquitectura Nativa en el Kernel de Linux
En entornos Linux, la asignación de memoria virtual se rastrea mediante descriptores de memoria (`mm_struct`) y áreas de memoria virtual (`vm_area_struct`). Cuando un proceso solicita memoria mediante la llamada al sistema `mmap()`, el kernel tradicional busca bloques libres en la lista de páginas físicas del sistema (Buddy Allocator).

El módulo **vOS Linux LKM** altera este comportamiento inyectándose directamente en el manejador nativo de excepciones de memoria del archivo fuente `mm/memory.c`.

---

## 2. Intercepción del `handle_mm_fault`
En lugar de crear capas de emulación externas, el módulo reemplaza el vector de interrupción de la función crítica `handle_mm_fault()`. 

```text
[Llamada mmap / malloc] ──► [vm_area_struct (Puntero Sintético vOS)]
                                              │
                                              ▼ (Acceso al Dato)
                                 [ PAGE FAULT (Interrupción) ]
                                              │
                                              ▼
                                 [ vOS handle_mm_fault() ]
                                              │
                                              ├───► Aplica Operador Eje Z
                                              ├───► Calcula Trayectoria (X,Y,Z)
                                              ▼
                                  [ Inyección en Registros ]
