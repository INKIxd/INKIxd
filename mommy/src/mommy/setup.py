import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from mommy.router import router

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", include_in_schema=False)
def read_index():
    # Файл index.html должен лежать в той же папке, что и setup.py (в src/mommy/)
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(file_path)