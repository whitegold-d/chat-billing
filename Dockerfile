FROM python:3.11-slim
WORKDIR /scr
RUN pip install uv
COPY pyproject.toml uv.lock .
RUN uv sync
COPY /app /scr/app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.backend:app"]