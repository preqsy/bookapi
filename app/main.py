from fastapi import FastAPI
from endpoints import books, review, users, auth, likes


app = FastAPI()


app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)
app.include_router(review.router)

