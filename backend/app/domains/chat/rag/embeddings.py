from functools import lru_cache
from pathlib import Path

import numpy as np
import onnxruntime as ort
from langchain_core.embeddings import Embeddings
from tokenizers import Tokenizer

# 커밋된 INT8 ONNX 모델 — 런타임에 torch/transformers/HF 다운로드 불필요
MODEL_DIR = Path(__file__).resolve().parents[4] / "models" / "kominilm-onnx-int8"

_ORT_DTYPE = {"tensor(int64)": np.int64, "tensor(int32)": np.int32, "tensor(float)": np.float32}


class KoMiniLMOnnxEmbeddings(Embeddings):
    """BM-K/KoMiniLM(ONNX INT8) 문장 임베딩. mean pooling + L2 정규화 → 코사인=내적."""

    def __init__(self, model_dir: Path = MODEL_DIR):
        self.tokenizer = Tokenizer.from_file(str(model_dir / "tokenizer.json"))
        self.tokenizer.enable_truncation(max_length=512)
        self.tokenizer.enable_padding(pad_id=0, pad_token="[PAD]")
        self.session = ort.InferenceSession(
            str(model_dir / "model_quantized.onnx"), providers=["CPUExecutionProvider"]
        )
        self._inputs = self.session.get_inputs()

    def _embed(self, texts: list[str]) -> np.ndarray:
        encodings = self.tokenizer.encode_batch(texts)
        arrays = {
            "input_ids": np.array([e.ids for e in encodings], dtype=np.int64),
            "attention_mask": np.array([e.attention_mask for e in encodings], dtype=np.int64),
            "token_type_ids": np.array([e.type_ids for e in encodings], dtype=np.int64),
        }
        feeds = {
            spec.name: arrays[spec.name].astype(_ORT_DTYPE.get(spec.type, np.int64))
            for spec in self._inputs
            if spec.name in arrays
        }
        last_hidden = self.session.run(None, feeds)[0]  # [B, T, 384]
        mask = arrays["attention_mask"][..., None].astype(np.float32)
        pooled = (last_hidden * mask).sum(1) / np.clip(mask.sum(1), 1e-9, None)
        pooled /= np.clip(np.linalg.norm(pooled, axis=1, keepdims=True), 1e-9, None)
        return pooled.astype(np.float32)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(list(texts)).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text])[0].tolist()


@lru_cache(maxsize=1)
def get_embeddings() -> KoMiniLMOnnxEmbeddings:
    """최초 호출 시 ONNX 세션·토크나이저를 로드한다."""
    return KoMiniLMOnnxEmbeddings()
