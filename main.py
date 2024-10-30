import streamlit as st;
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_cleaned_content)

from parse import parse_with_ollama

st.title('AI Web Scraper')
url=st.text_input("Enter website URL : " )

if st.button('Scrape Site'):
    st.write('Scraping started')
    resuls = scrape_website(url)
    
    body_content = extract_body_content(resuls)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM content"):
        st.text_area('DOM Content', cleaned_content, height=500)

#Ask user which content is necessary to be extracted
if 'dom_content' in st.session_state:
    parse_description = st.text_area("Describe what you want to parse ?")

    if st.button("Parse Content"):
        if parse_description:
            st.write('Parsing the content')
            dom_chunks = split_cleaned_content(st.session_state.dom_content)
            results=parse_with_ollama(dom_chunks, parse_description)
            st.write(results)