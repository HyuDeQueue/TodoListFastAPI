from fastapi import FastAPI
from dotenv import load_dotenv
from src.api import routers

load_dotenv()

app = FastAPI()

for router in routers:
    app.include_router(router)