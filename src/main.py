import uvicorn
from fastapi import FastAPI
from line.urls import line_app
import config
app = FastAPI()

# LINE Bot
app.include_router(line_app)


if __name__ == "__main__":
    # Local WSGI: Uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(config.PORT),
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )