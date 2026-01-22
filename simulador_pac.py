import streamlit as st
import pandas as pd
import numpy as np
import hashlib

# Configuración de la página
st.set_page_config(page_title="Simulador PAC", layout="wide")

# ============================================================================
# SISTEMA DE AUTENTICACIÓN
# ============================================================================

def check_password():
    """Verifica si el usuario tiene la contraseña correcta."""
    
    def password_entered():
        """Valida la contraseña ingresada."""
        # Hash SHA-256 de la contraseña "pac2025" (puedes cambiarla)
        # Para generar un nuevo hash: hashlib.sha256("tu_contraseña".encode()).hexdigest()
        correct_password_hash = "23cbf064de8bff2afa689f9cdba3a829f0d892b9f7e6d1ceea35237586fc0697"  # "admin"
        
        entered_password_hash = hashlib.sha256(st.session_state["password"].encode()).hexdigest()
        
        if entered_password_hash == correct_password_hash:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # Si ya está autenticado, permitir acceso
    if st.session_state.get("password_correct", False):
        return True

    # Mostrar pantalla de login
    st.title("🔐 Simulador PAC - Acceso Restringido")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Introduce la contraseña de acceso")
        st.text_input(
            "Contraseña",
            type="password",
            on_change=password_entered,
            key="password",
            help="Contacta al administrador si no tienes acceso"
        )
        
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("❌ Contraseña incorrecta. Por favor, inténtalo de nuevo.")
        
        st.markdown("---")
        st.info("💡 **Nota**: Este simulador es de uso interno. Si necesitas acceso, contacta al administrador del sistema.")
    
    return False

# Verificar autenticación antes de mostrar la aplicación
if not check_password():
    st.stop()

# ============================================================================
# APLICACIÓN PRINCIPAL (Solo visible después de autenticación)
# ============================================================================

# Título principal
st.title("🎯 Simulador de Dimensionamiento PAC")
st.markdown("**Planificación operativa de personal por proceso y mes**")
st.info("ℹ️ **Lógica temporal**: Mes 1 ejecuta solo Orientación e Inscripción. Los procesos de Asesoramiento, Evaluación y Acreditación inician a partir del Mes 2.")

# Sidebar para configuración
st.sidebar.header("⚙️ Configuración del Simulador")

# Botón de logout en sidebar
if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state["password_correct"] = False
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# ============================================================================
# SECCIÓN 1: PARÁMETROS DE TIPOLOGÍA DE EMPRESAS
# ============================================================================
st.sidebar.subheader("📊 Expedientes por Tipo de Empresa")

expedientes_pequena = st.sidebar.number_input(
    "Expedientes por empresa pequeña",
    min_value=1,
    value=10,
    step=1
)

expedientes_mediana = st.sidebar.number_input(
    "Expedientes por empresa mediana",
    min_value=1,
    value=50,
    step=1
)

expedientes_grande = st.sidebar.number_input(
    "Expedientes por empresa grande",
    min_value=1,
    value=100,
    step=1
)

# ============================================================================
# SECCIÓN 2: PARÁMETROS DE ORIENTACIÓN
# ============================================================================
st.sidebar.subheader("🎓 Proceso de Orientación")

sesiones_base = st.sidebar.number_input(
    "Sesiones base por empresa",
    min_value=1,
    value=2,
    step=1
)

pct_solo_base = st.sidebar.slider(
    "% empresas solo sesiones base",
    min_value=0,
    max_value=100,
    value=70,
    step=5
)

# Sesiones adicionales por tipología (valores por defecto solicitados)
sesiones_adicionales_pequena = st.sidebar.number_input(
    "Sesiones adicionales promedio - pequeña",
    min_value=0,
    value=1,
    step=1
)

sesiones_adicionales_mediana = st.sidebar.number_input(
    "Sesiones adicionales promedio - mediana",
    min_value=0,
    value=2,
    step=1
)

sesiones_adicionales_grande = st.sidebar.number_input(
    "Sesiones adicionales promedio - grande",
    min_value=0,
    value=5,
    step=1
)

