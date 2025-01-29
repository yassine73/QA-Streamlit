from fastapi import FastAPI
import streamlit as st
import uvicorn
import logging
import os

from src.handlers.routers import chat_router
from src.components.main import load_design

load_design()
app = FastAPI()
app.include_router(chat_router)
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="./logs/logger.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

def main():
    # uvicorn.run(app=app, host="0.0.0.0", port=11111)
    # uvicorn.run("app:app", host="0.0.0.0", port=11003, reload=True)
    logger.info("Server started")

if __name__ == "__main__":
    main()
