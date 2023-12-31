from fastapi import FastAPI
from endpoints import books, users, auth, likes
from .database import engine
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

password = os.environ.get("PASSWORD")

# models.Base.metadata.create_all(bind=engine)



app = FastAPI()
        
app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)

# @app.get("/books")