# Estructura por tipología para pasar a las funciones de cálculo
sesiones_adicionales_por_tipo = {
    "pequena": sesiones_adicionales_pequena,
    "mediana": sesiones_adicionales_mediana,
    "grande": sesiones_adicionales_grande,
}

# Mantener variable global de compatibilidad (valor por defecto igual a mediana)
sesiones_adicionales = sesiones_adicionales_mediana

duracion_sesion_base = st.sidebar.number_input(
    "Duración sesión base (min)",
    min_value=1,
    value=90,
    step=5
)

duracion_sesion_adicional = st.sidebar.number_input(
    "Duración sesión adicional (min)",
    min_value=1,
    value=90,
    step=5
)

# ============================================================================
# SECCIÓN 3: TIEMPOS DE PROCESO POR EXPEDIENTE
# ============================================================================
st.sidebar.subheader("⏱️ Tiempos por Expediente")

tiempo_inscripcion_mes1 = st.sidebar.number_input(
    "Inscripción Mes 1 (min)",
    min_value=1,
    value=132,
    step=1
)

tiempo_inscripcion_mes2plus = st.sidebar.number_input(
    "Inscripción Mes ≥2 (min)",
    min_value=1,
    value=66,
    step=1
)

tiempo_asesoramiento = st.sidebar.number_input(
    "Asesoramiento (min)",
    min_value=1,
    value=6,
    step=1
)

tiempo_evaluacion = st.sidebar.number_input(
    "Evaluación (min)",
    min_value=1.0,
    value=7.2,
    step=0.1
)

tiempo_acreditacion = st.sidebar.number_input(
    "Acreditación (min)",
    min_value=1.0,
    value=9.6,
    step=0.1
)

# ============================================================================
# SECCIÓN 4: CAPACIDAD PRODUCTIVA
# ============================================================================
st.sidebar.subheader("👥 Capacidad Productiva")

minutos_por_fte = st.sidebar.number_input(
    "Minutos disponibles por FTE/mes",
    min_value=1,
    value=9600,
    step=100
)

# ============================================================================
# SECCIÓN 5: DISTRIBUCIÓN DE EMPRESAS POR TIPOLOGÍA
# ============================================================================
st.sidebar.subheader("📊 Distribución por Tipología")

pct_pequenas = st.sidebar.slider(
    "% Empresas pequeñas",
    min_value=0,
    max_value=100,
    value=50,
    step=5
)

pct_medianas = st.sidebar.slider(
    "% Empresas medianas",
    min_value=0,
    max_value=100,
    value=30,
    step=5
)

pct_grandes = st.sidebar.slider(
    "% Empresas grandes",
    min_value=0,
    max_value=100,
    value=20,
    step=5
)

# Validación de suma = 100%
suma_porcentajes = pct_pequenas + pct_medianas + pct_grandes
if suma_porcentajes != 100:
    st.sidebar.error(f"⚠️ La suma de porcentajes debe ser 100% (actual: {suma_porcentajes}%)")

# ============================================================================
# SECCIÓN 6: FACTORES DE ESCENARIOS
# ============================================================================
st.sidebar.subheader("📈 Factores de Escenarios")

factor_agresivo = st.sidebar.number_input(
    "Factor escenario agresivo",
    min_value=0.1,
    value=2.0,
    step=0.1
)

factor_conservador = st.sidebar.number_input(
    "Factor escenario conservador",
    min_value=0.1,
    value=0.5,
    step=0.1
)

# ============================================================================
# SECCIÓN 7: ENTRADA DE EMPRESAS - ESCENARIO MODERADO
# ============================================================================
st.header("📥 Entrada Total de Empresas por Mes - Escenario Moderado")

st.info(f"Distribución automática: {pct_pequenas}% pequeñas, {pct_medianas}% medianas, {pct_grandes}% grandes")

col1, col2, col3, col4, col5 = st.columns(5)

total_empresas_mes = []

with col1:
    st.subheader("Mes 1")
    empresas_mes1 = st.number_input(
        "Total empresas",
        min_value=0,
        value=5,
        step=1,
        key="total_mes_1"
    )
    total_empresas_mes.append(empresas_mes1)

