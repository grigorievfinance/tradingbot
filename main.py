import uvicorn

from fastapi import FastAPI
from models import model
from models.database import engine
from routers.items import router as items_router
from routers.users import router as users_router

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(
    router=items_router,
    prefix='/items',
)

app.include_router(
    router=users_router,
    prefix='/users',
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
