import pandas as pd
from io import StringIO
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
import logging
from app.models.transaction import TransactionCreate, TransactionType, TransactionSource

logger = logging.getLogger(__name__)


class CSVProcessor:
    """Handle CSV file processing for various bank formats"""
    
    # Bank-specific column mappings
    BANK_FORMATS = {
        'chase': {
            'date': 'Transaction Date',
            'description': 'Description',
            'amount': 'Amount',
            'type': 'Type',
            'balance': 'Balance',
            'check_number': 'Check Number'
        },
        'bank_of_america': {
            'date': 'Date',
            'description': 'Description',
            'amount': 'Amount',
            'type': 'Transaction Type'
        },
        'wells_fargo': {
            'date': 'Date',
            'description': 'Description',
            'amount': 'Amount',
            'type': 'Transaction Type'
        },
        'capital_one': {
            'date': 'Transaction Date',
            'description': 'Description',
            'amount': 'Debit',
            'credit': 'Credit'
        },
        'default': {
            'date': 'date',
            'description': 'description',
            'amount': 'amount'
        }
    }
    
    @staticmethod
    async def process_csv(
        file_content: str, 
        user_id: str,
        bank_format: str = 'default'
    ) -> List[TransactionCreate]:
        """
        Process CSV content and return standardized transactions
        """
        try:
            # Read CSV
            df = pd.read_csv(StringIO(file_content))
            logger.info(f"Processing CSV with {len(df)} rows, format: {bank_format}")
            
            # Get column mapping
            mapping = CSVProcessor.BANK_FORMATS.get(
                bank_format, 
                CSVProcessor.BANK_FORMATS['default']
            )
            
            # Standardize columns
            transactions = []
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    transaction = await CSVProcessor._create_transaction_from_row(
                        row, mapping, user_id, bank_format
                    )
                    if transaction:
                        transactions.append(transaction)
                except Exception as e:
                    errors.append(f"Row {idx + 2}: {str(e)}")
                    logger.warning(f"Error processing row {idx}: {e}")
            
            if errors:
                logger.warning(f"Encountered {len(errors)} errors while processing CSV")
            
            return transactions
            
        except Exception as e:
            logger.error(f"Failed to process CSV: {str(e)}")
            raise ValueError(f"Failed to process CSV: {str(e)}")
    
    @staticmethod
    async def _create_transaction_from_row(
        row: pd.Series, 
        mapping: Dict[str, str],
        user_id: str,
        bank_format: str
    ) -> Optional[TransactionCreate]:
        """Create transaction from CSV row"""
        
        # Parse date
        date = CSVProcessor._parse_date(row.get(mapping.get('date')))
        if not date:
            return None
        
        # Parse description
        description = str(row.get(mapping.get('description', ''), ''))
        if not description:
            return None
        
        # Parse amount and determine transaction type
        amount, transaction_type = await CSVProcessor._parse_amount_and_type(
            row, mapping, bank_format
        )
        
        # Create transaction
        return TransactionCreate(
            user_id=user_id,
            amount=amount,
            description=description[:500],  # Truncate if too long
            transaction_type=transaction_type,
            date=date,
            # source=TransactionSource.CSV_UPLOAD,
            # merchant_name=CSVProcessor._extract_merchant(description),
            # account_id=None  # Will be set by user if needed
        )
    
    @staticmethod
    def _parse_date(date_value) -> Optional[datetime]:
        """Parse various date formats"""
        if pd.isna(date_value):
            return None
        
        if isinstance(date_value, datetime):
            return date_value
        
        if isinstance(date_value, str):
            # Try common formats
            formats = [
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%d/%m/%Y',
                '%m-%d-%Y',
                '%Y%m%d',
                '%m/%d/%y',
                '%d-%b-%y'
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(date_value, fmt)
                except ValueError:
                    continue
        
        return datetime.now()  # Fallback
    
    @staticmethod
    async def _parse_amount_and_type(row: pd.Series, mapping: Dict[str, str], bank_format: str) -> tuple:
        """Parse amount and determine transaction type"""
        
        # Handle different bank formats
        if bank_format == 'capital_one':
            # Capital One has separate debit and credit columns
            debit = CSVProcessor._parse_amount(row.get(mapping.get('amount', '')))
            credit = CSVProcessor._parse_amount(row.get(mapping.get('credit', '')))
            
            if debit and debit > 0:
                return -abs(debit), TransactionType.EXPENSE
            elif credit and credit > 0:
                return abs(credit), TransactionType.INCOME
        
        else:
            # Standard format with amount column
            amount = CSVProcessor._parse_amount(row.get(mapping.get('amount', '')))
            
            # Check transaction type column if exists
            if 'type' in mapping and mapping['type'] in row:
                type_value = str(row[mapping['type']]).lower()
                if type_value in ['debit', 'payment', 'withdrawal', 'expense']:
                    return -abs(amount), TransactionType.EXPENSE
                elif type_value in ['credit', 'deposit', 'income', 'salary']:
                    return abs(amount), TransactionType.INCOME
            
            # If no type column, assume positive is income, negative is expense
            if amount < 0:
                return amount, TransactionType.EXPENSE
            else:
                return amount, TransactionType.INCOME
        
        return 0.0, TransactionType.EXPENSE
    
    @staticmethod
    def _parse_amount(amount_value) -> float:
        """Parse amount strings with currency symbols and commas"""
        if pd.isna(amount_value):
            return 0.0
        
        if isinstance(amount_value, (int, float)):
            return float(amount_value)
        
        if isinstance(amount_value, str):
            # Remove currency symbols, commas, and whitespace
            cleaned = re.sub(r'[$,£€\s]', '', amount_value)
            # Handle parentheses for negative numbers
            if cleaned.startswith('(') and cleaned.endswith(')'):
                cleaned = '-' + cleaned[1:-1]
            try:
                return float(cleaned)
            except ValueError:
                return 0.0
        
        return 0.0
    
    @staticmethod
    def _extract_merchant(description: str) -> Optional[str]:
        """Extract merchant name from description"""
        # Common patterns: "PURCHASE AT MERCHANT", "MERCHANT #1234"
        description = description.upper()
        
        # Remove common prefixes
        prefixes = ['PURCHASE AT ', 'PAYMENT TO ', 'DEBIT CARD ', 'ONLINE ']
        for prefix in prefixes:
            if description.startswith(prefix):
                description = description[len(prefix):]
        
        # Remove common suffixes
        suffixes = [' #', ' ##', ' REF', ' ID']
        for suffix in suffixes:
            if suffix in description:
                description = description.split(suffix)[0]
        
        return description.strip() or None
    
    @staticmethod
    def validate_csv_headers(headers: List[str]) -> tuple:
        """Validate CSV headers and suggest bank format"""
        headers_lower = [h.lower() for h in headers]
        
        # Check against known formats
        for bank, mapping in CSVProcessor.BANK_FORMATS.items():
            required = [v.lower() for v in mapping.values() if v]
            matches = sum(1 for r in required if any(r in h for h in headers_lower))
            
            if matches >= 2:  # At least 2 matching columns
                return True, bank
        
        # Check minimum required columns
        required_columns = ['date', 'description', 'amount']
        missing = [col for col in required_columns 
                  if not any(col in h for h in headers_lower)]
        
        if missing:
            return False, f"Missing required columns: {', '.join(missing)}"
        
        return True, 'default'