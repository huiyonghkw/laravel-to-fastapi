<?php
/**
 * Laravel 13 侧 · 对照 FastAPI 的代码骨架（源码级对照）
 *
 * ⚠️ 本目录只放对照源码，不附带完整 Laravel 工程（无 composer.json / artisan）。
 *    阅读对照即可；若要在本地真正跑通，请自行 `composer create-project laravel/laravel`
 *    后把这些文件拷进对应路径。
 *
 * 路由一律带 /epXX 前缀，与 FastAPI 的 /epXX/* 一一对应，避免路径互相覆盖。
 */

use App\Http\Controllers\Api\PostController;
use App\Http\Controllers\Api\UserController;
use Illuminate\Support\Facades\Route;

// EP00 世界观（对照 fastapi/app/ep00.py）
Route::prefix('ep00')->group(function () {
    Route::get('/hello', fn () => [
        'framework' => 'Laravel',
        'msg'       => 'Hello from a full-stack MVC framework (PHP-FPM, synchronous)',
    ]);
});

// EP01 心智模型：服务容器（对照 ep01.py）
Route::prefix('ep01')->group(function () {
    Route::get('/user/{user_id}', [UserController::class, 'show']);
});

// EP02 路由分组 + 中间件（对照 ep02.py 的 APIRouter）
Route::prefix('ep02')->middleware('auth:sanctum')->group(function () {
    Route::get('/posts', [PostController::class, 'index']);
    Route::post('/posts', [PostController::class, 'store']);
});

// EP03 控制器 vs 路径操作函数（对照 ep03.py）
Route::prefix('ep03')->group(function () {
    Route::get('/users', [UserController::class, 'index']);
    Route::get('/users/{uid}', [UserController::class, 'showByUid']);
    Route::post('/users', [UserController::class, 'store']);
    Route::put('/users/{uid}', [UserController::class, 'update']);
});

// EP04 请求与响应（对照 ep04.py）
Route::prefix('ep04')->group(function () {
    Route::get('/echo', fn (\Illuminate\Http\Request $r) => [
        'path'  => $r->path(),
        'token' => $r->header('x-token'),
    ]);
});

// EP05 校验与序列化（对照 ep05.py 的 Pydantic）
Route::prefix('ep05')->group(function () {
    Route::post('/users', [UserController::class, 'store']);
});

// EP06 ORM（对照 ep06.py）—— 真实项目用 Eloquent: Post::with('comments')
Route::prefix('ep06')->group(function () {
    Route::get('/posts', [PostController::class, 'index']);
});

// EP07 迁移（对照 ep07.py / Alembic）
// 真实命令：php artisan make:migration / php artisan migrate
Route::prefix('ep07')->group(function () {
    Route::get('/alembic', fn () => [
        'laravel' => ['php artisan migrate', 'php artisan migrate:rollback'],
        'note'    => 'FastAPI 侧见 GET /ep07/alembic',
    ]);
});

// EP08 事务（对照 ep08.py）—— 示意；真实需 Order 模型
Route::prefix('ep08')->group(function () {
    Route::post('/orders', function () {
        return \Illuminate\Support\Facades\DB::transaction(function () {
            // $order = \App\Models\Order::create(['amount' => 100]);
            return ['id' => 1, 'amount' => 100, 'note' => 'skeleton — wire Order model in real app'];
        });
    });
});

// EP09 依赖注入进阶（对照 ep09.py）
Route::prefix('ep09')->group(function () {
    Route::get('/db-url', fn () => ['url' => 'db://' . config('app.env')]);
});

// EP10 中间件（对照 ep10.py）—— 示意；真实需注册 log 中间件
Route::prefix('ep10')->group(function () {
    Route::middleware('log')->get('/secure', fn () => ['ok' => true]);
});

// EP11 认证（对照 ep11.py）
Route::prefix('ep11')->group(function () {
    Route::post('/login', fn () => [
        'access_token' => 'user:alice',
        'token_type'   => 'bearer',
        'note'         => 'skeleton stub — use Sanctum in real app',
    ]);
    Route::middleware('auth:sanctum')->get('/me', fn () => auth()->user());
});

// EP12 测试：见 tests/Feature/*（Pest）；FastAPI 见 fastapi/tests/test_ep12.py

// EP13 队列（对照 ep13.py BackgroundTasks）
Route::prefix('ep13')->group(function () {
    Route::post('/notify', function (\Illuminate\Http\Request $r) {
        // dispatch(new \App\Jobs\SendEmail($r->input('email')));
        return ['queued' => true, 'email' => $r->input('email'), 'note' => 'skeleton — wire Job in real app'];
    });
});

// EP14 部署：Laravel Nginx+PHP-FPM；FastAPI 见 fastapi/Dockerfile —— 无新增业务路由

// EP15 选型决策树（对照 ep15.py）
Route::prefix('ep15')->group(function () {
    Route::post('/advise', function (\Illuminate\Http\Request $r) {
        $needAi = (bool) $r->input('need_ai');
        $hasFrontend = (bool) $r->input('has_frontend');
        if ($needAi && ! $hasFrontend) {
            return ['pick' => 'FastAPI', 'why' => 'AI/ML 推理，Python 生态无摩擦'];
        }
        if ($hasFrontend) {
            return ['pick' => 'Laravel', 'why' => '要渲染页面/全栈，Laravel 开箱即用'];
        }
        return ['pick' => $r->input('need_realtime') ? 'FastAPI' : 'Laravel'];
    });
});
