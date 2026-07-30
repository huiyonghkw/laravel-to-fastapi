<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

/**
 * 源码对照用控制器（非完整 Laravel 工程）。
 * 对照 FastAPI：fastapi/app/ep01.py · ep03.py · ep05.py
 */
class UserController extends Controller
{
    // EP03：列表（对照 ep03.list_users）
    public function index()
    {
        return response()->json(['users' => []]);
    }

    // EP01：/ep01/user/{user_id}；EP03：/ep03/users/{uid}
    // Laravel 路由参数名须与方法参数名一致，故两个入口各写一个薄包装。
    public function show(int $user_id)
    {
        return response()->json([
            'user_id' => $user_id,
            'db'      => 'resolved-by-container',
        ]);
    }

    /** EP03 详情：路由参数名是 {uid} */
    public function showByUid(int $uid)
    {
        return $this->show($uid);
    }

    // EP05：校验（对照 ep05.create_user 的 Pydantic）
    public function store(Request $request)
    {
        $data = $request->validate([
            'name'  => 'required|string',
            'email' => 'required|email',
            'age'   => 'nullable|integer',
        ]);

        return response()->json([
            'id'    => 1,
            'name'  => $data['name'],
            'email' => $data['email'],
        ], 201);
    }

    // EP03 练习：更新（对照 ep03.update_user）
    public function update(int $uid)
    {
        return response()->json(['uid' => $uid, 'updated' => true]);
    }
}
