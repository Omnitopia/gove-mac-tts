# Gove Mac Skill

[简体中文](#简体中文) · [English](#english)

## 试听 · Audio demos

同一句问候，四种语言。 The same greeting in four languages.

| 语言 / Language | 台词 / Line | 试听 / Audio |
| --- | --- | --- |
| 普通话 / Mandarin | 你好呀，终于又见面了。 | [MP3](assets/demos/zh.mp3) |
| 英语 / English | Hey, it's so good to see you again. | [MP3](assets/demos/en.mp3) |
| 日语 / Japanese | こんにちは。やっとまた会えたね。 | [MP3](assets/demos/ja.mp3) |
| 粤语 / Cantonese | 你好呀，終於又見到你喇。 | [MP3](assets/demos/yue.mp3) |

## 简体中文

用 AI 在 Apple Silicon Mac 上安装 Gove，并生成第一段本地语音。Skill 会准备 GPT-SoVITS、从 OmniDimen 下载 Gove 权重和参考音频，最后交给你一个 WAV 文件。[Gove 模型](https://huggingface.co/OmniDimen/Gove)

### 复制给你的 AI

把下面这段话交给能使用这台 Mac 终端的 AI。

```text
请从 https://github.com/Omnitopia/gove-mac-tts 安装 Gove Skill，按它的说明在这台 Mac 上安装 Gove，再把「你好呀，终于又见面了。」的测试音频发给我。
```

### 安装位置

Gove 默认装到 `~/Gove-TTS`，试音文件会放在 `~/Gove-TTS/output/`。全新安装建议预留约 **20 GB 磁盘空间**和 **7 GB 下载流量**。你也可以在指令里指定一个不含空格的路径，例如 `/Volumes/SSD/Gove-TTS`。AI 会在下载前告诉你安装位置和预计下载量，遇到空间不足或目录冲突时再请你选个位置。已有可用的 Gove 环境可以直接试音。

已在 Apple Silicon Mac 上从空安装目录跑通全新安装，并成功生成测试 WAV。执行说明见 [SKILL.md](SKILL.md)。

## English

Use AI to install Gove on a Mac with Apple silicon and generate your first audio clip locally. The skill sets up GPT-SoVITS, downloads the Gove weights and reference audio from OmniDimen, and gives you a WAV file. [Gove model](https://huggingface.co/OmniDimen/Gove)

### Copy this prompt to your AI

Give this prompt to an AI agent that can run terminal commands on your Mac.

```text
Install the Gove Skill from https://github.com/Omnitopia/gove-mac-tts. Follow its instructions to set up Gove on this Mac, then give me the test WAV for “你好呀，终于又见面了。” (“Hey, it's so good to see you again.”)
```

### Install location

Gove installs to `~/Gove-TTS` by default and saves test audio in `~/Gove-TTS/output/`. Allow about **20 GB of free disk space** and **7 GB of downloads** for a fresh install. You can specify a path without spaces, such as `/Volumes/SSD/Gove-TTS`. The agent tells you the location and estimated download size before it starts and asks you to choose another folder if there is too little space or a folder conflict. It can also reuse a working Gove installation for the audio test.

A fresh install from an empty folder passed on a Mac with Apple silicon and produced the test WAV. See the [skill instructions](SKILL.md).
