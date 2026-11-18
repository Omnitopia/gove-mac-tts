<div align="center">

# Gove Mac Skill

**让 [Gove](https://github.com/OmniDimen/Gove) 的声音，在你的 Apple Silicon Mac 上本地开口说话。**  
*Run the [Gove](https://github.com/OmniDimen/Gove) voice locally on Apple Silicon Macs with one AI agent skill.*

[![Platform](https://img.shields.io/badge/macOS-Apple%20Silicon-black?logo=apple)](https://github.com/Omnitopia/gove-mac-tts)
[![Architecture](https://img.shields.io/badge/GPT--SoVITS-v2ProPlus-4a7c59)](https://github.com/RVC-Boss/GPT-SoVITS)
[![Upstream](https://img.shields.io/badge/Upstream-OmniDimen%2FGove-1f6feb?logo=github)](https://github.com/OmniDimen/Gove)
[![Weights](https://img.shields.io/badge/Hugging%20Face-OmniDimen%2FGove-ffd21e?logo=huggingface&logoColor=black)](https://huggingface.co/OmniDimen/Gove)

[试听 · Demos](#试听--audio-demos) · [简体中文](#简体中文) · [English](#english) · [SKILL.md](SKILL.md)

</div>

---

## 试听 · Audio Demos

同一句问候，四种语言，全部在 Apple Silicon Mac 本地合成。  
*The same greeting in four languages, synthesized locally on an Apple Silicon Mac.*

| 语言 / Language | 台词 / Line | 试听 / Audio |
| :--- | :--- | :---: |
| 普通话 / Mandarin | 你好呀，终于又见面了。 | [▶ 试听 MP3](assets/demos/zh.mp3) |
| 英语 / English | Hey, it's so good to see you again. | [▶ Listen MP3](assets/demos/en.mp3) |
| 日语 / Japanese | こんにちは。やっとまた会えたね。 | [▶ 試聴 MP3](assets/demos/ja.mp3) |
| 粤语 / Cantonese | 你好呀，終於又見到你喇。 | [▶ 試聽 MP3](assets/demos/yue.mp3) |

---

## 简体中文

### 一键安装，复制以下指令给你的 AI：

```text
请从 https://github.com/Omnitopia/gove-mac-tts 安装 Gove Skill，按说明在这台 Mac 上帮我装好 Gove，并生成一句「你好呀，终于又见面了。」的测试音频发给我。
```

### 安装前须知

| 项目 | 说明 |
| :--- | :--- |
| **适用设备** | Apple Silicon Mac（M1 / M2 / M3 / M4 及以上芯片，原生 arm64 终端） |
| **默认路径** | `~/Gove-TTS`（试音输出在 `~/Gove-TTS/output/`；可在指令中指定其他不含空格的路径，如 `/Volumes/SSD/Gove-TTS`） |
| **空间与流量** | 全新安装建议预留约 **20 GB 磁盘空间**与 **7 GB 下载流量**；AI 会在开始下载前向你确认 |
| **环境隔离** | 自带独立 Miniforge 与 Python 3.11 环境，不改动系统 Python；如本地已有可用的 Gove 环境，可直接复用试音 |

### Skill 会自动完成什么

1. **拉取锁定版本的 GPT-SoVITS**：固定在已实测通过的提交版本，避开上游变动导致的报错。
2. **搭建独立运行环境**：自动安装依赖并修复当前 macOS 下的 Gradio / FastAPI / Starlette / resampy 兼容问题。
3. **下载并校验 Gove 资产**：从 [Hugging Face](https://huggingface.co/OmniDimen/Gove) 拉取 Gove 权重与参考音频，并逐一进行 SHA-256 校验。
4. **本地进程内试音验证**：无需启动常驻服务或占用端口，支持自定义中文/英文/日语/粤语台词，直接合成并校验音频非空、非静音，输出可播放的 WAV 文件。

> 已在 Apple Silicon Mac 上从空目录跑通完整全新安装与本地试音。完整执行细则与复用已有 Conda 环境的方法见 [SKILL.md](SKILL.md)。

---

## English

### One-click setup: copy this prompt to your AI

```text
Install the Gove Skill from https://github.com/Omnitopia/gove-mac-tts. Follow its instructions to set up Gove on this Mac, then generate a test WAV for "Hey, it's so good to see you again." and send it to me.
```

### Before you start

| Item | Details |
| :--- | :--- |
| **Supported hardware** | Apple Silicon Mac (M1 / M2 / M3 / M4 or later, native arm64 terminal) |
| **Install location** | Defaults to `~/Gove-TTS` (test audio saved to `~/Gove-TTS/output/`). You can specify any path without spaces, such as `/Volumes/SSD/Gove-TTS`. |
| **Disk & bandwidth** | Allow about **20 GB of free disk space** and **7 GB of downloads** for a fresh install. The agent confirms path and download size before starting. |
| **Isolation** | Installs its own Miniforge and Python 3.11 environment without touching system Python. Existing working Gove setups can be reused directly for verification. |

### What the skill handles for you

1. **Pinned GPT-SoVITS checkout**: clones a tested commit so upstream changes will not break your install.
2. **Isolated macOS runtime**: sets up Python 3.11 and applies the known working Gradio, FastAPI, Starlette, and resampy pins.
3. **Verified Gove weights**: downloads the voice weights and reference audio from [Hugging Face](https://huggingface.co/OmniDimen/Gove) with SHA-256 verification.
4. **In-process smoke test**: exercises `/tts` directly without opening a port, supports custom Mandarin, English, Japanese, or Cantonese lines, verifies the WAV is non-empty and non-silent, and prints the output path.

> Tested end-to-end from a clean folder on Apple Silicon. See [SKILL.md](SKILL.md) for full agent instructions and reusing an existing Conda layout.

---

## 致谢 · Credits

- **Voice Model**: [OmniDimen/Gove](https://github.com/OmniDimen/Gove) ([Hugging Face](https://huggingface.co/OmniDimen/Gove))
- **TTS Engine**: [RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
- **Mac Skill Maintainer**: [Omnitopia](https://github.com/Omnitopia)
- **License**: Scripts and documentation are licensed under the [MIT License](LICENSE). Model weights and GPT-SoVITS remain subject to their upstream licenses.
