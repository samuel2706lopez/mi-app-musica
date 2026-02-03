import streamlit as st
import requests
import time

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO MAXIMALISTA ---
st.set_page_config(page_title="Music Hub Community", layout="wide")

# Inyectamos CSS personalizado para que NO parezca hecho por una IA robótica
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Spicy+Rice&family=Poppins:wght@400;700&display=swap');
    
    .stApp {
        background-color: #121212;
        color: #FFFAFA;
        font-family: 'Poppins', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Spicy Rice', serif;
        color: #FF4B4B;
        text-shadow: 3px 3px #FFD700;
    }
    
    .album-card {
        background: linear-gradient(135deg, #2b2b2b 0%, #1e1e1e 100%);
        border: 3px solid #FF4B4B;
        border-radius: 20px;
        padding: 15px;
        transition: transform 0.3s;
        box-shadow: 8px 8px 0px #FFD700;
    }
    
    .album-card:hover {
        transform: rotate(-2deg) scale(1.02);
    }
    
    .stButton>button {
        background-color: #FFD700;
        color: black;
        border-radius: 50px;
        border: 2px solid #FF4B4B;
        font-weight: bold;
        box-shadow: 4px 4px 0px #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE API ---
HEADERS = {'User-Agent': 'MusicCommunityHub/1.0 (tu-email@ejemplo.com)'}

def buscar_musica(query):
    time.sleep(1) # Límite de 1 seg para MusicBrainz
    url = f"https://musicbrainz.org/ws/2/release/?query={query}&fmt=json&limit=6"
    res = requests.get(url, headers=HEADERS)
    return res.json().get('releases', []) if res.status_code == 200 else []

# --- INTERFAZ DE NAVEGACIÓN (TABS) ---
tab1, tab2, tab3, tab4 = st.tabs(["🔥 Comunidad", "🏆 Tops Mensuales", "🔍 Buscador", "👤 Mi Perfil"])

with tab1:
    st.header("Discos de la Semana")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("💿 Disco Grupal: 'Un Verano Sin Ti'")
        st.image("https://coverartarchive.org/release/9991206f-6140-4229-bc9d-c7b41b124823/front-500", width=300)
        st.write("**Debate del día:** ¿Qué opinas de la producción de este álbum?")
        st.text_area("Escribe tu reseña...", placeholder="Me encanta el ritmo pero...")
        if st.button("Publicar Opinión"):
            st.success("¡Opinión compartida con la comunidad!")

with tab2:
    st.header("Monthly TOP 10 (Votos)")
    st.write("Vota por lo mejor de Febrero")
    st.info("1. Bad Bunny | 2. Taylor Swift | 3. Kendrick Lamar")
    # Aquí iría la lógica de votación que pediste

with tab3:
    st.header("Descubre Música")
    query = st.text_input("Busca un artista o álbum para debatir:", placeholder="Ej: Rosalía")
    
    if query:
        resultados = buscar_musica(query)
        cols = st.columns(3)
        for i, album in enumerate(resultados):
            with cols[i % 3]:
                st.markdown(f"""<div class="album-card">
                    <h4>{album['title']}</h4>
                    <p>{album['artist-credit'][0]['name']}</p>
                </div>""", unsafe_allow_html=True)
                img_url = f"https://coverartarchive.org/release/{album['id']}/front-250"
                st.image(img_url, use_container_width=True)
                if st.button("Añadir al Foro", key=album['id']):
                    st.session_state.foro = album['title']
                    st.write("¡Añadido!")

with tab4:
    st.header("Tu Perfil Melómano")
    st.write("Seguidores: 128 | Siguiendo: 45")
    st.button("Seguir nuevos perfiles")
