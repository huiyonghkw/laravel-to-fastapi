# Laravel ↔ FastAPI 对照学（免费试读）

> 用 Laravel 的肌肉记忆，平移上手 FastAPI。  
> **本仓 = MIT 试读档**：完整可跑的 3 期（世界观 / 路由 / 校验），不是残废 demo。

**版本基线**：Laravel 13（PHP 8.3+）· FastAPI 0.140.13  
**完整 15 期**：私有付费仓 [`laravel-to-fastapi-pro`](https://github.com/huiyonghkw/laravel-to-fastapi-pro)（商业授权 · ¥39.9 / 早鸟 ¥29.9）  
**站点**：本仓 GitHub Pages（推送 `main` 后开启）

## 试读包含什么

| 期 | 主题 | 代码 | HTML |
|----|------|------|------|
| EP00 | 世界观 / 请求生命周期 | `fastapi/app/ep00.py` | `ep00/` |
| EP02 | 路由 | `ep02.py` | `ep02/` |
| EP05 | 校验与序列化 (Pydantic) | `ep05.py` | `ep05/` |

装完就能 `uvicorn` + 打开 `/docs`，对照 Laravel 源码阅读。

## 快速开始

```bash
cd fastapi
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs

pytest
```

或：`docker compose up --build`

## 分档说明（能力边界）

| | 免费（本仓 · MIT） | 付费 PRO |
|---|---|---|
| 内容 | 3 期试读 + 可跑骨架 | 全 15 期 HTML + 全量对照代码 |
| 工程 | uvicorn + pytest 冒烟 | Alembic / 测试全集 / 部署 / 决策树 |
| 交付 | 公开 clone | 付款后加 GitHub collaborator（**无 zip**） |
| 更新 | tag 发布 | `git pull` 一年跟更 |

⛔ 本仓文案**只描述试读能力**。完整路线图、练习答案、选型决策树在付费仓。

## 授权

MIT — 见 `LICENSE`。
