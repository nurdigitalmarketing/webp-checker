import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_images(url):
    """ Fetch images from the given URL and check for WebP format """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    webp_images = [img['src'] for img in images if 'src' in img.attrs and img['src'].endswith('.webp')]
    return webp_images

def app():
    st.title('WebP Usage Checker Tool')
    url = st.text_input('Enter the URL of the webpage:')
    
    if url:
        webp_images = fetch_images(url)
        if webp_images:
            st.success(f"WebP images are being used on this site. Total: {len(webp_images)} WebP images found.")
            for img in webp_images:
                st.write(img)
        else:
            st.error("No WebP images found on this site.")

if __name__ == "__main__":
    app()
