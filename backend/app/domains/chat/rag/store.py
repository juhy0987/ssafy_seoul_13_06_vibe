"""sqlite3 기반 임베딩 스토어 + LangChain 리트리버.

임베딩은 정규화된 float32 벡터를 BLOB으로 저장하고, 조회 시 전량을 메모리에
올려 내적(코사인) 상위 k개를 반환한다. 네이티브 확장(sqlite-vec 등) 불필요.
"""
import sqlite3
from pathlib import Path

import numpy as np
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from pydantic import ConfigDict

DB_PATH = Path(__file__).resolve().parents[4] / "data" / "embeddings.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS spots (
    category  TEXT NOT NULL,
    spot_id   TEXT NOT NULL,
    title     TEXT NOT NULL,
    address   TEXT,
    lat       REAL,
    lng       REAL,
    document  TEXT NOT NULL,
    embedding BLOB NOT NULL,
    PRIMARY KEY (category, spot_id)
);
"""


def _to_blob(vector) -> bytes:
    return np.asarray(vector, dtype=np.float32).tobytes()


def _from_blob(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32)


class SQLiteVectorStore:
    def __init__(self, embeddings: Embeddings, db_path: Path = DB_PATH):
        self.embeddings = embeddings
        self.db_path = Path(db_path)
        self._rows: list[tuple] | None = None
        self._matrix: np.ndarray | None = None

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute(_SCHEMA)
        return conn

    def init(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.commit()

    def reset(self) -> None:
        """스토어를 비우고 스키마를 재생성한다(재적재 시 이전 모델 임베딩 잔존 방지)."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("DROP TABLE IF EXISTS spots")
            conn.execute(_SCHEMA)
            conn.commit()
        self._rows = self._matrix = None

    def count(self) -> int:
        with self._connect() as conn:
            return conn.execute("SELECT COUNT(*) FROM spots").fetchone()[0]

    def add(self, documents: list[Document], verbose: bool = False, skip_existing: bool = True) -> None:
        with self._connect() as conn:
            if skip_existing:
                # 이미 적재된 (category, spot_id)는 재임베딩하지 않는다(재개 가능·quota 절약)
                existing = set(conn.execute("SELECT category, spot_id FROM spots").fetchall())
                pending = [
                    doc for doc in documents
                    if (doc.metadata["category"], doc.metadata["id"]) not in existing
                ]
            else:
                pending = list(documents)

            if verbose:
                print(f"  skip {len(documents) - len(pending)} (already embedded), embed {len(pending)}", flush=True)

            for index, doc in enumerate(pending, start=1):
                vector = self.embeddings.embed_documents([doc.page_content])[0]
                conn.execute(
                    "INSERT OR REPLACE INTO spots"
                    "(category,spot_id,title,address,lat,lng,document,embedding)"
                    " VALUES (?,?,?,?,?,?,?,?)",
                    (
                        doc.metadata["category"], doc.metadata["id"], doc.metadata["title"],
                        doc.metadata.get("address"), doc.metadata.get("lat"), doc.metadata.get("lng"),
                        doc.page_content, _to_blob(vector),
                    ),
                )
                conn.commit()  # 임베딩 즉시 삽입·커밋 → 어느 지점에서 끊겨도 완료분 보존(문서 단위 재개)
                if verbose and (index % 50 == 0 or index == len(pending)):
                    print(f"  embedded {index}/{len(pending)}", flush=True)
        self._rows = self._matrix = None  # 캐시 무효화

    def _load(self) -> None:
        if self._matrix is not None:
            return
        with self._connect() as conn:
            self._rows = conn.execute(
                "SELECT category,spot_id,title,address,lat,lng,document,embedding FROM spots"
            ).fetchall()
        if not self._rows:
            self._matrix = np.zeros((0, 0), dtype=np.float32)
            return
        dims = {len(row[7]) for row in self._rows}
        if len(dims) > 1:
            raise RuntimeError(
                f"embeddings.db 에 서로 다른 임베딩 차원이 섞여 있습니다(발견: {sorted(d // 4 for d in dims)}). "
                "임베딩 모델 변경 후에는 data/embeddings.db 를 삭제하고 재적재(ingest)하세요."
            )
        self._matrix = np.vstack([_from_blob(row[7]) for row in self._rows])

    def search(self, query: str, k: int = 4, category: str | None = None) -> list[Document]:
        self._load()
        if not self._rows:
            return []
        indices = [i for i in range(len(self._rows)) if not category or self._rows[i][0] == category]
        if not indices:
            return []
        query_vec = np.asarray(self.embeddings.embed_query(query), dtype=np.float32)
        scores = self._matrix[indices] @ query_vec
        top = np.argsort(-scores)[:k]
        results = []
        for pos in top:
            row = self._rows[indices[pos]]
            results.append(
                Document(
                    page_content=row[6],
                    metadata={
                        "category": row[0], "id": row[1], "title": row[2], "address": row[3],
                        "lat": row[4], "lng": row[5], "score": float(scores[pos]),
                    },
                )
            )
        return results


class SQLiteRetriever(BaseRetriever):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    store: SQLiteVectorStore
    k: int = 4
    category: str | None = None

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> list[Document]:
        return self.store.search(query, self.k, self.category)