with col2:
    st.subheader("Mes 2")
    empresas_mes2 = st.number_input(
        "Total empresas",
        min_value=0,
        value=10,
        step=1,
        key="total_mes_2"
    )
    total_empresas_mes.append(empresas_mes2)

with col3:
    st.subheader("Mes 3")
    empresas_mes3 = st.number_input(
        "Total empresas",
        min_value=0,
        value=25,
        step=1,
        key="total_mes_3"
    )
    total_empresas_mes.append(empresas_mes3)

with col4:
    st.subheader("Mes 4")
    empresas_mes4 = st.number_input(
        "Total empresas",
        min_value=0,
        value=50,
        step=1,
        key="total_mes_4"
    )
    total_empresas_mes.append(empresas_mes4)

with col5:
    st.subheader("Mes 5")
    empresas_mes5 = st.number_input(
        "Total empresas",
        min_value=0,
        value=100,
        step=1,
        key="total_mes_5"
    )
    total_empresas_mes.append(empresas_mes5)

# Mostrar distribución por tipología
st.subheader("📊 Distribución de Empresas por Tipología (calculada)")

df_distribucion = pd.DataFrame({
    'Mes': range(1, 6),
    'Total': total_empresas_mes,
    'Pequeñas': [int(t * pct_pequenas / 100) for t in total_empresas_mes],
    'Medianas': [int(t * pct_medianas / 100) for t in total_empresas_mes],
    'Grandes': [int(t * pct_grandes / 100) for t in total_empresas_mes]
})

st.dataframe(df_distribucion, hide_index=True, use_container_width=True)

# ============================================================================
# SELECTOR DE ESCENARIO
# ============================================================================
st.header("🎯 Selección de Escenario")
escenario = st.radio(
    "Selecciona el escenario a simular:",
    ["Moderado", "Agresivo", "Conservador"],
    horizontal=True
)

# ============================================================================
# CÁLCULOS DEL SIMULADOR
# ============================================================================

def calcular_tiempo_orientacion_por_empresa():
    """Calcula el tiempo promedio de orientación por empresa en minutos"""
    tiempo_base = sesiones_base * duracion_sesion_base
    pct_adicionales = (100 - pct_solo_base) / 100
    tiempo_adicional = sesiones_adicionales * duracion_sesion_adicional * pct_adicionales
    return tiempo_base + tiempo_adicional

def aplicar_factor_escenario(empresas_totales, escenario):
    """Aplica el factor correspondiente según el escenario seleccionado"""
    if escenario == "Agresivo":
        return [int(np.ceil(e * factor_agresivo)) for e in empresas_totales]
    elif escenario == "Conservador":
        return [int(np.ceil(e * factor_conservador)) for e in empresas_totales]
    else:  # Moderado
        return empresas_totales

def distribuir_empresas_por_tipologia(total_empresas):
    """Distribuye el total de empresas según los porcentajes configurados"""
    pequenas = int(total_empresas * pct_pequenas / 100)
    medianas = int(total_empresas * pct_medianas / 100)
    grandes = int(total_empresas * pct_grandes / 100)
    return pequenas, medianas, grandes

def calcular_carga_orientacion(empresas_mes):
    """Calcula la carga total de orientación en minutos para un mes"""
    # Espera empresas_mes = [pequenas, medianas, grandes]
    pequenas, medianas, grandes = empresas_mes

    # Si existe la estructura por tipo, usarla; si no, usar el cálculo global
    try:
        tiempos_por_tipo = calcular_tiempos_orientacion_por_tipo(sesiones_adicionales_por_tipo)
        carga = (
            pequenas * tiempos_por_tipo['pequena'] +
            medianas * tiempos_por_tipo['mediana'] +
            grandes * tiempos_por_tipo['grande']
        )
        return carga
    except NameError:
        # Fallback: comportamiento anterior (global)
        total_empresas = sum(empresas_mes)
        tiempo_por_empresa = calcular_tiempo_orientacion_por_empresa()
        return total_empresas * tiempo_por_empresa

