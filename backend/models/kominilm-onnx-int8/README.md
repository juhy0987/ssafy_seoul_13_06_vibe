# KoMiniLM — ONNX INT8

`BM-K/KoMiniLM` 을 ONNX 로 내보내고 **동적 INT8** 로 양자화한 문장 임베딩 모델.
GitHub 커밋을 위해 런타임에 torch/HF 다운로드 없이 `onnxruntime` 만으로 로드 가능하도록 경량화했다.

## 사양
- 원본: `BM-K/KoMiniLM`
- 형식: ONNX `model_quantized.onnx`, 동적 INT8(weight-only, `avx512_vnni` recipe)
- 출력: `last_hidden_state`, hidden dim **384**
- 문장 임베딩: 토큰 임베딩 **mean pooling → L2 정규화**
- 크기: 약 23 MB
- 충실도: pooled cosine ≈ 0.99 (원본 fp32 대비)

## 재생성
```bash
pip install torch "optimum[onnxruntime]"
python scripts/export_kominilm_onnx_int8.py
```

## 사용 예 (런타임엔 torch 불필요)
```python
import numpy as np
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

D = "backend/models/kominilm-onnx-int8"
tok = AutoTokenizer.from_pretrained(D)
model = ORTModelForFeatureExtraction.from_pretrained(D, file_name="model_quantized.onnx")

def embed(texts: list[str]) -> np.ndarray:
    enc = tok(texts, padding=True, truncation=True, return_tensors="np")
    out = model(**enc).last_hidden_state            # [B, T, 384]
    mask = enc["attention_mask"][..., None]
    pooled = (out * mask).sum(1) / mask.sum(1)      # mean pooling
    return pooled / np.linalg.norm(pooled, axis=1, keepdims=True)
```

> 참고: `BM-K/KoMiniLM` 은 베이스 LM이라 raw 임베딩의 의미 분별력이 문장유사도 전용 모델보다 약할 수 있다. 양자화 자체는 원본을 충실히 보존한다(위 충실도 참고).
