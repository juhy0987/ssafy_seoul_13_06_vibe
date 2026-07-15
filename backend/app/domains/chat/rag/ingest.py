"""정제 데이터(seoul_rag/*.jsonl)를 임베딩하여 sqlite 스토어에 적재한다.

실행: python -m app.domains.chat.rag.ingest
"""
import json
from pathlib import Path

from langchain_core.documents import Document

from app.domains.chat.rag.embeddings import get_embeddings
from app.domains.chat.rag.store import SQLiteVectorStore

REFINED_DIR = Path(__file__).resolve().parents[4] / "data" / "seoul_rag"


def load_documents() -> list[Document]:
    documents = []
    for path in sorted(REFINED_DIR.glob("*.jsonl")):
        category = path.stem
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                title, address = rec.get("t", ""), rec.get("a", "")
                documents.append(
                    Document(
                        page_content=f"{title} {address}".strip(),
                        metadata={
                            "category": category, "id": rec["i"], "title": title,
                            "address": address or None, "lat": rec.get("y"), "lng": rec.get("x"),
                        },
                    )
                )
    return documents


def main() -> None:
    documents = load_documents()
    store = SQLiteVectorStore(get_embeddings())
    store.init()
    store.add(documents)
    print(f"ingested {len(documents)} documents -> {store.db_path}")


if __name__ == "__main__":
    main()
