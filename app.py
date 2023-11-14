import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title('Webpage Content Extractinator')

def extract_headings_and_paragraphs(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        st.error(f"Error fetching URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    content = []
    # Extracting headings
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        indent = '    ' * (int(tag.name[1]) - 1)
        content.append(f"{indent}<{tag.name}>{tag.text.strip()}</{tag.name}>")

    # Extracting all paragraphs
    paragraphs = [f"<p>{para.text.strip()}</p>" for para in soup.find('body').find_all('p')]
    content.extend(paragraphs)

    return content

urls = st.text_area("Enter up to 6 URLs (separated by new lines):").split("\n")

if st.button('Extract Content'):
    all_content = []
    for url in urls:
        if url.strip():  # Check if the string is not empty or just whitespace
            content = extract_headings_and_paragraphs(url)
            all_content.extend(content)

    # Join all content and create a copy button
    combined_content = "\n".join(all_content)
    copy_html = """
        <textarea id="copyText" style="width:100%;height:200px;">{}</textarea>
        <button onclick="copyToClipboard()">Copy to Clipboard</button>
        <script>
            function copyToClipboard() {{
                var copyText = document.getElementById("copyText");
                copyText.select();
                document.execCommand("copy");
            }}
        </script>
    """.format(combined_content)
    st.components.v1.html(copy_html, height=250)

    for url in urls:
        if url.strip():
            st.write(f"\nURL {url}\n")
            content = extract_headings_and_paragraphs(url)
            for item in content:
                st.markdown(item, unsafe_allow_html=True)

# About the App section in the sidebar
st.sidebar.header("About the App")
st.sidebar.text("This app extracts headings and all paragraphs from the body of up to 6 URLs.")
