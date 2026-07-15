"""원본 서울 데이터(가독성 위주)를 RAG용 compact JSONL로 재구성한다.

- 출력은 공간 효율만 고려: 1글자 키, 개행 구분(JSONL), ensure_ascii=False, 공백 없음.
- 카테고리는 파일명으로 표현하므로 레코드에 넣지 않는다.
실행: python -m app.domains.chat.rag.refine
"""
import json
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[4] / "data" / "서울"
DST_DIR = Path(__file__).resolve().parents[4] / "data" / "seoul_rag"


def _num(value) -> float | None:
    try:
        return round(float(value), 6) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def refine() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for src in sorted(SRC_DIR.glob("서울_*.json")):
        category = src.stem.split("_", 1)[1]
        data = json.loads(src.read_text(encoding="utf-8"))
        with (DST_DIR / f"{category}.jsonl").open("w", encoding="utf-8") as out:
            for item in data["items"]:
                rec = {"i": str(item["contentid"]), "t": item.get("title") or ""}
                if item.get("addr1"):
                    rec["a"] = item["addr1"]
                x, y = _num(item.get("mapx")), _num(item.get("mapy"))
                if x is not None:
                    rec["x"] = x
                if y is not None:
                    rec["y"] = y
                out.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
                written += 1
    return written


if __name__ == "__main__":
    total = refine()
    print(f"refined {total} records -> {DST_DIR}")
