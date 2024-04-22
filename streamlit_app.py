import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_images(url):
    """ Recupera le immagini dall'URL indicato e verifica i formati, restituendo un dizionario delle categorie con le rispettive immagini. """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    
    images_dict = {
        'webp': [],
        'jpeg': [],
        'png': []
    }
    
    for img in images:
        src = img.get('src', '')
        if src.endswith('.webp'):
            images_dict['webp'].append(src)
        elif src.endswith('.jpeg') or src.endswith('.jpg'):
            images_dict['jpeg'].append(src)
        elif src.endswith('.png'):
            images_dict['png'].append(src)
    
    return images_dict

def app():
    st.title('WebP Image Format Checker')
    url = st.text_input('Inserisci la URL della pagina web:')
    
    if url:
        images_dict = fetch_images(url)
        
        if images_dict['webp']:
            st.success(f"WebP Images: {len(images_dict['webp'])} trovate.")
            st.write("URL delle immagini WebP:")
            for img in images_dict['webp']:
                st.markdown(f"[{img}]({img})")
        
        if images_dict['jpeg']:
            st.info(f"JPG/JPEG Images: {len(images_dict['jpeg'])} che non utilizzano WebP.")
            st.write("URL delle immagini JPG/JPEG:")
            for img in images_dict['jpeg']:
                st.markdown(f"[{img}]({img})")
        
        if images_dict['png']:
            st.info(f"PNG Images: {len(images_dict['png'])} che non utilizzano WebP.")
            st.write("URL delle immagini PNG:")
            for img in images_dict['png']:
                st.markdown(f"[{img}]({img})")

if __name__ == "__main__":
    app()
