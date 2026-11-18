#!/bin/bash
set -euo pipefail

fail() {
  printf 'Gove: %s\n' "$*" >&2
  exit 1
}

mode=${1:-}
case "$mode" in
  install|verify) ;;
  -h|--help|"")
    printf 'Usage: bash gove-mac.sh {install|verify} [install-directory]\n'
    exit 0
    ;;
  *) fail "Unknown command: $mode" ;;
esac
[ "$#" -le 2 ] || fail 'Pass at most one install directory.'
[ "$(uname -s):$(uname -m)" = 'Darwin:arm64' ] ||
  fail 'Use an Apple Silicon Mac in a native arm64 terminal.'

skill_dir="$(cd "$(dirname "$0")/.." && pwd -P)"
root=${2:-"$HOME/Gove-TTS"}
[[ "$root" = /* ]] || fail 'Pass an absolute install directory.'
repo="$root/GPT-SoVITS"
runtime="$root/env"
conda="$root/miniforge3/bin/conda"
ref_dir="$repo/reference_audios/Gove"
revision=6d51ffceafbf240145619af4c92408a6e54b7924
model_revision=53009973e0c42a30ab37067cda57958f4cbbce66
gpt_sha=a28ef0b681cfcc4ebe07b079bae2aba9e38d85cb4ebcae55ebfda75d3fae9a6d
sovits_sha=0b86698af65dadc21b9a0aa13d2d7b3a9797c50d170e96c8c1e3c3f015845ac7
ref_sha=4dce5ef9fb0e42be3b7239aacfa63143ca3a6e0a067eaba5ba7fed9fa243df3d

verify_sha() {
  printf '%s  %s\n' "$1" "$2" | shasum -a 256 -c - ||
    fail "Missing file or checksum mismatch: $2"
}

has_model_files() {
  [ -s "$repo/GPT_weights_v2ProPlus/Gove.ckpt" ] &&
    [ -s "$repo/SoVITS_weights_v2ProPlus/Gove.pth" ] &&
    [ -s "$ref_dir/reference_en.wav" ]
}

if [ "$mode" = install ] && { [ ! -x "$runtime/bin/python" ] || ! has_model_files; }; then
  xcode-select -p >/dev/null 2>&1 ||
    fail 'Install the macOS Command Line Tools with xcode-select --install and then retry.'
  [[ "$root" != *[[:space:]]* ]] || fail 'Choose an install directory without spaces.'
  mkdir -p "$root"

  if [ ! -d "$repo" ]; then
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git "$repo"
    git -C "$repo" checkout --detach "$revision"
  fi
  [ "$(git -C "$repo" rev-parse HEAD)" = "$revision" ] ||
    fail "Expected GPT-SoVITS $revision. Use a separate install directory for this version."

  if [ ! -x "$conda" ]; then
    installer="$root/Miniforge3-MacOSX-arm64.sh"
    miniforge_url=https://github.com/conda-forge/miniforge/releases/download/26.9.4-2/Miniforge3-MacOSX-arm64.sh
    curl -fL --retry 3 -o "$installer" "$miniforge_url"
    verify_sha fb567612b76f4ef46de326f04425dbe381b6afc6a66c545f5043255a5ef34258 "$installer"
    bash "$installer" -b -p "$root/miniforge3"
  fi

  if [ ! -x "$runtime/bin/python" ]; then
    "$conda" create -y -p "$runtime" -c conda-forge python=3.11 wget
  elif [ ! -x "$runtime/bin/wget" ]; then
    "$conda" install -y -p "$runtime" -c conda-forge wget
  fi

  cd "$repo"
  if [ ! -f "$root/.gove-runtime-ready" ]; then
    TERM=xterm-256color "$conda" run --no-capture-output -p "$runtime" \
      bash install.sh --device MPS --source HF
    "$runtime/bin/python" -m pip install 'gradio==4.44.1' 'fastapi==0.115.2' \
      'starlette==0.40.0' 'resampy==0.4.3'
    touch "$root/.gove-runtime-ready"
  fi

  source_wav='ChatGPT is a generative artificial intelligence chatbot developed by OpenAI and launched in 2022. It is currently based on the GPT-4o large language model..wav'
  mkdir -p "$root/Gove" "$ref_dir" GPT_weights_v2ProPlus SoVITS_weights_v2ProPlus
  HF_HUB_DISABLE_IMPLICIT_TOKEN=1 "$runtime/bin/hf" download OmniDimen/Gove \
    Gove.ckpt Gove.pth "$source_wav" --revision "$model_revision" --local-dir "$root/Gove"
  verify_sha "$gpt_sha" "$root/Gove/Gove.ckpt"
  verify_sha "$sovits_sha" "$root/Gove/Gove.pth"
  verify_sha "$ref_sha" "$root/Gove/$source_wav"
  cp -n "$root/Gove/Gove.ckpt" GPT_weights_v2ProPlus/Gove.ckpt
  cp -n "$root/Gove/Gove.pth" SoVITS_weights_v2ProPlus/Gove.pth
  cp -n "$root/Gove/$source_wav" "$ref_dir/reference_en.wav"
  cp -n "$skill_dir/assets/reference_en.txt" "$ref_dir/reference_en.txt"
fi

[ -x "$runtime/bin/python" ] && [ -f "$repo/api_v2.py" ] ||
  fail "Expected a Python environment in $runtime and GPT-SoVITS in $repo."
verify_sha "$gpt_sha" "$repo/GPT_weights_v2ProPlus/Gove.ckpt"
verify_sha "$sovits_sha" "$repo/SoVITS_weights_v2ProPlus/Gove.pth"
verify_sha "$ref_sha" "$ref_dir/reference_en.wav"
cd "$repo"
PATH="$runtime/bin:$PATH" "$runtime/bin/python" -u "$skill_dir/scripts/smoke-test.py" \
  "$ref_dir/reference_en.wav" "$root/output"
