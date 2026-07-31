# li-answer-book-pub-

M5Stack Cardputer 1.1 多模式决策辅助应用 / Multi-Mode Decision Helper for M5Stack Cardputer 1.1

## 项目简介 / Overview

基于 M5Stack Cardputer 1.1 的随机决策辅助应用，支持 5 种玩法模式和中英双语。

A random decision helper application for M5Stack Cardputer 1.1, supporting 5 game modes with bilingual (Chinese/English) interface.

## 玩法模式 / Game Modes

1. **答案之书 / Book of Answers** - 50 条神秘答案，帮你解答疑惑
2. **抛硬币 / Coin Flip** - 正面或反面，随机抉择
3. **掷色子 / Roll Dice** - 1 到 6，概率均等
4. **今日运势 / Fortune** - 大吉/吉/中平/凶/大凶
5. **幸运数字 / Lucky Number** - 1 到 100，随机生成

## 硬件要求 / Hardware

- **设备 / Device**: M5Stack Cardputer 1.1 (K132-V11)
- **主控 / MCU**: Stamp-S3A (ESP32-S3FN8)
- **屏幕 / Display**: ST7789V2 1.14" TFT, 240×135 px
- **输入 / Input**: 56-key keyboard + G0 User button
- **固件 / Firmware**: UIFlow2 (latest)

## 安装 / Installation

1. 下载 `main.py` 文件
2. 将 `main.py` 上传到 Cardputer 根目录
3. 重启设备即可运行

1. Download `main.py`
2. Upload `main.py` to the root directory of your Cardputer
3. Restart the device to run

## 操作方式 / Controls

| 操作 / Action | G0 按键 / G0 Button | 说明 / Description |
|---|---|---|
| 切换菜单 / Next menu | 单击 / Single click | 在菜单中切换下一个玩法 |
| 进入玩法 / Enter mode | 双击 / Double click | 进入当前选中的玩法 |
| 返回菜单 / Back to menu | 双击 / Double click | 在玩法中返回菜单 |
| 切换语言 / Toggle language | 三击 / Triple click | 中文 ↔ English |

## 屏幕提示 / Screen Hints

- 菜单页提示：`1切 2进 3语` (1:Next 2:Enter 3:Lang)
- 玩法页提示：`1开 2回 3语` (1:Go 2:Bk 3:Lang)
- 结果页提示：`1再 2回 3语` (1:Again 2:Bk 3:Lang)

## 功能特性 / Features

- ✅ 启动淡入淡出动画 / Boot fade-in animation
- ✅ 随机抽取滚动动画 / Shuffle animation
- ✅ 中英双语界面 / Bilingual UI (Chinese/English)
- ✅ 单色高效渲染 / Monochrome-optimized rendering
- ✅ 无外部依赖 / No external dependencies

## 版本历史 / Changelog

### v0.2-beta

- 适配 M5Stack Cardputer 1.1 / Adapted for M5Stack Cardputer 1.1
- 移除 v1.0.0 版本（Core 版本）/ Removed v1.0.0 (Core version)
- 初始 Cardputer 支持 / Initial Cardputer support

## 文件结构 / File Structure

```
li-answer-book-pub-/
├── main.py          # 主程序 / Main program
├── README.md
└── LICENSE
```

## 许可证 / License

GNU General Public License v3.0 (GPL-3.0)
