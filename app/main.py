from fastapi import FastAPI
from .routers import login
import uvicorn

app=FastAPI()

app.include_router(login.router)

@app.get('/')
async def root():
    return {'message':'hello world!'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)