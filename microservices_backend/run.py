import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",  # format: "filename:instance"
        host="0.0.0.0",
        port=8000,
        reload=True,  # auto-reload for development
    )
