"""BM-K/KoMiniLM 를 ONNX 로 내보내고 동적 INT8 로 양자화하여 저장한다(GitHub 커밋용).

실행: python scripts/export_kominilm_onnx_int8.py
필요: pip install torch "optimum[onnxruntime]"
결과: backend/models/kominilm-onnx-int8/ (model_quantized.onnx + 토크나이저/설정)
"""
from pathlib import Path

from optimum.onnxruntime import ORTModelForFeatureExtraction, ORTQuantizer
from optimum.onnxruntime.configuration import AutoQuantizationConfig
from transformers import AutoTokenizer

MODEL_ID = "BM-K/KoMiniLM"
OUT_DIR = Path(__file__).resolve().parents[1] / "models" / "kominilm-onnx-int8"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) PyTorch -> ONNX(fp32) 내보내기 + 토크나이저 저장
    model = ORTModelForFeatureExtraction.from_pretrained(MODEL_ID, export=True)
    model.save_pretrained(OUT_DIR)
    AutoTokenizer.from_pretrained(MODEL_ID).save_pretrained(OUT_DIR)

    # 2) 동적 INT8 양자화 (weight-only, CPU)
    quantizer = ORTQuantizer.from_pretrained(OUT_DIR)
    qconfig = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False)
    quantizer.quantize(save_dir=OUT_DIR, quantization_config=qconfig)

    # 3) 커밋 용량 절감: fp32 원본 onnx 제거(양자화본만 유지)
    fp32 = OUT_DIR / "model.onnx"
    if fp32.exists():
        fp32.unlink()

    print("saved:", OUT_DIR)
    for path in sorted(OUT_DIR.iterdir()):
        print(f"  {path.name:30} {path.stat().st_size / 1e6:8.2f} MB")


if __name__ == "__main__":
    main()
