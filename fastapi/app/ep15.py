"""EP15 收官：选型决策树

不是代码框架，而是一棵「什么时候用哪个」的判断函数。
把前面 15 期沉淀成一条可调用规则，对照你手上的项目特征给建议。
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class ProjectProfile(BaseModel):
    has_frontend: bool = Field(description="是否要渲染页面 / 全栈")
    need_realtime: bool = Field(description="是否要流式/高并发 I/O")
    team_knows_php: bool = Field(description="团队 PHP 储备")
    need_ai: bool = Field(default=False, description="是否重度依赖 Python AI/ML 生态")


@router.post("/advise")
def advise(p: ProjectProfile):
    # 决策逻辑（对照 Laravel 全栈 vs FastAPI API 的定位）
    if p.need_ai and not p.has_frontend:
        pick, why = "FastAPI", "AI/ML 推理，Python 生态无摩擦"
    elif p.has_frontend:
        pick, why = "Laravel", "要渲染页面/全栈，Laravel 开箱即用"
    elif p.need_realtime:
        pick, why = "FastAPI", "高并发 I/O / 流式响应，FastAPI 的异步红利明显"
    elif p.team_knows_php:
        pick, why = "Laravel", "团队 PHP 熟，先用 Laravel 交付"
    else:
        pick, why = "FastAPI", "纯后端 API，FastAPI 更轻更显式"
    return {"pick": pick, "why": why, "profile": p.model_dump()}
