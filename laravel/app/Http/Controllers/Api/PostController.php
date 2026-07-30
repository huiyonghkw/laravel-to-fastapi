<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class PostController extends Controller
{
    // EP02：列表（对照 FastAPI ep02.list_posts）
    public function index()
    {
        return response()->json(['posts' => []]);
    }

    // EP02：创建（对照 FastAPI ep02.create_post）
    public function store(Request $request)
    {
        $data = $request->validate([
            'title'   => 'required|string',
            'body'    => 'nullable|string',
        ]);

        return response()->json(['created' => true, 'data' => $data]);
    }
}
