"""Exercise the local GPT-SoVITS API without opening a port."""

import argparse
import asyncio
import importlib
import io
import sys
import tempfile
import wave
from pathlib import Path

import httpx


CONFIG = """\
custom:
  version: v2ProPlus
  device: cpu
  is_half: false
  t2s_weights_path: GPT_weights_v2ProPlus/Gove.ckpt
  vits_weights_path: SoVITS_weights_v2ProPlus/Gove.pth
  bert_base_path: GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large
  cnhuhbert_base_path: GPT_SoVITS/pretrained_models/chinese-hubert-base
"""

SUPPORTED_LANGS = (
    "zh",
    "en",
    "ja",
    "yue",
    "ko",
    "all_zh",
    "all_ja",
    "all_yue",
    "all_ko",
    "auto",
    "auto_yue",
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Exercise the local GPT-SoVITS API without opening a port."
    )
    parser.add_argument("reference_wav", help="Path to reference_en.wav")
    parser.add_argument("output_dir", help="Directory to save the generated WAV")
    parser.add_argument(
        "--text",
        default="你好呀，终于又见面了。",
        help="Text to synthesize (default: Mandarin greeting)",
    )
    parser.add_argument(
        "--lang",
        default="zh",
        choices=SUPPORTED_LANGS,
        help="GPT-SoVITS text_lang code (default: zh)",
    )
    return parser.parse_args()


async def synthesize(app, reference_audio, reference_text, text, lang):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        response = await client.post(
            "/tts",
            json={
                "text": text,
                "text_lang": lang,
                "ref_audio_path": str(reference_audio),
                "prompt_lang": "en",
                "prompt_text": reference_text,
                "text_split_method": "cut0",
                "media_type": "wav",
                "streaming_mode": False,
            },
        )
    if response.status_code != 200:
        raise SystemExit(f"Gove /tts returned {response.status_code}: {response.text}")
    return response.content


def main():
    args = parse_args()

    reference_audio = Path(args.reference_wav).resolve(strict=True)
    output_dir = Path(args.output_dir).resolve()
    checkout = Path.cwd()
    required_files = (
        "api_v2.py",
        "GPT_weights_v2ProPlus/Gove.ckpt",
        "SoVITS_weights_v2ProPlus/Gove.pth",
    )
    for relative_path in required_files:
        if not (checkout / relative_path).is_file():
            raise SystemExit(f"Run from the Gove GPT-SoVITS checkout. Missing {relative_path}")
    reference_text = (
        Path(__file__).resolve().parents[1] / "assets/reference_en.txt"
    ).read_text(encoding="utf-8").strip()

    with tempfile.TemporaryDirectory(prefix="gove-smoke-") as temporary_dir:
        config_path = Path(temporary_dir) / "gove.yaml"
        config_path.write_text(CONFIG, encoding="utf-8")
        sys.path.insert(0, str(checkout))
        sys.argv = ["api_v2.py", "-c", str(config_path)]
        app = importlib.import_module("api_v2").APP
        audio = asyncio.run(
            synthesize(app, reference_audio, reference_text, args.text, args.lang)
        )

    with wave.open(io.BytesIO(audio)) as wav:
        frames = wav.getnframes()
        sample_rate = wav.getframerate()
        if frames <= 0 or not any(wav.readframes(frames)):
            raise SystemExit("Gove returned a silent or empty WAV.")

    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=output_dir, prefix="gove-test-", suffix=".wav", delete=False
    ) as output:
        output.write(audio)
    print(f"Verified: {frames / sample_rate:.2f}s, {sample_rate} Hz")
    print(Path(output.name).resolve())


if __name__ == "__main__":
    main()
