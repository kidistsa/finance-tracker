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


def get_transaction_repo():
    return TransactionRepository()


@router.get("/", response_model=List[Transaction])
async def get_transactions(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    try:
        user_id = current_user.get('email') or current_user.get('uid')
        
        transactions = await repo.get_user_transactions(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            category=category,
            limit=limit
        )
        
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
                source=t.get('source', 'manual'),
                account_id=t.get('account_id'),
                merchant_name=t.get('merchant_name'),
                notes=t.get('notes'),
                tags=t.get('tags', '').split(',') if t.get('tags') else [],
                is_recurring=bool(t.get('is_recurring', False)),
                created_at=datetime.fromisoformat(t.get('created_at', datetime.now().isoformat())),
                updated_at=datetime.fromisoformat(t.get('updated_at', datetime.now().isoformat()))
            ))
        
        return result
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-csv", response_model=List[Transaction])
async def upload_transactions_csv(
    file: UploadFile = File(...),
    bank_format: str = Query("default", description="Bank format for CSV parsing"),
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Read file content
    try:
        content = await file.read()
        file_content = content.decode('utf-8')
        print(f"File content length: {len(file_content)}")
        print(f"First 500 chars: {file_content[:500]}")
    except Exception as e:
        print(f"Error reading file: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")
    
    # Process CSV
    try:
        df = pd.read_csv(io.StringIO(file_content))
        print(f"CSV columns: {list(df.columns)}")
        print(f"CSV rows: {len(df)}")
        
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
        user_id = current_user.get('email') or current_user.get('uid')
        
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
                            print(f"Invalid date format: {date_str}, skipping row {index}")
                            continue
                
                # Parse amount
                amount_str = str(row['amount']).replace('$', '').replace(',', '').strip()
                try:
                    amount = float(amount_str)
                except ValueError:
                    print(f"Invalid amount: {amount_str}, skipping row {index}")
                    continue
                
                # Determine transaction type
                transaction_type = "expense" if amount < 0 else "income"
                abs_amount = abs(amount)
                
                # Get category
                category = row.get('category', 'other')
                if pd.isna(category):
                    category = 'other'
                
                # Create transaction
                transaction = TransactionCreate(
                    user_id=user_id,
                    amount=abs_amount,
                    description=str(row['description']).strip(),
                    category=category,
                    transaction_type=transaction_type,
                    date=date,
                    source="csv_upload"
                )
                
                # Save to database
                created = await repo.create_transaction(transaction)
                created_transactions.append(created)
                print(f"Created transaction {index}: {created.description} - {created.amount}")
                
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                continue
        
        if not created_transactions:
            raise HTTPException(
                status_code=400,
                detail="No valid transactions found in CSV"
            )
        
        print(f"Successfully created {len(created_transactions)} transactions")
        return created_transactions
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"CSV processing error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {str(e)}")


@router.get("/summary", response_model=TransactionSummary)
async def get_transaction_summary(
    period: str = Query("month", pattern="^(week|month|year)$"),
    current_user: dict = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    try:
        user_id = current_user.get('email') or current_user.get('uid')
        now = datetime.now()
        
        if period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=365)
        
        transactions = await repo.get_user_transactions(
            user_id=user_id,
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
    except Exception as e:
        logger.error(f"Error getting summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
