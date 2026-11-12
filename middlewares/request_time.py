import time
from fastapi import APIRouter, Request, FastAPI

async def log_requests(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start

    print(
        f"{request.method} {request.url.path}"
        f" - {duration:.3f}s"
    )

    return response