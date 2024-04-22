import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_images(url):
    """ Fetch images from the given URL """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    return [img['src'] if img['src'].startswith('http') else url + img['src'] for img in images if 'src' in img.attrs]

def check_webp(images):
    """ Check if the images are in WebP format """
    webp_images = [img for img in images if img.endswith('.webp')]
    return webp_images

def app():
    st.title('WebP Checker Tool')
    url = st.text_input('Enter the URL of the webpage:')
    
    if url:
        images = fetch_images(url)
        webp_images = check_webp(images)
        if webp_images:
            st.success(f"Found {len(webp_images)} WebP images:")
            for img in webp_images:
                st.image(img, caption=img)
        else:
            st.error("No WebP images found.")

if __name__ == "__main__":
    app()
