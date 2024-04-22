import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_images(url):
    """ Recupera le immagini dall'URL indicato e verifica il formato WebP """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    webp_images = [img['src'] for img in images if 'src' in img.attrs and img['src'].endswith('.webp')]
    return webp_images

def app():
    st.title('WebP Checker Tool')
    url = st.text_input('Inserisci la URL della pagina web:')
    
    if url:
        webp_images = fetch_images(url)
        if webp_images:
            st.success(f"Questo sito utilizza immagini in WebP. Totale: {len(webp_images)} immagini WebP trovate.")
            for img in webp_images:
                st.write(img)
        else:
            st.error("Non sono state trovate immagini WebP in questo sito.")

if __name__ == "__main__":
    app()
