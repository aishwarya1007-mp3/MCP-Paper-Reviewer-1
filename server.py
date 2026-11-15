"""MCP tools for loading and assessing academic papers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-paper-reviewer")
PROJECT_DIR = Path(__file__).resolve().parent
CHECKLIST_PATH = PROJECT_DIR / "checklist.txt"
MAX_PAPER_CHARACTERS = 1_000_000

_cached_paper: str | None = None
_cached_path: str | None = None


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    if path.suffix.lower() != ".txt":
        raise ValueError("Only plain-text .txt papers are supported by this version.")
    content = path.read_text(encoding="utf-8-sig").strip()
    if not content:
        raise ValueError("The paper file is empty.")
    if len(content) > MAX_PAPER_CHARACTERS:
        raise ValueError(
            f"Paper is too large ({len(content):,} characters). Limit: "
            f"{MAX_PAPER_CHARACTERS:,} characters."
        )
    return content


def require_loaded_paper() -> tuple[str, str]:
    if _cached_paper is None or _cached_path is None:
        raise RuntimeError("No paper is loaded. Call load_paper first.")
    return _cached_paper, _cached_path


def read_checklist() -> str:
    if not CHECKLIST_PATH.is_file():
        raise FileNotFoundError(f"Review checklist not found: {CHECKLIST_PATH}")
    return CHECKLIST_PATH.read_text(encoding="utf-8").strip()


@mcp.tool()
def load_paper(paper_path: str) -> dict[str, Any]:
    """Load a paper from a plain-text .txt file path for subsequent review tools."""
    global _cached_paper, _cached_path

    supplied_path = Path(paper_path).expanduser()
    path = supplied_path if supplied_path.is_absolute() else (Path.cwd() / supplied_path)
    path = path.resolve()
    _cached_paper = read_text_file(path)
    _cached_path = str(path)
    return {
        "paper_loaded": True,
        "file": _cached_path,
        "character_count": len(_cached_paper),
        "message": "Paper loaded. You can now run the review tools.",
    }


@mcp.tool()
def get_review_checklist() -> dict[str, str]:
    """Return the project's academic paper review rubric."""
    return {"checklist": read_checklist()}


@mcp.tool()
def find_missing_citations() -> dict[str, Any]:
    """Return the loaded paper and checks for unsupported claims and citation gaps."""
    paper, source_path = require_loaded_paper()
    return {
        "task": "citation_and_related_work_review",
        "source_file": source_path,
        "paper": paper,
        "checks": [
            "unsupported claims that need citations",
            "missing or insufficient related work",
            "potentially outdated references",
            "claims that need comparison with prior work",
        ],
        "limitation": "This tool supplies the paper text for analysis; it does not independently verify references against external databases.",
    }


@mcp.tool()
def detect_logical_gaps() -> dict[str, Any]:
    """Return the loaded paper and checks for reasoning, assumptions, and methodology."""
    paper, source_path = require_loaded_paper()
    return {
        "task": "technical_and_logical_review",
        "source_file": source_path,
        "paper": paper,
        "checks": [
            "unstated or unjustified assumptions",
            "missing proof steps or unsupported deductions",
            "unclear methodology",
            "invalid or incomplete inferences",
            "mismatches between claims and evidence",
        ],
    }


@mcp.tool()
def analyze_novelty(conference: str = "ICLR") -> dict[str, Any]:
    """Return the loaded paper and novelty rubric for a target conference; the AI client performs the assessment."""
    paper, source_path = require_loaded_paper()
    if not conference.strip():
        raise ValueError("Conference name cannot be empty.")
    return {
        "task": "novelty_review",
        "target_venue": conference.strip(),
        "source_file": source_path,
        "paper": paper,
        "novelty_checks": [
            "genuinely new idea, method, or theoretical insight",
            "difference from closely related work",
            "incremental versus substantial contribution",
            "risk of repackaging known techniques",
        ],
        "review_checklist": read_checklist(),
        "requested_output": "A 0-10 novelty score with evidence-based justification and uncertainty noted.",
    }


@mcp.tool()
def get_article_statistics(articles: list[dict[str, Any]]) -> dict[str, Any]:
    """Count articles by category. Each item should contain title and category fields."""
    category_counts: dict[str, int] = {}
    missing_titles = 0
    for index, article in enumerate(articles):
        if not isinstance(article, dict):
            raise ValueError(f"Article at index {index} must be an object.")
        if not str(article.get("title", "")).strip():
            missing_titles += 1
        category = str(article.get("category") or "Unknown").strip() or "Unknown"
        category_counts[category] = category_counts.get(category, 0) + 1
    return {
        "total_articles": len(articles),
        "category_counts": category_counts,
        "articles_missing_titles": missing_titles,
    }


if __name__ == "__main__":
    mcp.run()
