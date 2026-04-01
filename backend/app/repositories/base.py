from typing import List, Dict, Any, Optional
from app.core.firebase import firebase_client


class BaseRepository:
    """Base repository for all repositories"""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        # Handle both real and mock Firebase clients
        if hasattr(firebase_client, 'get_db'):
            self.db = firebase_client.get_db()
        else:
            self.db = firebase_client
        self.collection = self.db.collection(collection_name)
    
    def create(self, data: Dict[str, Any]) -> str:
        """Create a new document"""
        # Use the add method which auto-generates an ID
        doc_ref, _ = self.collection.add(data)
        return doc_ref
    
    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        doc = self.collection.document(doc_id).get()
        if doc.exists():
            return doc.to_dict()
        return None
    
    def update(self, doc_id: str, data: Dict[str, Any]) -> bool:
        """Update document"""
        doc_ref = self.collection.document(doc_id)
        doc_ref.set(data, merge=True)
        return True
    
    def delete(self, doc_id: str) -> bool:
        """Delete document"""
        self.collection.document(doc_id).delete()
        return True
    
    def list(self, filters: Dict[str, Any] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List documents with optional filters"""
        query = self.collection
        if filters:
            for field, value in filters.items():
                if isinstance(value, tuple) and len(value) == 2:
                    operator, val = value
                    if operator == ">=":
                        query = query.where(field, ">=", val)
                    elif operator == "<=":
                        query = query.where(field, "<=", val)
                else:
                    query = query.where(field, "==", value)
        
        docs = query.limit(limit).get()
        return [doc.to_dict() for doc in docs]