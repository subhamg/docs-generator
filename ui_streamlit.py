import os
import streamlit as st
from app import get_repo_context, build_prompt, generate_markdown_with_gemini


st.set_page_config(page_title="Repo → Docs (gitingest + Gemini)", layout="wide")

st.title("Repo → Docs")
st.caption("Generate developer docs from a GitHub URL using gitingest and Gemini.")

with st.sidebar:
    st.header("Configuration")
    github_token = st.text_input("GitHub Token (optional)", type="password")
    gemini_api_key = st.text_input("Gemini API Key", type="password")
    model_name = st.text_input("Gemini Model", value="gemini-2.5-flash")
    style = st.text_input("Style/Tone", value="crisp, practical, senior-engineer tone")
    generate_button = st.button("Generate Docs", type="primary")

source = st.text_input("GitHub Repository URL", placeholder="https://github.com/owner/repo")

status = st.empty()
output_tab, raw_tab = st.tabs(["Markdown Output", "Raw Ingest (debug)"])

if generate_button:
    if not gemini_api_key:
        st.error("Please provide a Gemini API key.")
        st.stop()

    if not source:
        st.error("Please provide a GitHub repository URL.")
        st.stop()

    if github_token:
        os.environ["GITHUB_TOKEN"] = github_token
    os.environ["GEMINI_API_KEY"] = gemini_api_key

    try:
        status.info("Ingesting repository with gitingest…")
        summary, tree, content = get_repo_context(source)
    except Exception as e:
        st.exception(e)
        st.stop()

    with raw_tab:
        st.subheader("Ingest Summary")
        st.code(summary)
        st.subheader("Ingest Tree")
        st.code(tree)
        # Avoid dumping full content by default; provide a toggle
        if st.checkbox("Show full content digest (can be very large)"):
            st.subheader("Content Digest")
            st.code(content)

    try:
        status.info("Calling Gemini to generate Markdown…")
        prompt = build_prompt(summary, tree, content, style)
        markdown = generate_markdown_with_gemini(prompt, model_name)
    except Exception as e:
        st.exception(e)
        st.stop()
    finally:
        status.empty()

    with output_tab:
        st.download_button(
            label="Download docs.md",
            data=markdown,
            file_name="docs.md",
            mime="text/markdown",
        )
        st.markdown(markdown)


