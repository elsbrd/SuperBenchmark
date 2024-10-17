import os

from fastapi import FastAPI

from src.api.routes.benchmark_routes import router as benchmark_router

app = FastAPI()

DEBUG_MODE = os.getenv("SUPERBENCHMARK_DEBUG", "False").lower() == "true"

if DEBUG_MODE:
    app.include_router(benchmark_router)
else:
    raise NotImplementedError("Feature not ready for live yet.")
