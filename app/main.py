from fastapi import FastAPI
from app.logger import logger
from app.database import Base, engine
from app.routes import users
from app.routes import feedback

app = FastAPI()
app.include_router(users.router)
app.include_router(feedback.router)

@app.get("/")
async def root():
    return {"message": "Feedback API is live"}

# Run only once when the app starts
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database tables created")
