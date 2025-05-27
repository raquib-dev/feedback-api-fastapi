from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, schemas, auth
from app.database import get_db
from app.logger import logger

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------------------
# Register
# ---------------------------
@router.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(models.User).where(models.User.username == user.username)
    result = await db.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info(f"New user registered: {user.username}")
    return new_user

# ---------------------------
# Login
# ---------------------------
@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    query = select(models.User).where(models.User.username == user.username)
    result = await db.execute(query)
    db_user = result.scalars().first()

    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": db_user.username})
    logger.info(f"User logged in: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}
