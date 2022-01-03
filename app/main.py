from fastapi import FastAPI
from .routers import login,user
import uvicorn

app=FastAPI()

app.include_router(login.router)
app.include_router(user.router)

@app.get('/')
async def root():
    return {'message':'hello world!'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)