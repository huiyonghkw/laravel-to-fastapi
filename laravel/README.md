# Laravel 侧说明（源码对照，非可运行完整工程）

本目录**只放对照用的源码片段**，用来和 `fastapi/app/epXX.py` 左右对照阅读：

- `routes/api.php` — 全部 EP 的路由，统一 `/epXX` 前缀（与 FastAPI 对称）
- `app/Http/Controllers/Api/*` — 控制器示意

## 为什么没有 `composer.json` / `artisan`？

本系列的目标是**概念平移**，不是再维护一份完整 Laravel 应用。
附上全量 Laravel 骨架会引入 `vendor/`、环境变量、数据库等噪音，淹没「对照关系」本身。

## 若你想在本地真的跑 Laravel 侧

```bash
composer create-project laravel/laravel demo
# 把本目录 routes/api.php 与 Controllers 拷进 demo 对应路径
# 再按需补 Model / Job / 中间件注册
cd demo && php artisan serve
```

FastAPI 侧才是「复制即跑」的完整可运行骨架：见仓库根 README 的快速开始。
