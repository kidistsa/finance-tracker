from fastapi import APIRouter, Depends, HTTPException
from app.services.email_service import EmailService
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/email", tags=["Email Reports"])


@router.post("/weekly-report")
async def send_weekly_report(
    current_user: dict = Depends(get_current_user),
    email_service: EmailService = Depends()
):
    """Send weekly report to current user"""
    user_email = current_user.get("email") or current_user.get("uid")
    
    success = email_service.send_weekly_report(user_email)
    
    if success:
        return {"message": f"Weekly report sent to {user_email}"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")