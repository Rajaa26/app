from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from .routes import upload, download
from .utils import fs
import uvicorn
app = FastAPI()
app.include_router(upload.router)
app.include_router(download.router)

@app.on_event("startup")
async def startup():
    # corn job to delete expired files
    scheduler = BackgroundScheduler()
    scheduler.add_job(fs.delete_expired_files, 'interval', minutes=1)
    scheduler.start()
    print("Started corn job")
