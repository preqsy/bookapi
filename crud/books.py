from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Books
from app.schemas import BookCreate, BookUpdate

class BookCrud():
    
    def __init__(self, db : Session = Depends(get_db)):
        self.db = db
        
    def query_isbn(self, isbn : int):
        isbn_query =  self.db.query(Books).filter(Books.isbn==isbn)
        if not isbn_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with isbn: {isbn} doesn't exist")
        return isbn_query
        
    def get(self):
        return self.db.query(Books).all()
    
    def get_all_book(self, isbn : int):
        single_book = self.db.query(Books).filter(Books.isbn == isbn).first()
        return single_book
    
    def create(self, book : dict):
        
        self.db.add(book)
        self.db.commit()
        return book
    
    def update_book(self, isbn : int, book:BookUpdate):
        if self.query_isbn():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Book with isbn: {isbn} already exist")
        update_book = self.query_isbn.first()
        if not update_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with isbn: {isbn} does not exist")
        self.query_isbn.update(book.dict())
        
        self.db.commit()
        return update_book
    
    def delete(self, isbn : int):
        book_query = self.db.query(Books).filter(Books.isbn==isbn)
        if not book_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with isbn: {isbn} doesn't exist")
        book_query.delete()
        self.db.commit()
        
        return {"message":f"Book with isbn: {isbn} deleted successfully"}
    
book_crud = BookCrud()
    
    