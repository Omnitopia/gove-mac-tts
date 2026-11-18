---
name: gove-mac-tts
description: Install or verify the Gove v2ProPlus voice on an Apple Silicon Mac and generate a local test WAV. Use for Gove Mac setup, checking an existing installation, or recovering a failed first synthesis.
---

# Gove on Apple Silicon

Run the workflow on the user's Apple Silicon Mac with local terminal access. For a review or explanation request, describe the steps without running them. Intel Mac, Windows, Linux, and chat app integrations are outside this version's scope.

1. Check the requested install location and look for a usable Gove setup in the project or at `~/Gove-TTS`. The script's layout is an install root containing `GPT-SoVITS/` and `env/`. If the user already has Gove in a different layout, use their existing Python environment and project directory for the smoke test commands below.
2. For a fresh install, use the directory the user names, or default to `~/Gove-TTS`. Check the destination volume for about 20 GB of free space. Before downloading, tell the user the chosen path and budget about 7 GB of downloads. If space is too low, the path contains spaces, or existing files conflict with this layout, ask for another path before downloading. If `xcode-select -p` fails, the Mac first needs Apple's Command Line Tools. Run `xcode-select --install` only as part of a requested install and let the user finish the macOS dialog if it appears. Use the agent's normal permission flow for filesystem and download access.
3. From this skill folder, run the appropriate command. The optional directory argument defaults to `~/Gove-TTS`, and `--text` / `--lang` (`zh`, `en`, `ja`, `yue`, etc.) override the default Mandarin test line.

   ```bash
   bash scripts/gove-mac.sh install
   bash scripts/gove-mac.sh verify "/absolute/path/to/install-root" --text "Hey, it's so good to see you again." --lang en
   ```

   `install` creates the environment, downloads and moves the pinned GPT-SoVITS and Gove assets into place (removing staging copies and the Miniforge installer), then runs the smoke test. Use `verify` for a complete existing setup. The first run can take a while during the base-model download. If a command fails, inspect the failing step before retrying. If an existing checkout uses a different revision, use a separate install root or validate the existing environment independently.
4. Report success after the smoke test prints the path of a nonempty WAV. Link that file so the user can play it. The test runs the same `/tts` route in process on CPU and exits. If a download or synthesis fails, report the exact failing step and what is still missing.

## Existing Conda layout

If the user used a named Conda environment with the tested checkout, activate that environment, change into the GPT-SoVITS checkout, then run the bundled smoke test. Pass the absolute paths of the installed `reference_en.wav` and the output directory (plus optional `--text` and `--lang`).

```bash
python "/absolute/path/to/gove-mac-tts/scripts/smoke-test.py" \
  "/absolute/path/to/reference_en.wav" "/absolute/path/to/output" \
  --text "你好呀，终于又见面了。" --lang zh
```

For WebUI dependency troubleshooting on the tested checkout, the known working combination is Gradio 4.44.1, FastAPI 0.115.2, Starlette 0.40.0, and resampy 0.4.3. The installer applies the fixes inside its own Conda environment.

The scripts use the pinned [GPT-SoVITS checkout](https://github.com/RVC-Boss/GPT-SoVITS/tree/6d51ffceafbf240145619af4c92408a6e54b7924) and download the voice weights and reference WAV from the [Gove model repository](https://huggingface.co/OmniDimen/Gove).
