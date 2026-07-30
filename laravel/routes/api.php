<?php
/**
 * Laravel 13 侧 · 免费试读对照（EP00 / EP02 / EP05）
 * 完整 15 期路由见付费仓 laravel-to-fastapi-pro
 */
use App\Http\Controllers\Api\PostController;
use App\Http\Controllers\Api\UserController;
use Illuminate\Support\Facades\Route;

Route::prefix('ep00')->group(function () {
    Route::get('/hello', fn () => [
        'framework' => 'Laravel',
        'msg'       => 'Hello from a full-stack MVC framework (PHP-FPM, synchronous)',
    ]);
});

Route::prefix('ep02')->middleware('auth:sanctum')->group(function () {
    Route::get('/posts', [PostController::class, 'index']);
    Route::post('/posts', [PostController::class, 'store']);
});

Route::prefix('ep05')->group(function () {
    Route::post('/users', [UserController::class, 'store']);
});
