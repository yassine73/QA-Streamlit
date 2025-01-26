from fastapi import FastAPI
from src.handlers.routers import chat_router
import uvicorn

app = FastAPI()
app.include_router(chat_router)

def main():
    # uvicorn.run(app=app, host="0.0.0.0", port=11003)
    uvicorn.run("app:app", host="0.0.0.0", port=11003, reload=True)

if __name__ == "__main__":
    main()
