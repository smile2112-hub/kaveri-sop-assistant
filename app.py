from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

#maheshkajale2112@gmail.com
#Mahesh Ganesh Kajale
ROOT = Path(__file__).parent
DOCUMENTS = ROOT / "documents"
STATIC = ROOT / "static"
STOP_WORDS = frozenset(
    "a an and are as at be by can centre could does for from how i in is it of on or "
    "should the their them this to what when where who with would".split()
)


@dataclass(frozen=True)
class Chunk:
    source: str
    text: str
    terms: frozenset[str]


def terms(text: str) -> frozenset[str]:
    return frozenset(
        word for word in re.findall(r"[a-z0-9][a-z0-9-]+", text.lower()) if word not in STOP_WORDS
    )

#maheshkajale2112@gmail.com
#Mahesh Ganesh Kajale
def read_document(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader

            return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        except Exception as exc:
            raise RuntimeError(f"Could not read PDF {path.name}: {exc}") from exc
    return path.read_text(encoding="utf-8")


def load_chunks() -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(DOCUMENTS.iterdir()):
        if path.suffix.lower() not in {".pdf", ".txt"}:
            continue
        text = read_document(path)
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
        for paragraph in paragraphs:
            if "Document No." in paragraph and len(paragraph) < 220:
                continue
            if paragraph.startswith("Common alarms:"):
                sentences = [
                    ("Common alarms: " + sentence if index == 0 else sentence)
                    for index, sentence in enumerate(re.split(r"(?=AL-\d+)", paragraph))
                    if sentence.strip() and not (index == 0 and sentence.strip() == "Common alarms:")
                ]
            else:
                sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", paragraph)
            sentences = [
                sentence.strip()
                for sentence in sentences
                if sentence.strip()
            ]
            for sentence in sentences:
                chunks.append(Chunk(path.name, sentence, terms(sentence)))
    return chunks


def rank(query: str, chunks: Iterable[Chunk]) -> list[tuple[float, Chunk]]:
    query_terms = terms(query)
    if not query_terms:
        return []
    scored: list[tuple[float, Chunk]] = []
    for chunk in chunks:
        overlap = len(query_terms & chunk.terms)
        score = overlap / len(query_terms)
        if query.lower() in chunk.text.lower():
            score += 0.35
        scored.append((score, chunk))
    return sorted(scored, key=lambda item: item[0], reverse=True)


def answer_question(question: str, chunks: list[Chunk] | None = None) -> dict:
    ranked = rank(question, chunks if chunks is not None else load_chunks())
    if not ranked or ranked[0][0] < 0.18:
        return {
            "answer": "I couldn't find that in the plant documents. Please check the QMS or ask the relevant supervisor rather than relying on an unsupported assumption.",
            "source": None,
            "confidence": "not found",
        }

    top_score, top = ranked[0]
    supporting = [top.text]
    for score, chunk in ranked[1:3]:
        if score >= 0.25 and chunk.source == top.source and chunk.text not in supporting:
            supporting.append(chunk.text)
    return {
        "answer": "According to the document:\n\n" + "\n\n".join(supporting),
        "source": top.source,
        "confidence": "document match",
    }

#maheshkajale2112@gmail.com
#Mahesh Ganesh Kajale
app = FastAPI(title="Kaveri Plant Copilot", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return (STATIC / "index.html").read_text(encoding="utf-8")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/ask")
def ask(question: str = Query(min_length=2, max_length=500)) -> dict:
    return answer_question(question)
