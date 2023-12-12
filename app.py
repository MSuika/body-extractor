import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title('Webpage Content Extractinator')

def extract_content_in_order(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.ConnectionError:
        st.error(f"Connection error for URL {url}")
        return []
    except requests.HTTPError as e:
        st.error(f"HTTP error for URL {url}: {e}")
        return []
    except requests.RequestException as e:
        st.error(f"Error fetching URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    content = []
    for element in soup.find('body').find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        tag = element.name
        text = element.text.strip()
        if text:  # Exclude empty elements
            content.append(f"<{tag}>{text}</{tag}>")

    return content

urls = st.text_area("Enter up to 6 URLs (separated by new lines):").split("\n")

if st.button('Extract Content'):
    all_content = []
    for url in urls:
        if url.strip():
            content = extract_content_in_order(url)
            if content:
                all_content.append(f"URL: {url}\n")  # Present URL as plain text
                all_content.extend(content)

    combined_content = "\n".join(all_content)
    copy_html = f"""
        <textarea id="copyText" style="width:100%;height:200px;">{combined_content}</textarea>
        <button onclick="copyToClipboard()">Copy to Clipboard</button>
        <script>
            function copyToClipboard() {{
                var copyText = document.getElementById("copyText");
                copyText.select();
                document.execCommand("copy");
            }}
        </script>
    """
    st.components.v1.html(copy_html, height=250)

    for item in all_content:
        st.markdown(item, unsafe_allow_html=True)

if st.button('Extract Content', key='extract_content_button'):
    all_content = []
    for url in urls:
        if url.strip():
            content = extract_content_in_order(url)
            if content:
                all_content.append(f"URL: {url}\n")
                all_content.extend(content)

    combined_content = "\n".join(all_content)

    # Check if there is content to download
    if combined_content:
        # Use Streamlit's download button to offer the text for download
        st.download_button(
            label="Download Extracted Content as TXT",
            data=combined_content,
            file_name="extracted_content.txt",
            mime="text/plain"
        )

    # Display the content in the app (as you have already implemented)
    for item in all_content:
        st.markdown(item, unsafe_allow_html=True)

st.sidebar.header("About the App")
st.sidebar.text("This app extracts content in the order it appears on the web pages, including headings and paragraphs, from up to 6 URLs.")