def calcular_expedientes_mes(empresas_mes):
    """Calcula el total de expedientes generados en un mes"""
    pequenas_mes, medianas_mes, grandes_mes = empresas_mes
    total_expedientes = (
        pequenas_mes * expedientes_pequena +
        medianas_mes * expedientes_mediana +
        grandes_mes * expedientes_grande
    )
    return total_expedientes


def calcular_tiempos_orientacion_por_tipo(sesiones_adicionales_dict):
    """Calcula el tiempo promedio de orientación por empresa para cada tipología.

    sesiones_adicionales_dict: dict con claves 'pequena','mediana','grande'
    devuelve dict con minutos por empresa para cada tipo
    """
    tiempo_base = sesiones_base * duracion_sesion_base
    pct_adicionales = (100 - pct_solo_base) / 100

    tiempos = {}
    for tipo in ['pequena', 'mediana', 'grande']:
        sesiones_add = int(sesiones_adicionales_dict.get(tipo, 0))
        tiempo_adicional = sesiones_add * duracion_sesion_adicional * pct_adicionales
        tiempos[tipo] = tiempo_base + tiempo_adicional

    return tiempos

def ejecutar_simulacion():
    """Ejecuta la simulación completa y retorna los resultados"""
    
    # Validar que la suma de porcentajes sea 100%
    if suma_porcentajes != 100:
        st.error("⚠️ No se puede ejecutar la simulación. La suma de porcentajes debe ser exactamente 100%")
        return None
    
    # Aplicar factor de escenario al total de empresas
    empresas_totales_ajustadas = aplicar_factor_escenario(total_empresas_mes, escenario)
    
    # Estructuras para almacenar resultados
    resultados = {
        'mes': [],
        'empresas_entrantes': [],
        'empresas_pequenas': [],
        'empresas_medianas': [],
        'empresas_grandes': [],
        'expedientes_generados': [],
        'carga_orientacion': [],
        'carga_orientacion_pequena': [],
        'carga_orientacion_mediana': [],
        'carga_orientacion_grande': [],
        'fte_orientacion': [],
        'fte_orientacion_pequena': [],
        'fte_orientacion_mediana': [],
        'fte_orientacion_grande': [],
        'personas_orientacion': [],
        'personas_orientacion_pequena': [],
        'personas_orientacion_mediana': [],
        'personas_orientacion_grande': [],
        'carga_inscripcion': [],
        'fte_inscripcion': [],
        'personas_inscripcion': [],
        'carga_asesoramiento': [],
        'fte_asesoramiento': [],
        'personas_asesoramiento': [],
        'carga_evaluacion': [],
        'fte_evaluacion': [],
        'personas_evaluacion': [],
        'carga_acreditacion': [],
        'fte_acreditacion': [],
        'personas_acreditacion': []
    }
    
    for mes in range(1, 6):
        idx = mes - 1
        
        # Empresas totales este mes
        total_empresas = empresas_totales_ajustadas[idx]
        
        # Distribuir por tipología
        pequenas_mes, medianas_mes, grandes_mes = distribuir_empresas_por_tipologia(total_empresas)
        empresas_mes = [pequenas_mes, medianas_mes, grandes_mes]
        
        # Expedientes generados este mes
        expedientes_mes = calcular_expedientes_mes(empresas_mes)
        
        # 1. ORIENTACIÓN
        # Calcular carga por tipología usando los tiempos por tipo
        tiempos_por_tipo = calcular_tiempos_orientacion_por_tipo(sesiones_adicionales_por_tipo)

        carga_orientacion_peq = pequenas_mes * tiempos_por_tipo['pequena']
        carga_orientacion_med = medianas_mes * tiempos_por_tipo['mediana']
        carga_orientacion_gr = grandes_mes * tiempos_por_tipo['grande']

        carga_orientacion = carga_orientacion_peq + carga_orientacion_med + carga_orientacion_gr

        fte_orientacion_peq = carga_orientacion_peq / minutos_por_fte
        fte_orientacion_med = carga_orientacion_med / minutos_por_fte
        fte_orientacion_gr = carga_orientacion_gr / minutos_por_fte

        fte_orientacion = carga_orientacion / minutos_por_fte

        personas_orientacion_peq = int(np.ceil(fte_orientacion_peq))
        personas_orientacion_med = int(np.ceil(fte_orientacion_med))
        personas_orientacion_gr = int(np.ceil(fte_orientacion_gr))

        personas_orientacion = int(np.ceil(fte_orientacion))
        
        # 2. INSCRIPCIÓN
        if mes == 1:
            tiempo_inscripcion = tiempo_inscripcion_mes1
        else:
            tiempo_inscripcion = tiempo_inscripcion_mes2plus
        
        carga_inscripcion = expedientes_mes * tiempo_inscripcion
        fte_inscripcion = carga_inscripcion / minutos_por_fte
        personas_inscripcion = int(np.ceil(fte_inscripcion))
        
        # 3. ASESORAMIENTO (solo a partir del mes 2)
        if mes >= 2:
            carga_asesoramiento = expedientes_mes * tiempo_asesoramiento
            fte_asesoramiento = carga_asesoramiento / minutos_por_fte
            personas_asesoramiento = int(np.ceil(fte_asesoramiento))
        else:
            carga_asesoramiento = 0
            fte_asesoramiento = 0
            personas_asesoramiento = 0
        
        # 4. EVALUACIÓN (solo a partir del mes 2)
        if mes >= 2:
            carga_evaluacion = expedientes_mes * tiempo_evaluacion
            fte_evaluacion = carga_evaluacion / minutos_por_fte
            personas_evaluacion = int(np.ceil(fte_evaluacion))
        else:
            carga_evaluacion = 0
            fte_evaluacion = 0
            personas_evaluacion = 0
        
        # 5. ACREDITACIÓN (solo a partir del mes 2)
        if mes >= 2:
            carga_acreditacion = expedientes_mes * tiempo_acreditacion
            fte_acreditacion = carga_acreditacion / minutos_por_fte
            personas_acreditacion = int(np.ceil(fte_acreditacion))
        else:
            carga_acreditacion = 0
            fte_acreditacion = 0
            personas_acreditacion = 0
        
        # Almacenar resultados
        resultados['mes'].append(mes)
        resultados['empresas_entrantes'].append(total_empresas)
        resultados['empresas_pequenas'].append(pequenas_mes)
        resultados['empresas_medianas'].append(medianas_mes)
        resultados['empresas_grandes'].append(grandes_mes)
        resultados['expedientes_generados'].append(expedientes_mes)
        resultados['carga_orientacion'].append(carga_orientacion)
        resultados['carga_orientacion_pequena'].append(carga_orientacion_peq)
        resultados['carga_orientacion_mediana'].append(carga_orientacion_med)
        resultados['carga_orientacion_grande'].append(carga_orientacion_gr)
        resultados['fte_orientacion'].append(fte_orientacion)
        resultados['fte_orientacion_pequena'].append(fte_orientacion_peq)
        resultados['fte_orientacion_mediana'].append(fte_orientacion_med)
        resultados['fte_orientacion_grande'].append(fte_orientacion_gr)
        resultados['personas_orientacion'].append(personas_orientacion)
        resultados['personas_orientacion_pequena'].append(personas_orientacion_peq)
        resultados['personas_orientacion_mediana'].append(personas_orientacion_med)
        resultados['personas_orientacion_grande'].append(personas_orientacion_gr)
        resultados['carga_inscripcion'].append(carga_inscripcion)
        resultados['fte_inscripcion'].append(fte_inscripcion)
        resultados['personas_inscripcion'].append(personas_inscripcion)
        resultados['carga_asesoramiento'].append(carga_asesoramiento)
        resultados['fte_asesoramiento'].append(fte_asesoramiento)
        resultados['personas_asesoramiento'].append(personas_asesoramiento)
        resultados['carga_evaluacion'].append(carga_evaluacion)
        resultados['fte_evaluacion'].append(fte_evaluacion)
        resultados['personas_evaluacion'].append(personas_evaluacion)
        resultados['carga_acreditacion'].append(carga_acreditacion)
        resultados['fte_acreditacion'].append(fte_acreditacion)
        resultados['personas_acreditacion'].append(personas_acreditacion)
    
    return pd.DataFrame(resultados)

