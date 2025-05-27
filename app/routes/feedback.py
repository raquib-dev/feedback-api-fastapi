from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, schemas, auth
from app.database import get_db
from app.logger import logger

router = APIRouter(prefix="/feedback", tags=["Feedback"])

# ---------------------------
# Submit Feedback
# ---------------------------
@router.post("/", response_model=schemas.FeedbackOut)
async def submit_feedback(
    feedback: schemas.FeedbackCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_feedback = models.Feedback(
        content=feedback.content,
        user_id=current_user.id
    )
    db.add(new_feedback)
    await db.commit()
    await db.refresh(new_feedback)
    logger.info(f"Feedback submitted by user {current_user.username}")
    return new_feedback

# ---------------------------
# View Approved Feedback
# ---------------------------
@router.get("/", response_model=list[schemas.FeedbackOut])
async def get_public_feedback(db: AsyncSession = Depends(get_db)):
    query = select(models.Feedback).where(
        models.Feedback.is_approved == True,
        models.Feedback.is_deleted == False
    )
    result = await db.execute(query)
    return result.scalars().all()

# ---------------------------
# Admin: List All Feedback
# ---------------------------
@router.get("/admin", response_model=list[schemas.FeedbackOut])
async def get_all_feedback(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    result = await db.execute(select(models.Feedback))
    return result.scalars().all()

# ---------------------------
# Admin: Approve/Reject
# ---------------------------
@router.put("/admin/{feedback_id}")
async def moderate_feedback(
    feedback_id: int,
    is_approved: bool,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    query = select(models.Feedback).where(models.Feedback.id == feedback_id)
    result = await db.execute(query)
    feedback = result.scalars().first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    feedback.is_approved = is_approved
    await db.commit()
    logger.info(f"Admin {current_user.username} {'approved' if is_approved else 'rejected'} feedback {feedback_id}")
    return {"message": f"Feedback {'approved' if is_approved else 'rejected'}"}
