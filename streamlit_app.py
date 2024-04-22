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
    st.title('Formato Immagini Web Checker')
    url = st.text_input('Inserisci la URL della pagina web:')
    
    if url:
        images_dict = fetch_images(url)
        
        if images_dict['webp']:
            st.success(f"WebP Images: {len(images_dict['webp'])} trovate.")
            for img in images_dict['webp']:
                st.write(img)
        else:
            st.error("Non sono state trovate immagini WebP in questo sito.")
        
        if images_dict['jpeg']:
            st.info(f"JPG/JPEG Images: {len(images_dict['jpeg'])} che non utilizzano WebP.")
            for img in images_dict['jpeg']:
                st.write(img)
        
        if images_dict['png']:
            st.info(f"PNG Images: {len(images_dict['png'])} che non utilizzano WebP.")
            for img in images_dict['png']:
                st.write(img)

if __name__ == "__main__":
    app()
