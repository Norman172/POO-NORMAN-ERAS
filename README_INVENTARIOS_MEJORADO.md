# Sistema de Gestión de Inventarios Mejorado

## Descripción del Proyecto

Este es un sistema avanzado de gestión de inventarios desarrollado en Python que incorpora:

- **Almacenamiento persistente** en archivos JSON
- **Manejo robusto de excepciones**
- **Validación de datos** completa
- **Sistema de respaldos** automáticos
- **Interfaz de usuario** intuitiva en consola
- **Reportes detallados** del inventario

## Características Principales

### 🔒 Manejo de Excepciones Robusto

- **FileNotFoundError**: Manejo cuando el archivo de inventario no existe
- **PermissionError**: Gestión de permisos de lectura/escritura
- **JSONDecodeError**: Recuperación de archivos corruptos con sistema de backup
- **ValueError**: Validación de datos de entrada
- **InventarioException**: Excepción personalizada para errores específicos del inventario

### 💾 Persistencia de Datos

- **Formato JSON**: Almacenamiento estructurado y legible
- **Escritura atómica**: Prevención de corrupción de datos durante la escritura
- **Sistema de backups**: Respaldos automáticos antes de cada modificación
- **Carga automática**: Restauración del inventario al iniciar el programa

### 🛡️ Validación de Datos

- **IDs únicos**: Prevención de duplicados
- **Validación de tipos**: Verificación de tipos de datos correctos
- **Rangos válidos**: Control de valores mínimos y máximos
- **Sanitización**: Limpieza de espacios en blanco y caracteres especiales

### 📊 Funcionalidades Avanzadas

- **Búsqueda por nombre**: Búsqueda parcial case-insensitive
- **Búsqueda por ID**: Búsqueda exacta por identificador
- **Alertas de stock bajo**: Notificaciones para productos con inventario reducido
- **Reportes automáticos**: Generación de informes detallados
- **Estadísticas**: Cálculo de valores totales y métricas del inventario

## Estructura del Código

### Clase `Producto`
```python
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio)
    # Métodos getters y setters con validación
    # Serialización a diccionario para almacenamiento
    # Deserialización desde diccionario
```

**Atributos:**
- `_id`: Identificador único del producto
- `_nombre`: Nombre descriptivo del producto
- `_cantidad`: Cantidad disponible en inventario
- `_precio`: Precio unitario del producto
- `_fecha_creacion`: Timestamp de creación del producto

### Clase `Inventario`
```python
class Inventario:
    def __init__(self, archivo_inventario='inventario.json')
    # Métodos de gestión de productos
    # Manejo de archivos y excepciones
    # Sistema de backups
```

**Métodos principales:**
- `cargar_inventario()`: Carga datos desde archivo
- `guardar_inventario()`: Guarda datos al archivo
- `agregar_producto()`: Añade nuevo producto
- `eliminar_producto()`: Elimina producto existente
- `actualizar_producto()`: Modifica producto existente
- `buscar_por_nombre()`: Búsqueda textual
- `buscar_por_id()`: Búsqueda por identificador
- `generar_reporte()`: Crea informe detallado

### Clase `InventarioException`
```python
class InventarioException(Exception):
    # Excepción personalizada para errores específicos del sistema
```

## Manejo de Errores Implementado

### 1. Errores de Archivo
- **Archivo no encontrado**: Crea nuevo inventario automáticamente
- **Permisos insuficientes**: Notifica al usuario y sugiere soluciones
- **Archivo corrupto**: Crea backup y permite reiniciar con inventario limpio

### 2. Errores de Validación
- **Datos inválidos**: Valida tipos, rangos y formatos antes de procesar
- **IDs duplicados**: Previene la creación de productos con identificadores existentes
- **Valores negativos**: Controla que cantidades y precios sean válidos

### 3. Errores de Sistema
- **Interrupciones de usuario**: Maneja Ctrl+C gracefully
- **Errores inesperados**: Captura y reporta excepciones no previstas
- **Operaciones atómicas**: Asegura consistencia de datos en operaciones críticas

## Uso del Sistema

### Ejecución
```bash
python gestion-inventarios-mejorado.py
```

### Funciones del Menú

1. **📝 Añadir producto**: Crear nuevo producto con validación completa
2. **🗑️ Eliminar producto**: Remover producto por ID con confirmación
3. **✏️ Actualizar producto**: Modificar atributos existentes
4. **🔍 Buscar por nombre**: Localizar productos por nombre parcial
5. **🔎 Buscar por ID**: Encontrar producto específico por identificador
6. **📦 Mostrar inventario**: Visualizar todos los productos con estadísticas
7. **⚠️ Stock bajo**: Listar productos con inventario crítico
8. **📄 Generar reporte**: Crear informe detallado en archivo de texto
9. **🔄 Recargar inventario**: Refrescar datos desde archivo
0. **🚪 Salir**: Cerrar aplicación con guardado automático

## Archivos Generados

- `inventario.json`: Archivo principal de datos
- `backups/inventario_backup_YYYYMMDD_HHMMSS.json`: Respaldos automáticos
- `reporte_inventario_YYYYMMDD_HHMMSS.txt`: Reportes generados

## Mejoras Implementadas vs Versión Original

| Característica | Versión Original | Versión Mejorada |
|---|---|---|
| Persistencia | ❌ Solo memoria | ✅ Archivos JSON |
| Manejo de errores | ❌ Básico | ✅ Robusto y completo |
| Validación | ❌ Mínima | ✅ Exhaustiva |
| Backups | ❌ No disponible | ✅ Automáticos |
| Reportes | ❌ Solo pantalla | ✅ Archivos detallados |
| Búsqueda | ❌ Solo por nombre | ✅ Por nombre e ID |
| Alertas | ❌ No disponible | ✅ Stock bajo |
| Interfaz | ❌ Básica | ✅ Rica con emojis |
| Recuperación | ❌ No disponible | ✅ Desde archivos corruptos |
| Atomicidad | ❌ No garantizada | ✅ Operaciones atómicas |

## Requisitos del Sistema

- Python 3.6+
- Librerías estándar: `os`, `json`, `datetime`
- Permisos de lectura/escritura en el directorio de ejecución

## Pruebas Recomendadas

1. **Funcionamiento normal**: Crear, modificar y eliminar productos
2. **Persistencia**: Reiniciar programa y verificar datos guardados
3. **Errores de archivo**: Eliminar archivo de inventario y reiniciar
4. **Archivo corrupto**: Modificar manualmente archivo JSON con datos inválidos
5. **Permisos**: Cambiar permisos del archivo a solo lectura
6. **Validaciones**: Ingresar datos inválidos (negativos, vacíos, etc.)
7. **Interrupciones**: Usar Ctrl+C durante operaciones
8. **Stock bajo**: Crear productos con cantidades bajas y probar alertas
9. **Reportes**: Generar informes y verificar contenido
10. **Backups**: Verificar creación automática de respaldos

## Conclusiones

Este sistema mejorado demuestra la aplicación práctica de conceptos avanzados de programación orientada a objetos en Python:

- **Encapsulación**: Atributos privados con acceso controlado
- **Abstracción**: Métodos que ocultan la complejidad interna
- **Manejo de excepciones**: Gestión robusta de errores
- **Persistencia de datos**: Almacenamiento y recuperación confiables
- **Validación**: Aseguramiento de integridad de datos
- **Usabilidad**: Interfaz intuitiva y retroalimentación clara

El código está diseñado para ser mantenible, extensible y robusto para uso en entornos de producción.
