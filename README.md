# MCP Paper Reviewer

An AI-assisted academic paper review tool built with the **Model Context Protocol (MCP)** and the **OpenAI API**. It loads a plain-text research paper, exposes review functions as MCP tools, and asks an OpenAI model to synthesize an evidence-based review.

## Features

- Load a research paper from a UTF-8 `.txt` file.
- Review novelty against a selected target venue (for example, ICLR, NeurIPS, or CCS).
- Examine logical gaps, assumptions, methodology, and claims.
- Identify claims that may need citations and gaps in related work.
- Use a customizable academic review checklist.
- Run the MCP server automatically as a child process of the client.

**Scope note:** The project analyzes the text supplied by the user. It does not independently search scholarly databases, verify whether references exist, or guarantee a conference acceptance prediction. Its review is an AI-generated aid, not a substitute for expert peer review.

## Project structure

```text
MCP-Paper-Reviewer/
├── .env.example       # Template for local secrets/configuration
├── .gitignore         # Excludes .env, virtual environments, and caches
├── README.md
├── checklist.txt      # Review rubric
├── client.py          # OpenAI client and MCP tool-calling loop
├── main.py            # Convenience entry point
├── pyproject.toml
├── requirements.txt
├── server.py           # MCP server and review tools
└── papers/             # Put your own .txt papers here
```

## Requirements

- Python 3.10 or newer
- An OpenAI API key with API access and available billing/credits
- Internet connection for OpenAI API requests

## Setup (macOS / Linux)

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and replace `your_api_key_here` with your own key:

```env
OPENAI_API_KEY=your_actual_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Do not put the key in `client.py`, `server.py`, `README.md`, or `.gitignore`. The `.gitignore` file excludes `.env` from Git commits. **Never commit or share your real API key.**

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Then edit `.env` and add your API key.

## Run

Activate the virtual environment, then run either command from the project directory:

```bash
python main.py
```

or

```bash
python client.py
```

The client starts `server.py` automatically over MCP stdio. You do **not** need to open a separate terminal for the server.

## Example request

At the `You:` prompt, enter:

```text
Review ./papers/my_research_paper.txt for ICLR. Give me strengths, weaknesses, a novelty score, and an overall recommendation.
```

The paper must be a UTF-8 plain-text `.txt` file. You can also provide an absolute path. Type `quit` to exit.

## MCP tools

| Tool | Purpose |
|---|---|
| `load_paper` | Loads the `.txt` paper and stores it for the current server session. |
| `get_review_checklist` | Returns the project's full review rubric. |
| `find_missing_citations` | Supplies paper text and checks for citation/related-work gaps. |
| `detect_logical_gaps` | Supplies paper text and checks for technical and reasoning gaps. |
| `analyze_novelty` | Supplies the paper and novelty criteria for the requested venue. |
| `get_article_statistics` | Counts articles by category for a list of article records. |

## Customizing the checklist

Edit `checklist.txt` to change the evaluation criteria. The `get_review_checklist` tool returns the full rubric, and `analyze_novelty` includes it in the context sent to the model.

## Troubleshooting

- **`OPENAI_API_KEY is missing`:** Ensure `.env` exists in the project directory and contains `OPENAI_API_KEY=...`.
- **Authentication or quota error:** Check that the key is valid and that the OpenAI account has API access and available quota. ChatGPT subscriptions and API billing are separate.
- **Paper not found:** Check the path and run the command from the project directory, or use an absolute path.
- **Unsupported file:** This version accepts `.txt` files only. Convert PDF/DOCX papers to text before loading.
- **Dependency/import error:** Activate `.venv` and run `pip install -r requirements.txt` again.

## Team

1. Aishwarya Gadhave
2. Vishwajeet Godse
3. Vaishnavi Repal

## License

No license has been specified. Add a license before distributing the project if you want to grant reuse rights.
