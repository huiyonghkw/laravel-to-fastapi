# EP14 部署对照：Laravel 用 Nginx+PHP-FPM，FastAPI 用 Gunicorn + UvicornWorker (ASGI)。
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
# EP07 Alembic 最小可跑骨架（迁移对照）
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

ENV HOST=0.0.0.0 PORT=8000 WORKERS=4
EXPOSE 8000

# 生产：Gunicorn + Uvicorn worker（多进程跑 ASGI）
CMD gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WORKERS} -b ${HOST}:${PORT}
