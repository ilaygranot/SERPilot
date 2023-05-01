from io import BytesIO
import tempfile
import streamlit as st
import pandas as pd
import time
import re
import os
import zipfile
from datetime import datetime as dt
from prompts import prompts
from app import (
    create_url_path,
    create_full_path,
    generate_content,
    generate_related_links,
    generate_article,
    MyHTMLParser,
    save_article_as_docx,
    render_expanders
)
from expanders import expanders

def generate_text(api_key, model, prompt, max_tokens, n, stop, temperature, top_p):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
        top_p=top_p,
    )

    return response

def article_app():
    st.title("Article Generation")
    st.subheader("Generate high-quality, SEO-friendly content using GPT-4")

    # UI Elements for Article Generation
    with st.sidebar:
        st.header("Article Generation Parameters")
        openai_api_key = st.text_input("OpenAI API Key", value="", help="Enter your OpenAI API Key.", type="password")
        gpt_model = st.selectbox("GPT Model", ["gpt-3.5-turbo", "gpt-4"], help="Select the GPT model you want to use for generating content.")
        marketing_term = st.text_input("Marketing Term", value="", help="Enter the marketing term you want to generate an article about.")
        generate_button = st.button("Generate Article")

    if generate_button:
        if not openai_api_key:
            st.error("Please provide an OpenAI API Key.")
        elif not marketing_term:
            st.error("Please provide a marketing term.")
        else:
            # Add your code here to generate the article using the OpenAI API
            openai.api_key = openai_api_key
            generated_article = generate_text(
                    openai_api_key,
                    model=gpt_model,
                    prompt=prompts["article_prompt"].format(
                    term, outline, prompts["related_links_prompt"].format("\n".join(related_links))
                ),
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.8,
                top_p=1,
            )

        generated_article = generated_article.choices[0].text.strip()

        st.header("Generated Article")
        st.write(generated_article)


        # Display the generated article
        st.header("Generated Article")
        st.write("The generated article will be displayed here.")

def serp_app():
    st.title("SERP Outline")
    st.subheader("Extract search results using SpaceSerp API and generate content outlines")

    # UI Elements for SERP Outline
    with st.sidebar:
        st.header("Parameters")
        api_key = st.text_input("API Key", value="", help="Enter your SpaceSerp API Key.", type="password")
        query_text = st.text_area("Query", value="", help="Enter one or multiple keywords to search (one per line).")
        search_queries = [q.strip() for q in query_text.split('\n') if q.strip()]
        domain = st.selectbox("Domain", [x["domain"] for x in google_domains])
        gl = st.selectbox("Country Code", [x["code"] for x in google_countries])
        hl = st.selectbox("Language Code", [x["code"] for x in google_languages])
        device = st.selectbox("Device", devices)
        mobile_os = st.selectbox("Mobile OS", mobile_os) if device != "desktop" else None
        page_size = st.number_input("Page Size", min_value=1, max_value=100, value=10, step=1)
        page_number = st.number_input("Page Number", min_value=1, max_value=100, value=1, step=1)
        result_blocks = st.multiselect("Result Blocks", result_block_options, help="Select the types of results you want to include.")

        # GPT Model Parameters
        openai_api_key = st.text_input("OpenAI API Key", value="", help="Enter your OpenAI API Key.", type="password")
        gpt_model = st.selectbox("GPT Model", ["gpt-3.5-turbo", "gpt-4"], help="Select the GPT model you want to use for generating outlines.")

    if st.button("Fetch Search Results"):
        if not api_key:
            st.error("Please provide an API key.")
        elif not query_text:
            st.error("Please provide a query.")
        elif not openai_api_key:
            st.error("Please provide an OpenAI API Key.")
        else:
            # Fetch Search Results
            search_results = get_search_results(api_key, search_queries, domain, gl, hl, device, mobile_os, page_size, page_number, result_blocks)
            if search_results:
                # Generate Outlines
                outlines = []
                for result in search_results:
                    outline = generate_outline(openai_api_key, gpt_model, result['title'], result['snippet'], result['url'])
                    outlines.append(outline)

                # Display Outlines
                st.header("Search Results & Outlines")
                for i, (result, outline) in enumerate(zip(search_results, outlines)):
                    st.subheader(f"{i + 1}. {result['title']}")
                    st.write(f"URL: {result['url']}")
                    st.write(f"Snippet: {result['snippet']}")
                    st.write("Outline:")
                    st.write(outline)
            else:
                st.warning("No search results found for the given query.")

# Main App
st.set_page_config(page_title="GPT-4 Powered Content Generation", layout="wide")
st.sidebar.title("Choose a Mode")
mode = st.sidebar.radio("", ["Article Generation", "SERP Outline"])
if mode == "Article Generation":
    article_app()
else:
    serp_app()
