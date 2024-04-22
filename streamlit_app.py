import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import pandas as pd

def fetch_images(url):
    """ Recupera le immagini dall'URL indicato e verifica i formati, restituendo un dizionario delle categorie con le rispettive immagini. """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    
    # Analizza l'URL per ottenere una base corretta che termina con uno slash
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    
    images_dict = {
        'webp': [],
        'jpeg': [],
        'png': []
    }
    
    for img in images:
        src = img.get('src', '')
        # Normalizza l'URL unendo il dominio se l'URL dell'immagine è relativo
        full_url = urljoin(base_url, src)
        
        if full_url.endswith('.webp'):
            images_dict['webp'].append(full_url)
        elif full_url.endswith('.jpeg') or full_url.endswith('.jpg'):
            images_dict['jpeg'].append(full_url)
        elif full_url.endswith('.png'):
            images_dict['png'].append(full_url)
    
    return images_dict

def display_images(category, images):
    """ Visualizza le prime 5 immagini e offre la possibilità di espandere per vedere tutte le immagini. """
    if len(images) > 5:
        expand = st.expander(f"Mostra tutte le {len(images)} immagini {category}")
        with expand:
            for img in images:
                st.markdown(f"[{img}]({img})")
    else:
        for img in images:
            st.markdown(f"[{img}]({img})")

def export_to_csv(category, images):
    """ Esporta la lista di immagini in formato CSV. """
    if st.button(f"Esporta {category} come CSV"):
        df = pd.DataFrame(images, columns=["URL"])
        st.download_button(
            label="Scarica CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"{category}_images.csv",
            mime='text/csv',
        )

def app():
    st.title('WebP Image Format Checker')
    url = st.text_input('Inserisci la URL della pagina web:')
    
    if url:
        images_dict = fetch_images(url)
        
        for category in ['webp', 'jpeg', 'png']:
            images = images_dict[category]
            if images:
                st.success(f"**{category.upper()}**: {len(images)} trovate.")
                display_images(category, images)
                export_to_csv(category, images)
            else:
                st.error(f"Non sono state trovate immagini {category.upper()} in questo URL.")

if __name__ == "__main__":
    app()
