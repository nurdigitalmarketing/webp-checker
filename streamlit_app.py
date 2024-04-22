import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_images(url):
    """ Recupera le immagini dall'URL indicato e verifica i formati """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    
    webp_count = 0
    jpeg_count = 0
    png_count = 0
    
    for img in images:
        src = img.get('src', '')
        if src.endswith('.webp'):
            webp_count += 1
        elif src.endswith('.jpeg') or src.endswith('.jpg'):
            jpeg_count += 1
        elif src.endswith('.png'):
            png_count += 1
    
    return webp_count, jpeg_count, png_count

def app():
    st.title('Formato Immagini Web Checker')
    url = st.text_input('Inserisci la URL della pagina web:')
    
    if url:
        webp_count, jpeg_count, png_count = fetch_images(url)
        
        if webp_count > 0:
            st.success(f"Questo sito utilizza immagini in WebP. Totale: {webp_count} immagini WebP trovate.")
        else:
            st.error("Non sono state trovate immagini WebP in questo sito.")
        
        if jpeg_count > 0:
            st.info(f"Ci sono {jpeg_count} immagini JPG/JPEG che non utilizzano WebP.")
        
        if png_count > 0:
            st.info(f"Ci sono {png_count} immagini PNG che non utilizzano WebP.")

if __name__ == "__main__":
    app()
