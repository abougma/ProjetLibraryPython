from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel



Base = declarative_base()
app = FastAPI()

# Creation de la classe
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    release_date = Column(String(32))
    author_name = Column(String(120))
    number_of_pages = Column(Integer, nullable=False)

class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    pseudo = Column(String(32), unique=True)
    password = Column(String(32))

class NewBookInput(BaseModel):
    name: str
    release_date: str
    author_name : str
    number_of_pages : int

class UserIn(BaseModel):
    pseudo: str
    password: str

# Connexion avec la base de donnee
engine = create_engine('mysql+pymysql://root:Lemonde2020@localhost:3308/2ams')
Base.metadata.create_all(engine)    

Session = sessionmaker(bind=engine)
session = Session()

# Fonction permettant de creer un livre

def save_book (name: str, release_date: str, author_name: str, number_of_pages: int):
    try:
        today = datetime.now().date()
        release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

        if release_date>today:
            raise ValueError("Release date is not AFTER TODAY")
        
        if number_of_pages < 2:
            raise ValueError("The number of pages is greater than 2")
        
        std = session.query(Book).filter_by(name = name).first()
        if std:
            raise ValueError("The name of book is already use")

        new_book = Book(name = name, release_date= release_date, author_name= author_name, number_of_pages = int(number_of_pages))
        session.add(new_book)
        session.commit()
        return new_book.id 
    except ValueError as erreur:
        session.rollback()
        raise erreur
    except Exception as erreur:
        session.rollback()
        raise erreur
    
# Fonction permettant de creer un utilisateur

def create_user(pseudo: str, password: str):
    try:
        new_user = user(pseudo = pseudo, password = password)
        session.add(new_user)
        session.commit()
        return {"pseudo": pseudo}
    except Exception as error :
        session.rollback()
        raise HTTPException(status_code=400, detail="Error") from error

# Route permettant de creer un utilisateur
@app.post("/users", status_code=201)
async def save_user(user: UserIn):
    result = create_user(user.pseudo, user.password)
    return {"pseudo": user.pseudo}


# Route permettant de creer un nouveau livre
@app.post("/books/", status_code=201)
async def create_book(new_book: NewBookInput):
    try:
        book_id = save_book(new_book.name, new_book.release_date, new_book.author_name, new_book.number_of_pages)
        return {"The book Id is": book_id}
    except ValueError as erreur:
        raise HTTPException(status_code=400, detail=str(erreur))
    

# Route pour editer un livre
@app.put("/books/{id_book}", status_code=200)
async def update_book(id_book : int, new_book: NewBookInput):
    std = session.query(Book).filter_by(id=id_book).first()
    if std == None:
        raise HTTPException(status_code=400, detail="The book not found")
    std.name = new_book.name
    std.release_date = new_book.release_date
    std.author_name = new_book.author_name
    std.number_of_pages = new_book.number_of_pages
    session.commit()
    return {"Reponse" : " The book has been updated"}   

# Route pour supprimer un livre
@app.delete("/books/{id_book}", status_code=200)
async def delete_book(id_book: int):
    std = session.query(Book).filter_by(id=id_book).first()
    if std is None:
        raise HTTPException(status_code=400, detail="The book was not found")
    session.delete(std)
    session.commit()
    return {"message": "The book has been deleted"}

# Route pour lister tout les livres
@app.get("/books", status_code=200)
async def list_books():
    result = session.query(Book).all()
    New_list = []
    for std in result:
        New_list.append({"Name" : std.name, "Release date" : std.release_date, "Author name": std.author_name, "Number of pages" : std.number_of_pages})
    return {"Reponse" : New_list}    


# Route pour obtenir un livre
@app.get("/books/{id_book}", status_code=200)
async def get_book(id_book : int):
    std = session.query(Book).filter_by(id = id_book).first()
    if std is None:
        raise HTTPException(status_code=404, detail="The book not found")
    return{"Name" : std.name, "Release date" : std.release_date, "Author name": std.author_name, "Number of pages" : std.number_of_pages}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    