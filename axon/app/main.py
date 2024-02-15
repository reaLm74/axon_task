import uvicorn
from app.api.routers import all_routers
from fastapi import FastAPI

app = FastAPI(title='axon')

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
