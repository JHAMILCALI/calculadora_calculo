import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import *
import numpy as np
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Calculadora de Integrales", page_icon="📐")

st.title("🧮 Calculadora de Cálculo Integral con Paso a Paso")

# Inicializar estados de sesión
if 'function_input' not in st.session_state:
    st.session_state['function_input'] = "x^2 + exp(x)"
if 'integral_variable' not in st.session_state:
    st.session_state['integral_variable'] = "x"
if 'integral_lower_limit' not in st.session_state:
    st.session_state['integral_lower_limit'] = "0"
if 'integral_upper_limit' not in st.session_state:
    st.session_state['integral_upper_limit'] = "1"

# Entrada del usuario
with st.form("input_form"):
    st.subheader("1️⃣ Ingresa la función a integrar")
    function_input = st.text_input("Función (usa x como variable):", key="function_input")
    st.subheader("2️⃣ Límite inferior y superior (opcional para integral definida)")
    col1, col2, col3 = st.columns(3)
    with col1:
        integral_variable = st.text_input("Variable de integración:", key="integral_variable")
    with col2:
        integral_lower = st.text_input("Límite inferior:", key="integral_lower_limit")
    with col3:
        integral_upper = st.text_input("Límite superior:", key="integral_upper_limit")
    submitted = st.form_submit_button("Calcular")

# Procesamiento
if submitted:
    try:
        expr = parse_expr(function_input, transformations='all')
        var = parse_expr(integral_variable, transformations='all')
        lower = parse_expr(integral_lower, transformations='all')
        upper = parse_expr(integral_upper, transformations='all')

        st.subheader("📌 Función original:")
        st.latex("f(x) = " + sp.latex(expr))

        # Paso a paso simbólico
        st.subheader("📋 Integral indefinida paso a paso:")
        st.markdown("- **Paso 1:** Escribimos la integral:")
        st.latex(r"\int " + sp.latex(expr) + r"\, d" + sp.latex(var))

        # Regla básica (esto es simbólico, no 100% paso a paso real)
        result = sp.integrate(expr, var)
        st.markdown("- **Paso 2:** Aplicamos reglas de integración:")
        st.latex(r"= " + sp.latex(result))

        st.subheader("📐 Integral definida:")
        st.latex(r"\int_{" + sp.latex(lower) + r"}^{" + sp.latex(upper) + r"} " + sp.latex(expr) + r"\, d" + sp.latex(var))
        value = sp.integrate(expr, (var, lower, upper))
        st.latex(r"= " + sp.latex(value))
        # Generar gráfica con GeoGebra mostrando la función y el área bajo la curva
        st.subheader("📊 Gráfica interactiva con GeoGebra: función + área bajo la curva")

        ggb_script = f"""
        <script src="https://www.geogebra.org/apps/deployggb.js"></script>
        <div id="ggb-element"></div>
        <script>
        var ggbApp = new GGBApplet({{
            "appName": "graphing",
            "showToolBar": false,
            "showAlgebraInput": false,
            "showMenuBar": false,
            "width": 800,
            "height": 400,
            "appletOnLoad": function(api) {{
                api.evalCommand("f(x) = {function_input}");
                api.evalCommand("a = {float(lower)}");
                api.evalCommand("b = {float(upper)}");
                api.evalCommand("Integral(f, a, b)");
            }}
        }}, true);
        window.addEventListener("load", function() {{
            ggbApp.inject('ggb-element');
        }});
        </script>
        """
        components.html(ggb_script, height=450)

        # Generar gráfica con GeoGebra
        st.subheader("📊 Gráfica interactiva con GeoGebra")

        ggb_script = f"""
        <script src="https://www.geogebra.org/apps/deployggb.js"></script>
        <div id="ggb-element"></div>
        <script>
          var ggbApp = new GGBApplet({{
              "appName": "graphing",
              "showToolBar": false,
              "showAlgebraInput": false,
              "showMenuBar": false,
              "width": 800,
              "height": 400,
              "appletOnLoad": function(api) {{
                  api.evalCommand("f(x) = {function_input}");
              }}
          }}, true);
          window.addEventListener("load", function() {{
              ggbApp.inject('ggb-element');
          }});
        </script>
        """
        components.html(ggb_script, height=450)

    except Exception as e:
        st.error("Ocurrió un error al procesar la función. Verifica la sintaxis.")
        st.exception(e)