# ============================================================================
# BOTÓN DE SIMULACIÓN Y RESULTADOS
# ============================================================================

if st.button("🚀 Ejecutar Simulación", type="primary"):
    
    # Ejecutar simulación
    df_resultados = ejecutar_simulacion()
    # Verificar si la simulación fue exitosa
    if df_resultados is None:
        st.stop()
    
    st.header(f"📊 Resultados - Escenario {escenario}")
    
    # ========================================================================
    # KPIs GENERALES
    # ========================================================================
    st.subheader("📈 KPIs Generales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_empresas = df_resultados['empresas_entrantes'].sum()
        st.metric("Total Empresas Atendidas", f"{total_empresas:,}")
    
    with col2:
        total_expedientes = df_resultados['expedientes_generados'].sum()
        st.metric("Total Expedientes Procesados", f"{total_expedientes:,}")
    
    with col3:
        max_fte_total = (
            df_resultados['fte_orientacion'].max() +
            df_resultados['fte_inscripcion'].max() +
            df_resultados['fte_asesoramiento'].max() +
            df_resultados['fte_evaluacion'].max() +
            df_resultados['fte_acreditacion'].max()
        )
        st.metric("FTE Máximo Total (pico)", f"{max_fte_total:.2f}")
    
    with col4:
        max_personas_total = (
            df_resultados['personas_orientacion'].max() +
            df_resultados['personas_inscripcion'].max() +
            df_resultados['personas_asesoramiento'].max() +
            df_resultados['personas_evaluacion'].max() +
            df_resultados['personas_acreditacion'].max()
        )
        st.metric("Personas Máximo Total (pico)", f"{max_personas_total:,}")
    
    # ========================================================================
    # TABLA RESUMEN POR MES
    # ========================================================================
    st.subheader("📋 Resumen por Mes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Empresas por Tipología**")
        df_empresas_detalle = df_resultados[['mes', 'empresas_entrantes', 'empresas_pequenas', 'empresas_medianas', 'empresas_grandes']].copy()
        df_empresas_detalle.columns = ['Mes', 'Total', 'Pequeñas', 'Medianas', 'Grandes']
        st.dataframe(df_empresas_detalle, hide_index=True, use_container_width=True)
    
    with col2:
        st.write("**Expedientes Generados**")
        df_expedientes = df_resultados[['mes', 'expedientes_generados']].copy()
        df_expedientes.columns = ['Mes', 'Expedientes']
        st.dataframe(df_expedientes, hide_index=True, use_container_width=True)
        
        st.write("**Totales 5 Meses**")
        totales = pd.DataFrame({
            'Concepto': ['Empresas', 'Expedientes'],
            'Total': [
                df_resultados['empresas_entrantes'].sum(),
                df_resultados['expedientes_generados'].sum()
            ]
        })
        st.dataframe(totales, hide_index=True, use_container_width=True)
    
    # ========================================================================
    # TABLA DE FTE Y PERSONAS POR PROCESO
    # ========================================================================
    st.subheader("👥 Dimensionamiento por Fase del Proceso y Mes")
    
    # Crear tabla pivotada para mejor visualización
    procesos = ['Orientación', 'Inscripción', 'Asesoramiento', 'Evaluación', 'Acreditación']
    
    for proceso in procesos:
        st.write(f"**{proceso}**")
        
        proceso_key = proceso.lower().replace('ó', 'o').replace('ñ', 'n')
        
        df_proceso = pd.DataFrame({
            'Mes': df_resultados['mes'],
            'FTE': df_resultados[f'fte_{proceso_key}'].round(2),
            'Personas': df_resultados[f'personas_{proceso_key}'],
            'Carga (min)': df_resultados[f'carga_{proceso_key}'].astype(int)
        })
        
        st.dataframe(df_proceso, hide_index=True, use_container_width=True)
        # Si es Orientación, mostrar desglose por tipología
        if proceso_key == 'orientacion':
            df_orient_tipo = pd.DataFrame({
                'Mes': df_resultados['mes'],
                'Carga Pequeña (min)': df_resultados['carga_orientacion_pequena'].astype(int),
                'Carga Mediana (min)': df_resultados['carga_orientacion_mediana'].astype(int),
                'Carga Grande (min)': df_resultados['carga_orientacion_grande'].astype(int),
                'FTE Pequeña': df_resultados['fte_orientacion_pequena'].round(2),
                'FTE Mediana': df_resultados['fte_orientacion_mediana'].round(2),
                'FTE Grande': df_resultados['fte_orientacion_grande'].round(2),
                'Personas Pequeña': df_resultados['personas_orientacion_pequena'],
                'Personas Mediana': df_resultados['personas_orientacion_mediana'],
                'Personas Grande': df_resultados['personas_orientacion_grande']
            })
            st.write("**Desglose Orientación por Tipología**")
            st.dataframe(df_orient_tipo, hide_index=True, use_container_width=True)

        st.markdown("---")
    
    # ========================================================================
    # TABLA CONSOLIDADA FTE
    # ========================================================================
    st.subheader("📊 Tabla Consolidada - FTE por Proceso y Mes")
    
    df_fte_consolidado = pd.DataFrame({
        'Mes': df_resultados['mes'],
        'Orientación': df_resultados['fte_orientacion'].round(2),
        'Inscripción': df_resultados['fte_inscripcion'].round(2),
        'Asesoramiento': df_resultados['fte_asesoramiento'].round(2),
        'Evaluación': df_resultados['fte_evaluacion'].round(2),
        'Acreditación': df_resultados['fte_acreditacion'].round(2)
    })
    
    df_fte_consolidado['TOTAL'] = df_fte_consolidado.iloc[:, 1:].sum(axis=1).round(2)
    
    st.dataframe(df_fte_consolidado, hide_index=True, use_container_width=True)
    
    # ========================================================================
    # TABLA CONSOLIDADA PERSONAS
    # ========================================================================
    st.subheader("📊 Tabla Consolidada - Personas por Proceso y Mes")
    
    df_personas_consolidado = pd.DataFrame({
        'Mes': df_resultados['mes'],
        'Orientación': df_resultados['personas_orientacion'],
        'Inscripción': df_resultados['personas_inscripcion'],
        'Asesoramiento': df_resultados['personas_asesoramiento'],
        'Evaluación': df_resultados['personas_evaluacion'],
        'Acreditación': df_resultados['personas_acreditacion']
    })
    
    df_personas_consolidado['TOTAL'] = df_personas_consolidado.iloc[:, 1:].sum(axis=1)
    
    st.dataframe(df_personas_consolidado, hide_index=True, use_container_width=True)
    
    # ========================================================================
    # ANÁLISIS DE PICOS
    # ========================================================================
    st.subheader("🔝 Análisis de Picos por Proceso")
    
    analisis_picos = pd.DataFrame({
        'Proceso': procesos,
        'FTE Máximo': [
            df_resultados['fte_orientacion'].max(),
            df_resultados['fte_inscripcion'].max(),
            df_resultados['fte_asesoramiento'].max(),
            df_resultados['fte_evaluacion'].max(),
            df_resultados['fte_acreditacion'].max()
        ],
        'Mes Pico': [
            df_resultados.loc[df_resultados['fte_orientacion'].idxmax(), 'mes'],
            df_resultados.loc[df_resultados['fte_inscripcion'].idxmax(), 'mes'],
            df_resultados.loc[df_resultados['fte_asesoramiento'].idxmax(), 'mes'],
            df_resultados.loc[df_resultados['fte_evaluacion'].idxmax(), 'mes'],
            df_resultados.loc[df_resultados['fte_acreditacion'].idxmax(), 'mes']
        ],
        'Personas Máximo': [
            df_resultados['personas_orientacion'].max(),
            df_resultados['personas_inscripcion'].max(),
            df_resultados['personas_asesoramiento'].max(),
            df_resultados['personas_evaluacion'].max(),
            df_resultados['personas_acreditacion'].max()
        ]
    })
    
    analisis_picos['FTE Máximo'] = analisis_picos['FTE Máximo'].round(2)
    
    st.dataframe(analisis_picos, hide_index=True, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("**Simulador PAC v1.0** | Dimensionamiento de personal para procesos secuenciales")
