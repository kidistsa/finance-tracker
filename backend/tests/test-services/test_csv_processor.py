import pytest
from app.services.csv_processor import CSVProcessor
from datetime import datetime

@pytest.mark.asyncio
async def test_process_csv_chase_format():
    """Test processing Chase bank CSV format"""
    csv_content = """Transaction Date,Description,Amount,Type,Balance
01/15/2024,Starbucks,-4.50,Debit,1000.50
01/15/2024,Salary,5000.00,Credit,6000.50
01/14/2024,Amazon,-25.30,Debit,997.50"""
    
    transactions = await CSVProcessor.process_csv(
        file_content=csv_content,
        user_id="test_user",
        bank_format="chase"
    )
    
    assert len(transactions) == 3
    
    # Check first transaction (expense)
    assert transactions[0].amount == -4.50
    assert transactions[0].description == "Starbucks"
    assert transactions[0].transaction_type == "expense"
    
    # Check second transaction (income)
    assert transactions[1].amount == 5000.00
    assert transactions[1].description == "Salary"
    assert transactions[1].transaction_type == "income"


@pytest.mark.asyncio
async def test_process_csv_invalid_format():
    """Test processing invalid CSV format"""
    csv_content = """Invalid,Columns,Here
1,2,3
4,5,6"""
    
    with pytest.raises(ValueError):
        await CSVProcessor.process_csv(
            file_content=csv_content,
            user_id="test_user",
            bank_format="default"
        )


def test_parse_amount():
    """Test amount parsing"""
    assert CSVProcessor._parse_amount("$1,234.56") == 1234.56
    assert CSVProcessor._parse_amount("(50.00)") == -50.00
    assert CSVProcessor._parse_amount("€99.99") == 99.99
    assert CSVProcessor._parse_amount("1,234") == 1234.0
    assert CSVProcessor._parse_amount("invalid") == 0.0