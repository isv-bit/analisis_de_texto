import streamlit as st 
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator
from PIL import Image

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Analizador de Texto Simple",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# 🎨 ESTILOS (AZUL + MAGENTA)
# =====================================================
st.markdown("""
<style>

/* FONDO GENERAL */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* TITULOS */
h1, h2, h3 {
    color: #00c6ff !important;
}

/* TEXTO */
p, label, div {
    color: #e2e8f0 !important;
}

/* BOTONES */
.stButton>button {
    background: linear-gradient(135deg, #ff0080, #00c6ff);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(255,0,150,0.6);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* INPUT */
.stTextArea textarea {
    border-radius: 10px;
    border: 1px solid #00c6ff;
}

/* PROGRESS */
.stProgress > div > div {
    background: linear-gradient(90deg, #ff0080, #00c6ff);
}

</style>
""", unsafe_allow_html=True)


# TITULO
# =====================================================
st.title("📝 Analizador de Texto con IA")
st.markdown("""
Analiza texto usando inteligencia artificial:
- 💡 Sentimiento
- 📊 Frecuencia de palabras
- 🌐 Traducción automática
""")
# =====================================================
# 🖼️ IMAGEN 
# =====================================================
image = Image.open("analisistexto.jpg")  # puedes cambiarla
st.image(image, width=300)
# =====================================================
# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("⚙️ Opciones")
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
)

# =====================================================
# FUNCIONES (NO TOCADAS)
# =====================================================
def contar_palabras(texto):
    stop_words = set(["a","de","la","el","y","the","and","is","in","to"])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]

    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1

    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True)), palabras_filtradas

translator = Translator()

def traducir_texto(texto):
    try:
        return translator.translate(texto, src='es', dest='en').text
    except:
        return texto

def procesar_texto(texto):
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)

    return {
        "sentimiento": blob.sentiment.polarity,
        "subjetividad": blob.sentiment.subjectivity,
        "contador_palabras": contar_palabras(texto_ingles)[0],
        "texto_original": texto,
        "texto_traducido": texto_ingles
    }

# =====================================================
# VISUALIZACIÓN
# =====================================================
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Sentimiento")
        st.progress((resultados["sentimiento"] + 1)/2)

        if resultados["sentimiento"] > 0:
            st.success("😊 Positivo")
        elif resultados["sentimiento"] < 0:
            st.error("😟 Negativo")
        else:
            st.info("😐 Neutral")

        st.subheader("💭 Subjetividad")
        st.progress(resultados["subjetividad"])

    with col2:
        st.subheader("🔥 Palabras frecuentes")
        st.bar_chart(resultados["contador_palabras"])

    st.subheader("🌐 Traducción")
    col1, col2 = st.columns(2)

    with col1:
        st.text(resultados["texto_original"])
    with col2:
        st.text(resultados["texto_traducido"])

# =====================================================
# LOGICA PRINCIPAL
# =====================================================
if modo == "Texto directo":
    texto = st.text_area("Escribe tu texto...")

    if st.button("🚀 Analizar texto"):
        if texto:
            with st.spinner("Analizando..."):
                crear_visualizaciones(procesar_texto(texto))
        else:
            st.warning("Escribe algo")

elif modo == "Archivo de texto":
    archivo = st.file_uploader("Sube archivo", type=["txt"])

    if archivo:
        contenido = archivo.read().decode("utf-8")

        if st.button("📊 Analizar archivo"):
            crear_visualizaciones(procesar_texto(contenido))

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown("✨ Hecho con Streamlit + IA")
