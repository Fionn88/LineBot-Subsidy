import os

import uvicorn
from fastapi import FastAPI
from line.urls import line_app

app = FastAPI()

# LINE Bot
app.include_router(line_app)


if __name__ == "__main__":
    # Local WSGI: Uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=4,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )