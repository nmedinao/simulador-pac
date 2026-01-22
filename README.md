# Simulador PAC - Dimensionamiento de Personal

## Descripción

Simulador para dimensionar mensualmente el número de personas (FTE) necesarias para atender un servicio PAC compuesto por 5 procesos secuenciales, bajo distintos escenarios de entrada de empresas.

## Características

- ✅ Simulación de 5 meses con ajuste mensual de dotación
- ✅ 5 procesos secuenciales: Orientación, Inscripción, Asesoramiento, Evaluación, Acreditación
- ✅ **Lógica temporal**: Mes 1 solo ejecuta Orientación e Inscripción; procesos 3-5 inician en Mes 2
- ✅ 3 tipologías de empresa: Pequeña, Mediana, Grande
- ✅ 3 escenarios: Moderado, Agresivo, Conservador
- ✅ Parámetros configurables desde la UI
- ✅ Cálculo de FTE (decimales) y personas (enteras)
- ✅ KPIs agregados y análisis de picos
- ✅ Sistema de autenticación con contraseña

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

Alternativa conda (recomendada si usas Anaconda/Miniconda):

```bash
# Crear entorno con Python 3.10
conda create -n simulpac python=3.10 -y

# Activar el entorno
conda activate simulpac

# Instalar dependencias
pip install -r requirements.txt

# Asegurar Streamlit
pip install streamlit
```

## Seguridad y Autenticación

El simulador incluye un sistema de autenticación con contraseña para restringir el acceso.

### Contraseña por defecto
- **Contraseña actual**: `admin`
- ⚠️ **IMPORTANTE**: Cambia esta contraseña antes de desplegar en producción

### Cambiar la contraseña

**Opción 1 - Usando el script:**
```bash
python generar_password.py
# Introduce tu nueva contraseña cuando se te solicite
# Copia el hash generado
```

**Opción 2 - Manualmente en Python:**
```python
import hashlib
nueva_password = "tu_contraseña_segura"
hash = hashlib.sha256(nueva_password.encode()).hexdigest()
print(hash)
```

**Paso 3 - Actualizar en el código:**
1. Abre `simulador_pac.py`
2. Busca la línea: `correct_password_hash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"`
3. Reemplaza el hash con tu nuevo hash
4. Guarda y redeploy

### Funciones de seguridad
- ✅ Pantalla de login antes de acceder al simulador
- ✅ Contraseña hasheada (SHA-256) - no se almacena en texto plano
- ✅ Botón de "Cerrar Sesión" en sidebar
- ✅ Sesión persiste mientras el navegador esté abierto

## Uso

```bash
# Ejecutar el simulador localmente
streamlit run simulador_pac.py
```

El simulador se abrirá en tu navegador en `http://localhost:8501`

**Primera vez**: Introduce la contraseña (por defecto: `admin`)

---

## Deployment en Streamlit Community Cloud

### Prerequisitos
- Cuenta de GitHub
- Cuenta en Streamlit Cloud (share.streamlit.io)

### Paso 1: Subir código a GitHub

```bash
# Inicializar repositorio
git init
git add .
git commit -m "Initial commit: Simulador PAC con autenticación"

# Crear repositorio en GitHub (desde github.com)
# New repository → "simulador-pac"

# Conectar y subir
git remote add origin https://github.com/TU_USUARIO/simulador-pac.git
git branch -M main
git push -u origin main
```

### Paso 2: Deploy en Streamlit Cloud

1. Ve a **share.streamlit.io**
2. Click "Sign in" con GitHub
3. Click "New app"
4. Configura:
   - **Repository**: `TU_USUARIO/simulador-pac`
   - **Branch**: `main`
   - **Main file path**: `simulador_pac.py`
5. Click "Deploy"

### Paso 3: Compartir acceso

Una vez desplegado:
1. Copia la URL: `https://TU_USUARIO-simulador-pac.streamlit.app`
2. Cambia la contraseña por defecto (ver sección Seguridad)
3. Comparte URL + contraseña solo con usuarios autorizados

⚠️ **Nota de seguridad**: La aplicación será públicamente accesible vía URL, pero protegida por contraseña. Para mayor seguridad, considera usar Streamlit Teams ($250/mes) con SSO empresarial.

---

## Configuración

### Parámetros configurables en la UI:

1. **Expedientes por tipo de empresa**: Pequeña (50), Mediana (100), Grande (500)
2. **Distribución por tipología**: 
   - % Empresas pequeñas (50%)
   - % Empresas medianas (30%)
   - % Empresas grandes (20%)
   - ⚠️ La suma debe ser exactamente 100%
3. **Proceso de Orientación**:
   - Sesiones base por empresa (2)
   - % empresas solo sesiones base (70%)
   - Sesiones adicionales promedio por tipología:
     - Pequeña: 1
     - Mediana: 2
     - Grande: 5
   - Duración sesiones (120 min)
4. **Tiempos por expediente**:
   - Inscripción Mes 1: 132 min
   - Inscripción Mes ≥2: 66 min
   - Asesoramiento: 6 min
   - Evaluación: 7.2 min
   - Acreditación: 9.6 min
5. **Capacidad productiva**: 9,600 min/FTE/mes
6. **Factores de escenarios**:
   - Agresivo: 1.5x
   - Conservador: 0.5x

### Entrada de empresas (Escenario Moderado):

Ahora se introduce el **total de empresas por mes** y se distribuyen automáticamente según los porcentajes configurados:

| Mes | Total Empresas |
|-----|----------------|
| 1   | 3              |
| 2   | 30             |
| 3   | 60             |
| 4   | 150            |
| 5   | 150            |

La distribución por tipología se calcula automáticamente y se muestra en una tabla de previsualización.

## Outputs

### KPIs Generales:
- Total empresas atendidas (5 meses)
- Total expedientes procesados (5 meses)
- FTE máximo total (pico)
- Personas máximo total (pico)

### Tablas:
- Resumen por mes (empresas y expedientes)
- FTE y personas por proceso y mes
- Tabla consolidada FTE
- Tabla consolidada Personas
- Análisis de picos por proceso

## Supuestos del Modelo

- ✅ Sin backlog (toda la demanda se absorbe cada mes)
- ✅ Sin polivalencia (cada persona en un único proceso)
- ✅ Sin retrabajos
- ✅ Productividad constante
- ✅ Determinista (sin variabilidad estocástica)
- ✅ Orientación una vez por empresa
- ✅ Todos los expedientes entregados simultáneamente tras orientación
- ✅ **Mes 1**: Solo Orientación e Inscripción
- ✅ **Mes 2+**: Todos los procesos (Orientación, Inscripción, Asesoramiento, Evaluación, Acreditación)

## Estructura del Código

```
simulador_pac.py
├── Configuración UI (Sidebar)
│   ├── Parámetros de empresa
│   ├── Parámetros de orientación
│   ├── Tiempos por expediente
│   ├── Capacidad productiva
│   └── Factores de escenarios
├── Entrada de datos
│   └── Empresas por mes y tipo
├── Motor de cálculo
│   ├── calcular_tiempo_orientacion_por_empresa()
│   ├── aplicar_factor_escenario()
│   ├── calcular_carga_orientacion()
│   ├── calcular_expedientes_mes()
│   └── ejecutar_simulacion()
└── Visualización de resultados
    ├── KPIs generales
    ├── Tablas por proceso
    ├── Tablas consolidadas
    └── Análisis de picos
```

## Versión

**v1.0** - Enero 2026

## Contacto

Desarrollado por Jorge para dimensionamiento operativo PAC.
