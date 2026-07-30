"""EP13 异步与队列：Laravel Queue vs BackgroundTasks / 真队列边界

Laravel：dispatch(Job::class) 进队列，独立 Worker 进程异步处理。
FastAPI 两档：
  1) BackgroundTasks —— 响应返回后、**同一进程内**执行（轻量，重启会丢）
  2) Celery / ARQ / RQ —— 跨进程真队列（对标 Laravel Queue），本仓只给边界说明

本页可跑的是第 1 档；第 2 档见 /ep13/queue-map 与下方注释骨架。
"""
import time

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr

router = APIRouter()


class NotifyIn(BaseModel):
    email: EmailStr


def _send_email(email: str):
    # 模拟耗时任务（发邮件/写日志），在响应返回后、同进程执行
    time.sleep(0.05)
    print(f"[ep13] sent email to {email}")


@router.post("/notify")
def notify(payload: NotifyIn, bg: BackgroundTasks):
    # 对照 Laravel: dispatch(new SendEmail($email)); 立即返回
    bg.add_task(_send_email, payload.email)
    return {
        "queued": True,
        "email": payload.email,
        "engine": "BackgroundTasks",
        "caveat": "同进程；进程重启会丢。重活请上 Celery/ARQ",
    }


@router.get("/queue-map")
def queue_map():
    """Laravel Queue ↔ FastAPI 真队列对照（命令/概念，非可跑 Worker）。"""
    return {
        "laravel": {
            "dispatch": "dispatch(new SendEmail($email))",
            "worker": "php artisan queue:work",
            "driver": "database / redis / sqs",
        },
        "fastapi_light": {
            "dispatch": "bg.add_task(fn, ...)",
            "worker": "无需（同进程）",
            "when": "发邮件日志等轻量、可丢",
        },
        "fastapi_heavy": {
            "celery": "celery -A worker worker -l info",
            "arq": "arq worker.WorkerSettings",
            "when": "跨进程、可重试、可水平扩展 —— 对标 Laravel Queue",
        },
        # ---- Celery 最小骨架（需另装 celery[redis]）----
        # from celery import Celery
        # celery_app = Celery("ep13", broker="redis://localhost:6379/0")
        # @celery_app.task
        # def send_email(email: str): ...
        # send_email.delay(email)
    }
