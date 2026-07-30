# Laravel ↔ FastAPI 对照学

> 用 Laravel 的肌肉记忆，平移上手 FastAPI。每期一个概念，左 Laravel / 右 FastAPI 同框可运行。
> 本系列以 **HTML 长文 + 可运行代码** 的形式发布在 **GitHub Pages**，不发小红书。

**版本基线**：Laravel 13（PHP 8.3+）· FastAPI 0.140.13  
**仓库**：https://github.com/huiyonghkw/laravel-to-fastapi  
**站点**：推送 `main` 后开 Pages → `https://huiyonghkw.github.io/laravel-to-fastapi/`

## EP 索引

| 期 | 主题 | FastAPI 代码 | HTML 正文 | 深度 |
|----|------|--------------|-----------|------|
| EP00 | 世界观 / 请求生命周期 | `fastapi/app/ep00.py` | `ep00/` | 厚 |
| EP01 | 心智模型 / DI / 异步 | `ep01.py` | `ep01/` | 厚 |
| EP02 | 路由 | `ep02.py` | `ep02/` | 厚 |
| EP03 | 控制器 vs 路径操作函数 | `ep03.py` | `ep03/` | 中 |
| EP04 | 请求与响应 | `ep04.py` | `ep04/` | 中 |
| EP05 | 校验与序列化 (Pydantic) | `ep05.py` | `ep05/` | 厚 |
| EP06 | ORM（SQLAlchemy 2.0 `select`） | `ep06.py` | `ep06/` | 厚 |
| EP07 | 迁移（Alembic 可跑骨架） | `ep07.py` + `alembic/` | `ep07/` | 中 |
| EP08 | 事务（同步 Session） | `ep08.py` | `ep08/` | 中 |
| EP09 | 依赖注入进阶 | `ep09.py` | `ep09/` | 中 |
| EP10 | 中间件（路由依赖 + CORS） | `ep10.py` + `main.py` | `ep10/` | 中 |
| EP11 | 认证授权（OAuth2 stub） | `ep11.py` | `ep11/` | 中 |
| EP12 | 测试 | `tests/test_ep12.py` | `ep12/` | 中 |
| EP13 | 异步与队列边界 | `ep13.py` | `ep13/` | 中 |
| EP14 | 部署 | `Dockerfile` + `ep14.py` | `ep14/` | 中 |
| EP15 | 收官：选型决策树 | `ep15.py` | `ep15/` | 中 |

> FastAPI 侧 **复制即跑**。Laravel 侧是**源码对照**（见 `laravel/README.md`），不要求 `composer install`。

## 目录结构

```
laravel-to-fastapi/
├── index.html               # GitHub Pages 首页
├── PLAN.md                  # EP 大纲 + 发布 SOP
├── README.md                # 本文件
├── docker-compose.yml       # 一键起 API
├── .github/workflows/ci.yml # pytest + docker build
├── assets/theme.css         # V6焰彩白主题
├── ep00/ … ep15/            # 各期 HTML 正文
├── fastapi/                 # 可运行对照骨架
│   ├── requirements.txt
│   ├── pytest.ini           # pythonpath=. 保证 pytest 可发现 app
│   ├── Dockerfile
│   ├── alembic.ini + alembic/  # EP07 迁移骨架
│   ├── app/main.py + ep00.py…ep15.py + db.py
│   └── tests/test_ep12.py
└── laravel/                 # 源码对照（非完整工程）
    ├── README.md
    ├── routes/api.php       # 统一 /epXX 前缀，与 FastAPI 对称
    └── app/Http/Controllers/Api/
```

## 快速开始（FastAPI · 复制即跑）

```bash
cd fastapi
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# 浏览器开 http://127.0.0.1:8000/docs

# 跑测试（无需手动设 PYTHONPATH，pytest.ini 已配置）
pytest

# 或 Docker
cd .. && docker compose up --build
```

### Laravel 侧（阅读对照）

见 [`laravel/README.md`](laravel/README.md)。路由已按 `/ep00`…`/ep15` 与 FastAPI 对齐；若要真跑，自行 `composer create-project` 后拷入文件。

## 发布到 GitHub Pages

仓库根目录即站点根。链接均用**相对路径**。

1. 推到 GitHub（本仓 `huiyonghkw/laravel-to-fastapi`）。
2. **Settings → Pages → Source = Deploy from a branch**，目录 **/ (root)**。
3. 访问 `https://huiyonghkw.github.io/laravel-to-fastapi/`。

> `.nojekyll` 已就位。

## 每期写作模板

每个 `epXX/index.html` 复用 `assets/theme.css`：
**①一句话概念 → ②左 Laravel / 右 FastAPI → ③差异点 → ④上手练习 → ⑤上下期导航**。
