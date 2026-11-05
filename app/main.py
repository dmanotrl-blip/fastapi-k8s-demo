from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Kubernetes Demo",
    description="A small FastAPI service packaged with Docker and deployed to Kubernetes.",
    version="1.0.0",
)


@app.get("/", tags=["root"])
def home():
    return {
        "message": "Hello from FastAPI!",
        "platform": "Kubernetes",
    }


@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}


@app.get("/api/v1/hello/{name}", tags=["demo"])
def hello(name: str):
    return {"message": f"Hello, {name}!"}
