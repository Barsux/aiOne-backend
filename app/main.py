import uvicorn
from fastapi import FastAPI
from .settings import settings
from .tables import Base
from .database import engine
from .api import router

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.server_host,
        port=settings.server_port,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
        reload=True
    )
