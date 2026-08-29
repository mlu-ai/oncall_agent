"""FastAPI 应用工厂。"""

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Super AI")

    @app.get("/health")
    async def health() -> dict[str, str]:  # pyright: ignore[reportUnusedFunction]
        return {"status": "ok"}

    return app
