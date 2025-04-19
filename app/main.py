from fastapi import FastAPI
from app.auth import app_auth as auth_app

app = FastAPI()
app.include_router(auth_app, prefix="/authentication")

@app.get("/",include_in_schema=False)
@app.head("/", include_in_schema=False)
def root():
    return "Home Page ......"
