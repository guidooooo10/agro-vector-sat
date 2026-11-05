import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Agro Vector Sat", layout="wide")
st.title("🛰️ Agro Vector Sat: Monitoreo Agrícola y Geoespacial")
st.markdown("Herramienta de análisis topográfico, escorrentía y prevención de riesgos sísmicos.")

st.sidebar.header("Parámetros de Simulación")
masa = st.sidebar.slider("Masa del suelo simulada (kg)", 1.0, 5.0, 1.0)
sismo_activo = st.sidebar.checkbox("Simular Evento Sísmico")

x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
H = 10 * np.exp(-(X**2 + Y**2) / 10)
distancia_nodos = x[1] - x[0]
gravedad = 9.81

if sismo_activo:
    st.warning("⚠️ Alerta: Simulación de alteración topográfica por sismo activada.")
    perturbacion = 2.5 * np.exp(-((X - 1)**2 + (Y - 1)**2) / 2.0)
    H = H + perturbacion

grad_y, grad_x = np.gradient(H, distancia_nodos, distancia_nodos)
F_x = masa * gravedad * grad_x
F_y = masa * gravedad * grad_y
magnitud_fuerza = np.sqrt(F_x**2 + F_y**2)
v_x, v_y = -2 * X, -3 * Y

col1, col2 = st.columns(2)

with col1:
    st.subheader("Relieve y Escorrentía Hídrica")
    fig1 = plt.figure(figsize=(6, 5))
    ax1 = fig1.add_subplot(111)
    cp1 = ax1.contourf(X, Y, H, levels=20, cmap='terrain', alpha=0.6)
    ax1.quiver(X[::3, ::3], Y[::3, ::3], v_x[::3, ::3], v_y[::3, ::3], color='blue')
    fig1.colorbar(cp1, ax=ax1, label='Elevación')
    st.pyplot(fig1)

with col2:
    st.subheader("Mapa de Riesgo Gravitacional")
    fig2 = plt.figure(figsize=(6, 5))
    ax2 = fig2.add_subplot(111)
    cp2 = ax2.contourf(X, Y, magnitud_fuerza, levels=25, cmap='Reds')
    fig2.colorbar(cp2, ax=ax2, label='Fuerza Tangencial (N)')
    st.pyplot(fig2)
