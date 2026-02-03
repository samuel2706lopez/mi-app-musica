import streamlit as st
import requests
import time

# Configuración de la página
st.set_page_config(page_title="Mi App de Música IA", layout="wide")
st.title("🎵 Explorador de Música (MusicBrainz)")

# --- CONFIGURACIÓN TÉCNICA ---
# MusicBrainz pide un User-Agent. Cámbialo por tu nombre/email.
HEADERS = {'User-Agent': 'MiAppMusical/1.0 (contacto@tuemail.com)'}
BASE_URL = "https://musicbrainz.org/ws/2/"

# Barra de búsqueda
busqueda = st.text_input("Busca un álbum o artista:", "")

if busqueda:
    # 1. Buscamos el álbum
    st.write(f"Buscando resultados para: {busqueda}...")
    params = {'query': busqueda, 'fmt': 'json', 'limit': 10}
    
    response = requests.get(f"{BASE_URL}release/", params=params, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        albums = data.get('releases', [])
        
        if not albums:
            st.warning("No se encontraron resultados.")
        else:
            # Creamos una cuadrícula de 3 columnas
            cols = st.columns(3)
            
            for idx, album in enumerate(albums):
                with cols[idx % 3]:
                    album_id = album['id']
                    titulo = album.get('title', 'Sin título')
                    artista = album.get('artist-credit', [{}])[0].get('name', 'Desconocido')
                    
                    # Intentamos traer la portada del Cover Art Archive
                    img_url = f"https://coverartarchive.org/release/{album_id}/front-250"
                    
                    st.image(img_url, caption=f"{titulo} - {artista}", use_container_width=True)
                    
                    # Botón para ver canciones
                    if st.button(f"Ver canciones", key=album_id):
                        # Pedimos las canciones de ese álbum específico
                        time.sleep(1) # Respetamos el límite de 1 seg de MusicBrainz
                        res_songs = requests.get(f"{BASE_URL}release/{album_id}?inc=recordings&fmt=json", headers=HEADERS)
                        if res_songs.status_code == 200:
                            songs_data = res_songs.json()
                            tracks = songs_data.get('media', [{}])[0].get('track-list', [])
                            for t in tracks:
                                st.write(f"▶ {t['title']}")
    else:
        st.error("Error al conectar con MusicBrainz. Inténtalo de nuevo en un momento.")
