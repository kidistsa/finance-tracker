from app.core.db import db_client
import uuid
from datetime import datetime

class MockFirestoreCollection:
    """A mock Firestore collection that uses SQLite"""
    
    def __init__(self, collection_name, user_id=None):
        self.collection_name = collection_name
        self.user_id = user_id
        self._filters = []  # Store filters for chaining
        self._limit_value = None  # Store limit value
    
    def document(self, doc_id=None):
        """Get a document reference - doc_id is optional for auto-generated IDs"""
        if doc_id is None:
            # Auto-generate ID if none provided
            doc_id = str(uuid.uuid4())
        return MockFirestoreDocument(self.collection_name, doc_id, self.user_id)
    
    def add(self, data):
        """Add a new document to the collection (auto-generates ID)"""
        doc_ref = self.document()
        doc_ref.set(data)
        return doc_ref.doc_id, None
    
    def where(self, field, operator, value):
        """Add a where filter"""
        self._filters.append((field, operator, value))
        return self
    
    def limit(self, limit_value):
        """Add a limit to the query"""
        self._limit_value = limit_value
        return self
    
    def get(self):
        """Execute the query and get documents"""
        # Build SQL query based on collection
        if self.collection_name == "transactions":
            query = "SELECT * FROM transactions"
            params = []
            
            if self._filters:
                conditions = []
                for field, operator, value in self._filters:
                    if field == 'user_id':
                        conditions.append("user_id = ?")
                        params.append(value)
                    elif field == 'date':
                        if operator == ">=":
                            conditions.append("date >= ?")
                            params.append(value)
                        elif operator == "<=":
                            conditions.append("date <= ?")
                            params.append(value)
                    elif field == 'category':
                        conditions.append("category = ?")
                        params.append(value)
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY date DESC"
            
            if self._limit_value:
                query += f" LIMIT {self._limit_value}"
            
            results = db_client.fetch_all(query, tuple(params))
            return [MockFirestoreDocument.from_row(row, self.collection_name) for row in results]
        
        elif self.collection_name == "budgets":
            query = "SELECT * FROM budgets"
            params = []
            
            if self._filters:
                conditions = []
                for field, operator, value in self._filters:
                    if field == 'user_id':
                        conditions.append("user_id = ?")
                        params.append(value)
                    elif field == 'category':
                        conditions.append("category = ?")
                        params.append(value)
                    elif field == 'month':
                        conditions.append("month = ?")
                        params.append(value)
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            
            if self._limit_value:
                query += f" LIMIT {self._limit_value}"
            
            results = db_client.fetch_all(query, tuple(params))
            return [MockFirestoreDocument.from_row(row, self.collection_name) for row in results]
        
        return []


class MockFirestoreDocument:
    """A mock Firestore document that uses SQLite"""
    
    def __init__(self, collection_name, doc_id, user_id=None):
        self.collection_name = collection_name
        self.doc_id = doc_id
        self.user_id = user_id
    
    @classmethod
    def from_row(cls, row, collection_name):
        """Create a document from a database row"""
        doc = cls(collection_name, str(row['id']))
        doc._data = dict(row)
        return doc
    
    def set(self, data):
        """Save data to SQLite"""
        if self.collection_name == "users":
            if self.doc_id and self.doc_id != "mock":
                query = """
                    INSERT OR REPLACE INTO users (id, email, hashed_password, full_name, is_active)
                    VALUES (?, ?, ?, ?, ?)
                """
                db_client.execute_query(query, (
                    int(self.doc_id) if self.doc_id != "mock" else None,
                    data.get('email'),
                    data.get('hashed_password'),
                    data.get('full_name'),
                    1
                ))
            else:
                query = """
                    INSERT INTO users (email, hashed_password, full_name, is_active)
                    VALUES (?, ?, ?, ?)
                """
                db_client.execute_query(query, (
                    data.get('email'),
                    data.get('hashed_password'),
                    data.get('full_name'),
                    1
                ))
        
        elif self.collection_name == "transactions":
            # Insert or replace transaction
            query = """
                INSERT OR REPLACE INTO transactions (
                    id, user_id, amount, description, category, 
                    transaction_type, date, source, account_id, 
                    merchant_name, notes, tags, is_recurring, 
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db_client.execute_query(query, (
                data.get('id'),
                data.get('user_id'),
                data.get('amount'),
                data.get('description'),
                data.get('category'),
                data.get('transaction_type'),
                data.get('date'),
                data.get('source', 'manual'),
                data.get('account_id'),
                data.get('merchant_name'),
                data.get('notes'),
                data.get('tags'),
                data.get('is_recurring', 0),
                data.get('created_at', datetime.now().isoformat()),
                data.get('updated_at', datetime.now().isoformat())
            ))
        
        elif self.collection_name == "budgets":
            # Insert or replace budget
            query = """
                INSERT OR REPLACE INTO budgets (
                    id, user_id, category, amount, month, 
                    notification_threshold, rollover_enabled, 
                    spent, remaining, percentage_used,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db_client.execute_query(query, (
                data.get('id'),
                data.get('user_id'),
                data.get('category'),
                data.get('amount'),
                data.get('month'),
                data.get('notification_threshold', 80),
                data.get('rollover_enabled', 0),
                data.get('spent', 0),
                data.get('remaining', data.get('amount', 0)),
                data.get('percentage_used', 0),
                data.get('created_at', datetime.now().isoformat()),
                data.get('updated_at', datetime.now().isoformat())
            ))
    
    def get(self):
        """Retrieve data from SQLite"""
        class MockSnapshot:
            def __init__(self, data, exists):
                self._data = data
                self._exists = exists
            
            def exists(self):
                return self._exists
            
            def to_dict(self):
                return self._data
        
        if self.collection_name == "users" and self.doc_id and self.doc_id != "mock":
            query = "SELECT * FROM users WHERE id = ?"
            result = db_client.fetch_one(query, (int(self.doc_id),))
            if result:
                return MockSnapshot(dict(result), True)
        
        elif self.collection_name == "transactions" and self.doc_id and self.doc_id != "mock":
            query = "SELECT * FROM transactions WHERE id = ?"
            result = db_client.fetch_one(query, (self.doc_id,))
            if result:
                return MockSnapshot(dict(result), True)
        
        elif self.collection_name == "budgets" and self.doc_id and self.doc_id != "mock":
            query = "SELECT * FROM budgets WHERE id = ?"
            result = db_client.fetch_one(query, (self.doc_id,))
            if result:
                return MockSnapshot(dict(result), True)
        
        return MockSnapshot({}, False)


class MockFirestore:
    """Mock Firestore client that uses SQLite"""
    
    def __init__(self):
        self.db = self
        print("✅ Firebase mock client initialized (using SQLite)")
    
    def collection(self, name):
        return MockFirestoreCollection(name)
    
    def get_db(self):
        """Return the database instance for compatibility"""
        return self.db


# Create the firebase_client instance that your app expects
firebase_client = MockFirestore()