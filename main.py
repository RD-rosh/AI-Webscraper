import streamlit as st;
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_cleaned_content)

from parse import parse_with_ollama

st.set_page_config(
    page_title="InfoScrapey",
    layout="wide",
)

col1, col2 = st.columns([5, 1])

with col1:
    st.title('InfoScrapey')
    url=st.text_input("Enter website URL : " )
     
    if st.button('Scrape Site'):
        progress_bar = st.progress(0)
        progress_bar.progress(10)
        st.write('Scraping started')
        results = scrape_website(url)
        progress_bar.progress(40)
        body_content = extract_body_content(results)
        progress_bar.progress(70)
        cleaned_content = clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content
        progress_bar.progress(100)
        with st.expander("View Content"):
            st.text_area('Content', cleaned_content, height=500)
    
    with col2:
        st.image('image.png', use_column_width=True)

    #Ask user which content is necessary to be extracted
    if 'dom_content' in st.session_state:
        parse_description = st.text_area("Describe what you want to parse ?")

        if st.button("Parse Content"):
            if parse_description:
                st.write('Parsing the content')
                dom_chunks = split_cleaned_content(st.session_state.dom_content)
                progress_bar = st.progress(0)

                def update_progress(progress):
                    progress_bar.progress(progress)
                
                results=parse_with_ollama(dom_chunks, parse_description, update_progress)
                #results_download = ''.join(results)
                st.session_state.parsed_results = results

            if 'downloaded' not in st.session_state:
                    st.session_state.downloaded = False

            col1, col2, col3 = st.columns(3)

            with col1:
                if not st.session_state.downloaded:
                    if st.download_button(
                        label='Download as TXT',
                        data=results,
                        file_name='results.txt',
                        mime='text/plain'
                    ):
                        st.session_state.downloaded = True

            with col2:
                if not st.session_state.downloaded:
                    if st.download_button(
                        label='Download as CSV',
                        data=results,
                        file_name='results.csv',
                        mime='text/csv'
                    ):
                        st.session_state.downloaded = True

            with col3:
                if not st.session_state.downloaded:
                    if st.download_button(
                        label='Download as JSON',
                        data=results,
                        file_name='results.json',
                        mime='application/json'
                    ):
                        st.session_state.downloaded = True
                
    if 'parsed_results' in st.session_state:
        st.write("Parsed Results:")
        st.write(st.session_state.parsed_results)

            