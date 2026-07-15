from fastapi import FastAPI

app = FastAPI(
    title="Industrial Knowledge Intelligence Platform",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Industrial Knowledge Intelligence Platform"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }