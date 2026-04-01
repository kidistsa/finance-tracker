from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd
import io
import logging

from app.models.transaction import (
    Transaction, TransactionCreate, TransactionUpdate,
    TransactionSummary, TransactionFilters
)
from app.repositories.transaction_repo import TransactionRepository
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])
logger = logging.getLogger(__name__)


# Dependency to get repository
async def get_repository():
    return TransactionRepository()


@router.post("/upload-csv", response_model=List[Transaction])
async def upload_transactions_csv(
    file: UploadFile = File(...),
    bank_format: str = Query("default", description="Bank format for CSV parsing"),
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_repository)
):
    """
    Upload transactions via CSV file
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Read file content
    try:
        content = await file.read()
        file_content = content.decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")
    
    # Process CSV
    import pandas as pd
    import io
    
    try:
        df = pd.read_csv(io.StringIO(file_content))
        
        # Check required columns
        required_columns = ['date', 'amount', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"CSV missing required columns: {missing_columns}. Found: {list(df.columns)}"
            )
        
        # Process each row
        created_transactions = []
        for index, row in df.iterrows():
            try:
                # Parse date
                date_str = str(row['date']).strip()
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    try:
                        date = datetime.strptime(date_str, '%m/%d/%Y')
                    except ValueError:
                        try:
                            date = datetime.strptime(date_str, '%d/%m/%Y')
                        except ValueError:
                            logger.warning(f"Invalid date format: {date_str}, skipping row {index}")
                            continue
                
                # Parse amount
                amount_str = str(row['amount']).replace('$', '').replace(',', '').strip()
                try:
                    amount = float(amount_str)
                except ValueError:
                    logger.warning(f"Invalid amount: {amount_str}, skipping row {index}")
                    continue
                
                # Get transaction type from CSV if available
                if 'transaction_type' in df.columns and not pd.isna(row['transaction_type']):
                    transaction_type = str(row['transaction_type']).strip().lower()
                    # Validate transaction type
                    if transaction_type not in ['income', 'expense']:
                        logger.warning(f"Invalid transaction type: {transaction_type}, using amount sign")
                        transaction_type = "expense" if amount < 0 else "income"
                else:
                    # Determine by amount sign
                    transaction_type = "expense" if amount < 0 else "income"
                
                # Use absolute amount (always positive)
                abs_amount = abs(amount)
                
                # Get category from CSV if available
                if 'category' in df.columns and not pd.isna(row['category']):
                    category = str(row['category']).strip().lower()
                else:
                    category = 'other'
                
                # Get description
                description = str(row['description']).strip()
                
                # Create transaction
                transaction = TransactionCreate(
                    user_id=current_user["uid"],
                    amount=abs_amount,
                    description=description,
                    category=category,
                    transaction_type=transaction_type,
                    date=date
                    # source="csv_upload"
                )
                
                # Save to database
                created = await repo.create_transaction(transaction)
                created_transactions.append(created)
                logger.info(f"Created transaction: {created.description} - ${created.amount} ({created.transaction_type})")
                
            except Exception as e:
                logger.error(f"Error processing row {index}: {e}")
                continue
        
        if not created_transactions:
            raise HTTPException(
                status_code=400,
                detail="No valid transactions found in CSV"
            )
        
        logger.info(f"Successfully created {len(created_transactions)} transactions")
        return created_transactions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CSV processing error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {str(e)}")


@router.get("/", response_model=List[Transaction])
async def get_transactions(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_repository)
):
    """
    Get user transactions with optional filters
    """
    # FIX: Added await here
    transactions = await repo.get_user_transactions(
        user_id=current_user["uid"],
        start_date=start_date,
        end_date=end_date,
        category=category,
        limit=limit
    )
    
    # Convert to Transaction objects
    result = []
    for t in transactions:
        result.append(Transaction(
            id=t.get('id', ''),
            user_id=t.get('user_id', ''),
            amount=t.get('amount', 0),
            description=t.get('description', ''),
            category=t.get('category', 'other'),
            transaction_type=t.get('transaction_type', 'expense'),
            date=datetime.fromisoformat(t.get('date', datetime.now().isoformat())),
            # source=t.get('source', 'manual'),
            # account_id=t.get('account_id'),
            # merchant_name=t.get('merchant_name'),
            # notes=t.get('notes'),
            # tags=t.get('tags', '').split(',') if t.get('tags') else [],
            # is_recurring=bool(t.get('is_recurring', False)),
            created_at=datetime.fromisoformat(t.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(t.get('updated_at', datetime.now().isoformat()))
        ))
    
    return result


@router.get("/summary", response_model=TransactionSummary)
async def get_transaction_summary(
    period: str = Query("month", pattern="^(week|month|year)$"),
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_repository)
):
    """
    Get transaction summary for dashboard
    """
    now = datetime.now()
    
    if period == "week":
        start_date = now - timedelta(days=7)
    elif period == "month":
        start_date = now - timedelta(days=30)
    else:  # year
        start_date = now - timedelta(days=365)
    
    # FIX: Added await here
    transactions = await repo.get_user_transactions(
        user_id=current_user["uid"],
        start_date=start_date,
        end_date=now
    )
    
    total_income = sum(t.get("amount", 0) for t in transactions if t.get("transaction_type") == "income")
    total_expenses = sum(t.get("amount", 0) for t in transactions if t.get("transaction_type") == "expense")
    
    return TransactionSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_savings=total_income - total_expenses,
        transaction_count=len(transactions),
        period_start=start_date,
        period_end=now
    )


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_repository)
):
    """
    Get transaction by ID
    """
    # FIX: Added await here
    transaction = await repo.get_transaction(transaction_id)
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if transaction.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this transaction")
    
    return Transaction(
        id=transaction_id,
        user_id=transaction.get('user_id', ''),
        amount=transaction.get('amount', 0),
        description=transaction.get('description', ''),
        category=transaction.get('category', 'other'),
        transaction_type=transaction.get('transaction_type', 'expense'),
        date=datetime.fromisoformat(transaction.get('date', datetime.now().isoformat())),
        source=transaction.get('source', 'manual'),
        account_id=transaction.get('account_id'),
        merchant_name=transaction.get('merchant_name'),
        notes=transaction.get('notes'),
        tags=transaction.get('tags', '').split(',') if transaction.get('tags') else [],
        is_recurring=bool(transaction.get('is_recurring', False)),
        created_at=datetime.fromisoformat(transaction.get('created_at', datetime.now().isoformat())),
        updated_at=datetime.fromisoformat(transaction.get('updated_at', datetime.now().isoformat()))
    )


@router.put("/{transaction_id}", response_model=Transaction)
async def update_transaction(
    transaction_id: str,
    transaction_update: TransactionUpdate,
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_repository)
):
    """
    Update transaction
    """
    # Check if transaction exists and belongs to user
    # FIX: Added await here
    existing = await repo.get_transaction(transaction_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if existing.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this transaction")
    
    # Update transaction - FIX: Added await here
    await repo.update_transaction(transaction_id, transaction_update)
    
    # Get updated transaction - FIX: Added await here
    updated = await repo.get_transaction(transaction_id)
    
    return Transaction(
        id=transaction_id,
        user_id=updated.get('user_id', ''),
        amount=updated.get('amount', 0),
        description=updated.get('description', ''),
        category=updated.get('category', 'other'),
        transaction_type=updated.get('transaction_type', 'expense'),
        date=datetime.fromisoformat(updated.get('date', datetime.now().isoformat())),
        source=updated.get('source', 'manual'),
        account_id=updated.get('account_id'),
        merchant_name=updated.get('merchant_name'),
        notes=updated.get('notes'),
        tags=updated.get('tags', '').split(',') if updated.get('tags') else [],
        is_recurring=bool(updated.get('is_recurring', False)),
        created_at=datetime.fromisoformat(updated.get('created_at', datetime.now().isoformat())),
        updated_at=datetime.fromisoformat(updated.get('updated_at', datetime.now().isoformat()))
    )


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_repository)
):
    """
    Delete transaction
    """
    # Check if transaction exists and belongs to user
    # FIX: Added await here
    existing = await repo.get_transaction(transaction_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if existing.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this transaction")
    
    # Delete transaction - FIX: Added await here
    await repo.delete_transaction(transaction_id)
    
    return {"message": "Transaction deleted successfully"}