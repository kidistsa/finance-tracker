# from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
# from app.api.dependencies.auth import get_current_user
# from app.services.ocr_service import OCRService
# from app.repositories.transaction_repo import TransactionRepository
# from app.models.transaction import TransactionCreate
# from datetime import datetime
# import logging

# router = APIRouter(prefix="/receipt-scanner", tags=["Receipt Scanner"])
# logger = logging.getLogger(__name__)


# @router.post("/scan")
# async def scan_receipt(
#     file: UploadFile = File(...),
#     current_user: dict = Depends(get_current_user),
#     repo: TransactionRepository = Depends()
# ):
#     if not file.content_type.startswith('image/'):
#         raise HTTPException(status_code=400, detail="File must be an image")
    
#     try:
#         receipt_data = await OCRService.extract_from_image(file)
        
#         if receipt_data.get("error"):
#             raise HTTPException(status_code=400, detail=receipt_data["error"])
        
#         transaction = None
#         if receipt_data.get("total"):
#             transaction_data = TransactionCreate(
#                 user_id=current_user["uid"],
#                 amount=receipt_data["total"],
#                 description=receipt_data.get("merchant") or "Receipt Transaction",
#                 category="shopping",
#                 transaction_type="expense",
#                 date=datetime.fromisoformat(receipt_data["date"]) if receipt_data.get("date") else datetime.now(),
#                 source="receipt_scanner"
#             )
            
#             transaction = await repo.create_transaction(transaction_data)
        
#         return {
#             "success": True,
#             "extracted_data": receipt_data,
#             "transaction": transaction.dict() if transaction else None,
#             "message": "Receipt scanned successfully" if transaction else "Receipt scanned but no amount found"
#         }
        
#     except Exception as e:
#         logger.error(f"Receipt scanning failed: {e}")
#         raise HTTPException(status_code=500, detail=f"Failed to scan receipt: {str(e)}")
