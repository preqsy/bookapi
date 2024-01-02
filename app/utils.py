import random

from passlib.context import CryptContext

def hash(password : str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def verify(new_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(new_password, hashed_password)

def generate_isbn():
    generated_isbn = random.randrange(1000000000000, 9999999999999)
    return generated_isbn