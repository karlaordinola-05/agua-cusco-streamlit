import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Dashboard: Cobertura de Agua en Cusco")
file_path = "Indicadores_de_Cobertura_en_el_Servicio_de_Agua_Potable_en_el_Departamento_de_Cusco_2016_2019.csv"

# Cargar datos
try:
    data = pd.read_csv(file_path, sep=';', encoding='utf-8')
except UnicodeDecodeError:
    data = pd.read_csv(file_path, sep=';', encoding='latin1')

# Procesar datos
data['FECHA_CORTE'] = pd.to_datetime(data['FECHA_CORTE'], format='%Y%m%d', errors='coerce')
data['PORCENTAJE_CON_COBERTURA'] = (data['POBLACION_CON_COBERTURA'] / data['TOTAL_POBLACION']) * 100
data['PORCENTAJE_SIN_COBERTURA'] = (data['POBLACION_SIN_COBERTURA'] / data['TOTAL_POBLACION']) * 100

# Filtrar distritos con población sin cobertura
distritos_con_problemas = data[data['POBLACION_SIN_COBERTURA'] > 0]

# Mostrar resumen
st.subheader("Resumen del Dataset")
st.write(f"Total de departamentos: {data['DEPARTAMENTO'].nunique()}")
st.write(f"Total de provincias: {data['PROVINCIA'].nunique()}")
st.write(f"Total de distritos: {data['DISTRITO'].nunique()}")
st.write(f"Distritos con población sin cobertura: {distritos_con_problemas['DISTRITO'].nunique()}")

# Gráfico 1: Gráfico de Torta de Cobertura en un Distrito (existente)
st.subheader("Análisis por Distrito")
distrito_seleccionado = st.selectbox(
    "Selecciona un distrito para analizar",
    distritos_con_problemas['DISTRITO'].unique()
)

distrito_data = distritos_con_problemas[distritos_con_problemas['DISTRITO'] == distrito_seleccionado]

total_con_cobertura = distrito_data['POBLACION_CON_COBERTURA'].sum()
total_sin_cobertura = distrito_data['POBLACION_SIN_COBERTURA'].sum()

# Gráfico comparativo
st.subheader(f"Distribución de Cobertura de Agua en {distrito_seleccionado}")
fig1, ax1 = plt.subplots()
labels = ['Con Acceso a Agua', 'Sin Acceso a Agua']
sizes = [total_con_cobertura, total_sin_cobertura]
colors = ['blue', 'red']
ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Asegura que el gráfico sea un círculo
plt.title(f"Población sin agua vs población con agua en {distrito_seleccionado}")
st.pyplot(fig1)

# Gráfico 2: Bar Chart - Top 5 Provincias con mayor Población sin Cobertura
st.subheader("Provincias con Mayor Población sin Cobertura de Agua")
provincia_sin_cobertura = data.groupby('PROVINCIA')['POBLACION_SIN_COBERTURA'].sum().reset_index()
top5_provincias = provincia_sin_cobertura.sort_values(by='POBLACION_SIN_COBERTURA', ascending=False).head(5)
fig2, ax2 = plt.subplots()
ax2.bar(top5_provincias['PROVINCIA'], top5_provincias['POBLACION_SIN_COBERTURA'], color='orange')
plt.xticks(rotation=45)
plt.ylabel('Población sin Cobertura')
plt.title('Top 5 Provincias con Mayor Población sin Cobertura')
st.pyplot(fig2)

# Gráfico 3: Línea de Tiempo - Cobertura en el Distrito Seleccionado
st.subheader(f"Evolución de Cobertura en {distrito_seleccionado} a lo largo del tiempo")
distrito_data_sorted = distrito_data.sort_values('FECHA_CORTE')
fig3, ax3 = plt.subplots()
ax3.plot(distrito_data_sorted['FECHA_CORTE'], distrito_data_sorted['PORCENTAJE_CON_COBERTURA'], marker='o')
plt.xticks(rotation=45)
plt.ylabel('Porcentaje de Cobertura')
plt.title(f"Evolución de Cobertura en {distrito_seleccionado}")
st.pyplot(fig3)

# Gráfico 4: Histograma - Distribución de Cobertura en Distritos
st.subheader("Distribución del Porcentaje de Cobertura en Todos los Distritos")
fig4, ax4 = plt.subplots()
ax4.hist(data['PORCENTAJE_CON_COBERTURA'], bins=20, color='green', edgecolor='black')
plt.xlabel('Porcentaje de Cobertura')
plt.ylabel('Número de Distritos')
plt.title('Distribución de Cobertura en Distritos')
st.pyplot(fig4)

# Gráfico 5: Scatter Plot - Población Total vs Porcentaje de Cobertura
st.subheader("Relación entre Población Total y Porcentaje de Cobertura en Distritos")
fig5, ax5 = plt.subplots()
ax5.scatter(data['TOTAL_POBLACION'], data['PORCENTAJE_CON_COBERTURA'], alpha=0.5)
plt.xlabel('Población Total')
plt.ylabel('Porcentaje de Cobertura')
plt.title('Población vs Cobertura')
st.pyplot(fig5)

# Tabla de datos del distrito seleccionado
st.subheader("Datos del Distrito Seleccionado")
st.dataframe(distrito_data)

# Conclusiones
st.subheader("Conclusiones")
st.write("""
- El gráfico de torta muestra la distribución de población con y sin acceso a agua en el distrito seleccionado.
- El gráfico de barras presenta las provincias con mayor cantidad de población sin cobertura de agua.
- El gráfico de línea muestra cómo ha cambiado la cobertura en el distrito seleccionado a lo largo del tiempo.
- El histograma indica cómo se distribuye el porcentaje de cobertura entre todos los distritos.
- El scatter plot permite visualizar la relación entre la población total de un distrito y su porcentaje de cobertura.
""")
