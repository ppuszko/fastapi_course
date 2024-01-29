from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote


#models.Base.metadata.create_all(bind=engine) it was used to create connection and tables in poetgres using sqlalchemy, 
# although currently alembic does this with more features and flexibility, co i leave it for educational purposes


app = FastAPI() #initializes app instance
#Po ponownym otwarciu pliku nalezy w terminalu wpisać sciezke do activate.bat czyli venv\Scripts\activate.bat, następnie
#uvicorn app.main:app --reload aby wszystko bylo aktywne, w przeciwnym wypadku requesty nie maja odpowiedzi

#to include migrations to our database(e.g. adding a new column to already existing postres table, the alembic tool is needed. 
# after instalation, it is required to initialize it, and create a folder for it, which can be done by this command: 
# alembic init alembic(it is a folder name, can be named however i want))
origins = ["*"] #allows every domain to reach my app, i can also list domains i want to allow

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router) #includes route to post-corelated PATH oeprations
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
def root():
    return {"message": "Hello World bro it works"}


