# 《Laravel ↔ FastAPI 对照学》专题 EP 规划

> 面向已有 PHP/Laravel 基础、想系统上手 Python/FastAPI 的开发者。
> 核心主张：**你不是从零学新语言，而是把 Laravel 的肌肉记忆平移到 FastAPI。**

---

## 1. 版本基线（2026-07 实测）

| 框架 | 版本 | 备注 |
|------|------|------|
| Laravel | **13** | 2026-03-17 发布，要求 PHP 8.3+ |
| FastAPI | **0.140.13** | 2026-07-28，Pydantic v2 · Starlette · ASGI |

**开篇钩子**：两个框架在 2026 不约而同拥抱 AI——Laravel 13 出了官方 AI SDK，FastAPI 成了 LLM 后端基础设施支柱。

---

## 2. 系列结构：4 幕 15 期（全部已落地）

每期固定板块：**①一句话概念 → ②左 Laravel / 右 FastAPI → ③差异点 → ④上手练习**。

| 幕 | 期 | 主题 | 状态 |
|----|----|------|------|
| 0 世界观 | EP00–EP01 | 框架哲学 / DI·异步心智 | ✅ 正文+代码 |
| 1 请求主干 | EP02–EP05 | 路由 / 控制器 / 请求响应 / Pydantic | ✅ |
| 2 数据持久化 | EP06–EP08 | SQLAlchemy 2.0 `select` / Alembic / 同步事务 | ✅ |
| 3 工程化 | EP09–EP15 | DI进阶 / 中间件·CORS / 认证 / 测试 / 队列边界 / 部署 / 决策树 | ✅ |

### 教学约定（防踩坑）

- **ORM 查询**：教 SQLAlchemy 2.0 `select()` + `session.execute`，**不教** legacy `db.query()`。
- **Session**：演示用**同步 Session**（对标 Eloquent 默认同步）；async SQLAlchemy 另开进阶，正文不混用「async session」口号。
- **队列**：`BackgroundTasks` = 同进程轻量；Celery/ARQ = 对标 Laravel Queue 的真队列（EP13 给边界图，不强制起 Worker）。
- **Laravel 侧**：源码对照，不维护完整 `composer` 工程（见 `laravel/README.md`）。
- **认证**：EP11 是 OAuth2 stub（`user:<name>` token），明确标注非生产 JWT。

---

## 3. HTML 长文模板（GitHub Pages）

每个 `epXX/index.html` 复用 `assets/theme.css`（V6焰彩白），相对路径。页脚含**上一期 / 下一期**导航。

---

## 4. GitHub Pages 发布 SOP

1. 对照代码落进 `fastapi/app/epXX.py`（及必要时 `laravel/routes/api.php`）。
2. 写/改 `epXX/index.html`，首页路线图保持同步。
3. `cd fastapi && pytest` 绿灯后再推。
4. Pages：Source = branch `/ (root)`。
5. CI：`.github/workflows/ci.yml` 自动跑 pytest + docker build。

---

## 5. 代码仓库使用说明

### FastAPI（复制即跑）
```bash
cd fastapi
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # /docs
pytest                          # pytest.ini 已设 pythonpath
```

### Docker
```bash
docker compose up --build
```

### Alembic（EP07）
```bash
cd fastapi
alembic upgrade head            # 使用 alembic/versions/0001_initial.py
```

### Laravel（源码对照）
见 `laravel/README.md`。路由统一 `/epXX` 前缀，与 FastAPI 对称。

---

## 6. 维护清单

- [ ] 改代码后跑 `pytest`
- [ ] HTML 与 `epXX.py` 同源（避免示意代码漂移）
- [ ] README / 本文件 / 首页卡片状态一致
- [ ] 不把 `.venv/`、`*.db`、`.DS_Store` 推进仓库
