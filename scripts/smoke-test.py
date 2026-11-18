"""Exercise the local GPT-SoVITS API without opening a port."""

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


async def synthesize(app, reference_audio, reference_text):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        response = await client.post(
            "/tts",
            json={
                "text": "你好呀，终于又见面了。",
                "text_lang": "zh",
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
    if len(sys.argv) != 3:
        raise SystemExit("Usage: smoke-test.py REFERENCE_WAV OUTPUT_DIRECTORY")

    reference_audio = Path(sys.argv[1]).resolve(strict=True)
    output_dir = Path(sys.argv[2]).resolve()
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
        audio = asyncio.run(synthesize(app, reference_audio, reference_text))

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
