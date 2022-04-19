from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import api.api

app = FastAPI()
app.include_router(api.api.router)
app.mount("/", StaticFiles(directory="client/public", html=True))
app.mount("/build", StaticFiles(directory="client/public/build"), name="build")
