import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # main.py with app = FastAPI()
        host="127.0.0.1",
        port=9000,
        reload=True,
    )
