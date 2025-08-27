# AI Agent: Repo-to-Docs (gitingest + Gemini)

Generate developer-grade Markdown documentation from any GitHub repository URL using `gitingest` for context and Google Gemini for writing.

## Quickstart

Prereqs: Python 3.10+ recommended

```bash
cd /Users/subhamgoyal/Code/ai-agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set API keys
export GEMINI_API_KEY=your_key_here    # or GOOGLE_API_KEY
# Optional for private GitHub repos
export GITHUB_TOKEN=github_pat_...

# Run
python app.py https://github.com/coderamp-labs/gitingest -o docs.md --style "crisp, practical, senior-engineer tone"
```

The generated Markdown is written to `docs.md` by default.

## CLI

```bash
python app.py SOURCE [--model gemini-1.5-pro] [-o docs.md] [--style "..."] [--print]
```

- `SOURCE`: GitHub URL (public or private) or local path.
- `--model`: Gemini model name. Default `gemini-1.5-pro`.
- `-o/--output`: Output Markdown file path. Default `docs.md`.
- `--style`: Optional tone/style guidance for the docs.
- `--print`: Also print the generated docs to STDOUT.

## Notes

- Uses `gitingest` to produce a summary, tree, and content digest. See PyPI: [`gitingest`](https://pypi.org/project/gitingest/).
- Uses `google-generativeai` to call Gemini. Provide `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
- If you hit token limits on very large repos, try running on a subdirectory or trimming the prompt style.

## License

MIT

## Streamlit UI

Run a simple web UI on localhost:

```bash
source .venv/bin/activate
streamlit run ui_streamlit.py
```

Enter your GitHub URL and Gemini API key in the sidebar. Optionally, include a GitHub token for private repos.
