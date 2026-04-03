from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.models.user import User, UserResponse, UserUpdate, UserRole, UserStatus
from app.repositories.user_repo import UserRepository
from app.api.dependencies.auth import get_current_user, require_admin
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


async def get_user_repo():
    return UserRepository()


async def get_admin_service():
    return AdminService()


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    status: Optional[str] = None,
    role: Optional[str] = None,
    current_user: dict = Depends(require_admin),
    repo: UserRepository = Depends(get_user_repo)
):
    # Get all users (admin only)
    users = await repo.get_all_users(limit, offset)
    
    # Apply filters
    if status:
        users = [u for u in users if u.get('status') == status]
    if role:
        users = [u for u in users if u.get('role') == role]
    
    return users


@router.get("/users/stats")
async def get_user_stats(
    current_user: dict = Depends(require_admin),
    repo: UserRepository = Depends(get_user_repo),
    admin_service: AdminService = Depends(get_admin_service)
):
    # Get user statistics (admin only)
    total = await repo.count_users()
    active = await repo.count_users("active")
    suspended = await repo.count_users("suspended")
    
    return {
        "total_users": total,
        "active_users": active,
        "suspended_users": suspended,
        "premium_users": 0,
        "growth": await admin_service.get_user_growth(30)
    }


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: dict = Depends(require_admin),
    repo: UserRepository = Depends(get_user_repo)
):
    # Get user by ID (admin only)
    user = await repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: dict = Depends(require_admin),
    repo: UserRepository = Depends(get_user_repo)
):
    # Update user (admin only)
    user = await repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    await repo.update_user(user_id, update_data)
    
    return {"message": "User updated successfully"}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: dict = Depends(require_admin),
    repo: UserRepository = Depends(get_user_repo)
):
    # Delete user (admin only)
    user = await repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deleting themselves
    if user_id == int(current_user.get("uid")):
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    await repo.delete_user(user_id)
    return {"message": "User deleted successfully"}


@router.post("/users/{user_id}/verify")
async def verify_user(
    user_id: int,
    current_user: dict = Depends(require_admin),
    repo: UserRepository = Depends(get_user_repo)
):
    # Verify a user (admin only)
    user = await repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await repo.update_user(user_id, {"is_verified": 1})
    return {"message": "User verified successfully"}
